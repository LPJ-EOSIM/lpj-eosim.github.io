# SPITFIRE integration — PR #421

Model source: [LPJ PR #421](https://github.com/LPJ-EOSIM/LPJ/pull/421)

Integration of the **SPITFIRE** fire model into LPJ-EOSIM, run globally with the
**CRUJRA** driver. The following figures include LPJ runs with the following flag combinations:

| run | spitfire | nitrogen | RESP_OPT/M10DAYR |
|---|:--:|:--:|:--:|
| `S2/S3-spitfire` | ✓ | – | – |
| `S2/S3-spitfire-N` | ✓ | ✓ | – |
| `S2/S3-spitfire-N-ropt` | ✓ | ✓ | ✓ |

All runs follow the standard LPJ-EOSIM protocol:
1000-yr nat-veg spin-up; 398-yr land-use spin-up; 1700–2024 transient, using CRUJRA climate forcing
on a 0.5° grid.


## Net Biome Production 

Global annual NBP. Under CRUJRA the **S2↔S3 split is large** (~1.1–1.5 PgC/yr lower
for S3, the transient-land-use drawdown), nitrogen lowers the sink, and resp-opt
nudges it back up. Resp opt simulates thermal acclimation of leaf respiration.

![NBP](img/spitfire/nbp.png)

### O₂/N₂ land-sink constraint (2014–2023 mean ∈ 0.2–1.8 PgC/yr)
Numbers from some guidance (that was subsequently discarded) from TRENDYv14.

Figure below includes all S3 runs vs the atmospheric O₂/N₂ constraint. TRENDYv13 is included as a reference.
**Satisfying:** `spitfire-N` (1.45), `spitfire-N-ropt` (1.74) and the no-N
`spitfire` (1.74) all fall inside; the non-fire `main` (1.96) and TRENDYv13 S3 (1.94)
overshoot. No model permutation gives unrealistic results.

![NBP O2/N2 constraint](img/spitfire/nbp_o2n2_constraint.png)
For 2015/16 there's a big NBP difference between TRENDYv13 and the rest of the ensemble. Difference maps are below.
Note that TRENDYv13 is run on monthly interpolated CRU data while the rest of the runs use daily CRUJRA.

![2016 NBP diff spitfire-N vs TRENDYv13](img/spitfire/nbp_diff_2016.png)

### Latitudinal NBP

Annual NBP summed over latitude bands — South (90°S–30°S), Tropics (30°S–30°N),
North (30°N–60°N), Boreal (60°N–90°N) — 2000–present, PgC/yr (+ = sink),
with TRENDYv13 S3 for reference. All newer models show the tropics as a significant source compared
to TRENDYv13. This potentially aligns with the 2015/2016 El Nino event.

![latitudinal NBP](img/spitfire/nbp_latbands.png)

## All stocks & fluxes on the same figure

Global GPP/NPP/NBP/Rh (PgC/yr), Veg/Soil/Litter C (PgC), Fire C (PgC/yr),
burned area (Mha/yr) and soil N₂O (TgN/yr, N runs). All generally show the same IAV and range of parameters, though 
soil carbon is a bit higher than the rest for the spitfire-n-ropt runs.

![stocks and fluxes 1980-present](img/spitfire/stocks_fluxes_1980.png)

Full transient (1700–present) shows aligned temporal resolution. The effect of fertilizer can
clearly be seen in the N2O plot.


![stocks and fluxes 1700-present](img/spitfire/stocks_fluxes_1700.png)

## Fire

### Global fire carbon emissions

![firec](img/spitfire/firec.png)

**Mean global fire C (PgC/yr)** — with the LPJmL retune all runs now sit **at or below** the
GFED4.1s reference (~2.2), spanning ~1.4–2.1 PgC/yr (S3-spitfire-N lowest at 1.4, S2-spitfire
closest at 2.1). TRENDYv13 shown for context:

Globally the model burns ~455–585 Mha/yr (run-dependent) vs GFED's ~475 Mha/yr (≈−5% to +25%).

### Burned fraction maps vs GFED4.1s (1996–2016 climatology)

Per run: model `firef` | GFED4.1s | model − GFED (%).

![firef vs GFED maps](img/spitfire/firef_vs_gfed_maps.png)


### Global summary vs literature

Global stocks and fluxes for all six runs against literature reference values
(30-yr mean, 1995–2024). Cell colour = % deviation (blue under, red over); the
composite score is the fire-weighted mean absolute deviation (lower = better).
Fire C now lands −5% to −37% of GFED (all runs at/below; S2-spitfire closest, −5%); burned area
brackets GFED (−4% to +23%). **S3-spitfire-N** is the best overall (composite 16.4%).

![global scorecard vs literature](img/spitfire/bench_global_scorecard.png)

### Skill summary

`model`/`GFED`/`bias` are global means (firef = area-weighted %/yr; firec =
PgC/yr). `r_interann` = global interannual correlation. `spatial r²/NSE/RMSE` =
across-region pattern skill over the 14 GFED regions (the scatter metric below).

Global burned area now brackets GFED (~3.3–4.3 %/yr vs 3.5); global fire C sits at/below GFED
(closest is S2-spitfire, bias −0.06 PgC/yr; the S3 nitrogen runs undershoot most, ~−0.8).
Across-region pattern skill is high (firec spatial r² 0.84–0.90, NSE 0.79–0.86); interannual
correlation is weak (|r| ≤ 0.36, several negative) — the runs capture *where* and *how much* fire
occurs better than *which years*.

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
EOSIM−LPJ-GUESS (2010–2016 overlap). With the LPJmL retune EOSIM now sits below GFED by
somewhat more than the LPJ-GUESS peer (mean EOSIM−GFED −5.3, LPJ-GUESS−GFED −2.3,
EOSIM−LPJ-GUESS −3.1 gC m⁻² yr⁻¹).

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
(~0.67 vs ~0.52 without) at no cost to the other carbon-cycle metrics.

- <a href="../ilamb-crujra-s3/">ILAMB benchmark (CRUJRA S3 bitlist)</a>

<iframe
  src="../ilamb-crujra-s3/"
  title="ILAMB results for CRUJRA S3 spitfire bitlist"
  style="width: 100%; min-height: 900px; border: 1px solid #d7dce2; border-radius: 0.2rem;"
></iframe>
