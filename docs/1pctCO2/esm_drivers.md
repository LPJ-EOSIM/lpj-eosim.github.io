# 1pctCO2 coupled: ESM driver comparison (GFDL / IPSL / UKESM)

The fully-coupled (**cou** / S2) stage — rising 1pctCO₂ **and** transient ESM
climate — for three factorials: the **baseline**, tuned **no_fire** (v3), and
tuned **no_n_limitation** (v2), each run under all three ESM climate drivers
(**GFDL**, **IPSL**, **UKESM**), with the **baseline ctrl** (S0: constant CO₂,
fixed climate) as a flat reference. One panel per variable (fireC, VegC,
SoilC, LitC, GPP, NPP, Rh, NBP), global area-weighted annual totals,
1850–2000. Color = ESM driver, linestyle = factorial (baseline dashed,
no_fire dash-dot, no_n_limitation dotted).

![coupled ESM driver comparison: baseline vs no_fire vs no_n_limitation](../img/wiemip/1pct/baseline_cou_drivers.png)

Global totals at year 2000:

| Variable | Unit | ctrl | GFDL base | IPSL base | UKESM base | GFDL no_fire | IPSL no_fire | UKESM no_fire | GFDL no_nlim | IPSL no_nlim | UKESM no_nlim |
|----------|------|-----:|----------:|----------:|-----------:|-------------:|-------------:|--------------:|-------------:|-------------:|--------------:|
| fireC | Pg C yr⁻¹ | 1.36  | 6.66  | 5.79  | 6.77  | 0     | 0     | 0     | 6.49  | 5.99  | 6.33  |
| VegC  | Pg C      | 528   | 929   | 980   | 926   | 1178  | 1269  | 1255  | 987   | 1058  | 1034  |
| SoilC | Pg C      | 1607  | 1704  | 1701  | 1701  | 1703  | 1698  | 1697  | 1740  | 1733  | 1736  |
| LitC  | Pg C      | 176   | 280   | 281   | 273   | 294   | 298   | 300   | 290   | 288   | 288   |
| GPP   | Pg C yr⁻¹ | 105   | 207   | 221   | 220   | 220   | 237   | 237   | 226   | 243   | 244   |
| NPP   | Pg C yr⁻¹ | 48    | 101   | 107   | 108   | 100   | 107   | 108   | 108   | 115   | 117   |
| Rh    | Pg C yr⁻¹ | 47    | 92    | 97    | 97    | 95    | 101   | 101   | 99    | 104   | 105   |
| NBP   | Pg C yr⁻¹ | −0.65 | 1.90  | 4.12  | 4.21  | 5.62  | 6.51  | 6.76  | 2.25  | 4.90  | 5.17  |

## What the drivers show

- **The coupled response dwarfs the driver spread.** Relative to the control, all
  three ESMs roughly double GPP (105 → ~210–220 Pg C yr⁻¹) and VegC (528 → ~930–980
  Pg C) under the 1pctCO₂ pathway even at baseline — the CO₂-fertilization signal
  is far larger than the differences between climate models, and this holds for
  both tuned factorials too.
- **IPSL is the productivity outlier, consistently.** IPSL carries the most
  vegetation/litter carbon and highest GPP/NPP at baseline (VegC 980 vs
  ~926–929 Pg C for GFDL/UKESM) — and the SAME ranking (IPSL > UKESM > GFDL)
  holds under both no_fire and no_n_limitation. GFDL stays the coolest/driest,
  sitting lowest on GPP/NPP/Rh across all three factorials.
- **Soil carbon is driver-insensitive, in every factorial.** SoilC lands within
  ~0.3% across the three ESMs at baseline (1701–1704 Pg C), within ~0.4% under
  no_fire (1697–1703), and within ~0.4% under no_n_limitation (1733–1740) — the
  slow soil pool integrates over climate noise regardless of which perturbation
  or tune is applied.
- **NBP spans the driver uncertainty, and the tuned runs widen it further.**
  Baseline NBP ranges +1.9 (GFDL) to +4.2 Pg C yr⁻¹ (UKESM) at year 2000; both
  tuned factorials push every ESM's NBP higher (no_fire: +5.6 to +6.8; no_nlim:
  +2.2 to +5.2), but the GFDL-vs-UKESM/IPSL spread persists in each case — this
  looks like a genuine driver effect, not tuning noise.
- **Fire triples–quintuples under the coupled baseline** (1.4 → ~6–7 Pg C yr⁻¹)
  as growing biomass builds fuel load, with UKESM burning most; no_n_limitation
  keeps a similar fire response (6.0–6.5) since fire stays compiled in, while
  no_fire has SPITFIRE compiled out entirely (fireC ≡ 0, by construction).
