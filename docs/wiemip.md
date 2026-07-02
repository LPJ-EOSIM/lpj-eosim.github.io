# WIEMIP

Comparison of the **WIEMIP CRUJRA** forcing against the **regular CRUJRA**
forcing, and the resulting LPJ-EOSIM runs.

## Forcing variables

Annual means (daily files aggregated per year). Blue = CRUJRA,
red = WIEMIP CRUJRA. CRUJRA covers 1901–2023; WIEMIP CRUJRA covers 1850–2024.

### Air temperature
![temperature](img/wiemip/tmp.png)

### Precipitation
Shown in the files' native (unconverted) units.
![precipitation](img/wiemip/pre.png)

### Specific humidity
![specific humidity](img/wiemip/spfh.png)

### Surface pressure
![surface pressure](img/wiemip/pres.png)

### Downward shortwave radiation
![downward shortwave](img/wiemip/dswrf.png)

### Downward longwave radiation
![downward longwave](img/wiemip/dlwrf.png)

### Wind speed
CRUJRA covers 1898–2023; WIEMIP CRUJRA covers 1850–2023.
![wind speed](img/wiemip/wind.png)

## Overshoot scenario comparison

Global annual-mean forcing for the WIEMIP **overshoot** scenarios
(2024–2300), with the WIEMIP-CRUJRA historical record (1850–2023, grey)
prepended for context. Three GCM drivers — **IPSL-CM6A-LR**, **GFDL-ESM4**,
**UKESM1-0-LL** — and eight overshoot scenarios: Very low (VL), Low (L),
Medium-low (ML), Medium (M) and High (HL), plus the `-CF` variants.

These are **raw** annual means: no smoothing, no value-masking. The CSVs were
regenerated directly from the source NetCDFs (the GFDL↔IPSL labels were
accidentally switched at write time and are corrected here). All source files
were re-synced from the WIEMIP bucket and validated: every field is NaN-free
and every source-year is timestep-complete (1460/1460 6-hourly steps).

### By driver — all variables

Each figure is one driver; the 4×2 panels are the seven forcing variables and
the eight scenarios are overlaid (legend bottom right).

#### IPSL-CM6A-LR
![IPSL all variables](img/wiemip/overshoot/IPSL_all_variables.png)

#### GFDL-ESM4
![GFDL all variables](img/wiemip/overshoot/GFDL_all_variables.png)

#### UKESM1-0-LL
![UKESM all variables](img/wiemip/overshoot/UKESM_all_variables.png)

### By variable — all drivers

Each figure is one variable; the 4×2 panels are the eight scenarios and the
three drivers are overlaid in each panel.

#### Air temperature
![drivers temperature](img/wiemip/overshoot/drivers_tmp.png)

#### Precipitation
![drivers precipitation](img/wiemip/overshoot/drivers_pre.png)

#### Specific humidity
![drivers specific humidity](img/wiemip/overshoot/drivers_spfh.png)

#### Surface pressure
![drivers surface pressure](img/wiemip/overshoot/drivers_pres.png)

#### Downward shortwave radiation
![drivers downward shortwave](img/wiemip/overshoot/drivers_dswrf.png)

#### Downward longwave radiation
![drivers downward longwave](img/wiemip/overshoot/drivers_dlwrf.png)

#### Wind speed
![drivers wind speed](img/wiemip/overshoot/drivers_wind.png)

## SPITFIRE fire drivers — tmin, tmax, wind

Daily **minimum/maximum temperature** and **wind speed** are required by
SPITFIRE but were missing from the initial overshoot conversion. They were
generated with the same `format_LPJ` pipeline as the other CRUJRA drivers —
`tmin`/`tmax` as the daily min/max of the 6-hourly `tmp`, `wind` as the daily
mean — for the historical CRUJRA record (1850–2024) and the four UKESM overshoot
scenarios (2024–2300). Shown here as the **global annual mean** (area-weighted
over land cells); the dotted line marks the 2024 historical→future handoff.

#### Daily minimum temperature
![tmin global annual mean](img/wiemip/overshoot/tmin_tmax_wind/tmin.png)

#### Daily maximum temperature
![tmax global annual mean](img/wiemip/overshoot/tmin_tmax_wind/tmax.png)

#### Wind speed
![wind global annual mean](img/wiemip/overshoot/tmin_tmax_wind/wind.png)

## LPJ-EOSIM performance

Global stocks & fluxes — WIEMIP CRUJRA (overshoot, S2) vs regular CRUJRA (S3).
Note the two runs use different scenarios, so this is not a like-for-like
comparison.

![WIEMIP vs regular CRUJRA stocks & fluxes](img/wiemip/crujra_wiemip_vs_regular.png)

### Overshoot scenario output — all variables

Global diagnostics for the four completed WIEMIP **overshoot** LPJ-EOSIM runs
(**HL**, **M**, **HL_CF**, **L**; 2024–2300), with the WIEMIP-CRUJRA historical
record (1850–2023, black) prepended. Each panel is one output variable; the
value is the **area-weighted global mean** in the variable's native units
(monthly variables are averaged to annual). This is a uniform diagnostic to show
global trajectories, not a carbon-budget integral. The dotted line marks 2024
(historical → scenario handoff).

![WIEMIP overshoot LPJ-EOSIM all-variable diagnostics](img/wiemip/overshoot_lpj/all_variables_diagnostics.png)

### Historical vs control — global carbon & trace-gas budgets

Global **totals** (area-weighted integral, `Σ value × cell area`) for the
overshoot **historical** run (`LPJ-hist`, S2 — transient CO₂, climate, N
deposition, population; land use fixed at 2023) against its **control**
(`LPJ-hist-ctrl`, S0 — CO₂MEAN, constant N deposition and population, recycled
climate, constant land use), both 1850–2023 and both branched from the same
1000+1000-yr spin-up. The control isolates the drift of an unforced system; the
gap between the two is the modelled response to transient forcing.

As expected, the control (dashed) sits near its spin-up equilibrium while the
historical run (solid) shows the CO₂/climate/N-driven rise across all carbon
pools and fluxes. Pools are in Pg C, carbon fluxes in Pg C yr⁻¹; trace gases are
kept in their native units (soil N₂O in Tg N yr⁻¹, fire CH₄ in Tg CH₄ yr⁻¹).

![Historical vs control global carbon & trace-gas budgets](img/wiemip/overshoot_lpj/hist_vs_histctrl_carbon.png)

### Soil carbon — sanity check vs TRENDYv13 LPJwsl

Is the mid-century rise and **~1980 flattening** of the historical soil-carbon
sink realistic, or an artefact? Comparing against the **TRENDYv13 LPJwsl S2**
run (an independent LPJ-family model, cSoil integrated the same way) says it's
real: both models show soil C accumulating strongly through the mid-20th century
and then **plateauing around 1980** — LPJwsl actually peaks ~1990 and declines
slightly after, while LPJ-EOSIM holds roughly flat. The S0 control stays at its
spin-up equilibrium throughout. Absolute pools differ (LPJ-EOSIM ~1610–1627 Pg C
vs LPJwsl ~1284–1317 Pg C) as expected from different soil-carbon schemes, so the
right panel shows the anomaly relative to 1901 to compare trends directly.

The signal is the classic split: the **soil/litter sink saturates under warming**
(decomposition catches up with rising inputs) while the vegetation sink keeps
growing under CO₂ fertilization.

![Soil C vs TRENDYv13 LPJwsl](img/wiemip/overshoot_lpj/soilc_vs_trendyv13.png)
