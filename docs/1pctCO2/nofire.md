# 1pctCO2 ctrl: nofire (untuned vs tuned vs baseline)

The **nofire** factorial — SPITFIRE compiled out (fire off), N-limitation on —
against the 1pctCO2 **baseline**. Three global control runs (S0): **baseline**
(grey solid), the **untuned** perturbation with default parameters (blue dotted),
and the CMA-ES **tuned** parameters (red dashed). All values are global,
area-weighted annual totals, 1850–2000. Per-variable final-year errors (tuned
vs baseline) are in the table below.

## Carbon stocks

![nofire carbon stocks: baseline vs untuned vs tuned](../img/wiemip/1pct/nofire_cstocks.png)

## Key stocks & fluxes

![nofire key stocks and fluxes: baseline vs untuned vs tuned](../img/wiemip/1pct/nofire_keyvars.png)

Global totals at year 2000 (error is tuned vs baseline):

| Variable | Unit | baseline | untuned | tuned | tuned err |
|----------|------|---------:|--------:|------:|----------:|
| VegC  | Pg C      | 528  | 605  | 539  | +2.1%  |
| SoilC | Pg C      | 1607 | 1551 | 1635 | +1.7%  |
| LitC  | Pg C      | 176  | 186  | 185  | +5.2%  |
| GPP   | Pg C yr⁻¹ | 105  | 104  | 120  | +13.9% |
| Rh    | Pg C yr⁻¹ | 47   | 46   | 51   | +8.5%  |
| NPP   | Pg C yr⁻¹ | 48   | 46   | 50   | +5.4%  |
| NBP   | Pg C yr⁻¹ | −0.65| −0.71| −0.73| +11.1% |

## What the tune corrected

Removing fire mainly reshuffles the vegetation and litter pools: the **untuned**
nofire run holds **VegC +15%** (fire no longer burns down biomass) and **SoilC
−3.5%** relative to the baseline. The tune brings the stocks close to the
baseline:

- **VegC +15% → +2.1%** — the biomass excess from removing fire is almost fully
  corrected.
- **SoilC −3.5% → +1.7%** and **LitC +5.2%** — both soil and litter pools land
  within a few percent.
- The **fluxes** run a stable ~5–14% above baseline (GPP +13.9%, Rh +8.5%): the
  tuned no-fire ecosystem is somewhat more productive, with the carbon pools held
  near the baseline.

## Rising-CO₂ stages: bgc & cou

The parameters were fit against the **ctrl** state only. These panels show how the
tuned no_fire run behaves under the rising-1pctCO₂ stages — **bgc** (S1, fixed
recycled climate) and **cou** (S2, transient UKESM climate) — against the baseline.
Two lines: baseline (black) vs tuned (vermillion); the untuned perturbation was
ctrl-only so it doesn't appear here.

### bgc (S1, rising CO₂ / fixed climate)

![nofire bgc: baseline vs tuned](../img/wiemip/1pct/nofire_bgc.png)

| Variable | Unit | baseline | tuned | err |
|----------|------|---------:|------:|----:|
| VegC  | Pg C      | 1045 | 1337 | +27.9% |
| SoilC | Pg C      | 1834 | 1883 | +2.7%  |
| LitC  | Pg C      | 369  | 411  | +11.6% |
| GPP   | Pg C yr⁻¹ | 199  | 252  | +26.4% |
| NPP   | Pg C yr⁻¹ | 102  | 117  | +14.9% |
| Rh    | Pg C yr⁻¹ | 91   | 110  | +20.7% |
| fireC | Pg C yr⁻¹ | 4.8  | 0    | (no fire) |

### cou (S2, transient UKESM climate)

![nofire cou: baseline vs tuned](../img/wiemip/1pct/nofire_cou.png)

| Variable | Unit | baseline | tuned | err |
|----------|------|---------:|------:|----:|
| VegC  | Pg C      | 926  | 1404 | +51.6% |
| SoilC | Pg C      | 1701 | 1738 | +2.2%  |
| LitC  | Pg C      | 273  | 325  | +19.2% |
| GPP   | Pg C yr⁻¹ | 220  | 279  | +26.9% |
| NPP   | Pg C yr⁻¹ | 108  | 126  | +17.0% |
| Rh    | Pg C yr⁻¹ | 97   | 117  | +20.7% |
| NBP   | Pg C yr⁻¹ | 4.2  | 9.2  | +119%  |

**Caveat:** because the tune only constrained the control state, the CO₂-forced
stages run substantially hot — SoilC stays close (+2–3%) but VegC and productivity
diverge strongly (VegC +28% bgc / +52% cou, GPP +27%). The ctrl-tuned parameters do
not constrain the transient CO₂-fertilization response.
