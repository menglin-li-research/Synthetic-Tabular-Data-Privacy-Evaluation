# Two-Dataset Gaussian Baseline — Audited Results

## Execution

The current pipeline completed successfully on GitHub Actions with Python 3.11.

Workflow run:

https://github.com/menglin-li-research/Synthetic-Tabular-Data-Privacy-Evaluation/actions/runs/37311344200

## Visual summary

![TRTR vs TSTR ROC-AUC](figures/utility_auc.svg)

![Privacy diagnostics](figures/privacy_diagnostics.svg)

![Resemblance summary](figures/resemblance_summary.svg)

## Pima Indians Diabetes

### Resemblance

| Metric | Value |
|---|---:|
| Mean KS statistic | 0.08225 |
| Mean absolute standardized mean difference | 0.05214 |
| Correlation-matrix RMSE | 0.06276 |

### Utility

| Metric | TRTR | TSTR | TSTR/TRTR |
|---|---:|---:|---:|
| Accuracy | 0.6948 | 0.6623 | 0.9533 |
| Balanced accuracy | 0.6980 | 0.6687 | 0.9580 |
| F1 | 0.6240 | 0.5938 | 0.9515 |
| ROC-AUC | 0.8134 | 0.7822 | 0.9616 |

### Privacy screening

| Metric | Value |
|---|---:|
| Synthetic-to-train median nearest-neighbour distance | 1.19085 |
| Held-out-real-to-train median nearest-neighbour distance | 1.01171 |
| Distance ratio | 1.17706 |
| Exact-match rate | 0.00000 |

### Upstream-style membership inference

| Hamming threshold | Mean precision | Mean accuracy |
|---|---:|---:|
| 0.4 | 0.5098 | 0.5098 |
| 0.3 | 0.5098 | 0.5045 |
| 0.2 | 0.4131 | 0.4654 |
| 0.1 | 0.5788 | 0.4955 |

## Contraceptive Method Choice

### Resemblance

| Metric | Value |
|---|---:|
| Mean KS statistic | 0.01264 |
| Mean absolute standardized mean difference | 0.01801 |
| Correlation-matrix RMSE | 0.05852 |

### Utility

| Metric | TRTR | TSTR | TSTR/TRTR |
|---|---:|---:|---:|
| Accuracy | 0.5492 | 0.5220 | 0.9506 |
| Balanced accuracy | 0.5487 | 0.5294 | 0.9647 |
| Macro F1 | 0.5422 | 0.5176 | 0.9546 |
| Macro ROC-AUC | 0.7330 | 0.7058 | 0.9628 |

### Privacy screening

| Metric | Value |
|---|---:|
| Synthetic-to-train median nearest-neighbour distance | 0.72833 |
| Held-out-real-to-train median nearest-neighbour distance | 0.42958 |
| Distance ratio | 1.69545 |
| Exact-match rate | 0.02547 |

The exact-match rate is higher than in Pima, but the Contraceptive dataset is composed of highly discrete integer-coded variables. Exact matching therefore requires additional contextual analysis and should not be treated as direct evidence of identity disclosure.

### Upstream-style membership inference

| Hamming threshold | Mean precision | Mean accuracy |
|---|---:|---:|
| 0.4 | 0.5135 | 0.5135 |
| 0.3 | 0.5135 | 0.5135 |
| 0.2 | 0.5232 | 0.5322 |
| 0.1 | 0.6051 | 0.6159 |

## Takeaway

Across both datasets, the Gaussian multivariate baseline retains approximately 96% of the real-data ROC-AUC benchmark. Privacy behaviour is less uniform: the continuous/mixed-scale Pima data show no exact duplicate under the current screening, whereas the highly discrete Contraceptive data show some exact matching and somewhat stronger attack accuracy at the strictest Hamming threshold.

These results support a central methodological point: **synthetic-data quality and synthetic-data privacy must be evaluated separately**.

None of the current privacy results constitute a formal differential-privacy guarantee.
