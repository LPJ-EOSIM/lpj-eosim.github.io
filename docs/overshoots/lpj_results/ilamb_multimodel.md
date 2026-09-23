# ILAMB: WIEMIP multi-model historical

[**Open the global ILAMB site →**](../../results/ilamb-wiemip-multimodel/index.html)
· [**North of 28.75°N (incl. DVM-DOS-TEM) →**](../../results/ilamb-wiemip-multimodel-north28n/index.html)

The WIEMIP overshoot **historical** run of every model that has one in
`s3://wiemip/overshoot/output/`, plus both LPJ-EOSIM historical runs, benchmarked
with ILAMB 2.7.3 on the same eight-row config as the
[hist vs fix-spitfire page](ilamb_hist.md).

## Global scorecard

| row | CLM | FATES | DLEM | JSBACH | JULES P0005 | JULES P0249 | JULES P0304 | JULES P0336 | JULES noFire | **LPJ-EOSIM** | **LPJ fix-SF** | LPX-Bern | TEM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Biomass | 0.587 | 0.674 | 0.608 | 0.660 | 0.634 | 0.614 | 0.634 | 0.651 | 0.641 | **0.697** | 0.695 | **0.704** | 0.573 |
| GPP | **0.670** | 0.668 | 0.579 | 0.615 | – | – | 0.596 | 0.592 | 0.593 | 0.654 | 0.654 | 0.600 | 0.636 |
| Ecosystem Respiration | 0.590 | **0.614** | 0.565 | 0.603 | 0.556 | 0.558 | 0.559 | 0.550 | 0.551 | 0.601 | 0.602 | 0.543 | **0.614** |
| NEE (−NBP for non-LPJ) | 0.499 | **0.508** | 0.452 | 0.466 | 0.462 | 0.462 | 0.467 | 0.462 | 0.465 | 0.438 | 0.439 | 0.484 | 0.447 |
| Soil Carbon | 0.352 | 0.685 | 0.577 | 0.507 | 0.596 | 0.569 | 0.590 | 0.552 | 0.553 | 0.685 | 0.685 | **0.701** | 0.571 |
| Evapotranspiration | 0.696 | **0.701** | – | 0.642 | – | – | – | – | – | 0.684 | 0.684 | 0.222 | – |
| Burned Area | 0.590 | 0.560 | – | 0.512 | 0.421 | 0.411 | 0.423 | 0.410 | – | 0.642 | **0.651** | 0.470 | – |
| Runoff | 0.707 | 0.702 | 0.661 | 0.610 | – | – | – | – | – | **0.710** | **0.710** | 0.701 | 0.699 |

"–" means the model did not upload that variable. There is no overall mean,
because models are missing different rows, so a mean would reward leaving
variables out.

**LPJ-EOSIM is at or near the top on four of eight rows.** The two LPJ-EOSIM
runs are 1st and 2nd on Burned Area and tied 1st on Runoff. They are 2nd on
Biomass and Soil Carbon (behind LPX-Bern, and tied with FATES on Soil Carbon).
They are mid-pack on GPP, ET and Ecosystem Respiration.

**NEE is LPJ-EOSIM's weakest row relative to the ensemble.** The two LPJ-EOSIM
runs are the two lowest scores (0.438, 0.439). The comparison is not like for like: LPJ-EOSIM is scored on its own
`nee`, while every other model is scored on −NBP, which includes fire and
land-use fluxes.

**Two outliers are data issues, not model skill:**

- **LPX-Bern ET (0.222).** Its `evapotrans` integrates to ~340,000 km³ yr⁻¹,
  about 5× typical terrestrial ET. The median land cell is ~4.5 mm d⁻¹.
  This is in the uploaded file. It looks like a units or aggregation problem
  on their side.
- **CLM Soil Carbon (0.352).** CLM's `cSoilAbove1m` totals ~3,300 Pg C, 2–3×
  HWSD, so it is biased high.

## Models in, and out

