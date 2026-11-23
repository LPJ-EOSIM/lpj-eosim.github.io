# Climate-effect fixes on main: PR #441, runs #57–#64

The long version of [LPJ PR #441](https://github.com/LPJ-EOSIM/LPJ/pull/441): the fixes, the runs on main, and every figure.
Build with `-DCLIMATE_EFFECT_FIXES` to turn the fixes on.

- Earlier write-up (runs #53 / #55): [Climate-effect fixes: runs #53 and #55](climate_effect_53_55.md)
- ILAMB: [site](https://lpj-eosim.github.io/results/ilamb-climate-effect-53-55/index.html) · [dashboard, absolute scores](https://lpj-eosim.github.io/results/ilamb-climate-effect-53-55/dashboard.html)

## Changes

| Old name, included in `-DCLIMATE_EFFECT_FIXES` | What it does | Source | LPJmL version (file, function) | Proposed by |
|---|---|---|---|---|
| `TREES_OVER_GRASS` | When tree + grass cover exceeds 1, grass shrinks instead of trees being thinned into litter | LPJmL - bugfix! | 4.0.001 → v6.1.9: `src/lpj/establishmentpft.c`, `establishmentpft()`, `reduce()` on grass only (`reduce_grass()` rescales FPC only) | Claude ¹ |
| `LARCH_SLA_LPJML` | Larch SLA set to LPJmL's 0.02118 (ours, from the longevity formula, is 0.041) | LPJmL parameter - stopped a lot of the boreal die-off leading to large respiration | v5.6.18 → v6.1.9: `par/pft.js`, later `par/pft.cjson`, larch `"sla"`, added in commit `a0cf7b3a` (2020-06-22). Not in 4.0.001–4.0.003, which use the longevity formula as we do | Claude |
| `LPJML_ESTAB_GATE` | Tree establishment stops at 0.95 cover. Ours used `&&` and never fired; LPJmL uses `\|\|`. Also stops tree PFTs being added with nind = 0 (NaN leak) | bug fix, gate as in LPJmL | gate: 4.0.001 → v6.1.9, `src/tree/establishment_tree.c`, `establishment_tree()`. The nind = 0 skip is ours; LPJmL avoids the NaN with the `isneg_tree()` guard in `allocation_tree()` (4.0.001 → v6.1.9) | Claude ² |
| `FPC_MIXVEG` | Recompute FPC when stand fractions change | bug fix | not in LPJmL: `mix_veg_tree()` / `mix_veg_grass()` don't recompute FPC in 4.0.001, 4.0.002, v5.6.18 or v6.1.9 | Claude |
| `RESPONSE_CAP` | Cap decomposition at its 10 °C, field-capacity rate: in `littersom.c` (as LPJmL) and, under NITROGEN, in CENTURY's `decayrates_century` | LPJmL (littersom); our port (CENTURY) | `littersom.c` part: 4.0.001 → v6.1.9, `src/soil/littersom.c`, `littersom()`, `response[l]>1 → 1`. CENTURY part: no LPJmL counterpart (LPJmL has no CENTURY) | Claude ³ |
| `K_MORT` | Growth-efficiency mortality coefficient 0.5 → 0.2 | LPJmL | k_mort = 0.2 in 4.0.001 → v6.0.6 (`par/param.par` in 4.0.001, `par/lpjparam.js` in 4.0.002–v5.7.9, `par/lpjparam.cjson` in v5.9.7–v6.0.6); used in `src/tree/mortality_tree.c`, same formula as ours. LPJmL changed it to **0.1** in v6.1.8 (`6df727ae`, 2026-08-31), and master is 0.1 (checked 2026-11-20); the code comment says so since `a27431e` | Claude |
| (no flag) | Non-finite or negative N deposition read as 0 in the monthly reader; `main`'s yearly reader already does this | data fix | — | Claude ⁴ |

**Proposed by:** "Claude" means a Claude model (Opus 5.5, or Fable 5.2 for `FPC_MIXVEG`) first proposed the change in a Claude Code session with Tom. Evidence: the session transcripts on Tom's laptop and on Hellgate, and the source audits in `climate_effect_work/`.

1. Claude traced the tree carbon loss to the total-cover rescale; Tom asked for a fix that stops grass pushing out trees, and Claude wrote it (2026-10-30). Claude found the LPJmL equivalent later (2026-11-05).
2. The gate comes from Ben's establish-then-thin churn hypothesis. A Claude hypothesis agent found the `&&` (2026-11-05), and a Fable 5.2 bug hunt found it again (2026-11-09). The nind = 0 skip fixes a NaN leak in Claude's own first version of the gate.
3. Both the `littersom.c` cap (2026-11-09 audit) and the CENTURY port (2026-11-12) were Claude's. Claude chose the CENTURY cap value (`temperature_modifier(10)` ≈ 0.19).
4. Found while debugging a NITROGEN + PERMAFROST crash that Tom asked Claude to debug (2026-11-11).

## Runs on main (57–64)

All global, S0/S3/S5, PR #441 flags on LPJ main.

| Run | Folder | Flag set |
|---|---|---|
| KGO | — | main CI known-good S3 (no PR flags) |
| **57** | `main53` | run 53 flags on main: `TREES_OVER_GRASS LARCH_SLA_LPJML PERMAFROST LPJML_ESTAB_GATE FPC_MIXVEG RESPONSE_CAP NITROGEN K_MORT` |
| 58 | `main55` | 57 without `PERMAFROST` |
| 59 | `main56` | 58 without `NITROGEN` |
| 60 | `main60` | 57 − `RESPONSE_CAP` + `RESP_OPT=6` + `M10DAYR` |
| 61 | `main61` | 58 − `RESPONSE_CAP` + `RESP_OPT=6` + `M10DAYR` |
| 62 | `main62` | 59 − `RESPONSE_CAP` + `RESP_OPT=6` + `M10DAYR` |
| 63 | `main63` | 57 − `RESPONSE_CAP` |
| 64 | `main64` | 63 + `RESP_OPT=2` + `M10DAYR` (maintenance Ra only) |

Attribution chain: 57 → 63 (drop cap) → 64 (maint. Ra) → 60 (+ leaf Rd).

What `RESP_OPT=6` + `M10DAYR` changes vs `RESPONSE_CAP`:

- Rh, no NITROGEN (`littersom.c`): Lloyd-Taylor × moisture capped at 1 → Carey 2013 × moisture, no cap
- Rh, NITROGEN (`century.c`): CENTURY capped at 0.190 → CENTURY uncapped (`RESP_OPT`/`M10DAYR` not used here)
- Ra maintenance: Lloyd-Taylor → Tjoelker × Atkin (10-day mean T)
- Leaf Rd coefficient: constant → Heskel × Atkin (10-day mean) ÷ tstress (`RESP_OPT=6` only)
- `M10DAYR` buffers are not saved in restarts

![Respiration response functions](img/climate_effect_resp6_60_62/resp_response_functions.png)

## Climate effect

| S3 − S5 + S0, 1960–2025 (PgC) | v15 (#1) | **57** | 58 | 59 | 60 | 61 | 62 | 63 | 64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Global | −75.9 | **−32.2** | −33.1 | −41.8 | −33.9 | −33.9 | −37.4 | −38.6 | −30.0 |
| North (> 30°N) | −37.7 | −12.1 | −13.0 | −20.4 | −12.3 | −13.7 | −25.8 | −16.0 | −11.9 |
| Tropics (30°S–30°N) | −36.3 | −19.1 | −19.0 | −20.3 | −20.6 | −19.3 | −10.3 | −21.3 | −17.1 |
| South (< 30°S) | −1.9 | −1.1 | −1.1 | −1.1 | −1.0 | −1.0 | −1.3 | −1.4 | −1.0 |
| S3 cumulative NBP 1960–2024 (TRENDY v14 median 44.5) | 13.3 | **47.2** | 41.3 | 78.0 | 32.2 | 26.2 | 72.0 | 28.9 | 35.5 |
| S0 cumulative NBP 1960–2024 (drift) | | 1.40 | 0.83 | 0.26 | 1.70 | 1.62 | 0.70 | 1.59 | 1.66 |
| S0 budget gap 1901–2020 (stock change − cum. NBP) | | 0.63 | 0.76 | 0.00 | 0.23 | 0.23 | −0.00 | 0.62 | 0.23 |

Table: [climate_effect_table_runs57-64.csv](img/climate_effect_attribution_57_63_64_60/climate_effect_table_runs57-64.csv)

![GCB climate effect, runs 57–62](img/climate_effect_resp6_60_62/gcb_style_S3_S5_S0.png)

![GCB climate effect, attribution 57 → 63 → 64 → 60](img/climate_effect_attribution_57_63_64_60/gcb_style_S3_S5_S0.png)

### Attribution: cap vs RESP_OPT (S3 − S5, cumulative PgC)

| | 57 | 63 | 64 | 60 | cap (63−57) | maint. Ra (64−63) | leaf Rd (60−64) | total (60−57) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GPP | 129.80 | 136.75 | 146.11 | 147.72 | 6.95 | 9.36 | 1.60 | 17.92 |
| Ra | 110.58 | 118.09 | 111.73 | 115.85 | 7.51 | −6.36 | 4.12 | 5.27 |
| NPP | 19.22 | 18.66 | 34.38 | 31.86 | −0.56 | 15.72 | −2.52 | 12.64 |
| Rh | 55.60 | 62.78 | 68.00 | 70.28 | 7.18 | 5.21 | 2.28 | 14.67 |
| fire | 2.57 | 1.39 | 2.67 | 2.28 | −1.19 | 1.28 | −0.39 | −0.29 |
| LUC flux | −2.28 | −2.28 | −1.96 | −2.17 | −0.00 | 0.32 | −0.21 | 0.11 |
| NBP | −33.68 | −40.29 | −31.89 | −35.82 | −6.61 | 8.40 | −3.93 | −2.14 |
| Δ veg C | −9.49 | −9.34 | −2.52 | −4.88 | 0.16 | 6.81 | −2.36 | 4.61 |
| Δ soil + litter C | −24.60 | −31.49 | −29.68 | −31.31 | −6.89 | 1.81 | −1.63 | −6.71 |

Table: [attribution_S3_minus_S5_cumulative.csv](img/climate_effect_attribution_57_63_64_60/attribution_S3_minus_S5_cumulative.csv)

## Stocks and fluxes

Climate effect (S3 − S5):

![S3 − S5 stocks and fluxes, runs 57–62](img/climate_effect_resp6_60_62/stocks_fluxes_S3_minus_S5.png)

![S3 − S5 stocks and fluxes, attribution](img/climate_effect_attribution_57_63_64_60/stocks_fluxes_S3_minus_S5.png)

S3 against LPJ-GUESS and LPJmL (TRENDY v14):

![S3 vs LPJ-GUESS / LPJmL, runs 57–62](img/climate_effect_resp6_60_62/s3_stocks_fluxes_family_1960.png)

![S3 vs LPJ-GUESS / LPJmL, attribution](img/climate_effect_attribution_57_63_64_60/s3_stocks_fluxes_family_1960.png)

S3 global:

![S3 global stocks and fluxes, runs 57–62](img/climate_effect_resp6_60_62/stocks_fluxes_S3.png)

![S3 global stocks and fluxes, attribution](img/climate_effect_attribution_57_63_64_60/stocks_fluxes_S3.png)

## Temperate North America summer NEP

Temperate NA, 2015–2024 (PgC; 2000–2005 in [na_nep_table_2000-2005.csv](img/na_seasonal_resp6_60_62/na_nep_table_2000-2005.csv)). Runs 48/49 are from the earlier stack (before / after `RESPONSE_CAP`).

| Run | JJA NEP | JJA GPP | JJA Ra | JJA Rh | Annual NEP |
|---|---:|---:|---:|---:|---:|
| KGO | −0.239 | 6.312 | 4.195 | 2.356 | 0.265 |
| 57 | 0.222 | 5.595 | 3.746 | 1.626 | 0.315 |
| 58 | 0.186 | 5.670 | 3.895 | 1.589 | 0.319 |
| 59 | 0.242 | 6.344 | 4.288 | 1.814 | 0.426 |
| 60 | −0.017 | 5.642 | 3.400 | 2.259 | 0.345 |
| 61 | −0.067 | 5.738 | 3.478 | 2.327 | 0.356 |
| 62 | 0.205 | 6.409 | 3.852 | 2.352 | 0.489 |
| 63 | −0.161 | 5.589 | 3.737 | 2.013 | 0.253 |
| 64 | 0.057 | 5.654 | 3.429 | 2.168 | 0.349 |
| 48 | 0.123 | 5.942 | 3.917 | 1.903 | 0.390 |
| 49 | 0.436 | 5.943 | 3.910 | 1.597 | 0.496 |

Seasonal cycle (NEP, Ra, Rh):

![Temperate NA seasonal cycle 2000–2005](img/na_seasonal_resp6_60_62/na_seasonal_cycle_2000-2005.png)

![Temperate NA seasonal cycle 2015–2024](img/na_seasonal_resp6_60_62/na_seasonal_cycle_2015-2024.png)

![Temperate NA seasonal cycle, attribution, 2000–2005](img/climate_effect_attribution_57_63_64_60/na_seasonal_cycle_2000-2005.png)

![Temperate NA seasonal cycle, attribution, 2015–2024](img/climate_effect_attribution_57_63_64_60/na_seasonal_cycle_2015-2024.png)

JJA NEP maps:

![NA JJA NEP 2000–2005](img/na_seasonal_resp6_60_62/na_jja_nep_map_2000-2005.png)

![NA JJA NEP 2015–2024](img/na_seasonal_resp6_60_62/na_jja_nep_map_2015-2024.png)

![NA JJA NEP, attribution, 2000–2005](img/climate_effect_attribution_57_63_64_60/na_jja_nep_map_2000-2005.png)

![NA JJA NEP, attribution, 2015–2024](img/climate_effect_attribution_57_63_64_60/na_jja_nep_map_2015-2024.png)

JJA NEP difference maps:

![NA JJA NEP difference 2000–2005](img/na_seasonal_resp6_60_62/na_jja_nep_diff_map_2000-2005.png)

![NA JJA NEP difference 2015–2024](img/na_seasonal_resp6_60_62/na_jja_nep_diff_map_2015-2024.png)

![NA JJA NEP difference, attribution steps, 2000–2005](img/climate_effect_attribution_57_63_64_60/na_jja_nep_diff_map_2000-2005.png)

![NA JJA NEP difference, attribution steps, 2015–2024](img/climate_effect_attribution_57_63_64_60/na_jja_nep_diff_map_2015-2024.png)

## ILAMB: KGO vs runs 57–64

[**ILAMB site →**](https://lpj-eosim.github.io/results/ilamb-pr441-57-64/index.html) · [**dashboard, absolute scores →**](https://lpj-eosim.github.io/results/ilamb-pr441-57-64/dashboard.html)

S3, global region, same `ilamb.cfg` as the runs #53 / #55 page. Bold = best in the row.

| Overall score | 57 fixes | 58 noPF | 59 noPF noN | 60 resp6 | 61 resp6 noPF | 62 resp6 noPF noN | 63 nocap | 64 resp2 | KGO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Biomass | 0.634 | 0.596 | 0.535 | 0.609 | 0.568 | 0.509 | 0.634 | 0.618 | **0.639** |
| Gross Primary Productivity | **0.648** | 0.645 | 0.618 | 0.645 | 0.641 | 0.612 | 0.647 | 0.646 | 0.617 |
| Ecosystem Respiration | **0.588** | 0.582 | 0.560 | 0.568 | 0.563 | 0.557 | 0.565 | 0.570 | 0.561 |
| Soil Carbon | 0.662 | 0.686 | 0.705 | 0.691 | **0.729** | 0.663 | 0.699 | 0.704 | 0.698 |
| Evapotranspiration | 0.697 | 0.697 | 0.697 | 0.697 | 0.697 | 0.697 | 0.697 | **0.698** | 0.697 |
| Burned Area | 0.517 | 0.517 | 0.522 | 0.519 | 0.520 | **0.529** | 0.516 | 0.519 | 0.520 |
| Runoff | 0.691 | 0.693 | 0.694 | 0.692 | 0.694 | **0.694** | 0.691 | 0.692 | 0.694 |

- **57 fixes**: run 57: all six fixes + `PERMAFROST` + `NITROGEN`
- **58 noPF**: run 58: 57 without `PERMAFROST`
- **59 noPF noN**: run 59: 58 without `NITROGEN`
- **60 resp6**: run 60: 57 − `RESPONSE_CAP` + `RESP_OPT=6` + `M10DAYR`
- **61 resp6 noPF**: run 61: 58 − `RESPONSE_CAP` + `RESP_OPT=6` + `M10DAYR`
- **62 resp6 noPF noN**: run 62: 59 − `RESPONSE_CAP` + `RESP_OPT=6` + `M10DAYR`
- **63 nocap**: run 63: 57 − `RESPONSE_CAP`
- **64 resp2**: run 64: 63 + `RESP_OPT=2` + `M10DAYR`
- **KGO**: main CI known-good S3 (c71b641, no PR flags)

## CI: S3 KGO vs runs 57–62, all variables

![1/9](img/pr441_kgo_vs_57_62/global_annual_00.png)

![2/9](img/pr441_kgo_vs_57_62/global_annual_01.png)

![3/9](img/pr441_kgo_vs_57_62/global_annual_02.png)

![4/9](img/pr441_kgo_vs_57_62/global_annual_03.png)

![5/9](img/pr441_kgo_vs_57_62/global_annual_04.png)

![6/9](img/pr441_kgo_vs_57_62/global_annual_05.png)

![7/9](img/pr441_kgo_vs_57_62/global_annual_06.png)

![8/9](img/pr441_kgo_vs_57_62/global_annual_07.png)

![9/9](img/pr441_kgo_vs_57_62/global_annual_08.png)

---

## Earlier runs (#53 / #55 / #56)

### Climate effect

![GCB metric](img/climate_effect_53_55/gcb_style_S3_S5_S0_with56.png)

| S3 − S5 + S0, 1960–2025 (PgC) | v15 as submitted | **run 53** | run 55 | run 56 |
|---|---:|---:|---:|---:|
| Global | −75.9 | **−34.1** | −37.2 | −43.8 |
| North (> 30°N) | −37.7 | −13.5 | −16.6 | −21.5 |
| Tropics (30°S–30°N) | −36.3 | −19.6 | −19.7 | −21.4 |
| South (< 30°S) | −1.9 | −1.0 | −0.9 | −1.0 |
| S3 cumulative NBP 1960–2024 (TRENDY v14 median 44.5) | 13.3 | **44.7** | 38.4 | 65.1 |

v15 as submitted reproduces the GCB figure's LPJ-EOSIM numbers. Step by step (S3 − S5, no S0 term): v15 −75.6 → trees over grass −65.1 → larch SLA −60.6 → PERMAFROST −52.1 → establishment gate −55.6 → FPC refresh −55.5 → decomposition cap −46.0 → NITROGEN −46.5 → **k_mort 0.2 −35.0**.

- **PERMAFROST** is worth about 3 PgC on the final stack (run 55), down from 8.5 on the early stack.
- **NITROGEN** is worth about 7 PgC (run 56), mostly northern soil and litter, and brings the sink down to the median. k_mort 0.2 gains little without N. run 55 → run 56 also switches the cap between two decomposition schemes, so it is not a pure N test.

Against the LPJ family (TRENDY v14; only S1/S2 available), the tropics are now inside the family and the north is still 10–20 PgC more negative:

![S2 − S1 vs LPJ family](img/climate_effect_53_55/gcb_style_S2_S1_lpj_family.png)

### Stocks and fluxes

S3, against LPJ-GUESS and LPJmL (TRENDY v14):

![S3 stocks and fluxes](img/climate_effect_53_55/s3_stocks_fluxes_family_1960.png)

Climate effect (S3 − S5) for every stock and flux:

![S3 − S5 stocks and fluxes](img/climate_effect_53_55/stocks_fluxes_S3_minus_S5.png)

### ILAMB (global; LPJ-GUESS and LPJmL are TRENDY v14)

| Model | Biomass | GPP | Reco | Soil C | ET | Burned area | Runoff |
|---|---:|---:|---:|---:|---:|---:|---:|
| **run 53** | 0.639 | **0.645** | **0.605** | 0.656 | **0.691** | 0.517 | 0.688 |
| run 55 | 0.609 | 0.643 | 0.602 | 0.675 | 0.690 | 0.516 | 0.689 |
| v15 as submitted | 0.645 | 0.621 | 0.573 | 0.693 | 0.690 | **0.524** | 0.690 |
| LPJ-GUESS v14 | 0.695 | 0.632 | — | **0.732** | 0.676 | 0.499 | 0.701 |
| LPJmL v14 | **0.707** | 0.580 | 0.567 | 0.333 | 0.658 | 0.500 | **0.709** |

run 53 beats v15 as submitted on GPP and Reco and loses on soil carbon: it holds about 2,000 PgC of soil carbon against 1,300.
