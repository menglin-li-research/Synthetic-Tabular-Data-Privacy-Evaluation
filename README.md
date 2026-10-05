# Synthetic Tabular Data Privacy Evaluation

[![baseline-ci](https://github.com/menglin-li-research/Synthetic-Tabular-Data-Privacy-Evaluation/actions/workflows/baseline.yml/badge.svg)](https://github.com/menglin-li-research/Synthetic-Tabular-Data-Privacy-Evaluation/actions/workflows/baseline.yml)

Reproduction and evaluation of synthetic tabular data methods with a focus on **resemblance, utility, privacy, and fairness**.

This repository is being developed as a reproducible research exercise in privacy-enhancing technologies (PETs) and generative AI. The immediate goal is to reproduce a compact synthetic-tabular-data pipeline based on the study and codebase by Hernandez et al., then extend the analysis toward privacy/fairness questions.

## Current status

**Stage 1 — reproducible baseline executed and validated on GitHub Actions**

The first runnable baseline is designed around:

- **Dataset E:** Pima Indians Diabetes
- **Synthetic generator:** Gaussian multivariate / Gaussian-copula baseline
- **Resemblance:** distributional and correlation checks
- **Utility:** Train-on-Real/Test-on-Real (TRTR) vs. Train-on-Synthetic/Test-on-Real (TSTR)
- **Privacy screening:** nearest-neighbour distance and exact-duplicate diagnostics

The privacy diagnostics in this first stage are **screening proxies, not formal privacy guarantees**. Differential privacy, membership-inference evaluation, attribute-inference evaluation, and fairness analyses are planned extensions.

## Research questions

1. How closely does synthetic tabular data resemble the source data?
2. How much predictive utility is retained when a model is trained on synthetic rather than real data?
3. Does the synthetic sample show signs of excessive proximity to, or duplication of, training records?
4. How should privacy, utility, and fairness be evaluated jointly rather than as isolated objectives?

## Source study

This project is informed by:

> Hernandez, M., Epelde, G., Alberdi, A., Cilla, R., & Rankin, D.  
> *Synthetic Tabular Data Evaluation in the Health Domain Covering Resemblance, Utility, and Privacy Dimensions.*

Official codebase:  
https://github.com/Vicomtech/STDG-evaluation-metrics

The upstream repository evaluates synthetic tabular data across **resemblance, utility, and privacy** and provides six health-related datasets plus multiple generators, including Gaussian Multivariate, SDV, CTGAN, and WGAN-GP.

## Repository structure

~~~text
.
├── README.md
├── requirements.txt
├── environment.yml
├── data/
│   └── README.md
├── docs/
│   ├── methods.md
│   └── research_notes.md
├── notebooks/
│   └── README.md
├── results/
│   └── README.md
└── src/
    ├── __init__.py
    ├── config.py
    ├── download_data.py
    ├── generate.py
    ├── evaluate.py
    └── run_baseline.py
~~~

Generated datasets and result tables are intentionally excluded from version control and can be recreated from the scripts.

## Quick start

### 1. Create an environment

With Conda:

~~~bash
conda env create -f environment.yml
conda activate std-privacy-eval
~~~

or with pip:

~~~bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
~~~

### 2. Download the exact published train/test split

~~~bash
python -m src.download_data
~~~

This downloads the Pima Indians Diabetes train/test files from the official Vicomtech reproduction repository.

### 3. Run the baseline

~~~bash
python -m src.run_baseline
~~~

The script will:

1. load the real training and test data;
2. fit a Gaussian multivariate synthetic-data model;
3. generate a synthetic training set of the same size;
4. evaluate resemblance;
5. compare TRTR vs. TSTR predictive utility;
6. compute privacy-screening diagnostics;
7. write outputs under results/.

## Baseline results

The Stage-1 pipeline was executed successfully on GitHub Actions using Python 3.11 and the published Pima train/test split.

| Dimension | Metric | Result |
|---|---|---:|
| Resemblance | Mean KS statistic | 0.0823 |
| Resemblance | Mean absolute standardized mean difference | 0.0521 |
| Resemblance | Correlation-matrix RMSE | 0.0628 |
| Utility (TRTR) | ROC-AUC | 0.8134 |
| Utility (TSTR) | ROC-AUC | 0.7822 |
| Utility retention | TSTR/TRTR ROC-AUC ratio | 0.9616 |
| Privacy screening | Median synthetic-to-train NN distance | 1.1908 |
| Privacy screening | Median held-out-real-to-train NN distance | 1.0117 |
| Privacy screening | Distance ratio (synthetic / held-out) | 1.1771 |
| Privacy screening | Exact-match rate | 0.0000 |

The synthetic-data model retained about **96% of the real-data ROC-AUC baseline** under the current logistic-regression utility test. Synthetic records were not unusually close to the training set under the current nearest-neighbour screening: their median distance was slightly larger than that of held-out real records, and no exact duplicate was detected. These findings are encouraging but **do not constitute a formal privacy guarantee**.

Full audited results are stored under `results/audited/`.

## Interpretation

The first baseline is intentionally conservative. It is meant to establish a transparent, auditable pipeline before adding more complex generators or stronger privacy tests.

A successful run should be interpreted across three dimensions:

- **Resemblance:** lower distributional discrepancy is better.
- **Utility:** TSTR performance closer to TRTR indicates better downstream utility.
- **Privacy screening:** synthetic records should not collapse onto specific real training records.

No single metric is sufficient. High resemblance can coexist with poor utility, and high fidelity can also increase disclosure risk.

## Planned extensions

- reproduce a second dataset from the source study;
- add SDV/CTGAN generation;
- port the source repository's membership-inference and attribute-inference analyses;
- add differential-privacy experiments;
- add fairness metrics and subgroup analyses;
- compare privacy–utility–fairness trade-offs across generators;
- add notebooks and presentation-ready figures once the first run is validated.

## Reproducibility principles

- fixed random seeds where supported;
- explicit data provenance;
- no private/raw sensitive data committed to GitHub;
- generated outputs separated from source code;
- clear distinction between replication, adaptation, and extension;
- conservative interpretation of privacy metrics.

## Author

**Menglin Li**  
City University of Macau

## Acknowledgement

This repository is an independent reproduction/learning project. It does not claim authorship of the original evaluation framework or datasets. Please cite the original study and upstream repository when reusing their materials or ideas.
