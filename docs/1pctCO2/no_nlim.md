# 1pctCO2 ctrl: no_n_limitation (untuned vs tuned vs baseline)

The **no_n_limitation** factorial — N-limitation disabled (`NONLIM`), fire ON —
against the 1pctCO2 **baseline**. Three global control runs (S0): **baseline**
(grey solid), the **untuned** perturbation with default parameters (blue dotted),
and the CMA-ES **tuned** parameters (red dashed). All values are global,
area-weighted annual totals, 1850–2000. Per-variable final-year errors (tuned
vs baseline) are in the table below.

## Carbon stocks

![no_n_limitation carbon stocks: baseline vs untuned vs tuned](../img/wiemip/1pct/nolim_cstocks.png)

## Key stocks & fluxes

![no_n_limitation key stocks and fluxes: baseline vs untuned vs tuned](../img/wiemip/1pct/nolim_keyvars.png)

Global totals at year 2000 (error is tuned vs baseline):

| Variable | Unit | baseline | untuned | tuned | tuned err |
|----------|------|---------:|--------:|------:|----------:|
| VegC  | Pg C      | 528  | 604  | 568  | +7.6%  |
| SoilC | Pg C      | 1607 | 1793 | 1601 | −0.4%  |
| LitC  | Pg C      | 176  | 234  | 177  | +0.6%  |
| GPP   | Pg C yr⁻¹ | 105  | 121  | 115  | +9.7%  |
| Rh    | Pg C yr⁻¹ | 47   | 50   | 53   | +12.2% |
| NPP   | Pg C yr⁻¹ | 48   | 50   | 55   | +14.3% |
| NBP   | Pg C yr⁻¹ | −0.65| −0.84| −0.59| −10.2% |

## What the tune corrected

Removing N-limitation inflates the carbon pools: the **untuned** run sits
**SoilC +12%, LitC +33%, VegC +14%** above the baseline, with GPP +15%. The tune
recovers the stocks almost exactly:

- **SoilC +12% → −0.4%** and **LitC +33% → +0.6%** — the slow soil/litter
  reservoirs, badly inflated by the perturbation, are recovered essentially
  perfectly.
- **VegC +14% → +7.6%** — roughly halved, a small residual high bias.
- The **fluxes** settle a stable ~10–14% above baseline: the tuned ecosystem
  cycles carbon somewhat faster while the pools stay balanced.
