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

These are **raw** annual means: no smoothing, no masking, no gap-filling. Where
files are missing the lines simply break; a handful of points are exactly zero
(a source NaN coerced to 0) and show up as spikes-to-zero. Every missing,
NaN and zero value is itemised in the
[data-integrity report](img/wiemip/overshoot/missing_and_nan_report.txt).

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

## LPJ-EOSIM performance

Global stocks & fluxes — WIEMIP CRUJRA (overshoot, S2) vs regular CRUJRA (S3).
Note the two runs use different scenarios, so this is not a like-for-like
comparison.

![WIEMIP vs regular CRUJRA stocks & fluxes](img/wiemip/crujra_wiemip_vs_regular.png)
