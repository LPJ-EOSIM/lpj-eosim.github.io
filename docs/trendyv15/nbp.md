# TRENDYv15 — NBP and the O₂/N₂ land-sink constraint

Global net biome production for the S3 runs (all forcings varying), as annual
area-weighted sums on the native 0.5° grid, months summed to years,
unsmoothed. The TRENDYv15 and CRU TS 4.10 series are the rebuilt runs on the
phase-continuous spinup; TRENDYv14, v13 and v12 are the earlier vintages.

## O₂/N₂ land-sink constraint

The atmospheric O₂/N₂ budget constrains the **2014–2023 mean land sink to
0.2–1.8 PgC yr⁻¹**, drawn as the green band over exactly that window — the
constraint binds the decadal mean, not any single year. Thick horizontal bars
are each run's 2014–2023 mean.

![Global NBP against the O2/N2 land-sink constraint](../img/trendyv15/nbp_o2n2_constraint.png)

| run | 2014–2023 mean (PgC yr⁻¹) | vs constraint |
|---|---|---|
| CRU TS 4.10 | **1.61** | inside |
| TRENDYv15 (CRUJRAv15) | **1.88** | just above the 1.8 ceiling |
| TRENDYv12 | 1.85 | just above |
| TRENDYv13 | 1.94 | above |
| TRENDYv14 | 2.49 | well above |

The monthly-driven run is the only one satisfying the constraint; the
daily-driven TRENDYv15 misses the ceiling by 0.08 PgC yr⁻¹. This ordering is
consistent with the driver-cadence effect seen throughout the diagnostics: the
daily CRUJRA forcing sustains a wider NPP−Rh gap and hence a stronger sink than
the monthly CRU forcing on identical model code.

## NBP since 1959, with the GCP record

Annual values and the accumulated sink, against the Global Carbon Project
estimate and its uncertainty. The cumulative panel is the quantity ILAMB's
Global Net Ecosystem Carbon Balance score compares; totals are labelled at
2015, where the GCP record ends, so all runs are compared over the same window.

![Global NBP since 1959 with GCP observations](../img/trendyv15/nbp_1959_present.png)

Over 1959–2015 the CRUJRA-driven runs accumulate ~25 PgC of the observed
~45 PgC land sink; the CRU-driven runs accumulate essentially none. All five
runs track the observed interannual pattern (ENSO troughs and uptake years)
closely — the differences are in the persistent offset, not the variability.

Note the tension between the two constraints: the daily-driven run is far
closer to the GCP *cumulative* sink, while the monthly-driven run is the one
inside the O₂/N₂ *decadal* window — no single run satisfies both.

## Recent NBP, S2 and S3, unsmoothed

The interannual structure over 1980–2025, annual values with no smoothing.

![S2 and S3 NBP 1980-2025 annual unsmoothed](../img/trendyv15/nbp_zoom_S2_S3.png)

All runs agree on the phase of the variability; the daily-driven TRENDYv15 has
the largest amplitude in both scenarios, and CRU TS 4.10 the most damped.

## Reproducing

Figures from `code/plot_nbp_o2n2.py` and `code/plot_nbp_1959.py` in the
simulations tree; series from `plots/aggregate.py` (area-weighted global sums
per year). The GCP reference ships with ILAMB
(`ilamb_data/nbp/GCP/nbp_1959-2016.nc`).
