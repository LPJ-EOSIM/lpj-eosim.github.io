# Soil-C plateau — investigation recap

The overshoot historical soil-carbon sink rises strongly through the mid-20th
century and then **flattens around 1980**. This page collects the full set of
experiments run to work out *why* — and the answer: it is **genuine model
behaviour** (intrinsic soil-pool turnover under nitrogen limitation), not a bug
in the drivers, the spin-up, or the post-processing.

Every hypothesis below was tested by rerunning the model (or auditing the
drivers) and comparing global soil C. The detailed carbon-pool figures for the
permafrost, N-cycle, TRENDY and land-use/climate-robustness tests are on the
[**LPJ Results**](lpj_results.md) page; this page is the summary and the
supporting driver/flux diagnostics.

## Summary — what we tested and what we found

| # | Hypothesis | Test | Verdict |
|---|------------|------|---------|
| 1 | Not real — model artefact | Compare to **TRENDYv13 LPJwsl S2** (independent model) | ❌ real — LPJwsl also plateaus ~1980 |
| 2 | Permafrost dynamics | Rerun spin-up→hist with **PERMAFROST off** | ❌ plateau present (stronger without) |
| 3 | N deposition frozen in time | Check applied ndep vs year | ❌ ndep rises monotonically through 1980 |
| 4 | N deposition wrong magnitude | Global-total ndep in Tg N/yr | ❌ ~77 Tg N/yr, correct (earlier scare was a g-vs-kg label bug) |
| 5 | N deposition spatially mis-registered (lat/lon flip) | Correlate input vs applied ndep fields | ❌ correlation 1.00; hotspots over N China Plain (correct) |
| 6 | Fire consuming the sink | Global fire C flux over time | ❌ ~1 Pg C/yr, flat, no 1980 spike |
| 7 | Coarse-woody-debris decay rate | **SURFCWD 4× → 1×** | ❌ lifts *litter* C hugely, soil plateau unchanged |
| 8 | Slow-SOM decay rate | **SLOWSOM halved, full re-spin** | ❌ raises soil-C *level* +110 Pg, same 1980 plateau |
| 9 | Land-use spin-up length | **lu-spinup 0 vs 1000 yr** | ❌ bit-identical |
| 10 | Recycled (not real) climate | Confirm runtime climate | ❌ already real CRUJRA (+1.8 °C); plateau reinforced by warming |
| 11 | WIEMIP-CRUJRA processing artefact | Rerun with **raw CRUJRA** reanalysis | ❌ identical plateau |
| 12 | Land-use change | **Transient LU** (LUH-GCB2025) | ❌ big vegetation-C change, soil plateau intact |
| ✅ | **Nitrogen limitation** | Rerun with **N cycle off** | ✅ soil C rises monotonically — no plateau |

**Bottom line:** the plateau is the classic first-order behaviour of the CENTURY
soil scheme — as warming accelerates decomposition and CO₂ raises productivity,
**heterotrophic respiration catches up with litter inputs and nitrogen becomes
limiting, capping the soil sink around 1980**. Vegetation carbon keeps growing
under CO₂ fertilization; the *dead* pools saturate. This is robust to the climate
dataset, land use, permafrost, spin-up length, and the decomposition-rate
constants (which move the *level*, not the *timing*).

## Fluxes, N deposition & N cycle (the core diagnostic)

For the "true" historical (`LPJ-hist-transientN`: WIEMIP-CRUJRA, transient N dep,
constant 2023 LU): NPP and Rh both rise, and **Rh catches NPP right at ~1980**
(51.6 vs 51.5 Pg C/yr) — the moment the dead pools stop accumulating. Applied N
deposition rises smoothly (23 → 77 Tg N/yr, no freeze), and fire is a small flat
term. So neither ndep timing nor fire explains the knee.

![Soil-C plateau flux & N diagnostics](../img/wiemip/overshoot_lpj/recap/soilc_plateau_diag.png)

## N deposition is spatially correct (no lat/lon flip)

The applied N-deposition field matches the input file **cell-for-cell**
(spatial correlation 1.00; any lat-flip or lon-roll destroys it), with deposition
maxima over the industrial/agricultural hotspots (North China Plain, Indo-Gangetic
plain, Europe, eastern US). So ndep is not landing in the wrong places.

![N deposition input vs applied](../img/wiemip/overshoot_lpj/recap/ndep_spatial_check.png)

## It already uses real transient climate — warming reinforces the plateau

The historical run was never on recycled climatology: its runtime air temperature
warms **+1.8 °C** over 1850–2023 (real CRUJRA, with the mid-century dip). Soil C
plateaus *as the warming accelerates* — warming raises Rh, which offsets the rising
CO₂/N inputs. Real climate makes the plateau **more** likely, not less.

![Runtime temperature vs soil C](../img/wiemip/overshoot_lpj/recap/temp_vs_soilc.png)

## Decomposition-rate knobs move the level, not the plateau

**Coarse-woody-debris decay (SURFCWD 4× → 1×):** slowing it lets the *litter* pool
accumulate hugely (litter C +150 Pg by 2023), but soil C is essentially unchanged
and still plateaus.

![CWD decay test](../img/wiemip/overshoot_lpj/recap/cwd_test_soil_litter.png)

**Slow-SOM decay (SLOWSOM halved, full re-spin):** the clean re-spin (equilibrated
at the new rate) raises the soil-C *level* by ~110 Pg C but reproduces the **same
1980 plateau**. (An earlier transient-from-old-spin-up run showed an apparent
"deferral" — that was purely the slow pool drifting toward its new equilibrium, a
spin-up artefact, corrected by the re-spin.)

![SLOWSOM re-spin test](../img/wiemip/overshoot_lpj/recap/slowsom_respin.png)

## The spin-up length is irrelevant

Running the transient with a 0-yr vs 1000-yr land-use spin-up gives **bit-identical**
soil C — the spin-up restart is already at equilibrium, so its length doesn't shape
the historical trajectory.

![lu-spinup length test](../img/wiemip/overshoot_lpj/recap/lu_spinup_test.png)
