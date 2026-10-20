# WIEMIP simulations

A record of the WIEMIP simulations that need to be run and their flag
combinations. The first suite is the **1pctCO2** idealised experiment: a
preindustrial spinup followed by `ctrl` / `bgc` / `cou`, repeated for five
flag-set variants (fire on/off, N-limitation on/off, and a transient-N-dep
variant).

!!! note "Requirements"
    Historical base run on **observed CRUJRA** data; check `ctrl` against this.

!!! question "Open questions"
    - **CH4 runs?** Is this a separate run / different configuration?

## How the columns map to the pipeline

Within each variant the four simulations differ only in the CO2 / climate /
N-dep treatment; everything else (N fert, land use, pop, lightning) is held
constant across the whole matrix. The per-stage CO2/climate treatment is set by
the `sim_type` profile (`simulation_profiles/<S?>/flags.json`):

| Simulation | `sim_type` | Driver | CO2 | Climate |
|---|:--:|:--:|---|---|
| `spinup` | S2 | STABLE | const 280 ppm (`CO2MEAN`) | stable (`RECYCLE_CLIMATE`) |
| `ctrl`   | S0 | STABLE | const 280 ppm (`CO2MEAN`) | stable (`RECYCLE_CLIMATE`) |
| `bgc`    | S1 | STABLE | transient | stable (`RECYCLE_CLIMATE`) |
| `cou`    | S2 | (climate driver) | transient | transient |

`ctrl` / `bgc` / `cou` all branch from the same preindustrial spinup restart.
The per-variant **additional flags** below are the only thing that changes
between variants — they are the compile-time flag set applied to every stage.

## 1pctCO2 runs

### 1pctCO2-base

**Additional flags:** `PERMAFROST`, `NITROGEN`, `NFERTILIZER`, `BVOC`, `SPITFIRE`, `M10DAYR`, `RESP_OPT=6`

| Simulation | CO2 | Climate | Nitrogen dep. | N fert | Land use | Pop | Lightning |
|---|---|---|---|---|---|---|---|
| spinup | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| ctrl   | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| bgc    | transient | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| cou    | transient | transient | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |

### 1pctCO2-nofire

**Additional flags:** `PERMAFROST`, `NITROGEN`, `NFERTILIZER`, `BVOC`, `M10DAYR`, `RESP_OPT=6` *(no `SPITFIRE`)*

| Simulation | CO2 | Climate | Nitrogen dep. | N fert | Land use | Pop | Lightning |
|---|---|---|---|---|---|---|---|
| spinup | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| ctrl   | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| bgc    | transient | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| cou    | transient | transient | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |

### 1pctCO2-no-nlim

**Additional flags:** `PERMAFROST`, `NONLIM`, `BVOC`, `SPITFIRE`, `M10DAYR`, `RESP_OPT=6` *(N-limitation off; no `NFERTILIZER`)*

| Simulation | CO2 | Climate | Nitrogen dep. | N fert | Land use | Pop | Lightning |
|---|---|---|---|---|---|---|---|
| spinup | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| ctrl   | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| bgc    | transient | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| cou    | transient | transient | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |

### 1pctCO2-no-nlim-no-fire

**Additional flags:** `PERMAFROST`, `NONLIM`, `BVOC`, `M10DAYR`, `RESP_OPT=6` *(N-limitation off; no `SPITFIRE`, no `NFERTILIZER`)*

| Simulation | CO2 | Climate | Nitrogen dep. | N fert | Land use | Pop | Lightning |
|---|---|---|---|---|---|---|---|
| spinup | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| ctrl   | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| bgc    | transient | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| cou    | transient | transient | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |

### 1pctCO2-base-ndep

**Additional flags:** `PERMAFROST`, `NITROGEN`, `NFERTILIZER`, `BVOC`, `SPITFIRE`, `M10DAYR`, `RESP_OPT=6` *(same as base; N dep. is **transient** for `bgc`/`cou`)*

| Simulation | CO2 | Climate | Nitrogen dep. | N fert | Land use | Pop | Lightning |
|---|---|---|---|---|---|---|---|
| spinup | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| ctrl   | const 280 ppm + `CO2MEAN` | stable + `RECYCLE_CLIMATE` | const PI + `CONSTANT_NDEP` | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| bgc    | transient | stable + `RECYCLE_CLIMATE` | **transient** | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
| cou    | transient | transient | **transient** | constant 1850 | constant 1850 + `CONST_LU` | const PI | const PI |
