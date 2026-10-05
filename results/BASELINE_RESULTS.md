# Audited Stage-1 Baseline Results

## Execution status

The baseline completed successfully on GitHub Actions.

- Dataset: Pima Indians Diabetes
- Published split: 614 training rows / 154 test rows
- Synthetic rows: 614
- Generator: GaussianMultivariate from `copulas`
- Utility model: balanced logistic regression
- Runtime: GitHub Actions, Ubuntu, Python 3.11
- Workflow run: https://github.com/menglin-li-research/Synthetic-Tabular-Data-Privacy-Evaluation/actions/runs/37310789357

## Resemblance

| Metric | Value |
|---|---:|
| Mean KS statistic | 0.08225 |
| Mean absolute standardized mean difference | 0.05214 |
| Correlation-matrix RMSE | 0.06276 |

These values indicate that the Stage-1 synthetic sample is reasonably close to the real training data on the selected marginal and correlational diagnostics. They should not be interpreted as a complete fidelity assessment.

## Utility

| Metric | TRTR | TSTR | TSTR/TRTR |
|---|---:|---:|---:|
| Accuracy | 0.6948 | 0.6623 | 0.9533 |
| Balanced accuracy | 0.6980 | 0.6687 | 0.9580 |
| F1 | 0.6240 | 0.5938 | 0.9515 |
| ROC-AUC | 0.8134 | 0.7822 | 0.9616 |

Under this baseline, training on synthetic data retains roughly 95–96% of the corresponding real-data predictive performance, depending on the metric.

## Privacy screening

| Metric | Value |
|---|---:|
| Median synthetic-to-train nearest-neighbour distance | 1.19085 |
| Median held-out-real-to-train nearest-neighbour distance | 1.01171 |
| Distance ratio (synthetic / held-out) | 1.17706 |
| Exact-match rate | 0.00000 |

The synthetic sample is not closer to the training records than the held-out real sample under this median nearest-neighbour diagnostic, and no exact duplicate was found.

**Important:** this is only a disclosure-risk screening. It is not differential privacy and does not establish resistance to membership inference, attribute inference, or other attacks.

## Runtime notes

The GaussianMultivariate fitting stage emitted non-fatal SciPy distribution-fitting warnings. The job nevertheless completed successfully and produced all expected outputs. These warnings should be investigated before treating the baseline as a final reproduction of the upstream method.

## Next validation steps

1. inspect variable-level distributions rather than only aggregate resemblance metrics;
2. reproduce the upstream privacy tests (similarity, membership inference, attribute inference);
3. add a second generator such as SDV/CTGAN;
4. add a second dataset;
5. test fairness and subgroup utility explicitly.
