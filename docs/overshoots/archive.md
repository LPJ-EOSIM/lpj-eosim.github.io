# WIEMIP Overshoots — Archive (older future runs)

!!! warning "Superseded figures"
    The future-scenario figures below were produced with an **earlier version of
    the model and a different flag set** (notably the futures branched with
    `CONSTANT_NDEP`/`CONSTANT_POP`, freezing N deposition and population at 1850
    values). They are kept here for reference only and should **not** be used for
    current analysis. Up-to-date historical results are on the
    [**LPJ Results**](lpj_results/index.md) page.

## Historical + HL future — full trajectory (global totals)

Key stocks and fluxes over the whole **1850–2300** timeline: the historical run
(`LPJ-hist`, S2; blue) spliced with the **HL** future (2024–2300; red), each as
an area-weighted global total (`Σ value × cell area`). Pools in Pg C, carbon
fluxes in Pg C yr⁻¹; trace gases in native units (soil N₂O in Tg N yr⁻¹, fire
CH₄ in Tg CH₄ yr⁻¹). The dotted line marks the 2024 historical→future handoff.

![Historical + HL future stocks & fluxes](../img/wiemip/overshoot_lpj/hist_hl_future_stocks_fluxes.png)

## Overshoot scenario output — all variables

Global diagnostics for the four completed WIEMIP **overshoot** LPJ-EOSIM runs
(**HL**, **M**, **HL_CF**, **L**; 2024–2300), with the WIEMIP-CRUJRA historical
record (1850–2023, black) prepended. Each panel is one output variable, reduced
to the physically meaningful global quantity for its type:

- **Extensive** mass variables are **global sums** (area integral
  `Σ value × gridarea`): carbon pools and fluxes in **Pg C** (`kg C m⁻²`
  fluxes summed to annual totals first), nitrogen fluxes/pools in **Tg N**, and
  fire trace gases in **Tg species** (CH₄, CO₂, CO, NOₓ, VOC, TPM). A handful of
  N-cycle fields that LPJ tags with a carbon unit string (`g C m⁻²`) are treated
  as nitrogen by name.
- **Intensive** variables (air/soil temperature, LAI, wind, soil moisture,
  radiation, precipitation, population density, …) are shown as the
  **area-weighted global mean** in native units, since a spatial sum is not
  meaningful for them.

Validated against known global magnitudes (e.g. GPP ≈ 126 Pg C yr⁻¹, soil C
≈ 1630 Pg C, veg C ≈ 520 Pg C, BNF ≈ 135 Tg N yr⁻¹). The dotted line marks 2024
(historical → scenario handoff).

![WIEMIP overshoot LPJ-EOSIM all-variable diagnostics](../img/wiemip/overshoot_lpj/all_variables_diagnostics.png)
