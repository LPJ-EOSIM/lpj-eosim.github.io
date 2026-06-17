# WIEMIP

Comparison of the **WIEMIP CRUJRA** forcing against the **regular CRUJRA**
forcing, and the resulting LPJ-EOSIM runs.

## Forcing variables

Annual means, 1850–2024 (daily files aggregated per year). Blue = CRUJRA,
red = WIEMIP CRUJRA.

CRUJRA is flat because its per-year annual mean is held constant across the
whole record (a detrended, constant-mean recycled climatology — daily
variability still differs year to year). WIEMIP CRUJRA carries the real
transient trend.

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
Only 1850–1891 is available in these files.
![wind speed](img/wiemip/wind.png)

## LPJ-EOSIM performance

Global stocks & fluxes — WIEMIP CRUJRA (overshoot, S2) vs regular CRUJRA (S3).
Note the two runs use different scenarios, so this is not a like-for-like
comparison.

![WIEMIP vs regular CRUJRA stocks & fluxes](img/wiemip/crujra_wiemip_vs_regular.png)
