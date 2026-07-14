# 1pctCO2 benchmarking

Global, area-weighted annual totals and spatial patterns for the WIEMIP
1pctCO2 experiment, comparing three factorials across all three protocol
stages:

- **Baseline** — the reference parameterization (fire on, N-limited).
- **No-fire (tuned)** — `nofire_simplified_v3`, SPITFIRE disabled and
  re-tuned to match baseline behavior where possible.
- **No-fire (untuned)** — SPITFIRE disabled, default/untuned parameters; a
  ctrl-only ablation reference (no bgc/cou-ukesm stage exists for this run).

Stages: **S0 (ctrl)** — fixed climate and land use, rising CO₂ only;
**S1 (bgc)** — biogeochemically-coupled (CO₂ fertilization under fixed
climate); **S2 (cou-ukesm)** — fully coupled to a transient UKESM1-0-LL
climate. All runs span 1850–2000 (151 years) on the 0.5° global grid.

Monthly output is grouped by calendar year and summed to an annual value
before area-weighting (a no-op for variables already reported annually).
Carbon stocks & fluxes are in **Pg C** / **Pg C yr⁻¹**; the nitrogen-cycle
variables (soil N₂O, biological N fixation) are in **Tg N yr⁻¹**;
evapotranspiration is an area-weighted global-mean depth in **mm yr⁻¹**.

!!! note "wet_frac omitted"
    Wetland fraction (`wet_frac`) was requested but is not present in the
    LPJ-EOSIM output configuration for any of these runs — it is omitted here
    rather than approximated.

Each variable section below shows the global time series (subplots = stage,
lines = factorial) followed by the spatial pattern at 1850 vs 2000 for each
stage (S0 compares all three factorials; S1/S2 compare baseline vs no-fire
tuned only, since the untuned run has no bgc/cou-ukesm stage).

## GPP

![GPP: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_gpp.png)
![GPP maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_gpp_ctrl.png)
![GPP maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_gpp_bgc.png)
![GPP maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_gpp_cou-ukesm.png)

## NPP

![NPP: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_npp.png)
![NPP maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_npp_ctrl.png)
![NPP maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_npp_bgc.png)
![NPP maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_npp_cou-ukesm.png)

## Heterotrophic respiration (Rh)

![Rh: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_rh.png)
![Rh maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_rh_ctrl.png)
![Rh maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_rh_bgc.png)
![Rh maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_rh_cou-ukesm.png)

## NBP

![NBP: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_mnbp.png)
![NBP maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_mnbp_ctrl.png)
![NBP maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_mnbp_bgc.png)
![NBP maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_mnbp_cou-ukesm.png)

## Soil carbon

![Soil C: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_soilc.png)
![Soil C maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_soilc_ctrl.png)
![Soil C maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_soilc_bgc.png)
![Soil C maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_soilc_cou-ukesm.png)

## Vegetation carbon

![Veg C: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_vegc.png)
![Veg C maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_vegc_ctrl.png)
![Veg C maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_vegc_bgc.png)
![Veg C maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_vegc_cou-ukesm.png)

## Litter carbon

![Litter C: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_litc.png)
![Litter C maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_litc_ctrl.png)
![Litter C maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_litc_bgc.png)
![Litter C maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_litc_cou-ukesm.png)

## Soil N₂O

![Soil N2O: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_mn2o_soil.png)
![Soil N2O maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_mn2o_soil_ctrl.png)
![Soil N2O maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_mn2o_soil_bgc.png)
![Soil N2O maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_mn2o_soil_cou-ukesm.png)

## Fire carbon emission

![Fire C: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_firec.png)
![Fire C maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_firec_ctrl.png)
![Fire C maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_firec_bgc.png)
![Fire C maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_firec_cou-ukesm.png)

## Establishment flux

![Establishment flux: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_flux_estab.png)
![Establishment flux maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_flux_estab_ctrl.png)
![Establishment flux maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_flux_estab_bgc.png)
![Establishment flux maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_flux_estab_cou-ukesm.png)

## Ecosystem respiration (Reco)

![Reco: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_mreco.png)
![Reco maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_mreco_ctrl.png)
![Reco maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_mreco_bgc.png)
![Reco maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_mreco_cou-ukesm.png)

## Autotrophic respiration (Ra)

![Ra: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_mra.png)
![Ra maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_mra_ctrl.png)
![Ra maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_mra_bgc.png)
![Ra maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_mra_cou-ukesm.png)

## Biological N fixation (BNF)

![BNF: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_bnf.png)
![BNF maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_bnf_ctrl.png)
![BNF maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_bnf_bgc.png)
![BNF maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_bnf_cou-ukesm.png)

## Evapotranspiration

![Evapotranspiration: 1pctCO2 factorials](../../img/wiemip/benchmarking/1pctco2/lineplot_evapotrans.png)
![Evapotranspiration maps: S0 control](../../img/wiemip/benchmarking/1pctco2/map_evapotrans_ctrl.png)
![Evapotranspiration maps: S1 bgc-coupled](../../img/wiemip/benchmarking/1pctco2/map_evapotrans_bgc.png)
![Evapotranspiration maps: S2 fully coupled](../../img/wiemip/benchmarking/1pctco2/map_evapotrans_cou-ukesm.png)
