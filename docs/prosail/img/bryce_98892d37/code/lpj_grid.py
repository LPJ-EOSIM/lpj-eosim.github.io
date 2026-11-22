# Grid the LPJ-PROSAIL transient output (200 splits) onto the 0.5 deg grid.
#   lpj_bands_0p5.nc        resv convolved to MODIS bands 1-7, every year x month (2010-2023)
#   lpj_spectra_2020_0p5.nc full 211-bin resv spectrum, 2020, every month
# Runs in ~/projects/.venv-lpj.
from pathlib import Path

import numpy as np
import xarray as xr

if __name__ == "__main__":
    # --- edit me ---
    run_dir = Path("/mnt/beegfs/scratch/tc229954e/prosail/bryce_commit/transient_2023")
    outdir = Path("/mnt/beegfs/scratch/tc229954e/prosail/bryce_commit/analysis/data")
    years = np.arange(2010, 2024)
    spectra_year = 2020
    n_splits = 200
    # MODIS band edges (nm), bands 1-7
    modis_bands = [(620, 670), (841, 876), (459, 479), (545, 565), (1230, 1250), (1628, 1652), (2105, 2155)]
    # ---------------

    outdir.mkdir(parents=True, exist_ok=True)
    bands_f = outdir / "lpj_bands_0p5.nc"
    spectra_f = outdir / f"lpj_spectra_{spectra_year}_0p5.nc"
    if bands_f.exists() and spectra_f.exists():
        print("skip, both exist")
        raise SystemExit

    # bin k averages the 1-nm PROSAIL values 400+10k .. 409+10k nm (last bin is 2500 only).
    # Band weight of bin k = nm of the band that fall in the bin.
    nbin = 211
    lo = 400 + 10 * np.arange(nbin)
    hi = np.minimum(lo + 9, 2500)
    weights = np.zeros((7, nbin))
    for b, (b0, b1) in enumerate(modis_bands):
        for k in range(nbin):
            weights[b, k] = max(0, min(hi[k], b1) - max(lo[k], b0) + 1)
        weights[b] /= weights[b].sum()

    lat = 89.75 - 0.5 * np.arange(360)
    lon = -179.75 + 0.5 * np.arange(720)
    bands = np.full((len(years), 12, 7, 360, 720), np.nan, dtype=np.float32)
    spectra = np.full((12, nbin, 360, 720), -1, dtype=np.int16)
    iy = int(spectra_year - years[0])

    ncell = 0
    for i in range(n_splits):
        g = np.fromfile(run_dir / f"grid_{i}.out", dtype=np.int16).reshape(-1, 2) / 100.0
        r = np.fromfile(run_dir / f"reflectance_resv_{i}.bin", dtype=np.int16).reshape(len(years), 12, len(g), nbin)  # LPJ loops month -> cell
        rows = np.round((89.75 - g[:, 1]) / 0.5).astype(int)
        cols = np.round((g[:, 0] + 179.75) / 0.5).astype(int)
        # (year, month, cell, bin) @ (bin, band) -> (year, month, cell, band)
        b = (r / 10000.0) @ weights.T
        bands[:, :, :, rows, cols] = b.transpose(0, 1, 3, 2)
        spectra[:, :, rows, cols] = r[iy].transpose(0, 2, 1)
        ncell += len(g)
        print(i, len(g), flush=True)
    print("cells", ncell)

    ds = xr.Dataset(
        {"resv": (("year", "month", "band", "lat", "lon"), bands)},
        coords={"year": years, "month": np.arange(1, 13), "band": np.arange(1, 8), "lat": lat, "lon": lon},
    )
    ds.resv.attrs["long_name"] = "LPJ-PROSAIL directional reflectance (resv) averaged over MODIS band edges"
    ds.to_netcdf(bands_f, encoding={"resv": {"zlib": True, "complevel": 1}})

    sp = xr.Dataset(
        {"resv": (("month", "wavelength", "lat", "lon"), spectra)},
        coords={"month": np.arange(1, 13), "wavelength": lo + 4.5, "lat": lat, "lon": lon},
    )
    sp.resv.attrs.update(long_name=f"LPJ-PROSAIL resv {spectra_year}, 10-nm bins", scale_factor_note="x10000, -1 = no cell")
    sp.to_netcdf(spectra_f, encoding={"resv": {"zlib": True, "complevel": 1}})
    print("wrote", bands_f, spectra_f)
