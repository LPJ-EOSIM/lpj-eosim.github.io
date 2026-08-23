# NMIP SH1 — BNF sensitivity, C & N budgets, ILAMB

[**Open the full ILAMB site →**](../results/ilamb-nmip-sh1/index.html)

Five SH1 runs, 1850–2024, global. Three of them are the `fix_harvest` runs and
differ from each other only by the BNF compile flag in `Makefile.inc`:

| label | run | BNF flag |
|---|---|---|
| `midbnf` | `nmip-20260822-midbnf` | `-DMID_BNF` |
| `upperbnf` | `nmip-20260822-upperbnf` | `-DUPPER_BNF` |
| `baseline20260821` | `nmip-20260821` | none |
| `NMIP3prod_SH1` | `nmip/NMIP3prod_SH1` | none, pre-`fix_harvest` |
| `NMIP3_SH1` | `nmip/NMIP3_SH1` | none, pre-`fix_harvest` |

## Biological N fixation

![Global annual BNF for the five SH1 runs](../img/nmip/bnf_annual.png)

Three tiers, flat across the record until a step down around 1978–80 that
appears in every run. 1995–2024 means: **upperbnf 135.2, midbnf 104.9,
baseline20260821 62.9, NMIP3_SH1 59.9, NMIP3prod_SH1 59.6 Tg N/yr**.

## Soil N₂O

![Global annual soil N2O for the five SH1 runs](../img/nmip/soil_n2o_annual.png)

2024 values span **8.29 Tg N/yr** (no BNF flag) to **12.61** (NMIP3_SH1), with
midbnf at 10.32 and upperbnf at 11.87.

The BNF flag does nearly all of its work on nitrogen and almost none on carbon:
N₂O spans 4.3 Tg N/yr across these runs while NBP moves 0.18 Pg C/yr, most of
which is the two older runs rather than the BNF setting.

## NBP

![Global annual NBP for the five SH1 runs](../img/nmip/nbp_annual.png)

NBP is recomputed from component fluxes for all five runs rather than read from
each run's `mnbp.nc`. Those files were built at different times with different
negative-flux groups — only midbnf and upperbnf included leaching, and
NMIP3_SH1 had no `mnbp` at all — so the stored versions are not comparable. One
formula for all five:

```
NBP = (flux_estab + mnpp)
    - (firec + woodharvest_{1,10,100}yr + deforestProduct_{2,25}yr
       + flux_luc + leachsum_cmass + mharvest + mrh)
```

`mharvest` stands in for `flux_harvest`, which these runs never wrote; summed
over a year it is the same quantity. Verified against the pipeline's own
`compute_nbp` for midbnf: max difference **1.6 × 10⁻⁵ Pg C/yr**.

The lower panel is a 10-year running mean. Interannual swings are ±3 Pg C/yr
and the spread between runs is ~0.2, so the annual panel alone hides it.

**midbnf is a net source in 127 of 175 years.** The long unbroken stretch is
1918–1949 (32 years, mean −1.32 Pg C/yr), then 1957–1967 (11 years, mean
−2.07). The smoothed curve only turns durably positive around 1990. Since then
the negative years are 1991, 1992, 1994, 1995, 1998, 2002, 2003, 2005, 2012,
2016, 2020, 2023 and 2024 — including each of the last two, though only
marginally (−0.09 mean).

## C & N fluxes and stocks

Variables are taken from the registry groups in
`pipeline/registries/output_registry.py` — `BASELINE_DIAGNOSTICS` for carbon,
`NITROGEN_DIAGNOSTICS` for nitrogen, plus the NMIP list's extra C pools and N
pools. Fluxes are summed to the year; pools are averaged, since a monthly pool
summed over twelve months would be twelve times its real size.

![Key carbon fluxes and stocks](../img/nmip/carbon_budget.png)

![Key nitrogen fluxes and stocks](../img/nmip/nitrogen_budget.png)

## The harvest bug is visible in these panels

`mharvest` and `mnharvest` are **identically zero across the whole record in
both pre-`fix_harvest` runs**. That carbon does not disappear — it leaves as
respiration instead. 1995–2024 means, midbnf against NMIP3prod_SH1:

| term | midbnf | NMIP3prod_SH1 |
|---|---|---|
| harvest export | 2.87 | 0.00 |
| `mrh` | 53.90 | 56.97 |
| `mnpp` | 60.98 | 61.06 |

The extra 3.07 Pg C/yr of Rh in the old run accounts for the 2.87 Pg C/yr of
harvest the new runs export, with NPP essentially unchanged. This is why the
NBP curves nearly coincide despite one group missing a 3 Pg C/yr term, and it
means old-vs-new comparisons are not like-for-like in mechanism even where the
totals agree.

## ILAMB benchmarking

![ILAMB scorecard for the five SH1 runs](../img/nmip/ilamb_scorecard.png)

Ten scored confrontations. Overall means: **NMIP3_SH1 0.635, NMIP3prod_SH1
0.632, baseline20260821 0.623, midbnf 0.618, upperbnf 0.617**.

Only three rows separate these runs at all — **NBP (spread 0.123), Soil Carbon
(0.054) and Leaf Area Index (0.044)**. The BNF pair takes Biomass, GPP and
Ecosystem Respiration by small margins; the two older runs take NBP, Soil
Carbon and LAI by larger ones, which is what drives their higher overall mean.

