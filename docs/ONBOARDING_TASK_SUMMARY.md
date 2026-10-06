# Onboarding Task Summary

This page maps the current repository directly to the coding task assigned by Dr. Qinyi Liu.

## Assigned coding task

The task was to:

1. follow the coding link accompanying the synthetic-tabular-data evaluation paper;
2. implement at least one synthetic-data generation method;
3. run the method on one or two datasets;
4. upload the code to GitHub;
5. provide a clear README and reproducible workflow.

## What has been completed

### Synthetic-data method

**Gaussian Multivariate** using the `copulas` implementation.

### Datasets

Two train/test splits released by the upstream project:

- **Pima Indians Diabetes**
- **Contraceptive Method Choice**

### Evaluation

The reproduction currently evaluates three distinct dimensions:

- **Resemblance** — KS statistic, standardized mean difference, correlation-matrix RMSE
- **Utility** — TRTR vs. TSTR performance
- **Privacy diagnostics** — nearest-neighbour screening, exact-match screening, and an upstream-style membership-inference simulation

### Reproducibility

The repository includes:

- explicit Python dependencies;
- a Conda environment specification;
- automatic download of the published data splits;
- deterministic seeds where supported;
- GitHub Actions execution in a clean Python 3.11 environment;
- documented methods, results, limitations, and next steps.

## Main empirical finding

Across both datasets, the Gaussian baseline retains about **96% of the real-data ROC-AUC benchmark** under the current TSTR evaluation.

However, the privacy diagnostics differ across datasets:

- Pima: no exact synthetic duplicate detected and membership-inference accuracy close to chance;
- Contraceptive Method Choice: 2.55% exact-match rate and stronger attack accuracy at the strictest Hamming threshold.

This supports the methodological conclusion that:

> **Synthetic-data utility and synthetic-data privacy should be evaluated separately.**

## Important boundary of the current work

The current generator is **not differentially private**. The privacy tests are empirical diagnostics, not formal guarantees.

Fairness is also **not yet implemented as an empirical evaluation dimension**. It remains a planned extension.

## Next technical extensions

The most useful next steps are:

1. add a second generator such as SDV or CTGAN;
2. reproduce similarity and attribute-inference analyses from the upstream project;
3. introduce an explicit differential-privacy mechanism and privacy budget;
4. add subgroup and fairness evaluation.

## Repository status

The latest integrated workflow completes successfully on GitHub Actions.
