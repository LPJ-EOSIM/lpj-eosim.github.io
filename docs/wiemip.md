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
