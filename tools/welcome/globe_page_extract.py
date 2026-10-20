"""2015-2024 climatologies of NMIP3 SH1 fields, averaged to 1 deg, for the LPJ-EOSIM scrollytelling page."""
import warnings
from pathlib import Path

import netCDF4
import numpy as np

warnings.filterwarnings("ignore", category=RuntimeWarning)  # all-NaN ocean blocks

if __name__ == "__main__":
    # --- edit me ---
    run = Path("/mnt/beegfs/scratch/tc229954e/NMIP/NMIP3_816c3d_SH1/ncdf_outputs")
    out = Path("/mnt/beegfs/scratch/tc229954e/NMIP/globe_page")
    monthly = ["mtair", "mppt", "mswdown",
               "mgpp", "mnpp", "mrh", "mfirec", "mlai", "mevapotrans", "mswc1", "mrunoff",
               "msnowpack", "mburntarea", "misopr", "mn2o_soil", "mbnf"]
    annual = ["vegc", "litc", "soilc"]
    years = 10
    # ---------------

    out.mkdir(parents=True, exist_ok=True)
    for v in monthly + annual:
        f = out / f"{v}.npz"
        if f.exists():
            print(f"skip {f}", flush=True)
            continue
        with netCDF4.Dataset(run / f"NMIP3_816c3d_SH1_{v}.nc") as ds:
            var = ds[v]
            nt = var.shape[0]
            n = years * 12 if v in monthly else years
            a = var[nt - n:].filled(np.nan).astype(np.float32)
            lat = ds["latitude"][:]
            units = getattr(var, "units", "")
            t = ds["time"]
            span = netCDF4.num2date(t[[nt - n, nt - 1]], t.units, getattr(t, "calendar", "standard"))
        clim = a.reshape(years, 12, 360, 720) if v in monthly else a[:, None]
        clim = np.nanmean(clim, axis=0)  # (12 or 1, 360, 720)
        if lat[0] < lat[-1]:
            clim = clim[:, ::-1]  # north first
        coarse = np.nanmean(clim.reshape(clim.shape[0], 180, 2, 360, 2), axis=(2, 4)).astype(np.float32)
        np.savez_compressed(f, data=coarse, units=units, span=str(span))
        print(f"{v}: {units} {span[0]}..{span[-1]} min {np.nanmin(coarse):.4g} p99 {np.nanpercentile(coarse, 99):.4g}", flush=True)
