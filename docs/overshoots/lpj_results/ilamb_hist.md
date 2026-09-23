# ILAMB: historical vs fix-spitfire historical

[**Open the full ILAMB site →**](../../results/ilamb-wiemip-hist/index.html)

The two WIEMIP overshoot historical runs (WIEMIP CRUJRA, 1850–2023, global),
benchmarked with ILAMB 2.7.3 against the eight-row confrontation set used on the
[NMIP SH1 fire-fix chain page](../../nmip/sh1_fire_fixes_ilamb.md).

| model | run directory | what it is |
|---|---|---|
| `wie_hist` | `wiemip_results/overshoot/LPJ-wie-hist` | the historical run behind every other page in this section |
| `fix_spitfire_hist` | `wiemip_results/overshoot_20260923/LPJ-wiemip-fix-spitfire-hist` | same flags and driver, rebuilt with the SPITFIRE fixes, from its own spinup (`LPJ-wiemip-fix-spitfire-spinup`) |

The compile flags are identical between the two `LPJ_snapshot/` trees. The
source differs in two groups of changes:

- **The full NMIP SPITFIRE fix chain:**
    - fire stand weighting (`afire_frac` is tracked per stand, not per cell)
    - live grass removed from the Byram flaming-front numerator (`dailyfire.c`)
    - PFT-resolved CENTURY surface fuel via `pft_fuel_mass()` (`moistfactor.c`, `fuelload.c`)
    - the `GLOBFIRM` + `SPITFIRE` `#error` guard in `lpj.h`
- **A killed-litter nitrogen fix** in `reclaim_land.c` and
  `landusechange_GROSS.c`. This one is not fire-related.

Differences below therefore mix both groups of changes and a different spinup.
They are not a fire-only ablation.

## Scorecard

| row | `wie_hist` | `fix_spitfire_hist` | Δ |
|---|---|---|---|
| Biomass | 0.6969 | 0.6951 | −0.0018 |
| Gross Primary Productivity | 0.6544 | 0.6543 | −0.0001 |
| Ecosystem Respiration | 0.6006 | 0.6018 | +0.0012 |
| Net Ecosystem Exchange | 0.4375 | 0.4385 | +0.0010 |
| Soil Carbon | 0.6846 | 0.6848 | +0.0002 |
| Evapotranspiration | 0.6836 | 0.6837 | +0.0001 |
| Burned Area | 0.6424 | **0.6513** | **+0.0088** |
| Runoff | 0.7103 | 0.7102 | −0.0000 |
| **Overall (mean of 8 rows)** | **0.6388** | **0.6400** | +0.0012 |

Every row is scored for both models, and no confrontation failed.

**Burned Area is the only row that moves.** The other seven agree to within
0.002. The overall mean moves by +0.0012, which is the Burned Area gain diluted
by seven flat rows. It is not a general improvement.

## Burned Area (GFED4.1S, 1997–2016)

| | `wie_hist` | `fix_spitfire_hist` |
|---|---|---|
| global mean / GFED4.1S | **0.71×** (0.236 vs 0.332 %) | **1.05×** (0.347 vs 0.332 %) |
| Bias Score | 0.7274 | 0.7206 |
| Spatial Distribution Score | 0.7001 | **0.7510** |
| RMSE Score | 0.6666 | 0.6666 |
| Seasonal Cycle Score | 0.4514 | 0.4514 |

- **The fix takes global burned area from 29% too low to 5% too high.** This is
  the opposite direction from NMIP SH1: there, the same fixes brought an
  overestimate down (1.57× → 1.25× GFED).
- **The Overall Score gain comes from the spatial pattern.** Bias Score drops
  slightly even though the global mean is much closer. Bias Score is a
  pointwise `exp(-|bias|/σ)` average, so where the fire sits can outweigh the
  global total.
- **Seasonality is unchanged.** RMSE and Seasonal Cycle scores are identical to
  four decimals. The 0.451 seasonal-cycle score is the same separate problem
  seen on the NMIP pages.

## The other rows

- **Biomass drops slightly (−0.0018).** Global vegetation C is ~1–2 Pg lower
  in `fix_spitfire_hist` (e.g. 454.5 vs 456.5 Pg on the ESACCI mask), which is
  consistent with more fire. Every product's Bias Score falls by a similar
  small amount.
- **Carbon fluxes move slightly.** GPP is ~0.5 Pg C yr⁻¹ lower and Reco
  ~0.7 Pg C yr⁻¹ lower (FLUXCOM masks). Ecosystem Respiration and NEE scores
  gain ~0.001.
- **Soil Carbon is a single-year snapshot** (`selyear,2000`), so the near-flat
  score mostly reflects the two spinup equilibria. Global soil C differs by
  ~3 Pg on the HWSD mask.

## Changes from the NMIP config

- **The `[Fluxnet]` NEE dataset is dropped.** Its custom obs file is gone and
  is not in the stock ILAMB-Data collection. NEE is scored against FLUXNET2015
  only, so this Net Ecosystem Exchange row is not directly comparable with the
  NMIP pages.
- **Reference data were re-fetched.** The old `scratch/tc229954e/ilamb_data/`
  tree is gone, so the 21 obs files this config uses were downloaded fresh
  from `ilamb.org/ILAMB-Data`, sha1-checked, into
  `/mnt/beegfs/projects/tc229954e/ilamb_data/`. The filenames are the same as
  in the old tree.

## Reproducing

All scripts are in `scratch/tc229954e/wiemip_results/ilamb_hist/code/`.

`run_ilamb.sh` is the whole slurm job:

1. It fetches any missing obs files listed in `needed.txt` and checks each
   against ILAMB's `SHA1SUM`.
2. It reformats both runs in parallel via `pipeline/util/format_ilamb.sh`,
   reading `ncdf_outputs/` directly.
3. It runs `ilamb-run` under `mpirun -np 12` with `code/ilamb.cfg`.

Unset the head-node proxy variables inside the job. Compute nodes have direct
internet but cannot reach `127.0.0.1:8899`.

The benchmark took ~4 minutes on one `cpu(all)` node once the reformatted
inputs existed. Only the HTML and figures are committed here, not the NetCDF.
