# Methods — Stage 1 Baseline

## Objective

Establish a minimal, reproducible synthetic-tabular-data experiment before attempting a full reproduction of the upstream evaluation framework.

## Dataset

The baseline uses **Dataset E: Pima Indians Diabetes**, using the exact train/test CSV files published in the Vicomtech repository.

Target variable: Outcome

## Generator

copulas.multivariate.GaussianMultivariate

The model is fitted to the published real training split and samples the same number of synthetic rows. Integer-valued variables are rounded back to integer form, non-negative clinical variables are clipped at zero, and the binary outcome is thresholded at 0.5.

This is an adaptation of the source study's Gaussian-multivariate family, not yet a byte-for-byte reproduction of its complete preprocessing pipeline.

## Resemblance

Three compact diagnostics are used:

1. mean Kolmogorov–Smirnov statistic across numeric predictors;
2. mean absolute standardized mean difference;
3. RMSE between real and synthetic correlation matrices.

Lower values indicate closer statistical resemblance.

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

## Privacy screening

Stage 1 uses two conservative screening diagnostics:

1. nearest-neighbour distance from synthetic rows to real training rows;
2. exact-duplicate rate after rounding to six decimal places.

The median synthetic-to-train distance is compared with the median held-out-real-to-train distance.

These are **not formal privacy guarantees** and should not be reported as differential privacy, membership-inference resistance, or proof of non-disclosure.

## Planned stronger privacy evaluation

- membership inference attack simulation;
- attribute inference;
- similarity/distance-based disclosure analyses matching the upstream code;
- differential-privacy mechanisms and explicit privacy budgets.
