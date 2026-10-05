# Methods — Current Two-Dataset Baseline

## Objective

Establish a transparent and reproducible synthetic-tabular-data evaluation pipeline before adding more complex generators and formal privacy mechanisms.

## Datasets

The current baseline uses two exact train/test splits released in the Vicomtech repository.

### Dataset E — Pima Indians Diabetes

- 614 real training rows
- 154 held-out test rows
- target: `Outcome`
- binary classification

### Dataset D — Contraceptive Method Choice

- 1,178 real training rows
- 295 held-out test rows
- target: `contraceptive_method_used`
- three-class classification

## Generator

The current generator is:

`copulas.multivariate.GaussianMultivariate`

For each dataset, the model is fitted only to the published real training split and generates a synthetic training set with the same number of rows.

For Pima, integer-valued variables are rounded and clinically non-negative variables are clipped at zero. The binary outcome is thresholded at 0.5.

For the Contraceptive dataset, all variables are discrete integer codes. Synthetic values are rounded and clipped to the observed training-data range.

This is an adaptation of the source study's Gaussian-multivariate family, not a byte-for-byte reproduction of every upstream preprocessing step.

## Resemblance

Three aggregate diagnostics are computed:

1. mean Kolmogorov–Smirnov statistic across predictors;
2. mean absolute standardized mean difference;
3. RMSE between real and synthetic correlation matrices.

Lower values indicate closer agreement on these selected statistical summaries.

## Utility

A balanced logistic-regression pipeline is evaluated under:

- **TRTR:** train on real, test on real;
- **TSTR:** train on synthetic, test on real.

Metrics:

- accuracy;
- balanced accuracy;
- F1;
- ROC-AUC;
- TSTR/TRTR ratio.

For the binary Pima task, standard binary F1 and ROC-AUC are used.

For the three-class Contraceptive task, macro F1 and one-vs-rest macro ROC-AUC are used.

## Privacy screening

Two initial disclosure-risk diagnostics are computed:

1. nearest-neighbour distance from synthetic rows to the real training set;
2. exact-duplicate rate.

The median synthetic-to-train nearest-neighbour distance is compared with the corresponding median distance from held-out real records to the training set.

These metrics are **screening diagnostics only**.

## Upstream-style membership-inference simulation

The upstream repository provides a membership-inference simulation based on Hamming distance after quantile coding.

This project implements a deterministic adaptation of that procedure:

1. each dataset is quantile-coded into up to five bins per numeric feature;
2. an attacker pool is built from equal numbers of training members and held-out non-members;
3. a record is predicted to be a member if its Hamming distance to any synthetic record falls below a chosen threshold;
4. thresholds 0.4, 0.3, 0.2, and 0.1 are evaluated;
5. precision and accuracy are averaged over attacker-data proportions from 0.2 to 1.0.

A fixed random seed is used for reproducibility.

This attack is useful for methodological comparison with the upstream code, but it is **not equivalent to a formal privacy guarantee** and does not establish differential privacy.

## Current limitations

- only one synthetic-data generator has been evaluated;
- aggregate resemblance metrics can hide subgroup or variable-level failures;
- the membership-inference simulation is threshold-dependent;
- no attribute-inference attack has yet been reproduced;
- no explicit differential-privacy mechanism is currently used;
- no fairness metric is yet included.

## Next methods

The next technical additions are planned to include:

- SDV or CTGAN as a second generator;
- upstream-style similarity evaluation;
- attribute inference;
- explicit differential privacy;
- subgroup fairness and utility analysis.
