# Benchmark runs at 7a1fa06 / fbc7d07 — ILAMB

[**Open the full ILAMB site →**](ilamb-benchmark-7a1fa06/index.html)

Nine runs benchmarked with ILAMB against observations, all from raw LPJ output:

- **This PR's runs:** TRENDY CRU S3 at 7a1fa06 (pre-1901 year sampling back on `rand()`),
  and at fbc7d07 TRENDY CRUJRA v1.5 S3, NMIP3 SH1, and the ERA5 / MERRA2 / JRA3Q CH4 runs.
- **Previous TRENDY S3 submissions:** v13, v14 and v15 (CRU410).

Scores run 0–1, where 1 is perfect agreement. Global region only.

## Scores

The mean is the unweighted average of the seven variable scores.

| Model | Mean | Biomass | GPP | Reco | Soil C | ET | Burned area | Runoff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NMIP3_SH1_fbc7d07 | **0.666** | 0.653 | 0.663 | 0.606 | 0.712 | 0.683 | 0.626 | 0.715 |
| TRENDYv15_CRU410_S3 | **0.634** | 0.645 | 0.621 | 0.573 | 0.693 | 0.690 | 0.524 | 0.690 |
| TRENDY_CRU_S3_7a1fa06 | **0.632** | 0.639 | 0.616 | 0.561 | 0.697 | 0.697 | 0.521 | 0.694 |
| ERA5_CH4_fbc7d07 | **0.632** | 0.628 | 0.620 | 0.561 | 0.721 | 0.705 | 0.537 | 0.648 |
| TRENDY_CRUJRAv15_S3_fbc7d07 | **0.631** | 0.640 | 0.618 | 0.543 | 0.702 | 0.681 | 0.520 | 0.714 |
| MERRA2_CH4_fbc7d07 | **0.630** | 0.656 | 0.603 | 0.553 | 0.726 | 0.695 | 0.531 | 0.648 |
| TRENDYv14_CRU_S3 | **0.627** | 0.658 | 0.619 | 0.574 | 0.625 | 0.693 | 0.533 | 0.688 |
| TRENDYv13_CRU_S3 | **0.622** | 0.645 | 0.620 | 0.572 | 0.694 | 0.640 | 0.496 | 0.689 |
| JRA3Q_CH4_fbc7d07 | **0.617** | 0.612 | 0.602 | 0.535 | 0.716 | 0.666 | 0.527 | 0.660 |

The runs from this PR fall in the same range as the previous TRENDY submissions: 0.617–0.666 against 0.622–0.634.
NMIP3 SH1 has the highest mean, leading on GPP, Reco, burned area and runoff.

## Benchmarks

Biomass (Saatchi, Thurner, ESACCI, XuSaatchi), GPP (FLUXNET2015, FLUXCOM, WECANN),
ecosystem respiration (FLUXNET2015, FLUXCOM), soil carbon (HWSD, NCSCDV22),
evapotranspiration (GLEAM v3.3a, MODIS, MOD16A2), burned area (GFED4.1S),
runoff (Dai, LORA, CLASS).

LAI, NBP, CO₂ and extended soil carbon (Koven) are **not included**: their reference
data is not on Hellgate. This page is therefore not directly comparable to the
[TRENDYv15 ILAMB page](../trendyv15/ilamb.md), which scored 13 variables.

## Caveats

- **XuSaatchi biomass bias score is about 0.03 for every model**, although model biomass (487–778 Pg)
  is close to the reference (475 Pg). Because the value is identical across models, it points to that
  benchmark's configuration, and it pulls every Biomass score down.
- **Burned-area seasonal-cycle score is 0.451 for every model.** `format_ilamb.sh` spreads annual
  burned area evenly across the 12 months, so no model has a seasonal cycle to score.
- **TRENDYv13**: burned area is about 10× the other runs (1.09% vs GFED 0.33%), and ET leaves out
  canopy interception because the run has no `minterc` output.
- **TRENDYv14**: soil carbon is 1912 Pg against HWSD's 1234 Pg.

## Reproducing

Driven by `code/ilamb/run_ilamb.py` in `/mnt/beegfs/scratch/tc229954e/benchmark`, which makes the
same calls as the pipeline's `ilamb.py` (`CommandWriter` + `postprocess.submit_ilamb_job`, then
`format_ilamb.sh` per model and `ilamb-run`). The config `code/ilamb/ilamb.cfg` is the pipeline's
`util/ilamb.cfg` with three changes: reference paths moved to `/mnt/beegfs/projects/tc229954e/ilamb_data`,
Biomass `alternate_vars = "vegc,cVeg"`, and the benchmarks listed above removed.
