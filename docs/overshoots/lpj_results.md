# WIEMIP Overshoots — LPJ Results

LPJ-EOSIM carbon and trace-gas output for the WIEMIP **overshoot** experiment:
a 1000+1000-yr spin-up → historical run (`LPJ-hist`, S2, 1850–2023) and its
control (`LPJ-hist-ctrl`, S0). The forcing data behind these runs is on the
[**Driver Data**](driver_data.md) page. Older future-scenario figures built with
a previous model version and flag set have moved to the
[**Archive**](archive.md).

The soil-carbon results and the full investigation of the ~1980 soil-carbon
plateau now live on the [**Soil-C plateau recap**](soilc_plateau_recap.md) page.

## WIEMIP vs regular CRUJRA

Global stocks & fluxes — WIEMIP CRUJRA (overshoot, S2) vs regular CRUJRA (S3).
Note the two runs use different scenarios, so this is not a like-for-like
comparison.

![WIEMIP vs regular CRUJRA stocks & fluxes](../img/wiemip/crujra_wiemip_vs_regular.png)

## Historical vs control — global carbon & trace-gas budgets

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

![Historical vs control global carbon & trace-gas budgets](../img/wiemip/overshoot_lpj/hist_vs_histctrl_carbon.png)
