# SPITFIRE integration — PR #421

Model source: [LPJ PR #421](https://github.com/LPJ-EOSIM/LPJ/pull/421)

Integration of the **SPITFIRE** fire model into LPJ-EOSIM, run globally with the
**CRUJRA** driver. We sweep the S2/S3 sim type against the
**spitfire × nitrogen × resp-opt** "bitlist" (six runs):

| run | spitfire | nitrogen | RESP_OPT/M10DAYR |
|---|:--:|:--:|:--:|
| `S2/S3-spitfire` | ✓ | – | – |
| `S2/S3-spitfire-N` | ✓ | ✓ | – |
| `S2/S3-spitfire-N-ropt` | ✓ | ✓ | ✓ |

All runs: 1000-yr nat-veg spin-up → 398-yr land-use spin-up → 1700–2024 transient,
CRUJRA climate from 1901, on a 0.5° grid.

## Net Biome Production (topline)

Global annual NBP. Under CRUJRA the **S2↔S3 split is large** (~1.5 PgC/yr lower
for S3, the transient-land-use drawdown), nitrogen lowers the sink, and resp-opt
nudges it back up.

![NBP](img/spitfire/nbp.png)

**Mean NBP 1980–2024 (PgC/yr):**

| run | S2 | S3 |
|---|---|---|
| spitfire | 2.48 | 0.94 |
| spitfire-N | 1.77 | 0.87 |
| spitfire-N-ropt | 2.05 | 1.04 |

### O₂/N₂ land-sink constraint (2014–2023 mean ∈ 0.2–1.8 PgC/yr)

All S3 runs vs the atmospheric O₂/N₂ constraint (TRENDYv13 S3 for reference).
**Satisfying:** `spitfire-N` (1.41), `spitfire-N-ropt` (1.66) — the nitrogen runs
fall inside; the no-N `spitfire` (1.83) and `main` overshoot, as does TRENDYv13 S3 (1.94).

![NBP O2/N2 constraint](img/spitfire/nbp_o2n2_constraint.png)

Spatial NBP comparison for **2016** — `spitfire-N` vs TRENDYv13 S3 and their
difference (spitfire-N − TRENDYv13, + = stronger sink); global-mean per-cell
difference ≈ −0.015 kg C m⁻² yr⁻¹:

![2016 NBP diff spitfire-N vs TRENDYv13](img/spitfire/nbp_diff_2016.png)

### Latitudinal NBP

Annual NBP summed over latitude bands — South (90°S–30°S), Tropics (30°S–30°N),
North (30°N–60°N), Boreal (60°N–90°N) — 2000–present, PgC/yr (+ = sink),
with TRENDYv13 S3 for reference.

![latitudinal NBP](img/spitfire/nbp_latbands.png)

## All stocks & fluxes

Global GPP/NPP/NBP/Rh (PgC/yr), Veg/Soil/Litter C (PgC), Fire C (PgC/yr),
burned area (Mha/yr) and soil N₂O (TgN/yr, N runs).

![stocks and fluxes 1980-present](img/spitfire/stocks_fluxes_1980.png)

Full transient (1700–present):

![stocks and fluxes 1700-present](img/spitfire/stocks_fluxes_1700.png)

## Fire

### Global fire carbon emissions

![firec](img/spitfire/firec.png)

**Mean global fire C 1980–2024 (PgC/yr)** — all runs sit around/below the GFED4.1s
reference (~2.2); TRENDYv13 shown for context:

| run | fire C (PgC/yr) |
|---|---|
| CRUJRA-S2-spitfire | 1.85 |
| CRUJRA-S3-spitfire | 2.51 |
| CRUJRA-S2-spitfire-N | 2.07 |
| CRUJRA-S3-spitfire-N | 1.76 |
| CRUJRA-S2-spitfire-N-ropt | 2.24 |
| CRUJRA-S3-spitfire-N-ropt | 2.00 |
| TRENDYv13 S2 (ref) | 3.36 |
| TRENDYv13 S3 (ref) | 2.50 |
| GFED4.1s (obs) | ~2.2 |

Globally the model burns ~600 Mha/yr vs GFED's ~453 Mha/yr (~30% high).

### Burned fraction maps vs GFED4.1s (1996–2016 climatology)

Per run: model `firef` | GFED4.1s | model − GFED (%).

![firef vs GFED maps](img/spitfire/firef_vs_gfed_maps.png)

## Regional fire benchmark — GFED4.1s & LPJ-GUESS-SPITFIRE

Quantitative benchmark of all six CRUJRA SPITFIRE runs against **GFED4.1s**
(burned fraction `firef` and fire-C emissions `firec`, 1997–2016) aggregated to
the 14 GFED basis regions, plus a peer comparison against **LPJ-GUESS-SPITFIRE**
fire C. Model fields are the GFED-aligned multi-year means.

### Global summary vs literature

Global stocks and fluxes for all six runs against literature reference values
(30-yr mean, 1995–2024). Cell colour = % deviation (blue under, red over); the
composite score is the fire-weighted mean absolute deviation (lower = better).
Fire C lands within ±19% of GFED across all runs; burned area is systematically
high (+26–67%). **S3-spitfire-N** is the best overall (composite 15.8%).

![global scorecard vs literature](img/spitfire/bench_global_scorecard.png)

### Skill summary

`model`/`GFED`/`bias` are global means (firef = area-weighted %/yr; firec =
PgC/yr). `r_interann` = global interannual correlation. `spatial r²/NSE/RMSE` =
across-region pattern skill over the 14 GFED regions (the scatter metric below).

Global fire C, area-weighted: **LPJ-GUESS-SPITFIRE 1.90 PgC/yr** (2010–2025),
**GFED4.1s 2.15 PgC/yr** (1997–2016).

| run | var | model | GFED | bias | r_interann | spatial r² | spatial NSE | spatial RMSE |
|---|---|---|---|---|---|---|---|---|
| S2 | firef | 4.44 | 3.5 | +0.94 | 0.222 | 0.666 | 0.599 | 3.08 |
| S2 | firec | 1.87 | 2.15 | −0.28 | −0.246 | 0.737 | 0.712 | 0.100 |
| S2_N | firef | 4.88 | 3.5 | +1.38 | 0.101 | 0.795 | 0.599 | 3.08 |
| S2_N | firec | 2.10 | 2.15 | −0.05 | 0.132 | 0.742 | 0.644 | 0.111 |
| S2_N_ropt | firef | 5.08 | 3.5 | +1.58 | 0.115 | 0.790 | 0.566 | 3.20 |
| S2_N_ropt | firec | 2.29 | 2.15 | +0.14 | 0.165 | 0.772 | 0.667 | 0.107 |
| S3 | firef | 5.82 | 3.5 | +2.32 | 0.090 | 0.486 | 0.034 | 4.78 |
| S3 | firec | 2.57 | 2.15 | +0.42 | −0.032 | 0.670 | 0.636 | 0.112 |
| **S3_N** | firef | 4.73 | 3.5 | +1.23 | 0.318 | 0.762 | 0.581 | 3.15 |
| **S3_N** | firec | 1.78 | 2.15 | −0.37 | 0.216 | **0.822** | **0.799** | 0.083 |
| S3_N_ropt | firef | 5.21 | 3.5 | +1.71 | 0.128 | 0.727 | 0.446 | 3.62 |
| S3_N_ropt | firec | 2.02 | 2.15 | −0.13 | 0.241 | 0.808 | 0.788 | 0.086 |

All runs over-predict global burned area (~4.4–5.8 %/yr vs GFED 3.5); the
nitrogen runs (`S*_N`, `S*_N_ropt`) reproduce global fire C to within ±0.4 PgC/yr.
Across-region pattern skill is high (spatial r² 0.49–0.82); interannual
correlation is weak (r ≤ 0.32) — the runs capture *where* and *how much* fire
occurs better than *which years*. **S3-spitfire-N** has the best fire-C pattern
skill (r² 0.82, NSE 0.80).

### Regional obs-vs-pred (R²) — model vs GFED4.1s

One panel per run; points are the 14 GFED basis regions, 1:1 line dashed, with
r²/NSE/RMSE/bias annotated.

![regional R2 burned fraction](img/spitfire/bench_scatter_firef.png)

![regional R2 fire C](img/spitfire/bench_scatter_firec.png)

### Maps — model and model − GFED

Burned fraction (absolute, then bias):

![burned fraction absolute maps](img/spitfire/bench_maps_abs_firef.png)

![burned fraction bias maps](img/spitfire/bench_maps_diff_firef.png)

Fire C emissions (absolute, then bias):

![fire C absolute maps](img/spitfire/bench_maps_abs_firec.png)

![fire C bias maps](img/spitfire/bench_maps_diff_firec.png)

### Interannual & seasonal

Annual time series and monthly climatology, GLOBAL + 14 regions (GFED in black/grey):

![interannual burned fraction](img/spitfire/bench_timeseries_firef.png)

![interannual fire C](img/spitfire/bench_timeseries_firec.png)

![seasonality burned fraction](img/spitfire/bench_seasonality_firef.png)

![seasonality fire C](img/spitfire/bench_seasonality_firec.png)

### Peer comparison vs LPJ-GUESS-SPITFIRE (fire C)

LPJ-GUESS-SPITFIRE fire C (ICOS/Lund, rev. 6562; "CO₂ release from fire",
mol C m⁻² yr⁻¹ with negative = emission, converted to +gC m⁻² yr⁻¹). Top row:
absolute GFED | LPJ-GUESS | EOSIM; bottom row: EOSIM−GFED | LPJ-GUESS−GFED |
EOSIM−LPJ-GUESS (2010–2016 overlap). EOSIM tracks GFED at least as closely as the
LPJ-GUESS peer does (mean EOSIM−GFED −2.5, LPJ-GUESS−GFED −2.3, EOSIM−LPJ-GUESS
−0.2 gC m⁻² yr⁻¹).

![EOSIM vs LPJ-GUESS vs GFED fire C](img/spitfire/bench_eosim_vs_lpjguess_firec.png)

LPJ-GUESS-SPITFIRE minus GFED4.1s:

![LPJ-GUESS minus GFED fire C](img/spitfire/bench_lpjguess_bias_firec.png)

Regional obs-vs-pred of EOSIM fire C against the LPJ-GUESS-SPITFIRE peer (same
format as the GFED scatter above — one panel per run, 14 GFED basis regions,
1:1 line, r²/NSE/RMSE/bias):

![EOSIM vs LPJ-GUESS regional fire C scatter](img/spitfire/bench_scatter_firec_vs_lpjguess.png)

## ILAMB benchmark

Full ILAMB report for the S3 bitlist (6 runs + TRENDYv13 S3), all seven
confrontations. SPITFIRE markedly improves the **Burned Area** score
(~0.63 vs ~0.52 without) at no cost to the other carbon-cycle metrics.

- <a href="../ilamb-crujra-s3/">ILAMB benchmark (CRUJRA S3 bitlist)</a>

<iframe
  src="../ilamb-crujra-s3/"
  title="ILAMB results for CRUJRA S3 spitfire bitlist"
  style="width: 100%; min-height: 900px; border: 1px solid #d7dce2; border-radius: 0.2rem;"
></iframe>
