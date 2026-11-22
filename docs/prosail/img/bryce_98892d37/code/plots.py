# Figures for the LPJ-PROSAIL (Bryce commit 98892d37) global run vs MODIS MCD43C4, 2020.
# Runs in ~/projects/.venv-lpj after lpj_grid.py and mcd43_month.py.
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import nc_tools
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap, LogNorm

if __name__ == "__main__":
    # --- edit me ---
    data = Path("/mnt/beegfs/scratch/tc229954e/prosail/bryce_commit/analysis/data")
    outdir = Path("/mnt/beegfs/scratch/tc229954e/prosail/bryce_commit/analysis/img")
    year = 2020
    snow_max = 5.0  # % snow in MCD43C4 above which a cell-month is left out of the band stats
    sites = {  # name: (lon, lat)
        "Amazon (Manaus)": (-60.25, -2.75),
        "Boreal forest (Manitoba)": (-98.25, 55.75),
        "Temperate forest (Maryland)": (-76.75, 39.25),
        "Cropland (Iowa)": (-93.25, 42.25),
        "Savanna (Sahel, Niger)": (2.25, 13.75),
        "Tundra (Yakutia)": (130.25, 70.25),
    }
    # ---------------
    outdir.mkdir(parents=True, exist_ok=True)

    # palette (dataviz reference instance)
    c_lpj, c_modis = "#2a78d6", "#eb6834"
    c_months = {1: "#2a78d6", 4: "#eb6834", 7: "#1baf7a", 10: "#eda100"}
    ink, ink2, grid_c, ocean = "#0b0b0b", "#52514e", "#e4e3df", "#eef1f4"
    div = LinearSegmentedColormap.from_list("div", ["#104281", "#3987e5", "#f0efec", "#e66767", "#a8282a"])
    seq_green = LinearSegmentedColormap.from_list("seqg", ["#f3f1e6", "#c7dfa6", "#7fbf6a", "#2f8f3a", "#0f5a22"])
    seq_blue = LinearSegmentedColormap.from_list("seqb", ["#cde2fb", "#6da7ec", "#2a78d6", "#184f95", "#0d366b"])
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": ink2, "axes.labelcolor": ink, "xtick.color": ink2,
                         "ytick.color": ink2, "axes.spines.top": False, "axes.spines.right": False})
    band_names = {1: "B1 red\n620-670 nm", 2: "B2 NIR\n841-876 nm", 3: "B3 blue\n459-479 nm", 4: "B4 green\n545-565 nm",
                  5: "B5 SWIR\n1230-1250 nm", 6: "B6 SWIR\n1628-1652 nm", 7: "B7 SWIR\n2105-2155 nm"}
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    robin = ccrs.Robinson()
    extent = [-180, 180, -90, 90]

    lpj_all = xr.open_dataset(data / "lpj_bands_0p5.nc").resv.load()  # (year, month, band, lat, lon)
    lpj = lpj_all.sel(year=year)
    # months with no MCD43C4 file (August failed to download) are left as NaN
    first = xr.open_dataset(sorted((data / "mcd43c4").glob(f"mcd43c4_0p5_{year}*.nc"))[0])
    nbar_m, snow_m = [], []
    for m in range(1, 13):
        f = data / "mcd43c4" / f"mcd43c4_0p5_{year}{m:02d}.nc"
        if f.exists():
            ds = xr.open_dataset(f)
            nbar_m.append(ds.nbar)
            snow_m.append(ds.percent_snow)
        else:
            print(f"missing {f.name}")
            nbar_m.append(first.nbar * np.nan)
            snow_m.append(first.percent_snow * np.nan)
    modis = xr.concat(nbar_m, dim="month").assign_coords(month=np.arange(1, 13)).load()
    snow = xr.concat(snow_m, dim="month").assign_coords(month=np.arange(1, 13)).load()
    # LPJ writes all-zero spectra where a cell has no PFTs (deserts, ice): PROSAIL never runs there
    lpj_wrote = lpj.max("band") >= 0.005
    both = lpj.notnull() & modis.notnull() & lpj_wrote
    lpj_c, modis_c = lpj.where(both), modis.where(both)
    ndvi_lpj = (lpj_c.sel(band=2) - lpj_c.sel(band=1)) / (lpj_c.sel(band=2) + lpj_c.sel(band=1))
    ndvi_modis = (modis_c.sel(band=2) - modis_c.sel(band=1)) / (modis_c.sel(band=2) + modis_c.sel(band=1))

    # ---- 1. true colour, LPJ vs MODIS, January and July ----
    outf = outdir / "truecolour_lpj_vs_modis.png"
    if outf.exists():
        print(f"skip {outf}")
    else:
        fig, axes = plt.subplots(2, 2, figsize=(13, 7), subplot_kw={"projection": robin})
        for row, month in enumerate([1, 7]):
            for col, (name, da) in enumerate([("LPJ-PROSAIL", lpj), ("MODIS MCD43C4", modis)]):
                rgb = np.stack([da.sel(month=month, band=b).values for b in (1, 4, 3)], axis=-1)
                rgb = np.clip(rgb / 0.3, 0, 1) ** (1 / 2.0)
                rgb = np.where(np.isnan(rgb), 1.0, rgb)
                rgba = np.concatenate([rgb, np.isfinite(da.sel(month=month, band=1).values)[..., None] * 1.0], axis=-1)
                ax = axes[row, col]
                ax.set_facecolor(ocean)
                ax.imshow(rgba, extent=extent, transform=ccrs.PlateCarree(), origin="upper", interpolation="nearest")
                ax.coastlines(lw=0.3, color=ink2)
                ax.set_global()
                ax.set_title(f"{name}, {month_names[month - 1]} {year}", color=ink)
        fig.suptitle("True colour from red / green / blue bands (B1, B4, B3), same stretch for both. "
                     "Black in LPJ: no PFTs, so the model writes zeros", color=ink)
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ---- 2. NDVI maps, LPJ / MODIS / difference ----
    outf = outdir / "ndvi_maps_lpj_vs_modis.png"
    if outf.exists():
        print(f"skip {outf}")
    else:
        fig, axes = plt.subplots(2, 3, figsize=(16, 6.4), subplot_kw={"projection": robin})
        for row, month in enumerate([1, 7]):
            panels = [("LPJ-PROSAIL", ndvi_lpj.sel(month=month), seq_green, 0, 1),
                      ("MODIS MCD43C4", ndvi_modis.sel(month=month), seq_green, 0, 1),
                      ("LPJ − MODIS", ndvi_lpj.sel(month=month) - ndvi_modis.sel(month=month), div, -0.5, 0.5)]
            for col, (name, da, cmap, vmin, vmax) in enumerate(panels):
                ax = axes[row, col]
                ax.set_facecolor(ocean)
                im = ax.imshow(da.values, extent=extent, transform=ccrs.PlateCarree(), origin="upper",
                               cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
                ax.coastlines(lw=0.3, color=ink2)
                ax.set_global()
                ax.set_title(f"{name}, {month_names[month - 1]} {year}", color=ink)
                fig.colorbar(im, ax=ax, orientation="horizontal", shrink=0.6, pad=0.03, label="NDVI" if col < 2 else "ΔNDVI")
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ---- 3. band-by-band 2D histograms, all land cell-months of the year, snow-free ----
    outf = outdir / "band_scatter_lpj_vs_modis.png"
    stats_csv = outdir / "band_stats.csv"
    if outf.exists() and stats_csv.exists():
        print(f"skip {outf}")
    else:
        fig, axes = plt.subplots(2, 4, figsize=(15, 7.5))
        rows = []
        for i, b in enumerate(range(1, 8)):
            ok = (both.sel(band=b) & (snow < snow_max)).values
            x = modis.sel(band=b).values[ok]
            y = lpj.sel(band=b).values[ok]
            bias = float(np.mean(y - x))
            rmse = float(np.sqrt(np.mean((y - x) ** 2)))
            r = float(np.corrcoef(x, y)[0, 1])
            rows.append({"band": b, "name": band_names[b].replace("\n", " "), "n": int(ok.sum()), "modis_mean": float(x.mean()),
                         "lpj_mean": float(y.mean()), "bias": bias, "rmse": rmse, "r": r})
            ax = axes.flat[i]
            top = 0.6 if b in (2, 5, 6) else 0.45
            ax.hist2d(x, y, bins=120, range=[[0, top], [0, top]], cmap=seq_blue, norm=LogNorm(), cmin=1)
            ax.plot([0, top], [0, top], color=ink2, lw=1, ls="--")
            ax.set_title(band_names[b].replace("\n", ", "), color=ink)
            ax.text(0.03, 0.97, f"bias {bias:+.3f}\nRMSE {rmse:.3f}\nr {r:.2f}", transform=ax.transAxes, va="top", color=ink)
            ax.set_xlabel("MODIS NBAR")
            ax.set_ylabel("LPJ-PROSAIL resv")
            ax.set_aspect("equal")
        ok = (ndvi_lpj.notnull() & ndvi_modis.notnull() & (snow < snow_max)).values
        x, y = ndvi_modis.values[ok], ndvi_lpj.values[ok]
        bias, rmse, r = float(np.mean(y - x)), float(np.sqrt(np.mean((y - x) ** 2))), float(np.corrcoef(x, y)[0, 1])
        rows.append({"band": 0, "name": "NDVI", "n": int(ok.sum()), "modis_mean": float(x.mean()), "lpj_mean": float(y.mean()),
                     "bias": bias, "rmse": rmse, "r": r})
        ax = axes.flat[7]
        ax.hist2d(x, y, bins=120, range=[[-0.1, 1], [-0.1, 1]], cmap=seq_blue, norm=LogNorm(), cmin=1)
        ax.plot([-0.1, 1], [-0.1, 1], color=ink2, lw=1, ls="--")
        ax.set_title("NDVI (B1, B2)", color=ink)
        ax.text(0.03, 0.97, f"bias {bias:+.3f}\nRMSE {rmse:.3f}\nr {r:.2f}", transform=ax.transAxes, va="top", color=ink)
        ax.set_xlabel("MODIS NBAR")
        ax.set_ylabel("LPJ-PROSAIL resv")
        ax.set_aspect("equal")
        # same stats for densely vegetated cells only (MODIS NDVI > 0.5)
        dense = ndvi_modis > 0.5
        for b in range(1, 8):
            okd = (both.sel(band=b) & (snow < snow_max) & dense).values
            x, y = modis.sel(band=b).values[okd], lpj.sel(band=b).values[okd]
            rows.append({"band": b, "name": band_names[b].replace("\n", " ") + " [MODIS NDVI > 0.5]", "n": int(okd.sum()),
                         "modis_mean": float(x.mean()), "lpj_mean": float(y.mean()), "bias": float(np.mean(y - x)),
                         "rmse": float(np.sqrt(np.mean((y - x) ** 2))), "r": float(np.corrcoef(x, y)[0, 1])})
        fig.suptitle(f"Every land cell-month of {year} with MCD43C4 snow < {snow_max:.0f} % and an LPJ spectrum. "
                     "Dashed: 1:1. Colour: cell-months (log).", color=ink2, y=1.01)
        fig.tight_layout()
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)
        pd.DataFrame(rows).to_csv(stats_csv, index=False, float_format="%.4f")

    # ---- 4. zonal-mean NDVI by month (Hovmöller) ----
    outf = outdir / "ndvi_zonal_hovmoller.png"
    if outf.exists():
        print(f"skip {outf}")
    else:
        zl = ndvi_lpj.mean("lon")
        zm = ndvi_modis.mean("lon")
        fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharey=True)
        for ax, (name, da, cmap, vmin, vmax) in zip(axes, [("LPJ-PROSAIL", zl, seq_green, 0, 0.9),
                                                          ("MODIS MCD43C4", zm, seq_green, 0, 0.9),
                                                          ("LPJ − MODIS", zl - zm, div, -0.3, 0.3)]):
            im = ax.pcolormesh(np.arange(1, 13), da.lat, da.T.values, cmap=cmap, vmin=vmin, vmax=vmax, shading="nearest")
            ax.set_title(f"{name}, zonal-mean NDVI {year}", color=ink)
            ax.set_xticks(range(1, 13), [m[0] for m in month_names])
            ax.set_ylim(-60, 80)
            fig.colorbar(im, ax=ax, shrink=0.85)
        axes[0].set_ylabel("Latitude (°)")
        fig.tight_layout()
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ---- 5. spectra at sites, four months, with MODIS bands ----
    outf = outdir / "site_spectra.png"
    if outf.exists():
        print(f"skip {outf}")
    else:
        sp = xr.open_dataset(data / f"lpj_spectra_{year}_0p5.nc").resv
        centres = {1: 645, 2: 858.5, 3: 469, 4: 555, 5: 1240, 6: 1640, 7: 2130}
        fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=True)
        for ax, (name, (lon, lat)) in zip(axes.flat, sites.items()):
            cell = sp.sel(lon=lon, lat=lat, method="nearest").load()
            for month, colour in c_months.items():
                s = cell.sel(month=month).values / 10000.0
                if (s < 0).all():
                    continue
                ax.plot(cell.wavelength, s, color=colour, lw=1.6, label=f"LPJ {month_names[month - 1]}")
                m = modis.sel(lon=lon, lat=lat, month=month, method="nearest").values
                ax.plot([centres[b] for b in range(1, 8)], m, "o", ms=6, color=colour, mec="white", mew=1.2,
                        label=f"MODIS {month_names[month - 1]}")
            for lo, hi in [(1350, 1450), (1800, 1950)]:
                ax.axvspan(lo, hi, color=grid_c, lw=0, zorder=0)
            ax.set_title(f"{name}  ({lat:.2f}, {lon:.2f})", color=ink)
            ax.grid(color=grid_c, lw=0.6)
        axes[0, 0].set_ylim(0, 0.7)
        for ax in axes[1]:
            ax.set_xlabel("Wavelength (nm)")
        for ax in axes[:, 0]:
            ax.set_ylabel("Reflectance")
        handles, labels = axes[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, ncol=8, loc="upper center", bbox_to_anchor=(0.5, 1.03), frameon=False)
        fig.text(0.5, -0.01, "Lines: LPJ-PROSAIL resv, 10-nm bins. Dots: MODIS MCD43C4 at band centres. "
                 "Grey: water-vapour absorption bands (no satellite signal there).", ha="center", color=ink2)
        fig.tight_layout()
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ---- 6. global land-mean seasonal cycle per band ----
    outf = outdir / "global_band_seasonal.png"
    if outf.exists():
        print(f"skip {outf}")
    else:
        gl = nc_tools.weight_by_cell_area(lpj_c.to_dataset(name="resv")).mean(("lat", "lon"))
        gm = nc_tools.weight_by_cell_area(modis_c.to_dataset(name="nbar")).mean(("lat", "lon"))
        fig, axes = plt.subplots(2, 4, figsize=(15, 6.5), sharex=True)
        for i, b in enumerate(range(1, 8)):
            ax = axes.flat[i]
            ax.plot(gl.month, gl.sel(band=b), color=c_lpj, lw=2, marker="o", ms=4)
            ax.plot(gm.month, gm.sel(band=b), color=c_modis, lw=2, marker="o", ms=4)
            ax.text(12.2, float(gl.sel(band=b, month=12)), "LPJ", color=ink, va="center")
            ax.text(12.2, float(gm.sel(band=b, month=12)), "MODIS", color=ink, va="center")
            ax.set_title(band_names[b].replace("\n", ", "), color=ink)
            ax.set_xticks(range(1, 13), [m[0] for m in month_names])
            ax.set_xlim(0.5, 13.6)
            ax.grid(color=grid_c, lw=0.6)
        axes.flat[0].set_ylabel("Area-weighted land mean")
        axes.flat[4].set_ylabel("Area-weighted land mean")
        axes.flat[7].axis("off")
        axes.flat[7].plot([], [], color=c_lpj, lw=2, label="LPJ-PROSAIL resv")
        axes.flat[7].plot([], [], color=c_modis, lw=2, label="MODIS MCD43C4 NBAR")
        axes.flat[7].legend(loc="center", frameon=False)
        fig.suptitle(f"Global land mean, {year}, cells where both have data and LPJ wrote a spectrum (snow included)", color=ink)
        fig.tight_layout()
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ---- 7. LPJ NDVI 2010-2023: JJA trend map + annual global series ----
    outf = outdir / "lpj_ndvi_2010_2023.png"
    if outf.exists():
        print(f"skip {outf}")
    else:
        nd = (lpj_all.sel(band=2) - lpj_all.sel(band=1)) / (lpj_all.sel(band=2) + lpj_all.sel(band=1))
        jja = nd.sel(month=[6, 7, 8]).mean("month")
        slope = jja.polyfit("year", 1).polyfit_coefficients.sel(degree=1) * 10
        north = nd.where(nd.lat > 30)
        ann = nc_tools.weight_by_cell_area(north.mean("month").to_dataset(name="ndvi")).mean(("lat", "lon"))
        jja_n = nc_tools.weight_by_cell_area(north.sel(month=[6, 7, 8]).mean("month").to_dataset(name="ndvi")).mean(("lat", "lon"))
        fig = plt.figure(figsize=(15, 5))
        ax = fig.add_subplot(1, 2, 1, projection=robin)
        ax.set_facecolor(ocean)
        im = ax.imshow(slope.values, extent=extent, transform=ccrs.PlateCarree(), origin="upper", cmap=div.reversed(),
                       vmin=-0.08, vmax=0.08, interpolation="nearest")
        ax.coastlines(lw=0.3, color=ink2)
        ax.set_global()
        ax.set_title("LPJ-PROSAIL JJA NDVI trend 2010–2023 (per decade)", color=ink)
        fig.colorbar(im, ax=ax, orientation="horizontal", shrink=0.6, pad=0.03, label="ΔNDVI per decade (blue = greening)")
        ax = fig.add_subplot(1, 2, 2)
        ax.plot(jja_n.year, jja_n, color=c_lpj, lw=2, marker="o", ms=4)
        ax.plot(ann.year, ann, color=c_lpj, lw=2, ls="--", marker="o", ms=4)
        ax.text(2023.3, float(jja_n[-1]), "JJA", color=ink, va="center")
        ax.text(2023.3, float(ann[-1]), "annual", color=ink, va="center")
        ax.set_xlim(2009.5, 2024.6)
        ax.grid(color=grid_c, lw=0.6)
        ax.set_title("LPJ-PROSAIL NDVI, land north of 30°N, area-weighted", color=ink)
        ax.set_ylabel("NDVI")
        fig.tight_layout()
        fig.savefig(outf, dpi=150, bbox_inches="tight")
        plt.close(fig)