**Two of those three rows are not like-for-like.** NBP was made comparable by
recomputing it (above). LAI cannot be — `mlai` means a different thing in the
two code vintages, see below. That leaves **Soil Carbon as the only row that
cleanly separates these runs**, and the overall-mean ranking should not be read
as a quality ordering.

Evapotranspiration, Burned Area and Runoff separate the models by 0.0003–0.0009
and are shown as ties rather than shaded, so that a spread of essentially zero
does not render as a large difference. BNF should not move hydrology or fire,
and it does not.

All five NBPs use the single definition above, so that row is a like-for-like
comparison. It still carries the harvest caveat: `mharvest` is zero in both
older runs, so their NBP and Soil Carbon advantage may be the harvest routing
rather than better physics.

## `mlai` is not the same quantity across these runs

![Global leaf area, showing the mlai definition split](../img/nmip/mlai_definition_split.png)

The older runs compute gridcell LAI over a different set of stands. In
`update_daily.c`, `update_pft_outputs_daily` early-returns on a negative slot,
and `mlai` is accumulated *after* that return:

```c
/* older code (NMIP3prod_SH1, NMIP3_SH1) */
static int pft_output_slot(const Stand *stand, const Pft *pft, int npft) {
    if (stand->landusetype == GRASSLAND)
        return npft + (stand->irrigation ? NGRASS : 0);
    if (stand->landusetype == AGRICULTURE || pft->par->id >= npft)
        return -1;                    /* caller: if (slot < 0) return; */
    return pft->par->id;
}

/* fix_harvest code — no stand test at all */
static int pft_output_slot(const Pft *pft, int npft, int month) {
    return pft->par->id < npft ? (month * npft) + pft->par->id : -1;
}
```

So **the older runs omit AGRICULTURE stands from `mlai` entirely, and the
`fix_harvest` runs count every stand.** The `lai_day` expression and the
`fpc * stand->frac / ndaysmonth` weighting are byte-identical between the two —
only the set of stands reaching the accumulation differs.

The data carries the signature: global leaf area agrees to **+0.4 % in 1850**,
when there is almost no cropland, then diverges monotonically to **+5.7 % by
1975** as cropland expands, and holds there.

This is what the ILAMB LAI row is measuring. Every run is biased high against
both satellite products, and the more complete definition is biased higher
still:

| vs AVH15C1 | midbnf | upperbnf | 20260821 | NMIP3prod_SH1 | NMIP3_SH1 |
|---|---|---|---|---|---|
| period mean | 2.366 | 2.281 | 2.397 | 2.216 | 2.230 |
| bias | +1.148 | +1.063 | +1.179 | +0.998 | +1.012 |
| LAI score | 0.461 | 0.468 | 0.463 | 0.505 | 0.504 |

Satellite LAI includes cropland, so the `fix_harvest` definition is the correct
one — yet it scores worse. Omitting cropland was masking part of a large
pre-existing high bias of roughly +1.0 LAI unit. The old runs' better LAI score
is a compensating error, not better agreement.

Unlike NBP, this cannot be repaired after the fact: the cropland contribution
was never written to the older runs' output. **The LAI row should be read as a
definition difference, not a model difference.**

**Three confrontations scored for no model**, so no run is penalised relative to
another: Surface Air Temperature and Precipitation need `mtair`/`mppt`, which
none of these runs merged, and Soil Carbon Extended (Koven) emitted no scalar.
`mch4e` is also absent, so there is no CH₄ confrontation. Each model formatted
to an identical 12-variable set.

## Caveats

**`ilamb.cfg` in the pipeline is still stale.** It looks for `biomass`/`vegc`
while `format_ilamb.sh` renames the variable to `cVeg`, so Biomass silently
scores nothing despite a weight of 5. This run used a local config copy setting
`alternate_vars = "vegc,cVeg"` — the same workaround as the TRENDYv15 page. The
fix has still not been made upstream.

**Nine nitrogen variables carry the wrong units attribute.** `mn2_soil`,
`mno_soil`, `mnh3_soil`, `mgross_nitrif`, `mgross_denitrif`, `mnet_nitrif`,
`mnet_denitrif`, `mleaching` and `mnavail` are all labelled `g c m-2` in their
NetCDF attributes. They are nitrogen. They are treated as g N here.

**Per-PFT output was not merged** for these runs, so PFT- and stand-level
members of the registry groups are absent from the budget figures.

**Two variables mean different things across code vintages** and are not
comparable between the `fix_harvest` runs and the older two: `mharvest`/
`mnharvest` (zero in the older runs) and `mlai` (cropland omitted in the older
runs). Both are documented above.

## Reproducing

ILAMB inputs are staged as symlinks per run with a consistently rebuilt `mnbp`,
so nothing is written into the run directories — `NMIP3prod_SH1` and the
upperbnf run are registry-published. Scripts live in
`scratch/tc229954e/ilamb_sh1_20260823/code/`: `prep_ilamb_inputs.py`,
`run_ilamb.sh`, `plot_ilamb_landing.py` and the patched `ilamb_sh1.cfg`. The
budget figures come from `plot_sh1_n2o_nbp.py` and `plot_c_n_budget.py` in the
midbnf run's `code/` directory.

The NetCDF that ILAMB writes alongside its figures (192 MB) is not committed —
only the HTML and figures needed to browse the results.