| model | run | notes |
|---|---|---|
| CLM | `hh_hist` | `burntArea` is labelled `fraction day-1` but is a monthly fraction (values up to 0.24); treated as monthly |
| CLM-FATES | `FATES_ukesm_hist_land` | burned area from `burntFractionAll` (%); starts 1851 |
| DLEM | `os_hist` | no total ET (only `evapo`), no burned area |
| JSBACH | `hist` | — |
| JULES | 4 fire-parameter variants + `noFire` | no ET or runoff; P0005/P0249 have no `gpp`; P0336 `rh`/`nbp` are in kg m⁻² yr⁻¹ (converted) |
| LPX-Bern | `ukesm_hist` | ET outlier above |
| TEM | `hist` | no ET, no burned area |
| **DVM-DOS-TEM** | `historic` | **north of 28.75°N only — scored in the separate north run** |
| LPJ-EOSIM | `LPJ-wie-hist`, `LPJ-wiemip-fix-spitfire-hist` | formatted by `format_ilamb.sh`, as on the [hist page](ilamb_hist.md) |

**Excluded:**

- **JSBACH `hist_dynveg`:** every value in every uploaded file is NaN.
- **VISIT-UT:** it has no historical run in the bucket, only control and
  futures.
- **17 model folders** in the bucket are empty (a single 0-byte folder marker each): BEPS, BiomeE, CARDAMOM-JPL, CLASSIC, CoLM, EDv3, ELM, GDSTEM, IBIS, KG-FM, LPJ-GUESS, LPJmL6, ModelE-SLSM, ORCHIDEE-MICT-CALIPSO, OSCAR, UVIC, VISIT-NIES.

## Why there are two ILAMB sites

`ilamb-run` clips every model to the **intersection of all models' lat/lon
extents** (`RestrictiveModelExtents` in `ilamb-run`). DVM-DOS-TEM only covers
28.75–90°N. With it included, every model was silently scored only north of
28.75°N: LPJ-EOSIM's GPP/FLUXCOM Overall Score, for example, went from 0.903
globally to 0.742.

- **The global site excludes DVM-DOS-TEM.** LPJ-EOSIM's scores there match the
  [two-model run](ilamb_hist.md) to four decimals on all eight rows.
- **The north site has all 14 models on the 28.75–90°N domain.** It is the only
  place DVM-DOS-TEM is scored. Don't compare its numbers with the global site.

## How the other models were formatted

Every uploaded model breaks the CF conventions somewhere:

- time units like `yr`, `year` or `months since` on a noleap calendar
- DVM-DOS-TEM's time values are all missing
- TEM stores its data as lon/lat/time
- DVM-DOS-TEM uses x/y dims

`standardize.py` therefore rebuilds time from the number of steps, since every
historical run ends in December 2023. It also puts dims into (time, lat, lon)
order with lon in −180..180, and writes the same variables, units and year
windows that `format_ilamb.sh` writes for LPJ:

| ILAMB variable | source | units | years |
|---|---|---|---|
| `cVeg` | `cVeg` | kg m⁻² | 1999–2020 |
| `gpp`, `ra`, `rh` | same | g m⁻² d⁻¹ | 1980–2014/15 |
| `nee` | −`nbp` | g m⁻² d⁻¹ | 1980–2015 |
| `cSoilAbove1m` | `cSoilAbove1m` if present, else `cSoil` | kg m⁻² | 2000 only |
| `et` | `evapotrans` | mm d⁻¹ | 1980–2020 |
| `burntArea` | `burntArea` / `burntFractionAll` | % month⁻¹ | 1997–2016 |
| `runoff` | `mrro` | kg m⁻² s⁻¹ | 1980–2010 |

Each formatting log prints global totals of every variable. That is how the
JULES P0336, CLM burned-area and LPX-Bern ET problems were caught.

## Reproducing

- **Downloads:** `scratch/tc229954e/wiemip_results/other_models_hist/code/`.
  `pull_hist.sh` runs 8 downloads at a time with the `wasabi-read-only`
  profile. The kept variables are in `ilamb_keep.txt`.
- **Formatting and ILAMB:** `scratch/tc229954e/wiemip_results/ilamb_multi/code/`.
    - `format_array.sh` is a slurm array with one task per model run, calling
      `standardize.py`.
    - `run_ilamb_global.sh` and `run_ilamb.sh` (the north run) are 32-rank
      `ilamb-run` jobs.

Formatting takes ~20 min and each ILAMB run ~15–20 min. Only the HTML and
figures are committed, not the NetCDF.
