# SPITFIRE in LPJ-EOSIM (CRUJRA)

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
