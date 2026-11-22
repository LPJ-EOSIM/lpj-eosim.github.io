# MODIS MCD43C4 v061 NBAR (0.05 deg CMG, 7 bands) -> monthly mean at 0.5 deg.
# One slurm array task per month. Runs in the ncdf conda env (its netCDF4 reads HDF4).
#   sbatch --array=1-12 ... --wrap "~/.conda/envs/ncdf/bin/python mcd43_month.py"
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

import netCDF4
import numpy as np

if __name__ == "__main__":
    # --- edit me ---
    year = 2020
    days = [1, 9, 17, 25]  # days of month sampled; MCD43 is a 16-day moving window
    outdir = Path("/mnt/beegfs/scratch/tc229954e/prosail/bryce_commit/analysis/data/mcd43c4")
    tmpdir = Path(os.environ.get("TMPDIR", "/tmp"))
    min_valid = 25  # of the 100 0.05-deg pixels in a 0.5-deg cell
    # ---------------

    month = int(os.environ["SLURM_ARRAY_TASK_ID"])
    outdir.mkdir(parents=True, exist_ok=True)
    outf = outdir / f"mcd43c4_0p5_{year}{month:02d}.nc"
    if outf.exists():
        print(f"skip {outf}")
        raise SystemExit

    sums = np.zeros((8, 360, 720))  # bands 1-7 + percent snow
    counts = np.zeros((8, 360, 720))
    for day in days:
        date = f"{year}-{month:02d}-{day:02d}"
        url = ("https://cmr.earthdata.nasa.gov/search/granules.json?short_name=MCD43C4&version=061"
               f"&temporal={date}T00:00:00Z,{date}T23:59:59Z&page_size=50")
        entries = json.load(urllib.request.urlopen(url))["feed"]["entry"]
        doy = (np.datetime64(date) - np.datetime64(f"{year}-01-01")).astype(int) + 1
        entries = [e for e in entries if f".A{year}{doy:03d}." in e["title"]]
        href = [l["href"] for l in entries[0]["links"] if l["href"].endswith(".hdf") and l["href"].startswith("https")][0]

        hdf = tmpdir / Path(href).name
        cookie = tmpdir / f"cookie_{month}"
        for attempt in range(5):  # LP DAAC returns the odd HTTP error
            r = subprocess.run(["curl", "-sS", "-f", "-L", "-n", "-c", cookie, "-b", cookie, "-o", hdf, href])
            if r.returncode == 0:
                break
            print("curl failed, retry", attempt, flush=True)
            time.sleep(30)
        else:
            raise SystemExit(f"download failed: {href}")
        print(date, hdf.name, hdf.stat().st_size)

        ds = netCDF4.Dataset(hdf)
        names = [f"Nadir_Reflectance_Band{b}" for b in range(1, 8)] + ["Percent_Snow"]
        for i, name in enumerate(names):
            a = ds[name][:].astype(np.float64).filled(np.nan)  # scale_factor applied by netCDF4
            a = a.reshape(360, 10, 720, 10)
            n = np.isfinite(a).sum(axis=(1, 3))
            m = np.nanmean(a, axis=(1, 3))
            ok = n >= min_valid
            sums[i][ok] += m[ok]
            counts[i][ok] += 1
        ds.close()
        hdf.unlink()

    mean = np.where(counts > 0, sums / np.maximum(counts, 1), np.nan)

    lat = 89.75 - 0.5 * np.arange(360)
    lon = -179.75 + 0.5 * np.arange(720)
    out = netCDF4.Dataset(outf, "w")
    out.createDimension("band", 7)
    out.createDimension("lat", 360)
    out.createDimension("lon", 720)
    out.createVariable("band", "i4", ("band",))[:] = np.arange(1, 8)
    out.createVariable("lat", "f4", ("lat",))[:] = lat
    out.createVariable("lon", "f4", ("lon",))[:] = lon
    v = out.createVariable("nbar", "f4", ("band", "lat", "lon"), zlib=True)
    v[:] = mean[:7]
    v.long_name = "MCD43C4 v061 nadir BRDF-adjusted reflectance, monthly mean of sampled days, 0.5 deg"
    s = out.createVariable("percent_snow", "f4", ("lat", "lon"), zlib=True)
    s[:] = mean[7]
    out.days_sampled = str(days)
    out.close()
    print("wrote", outf)
