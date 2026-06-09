# Simulations

LPJ-EOSIM simulations are configured and launched through the LPJ pipeline, a
Python package that snapshots the model source, resolves climate and CO₂
drivers, compiles LPJ, and runs it either locally or on HPC systems.

Simulations follow standard TRENDY-style protocols (S0–S3) plus a methane (CH4)
configuration, each expanding into spinup, land-use spinup, and transient
stages. Supported climate drivers include CRU, CRUJRA, MERRA-2, ERA5, and
JRA-3Q.
