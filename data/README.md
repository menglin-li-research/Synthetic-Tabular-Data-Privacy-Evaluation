# Data

This folder stores local copies of the real and synthetic datasets used by the scripts.

The repository does **not** commit downloaded real-data files or generated synthetic records by default.

## Current datasets

The pipeline downloads the exact published train/test splits for:

### Dataset E — Pima Indians Diabetes

- `E_PimaIndiansDiabetes_Real_Train.csv`
- `E_PimaIndiansDiabetes_Real_Test.csv`

### Dataset D — Contraceptive Method Choice

- `D_ContraceptiveMethod_Real_Train.csv`
- `D_ContraceptiveMethod_Real_Test.csv`

Run:

~~~bash
python -m src.download_data
~~~

to place these files under `data/raw/`.

Synthetic data are generated under `data/synthetic/`.

## Data provenance

Upstream project:

https://github.com/Vicomtech/STDG-evaluation-metrics

The source study describes six open-source datasets. This repository currently downloads only the two published splits required for the present experiments.
