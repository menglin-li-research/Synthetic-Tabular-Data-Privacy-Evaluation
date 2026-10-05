from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial import distance
from sklearn.metrics import accuracy_score, precision_score


def _quantile_code(df: pd.DataFrame, q: int = 5) -> pd.DataFrame:
    coded = pd.DataFrame(index=df.index)
    for col in df.columns:
        series = df[col]
        if pd.api.types.is_numeric_dtype(series):
            try:
                coded[col] = pd.qcut(series, q=q, duplicates="drop").cat.codes
            except ValueError:
                coded[col] = pd.Categorical(series).codes
        else:
            coded[col] = pd.Categorical(series).codes
    return coded


def _identified_record(
    record_values: np.ndarray,
    synthetic_data: pd.DataFrame,
    threshold: float,
) -> bool:
    distances = distance.cdist(
        np.reshape(record_values, (1, -1)),
        synthetic_data.to_numpy(),
        metric="hamming",
    )
    return bool((distances < threshold).any())


def upstream_style_membership_inference(
    real_train: pd.DataFrame,
    real_test: pd.DataFrame,
    synthetic: pd.DataFrame,
    q: int = 5,
    thresholds: tuple[float, ...] = (0.4, 0.3, 0.2, 0.1),
    proportions: tuple[float, ...] = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
    random_state: int = 42,
) -> dict[str, dict[str, float]]:
    """Deterministic adaptation of the upstream Hamming-distance MIA simulation.

    The source repository quantile-codes each dataset, builds an attacker pool
    from real training members and held-out non-members, and predicts
    membership when a record falls within a Hamming-distance threshold of any
    synthetic record.
    """
    train_coded = _quantile_code(real_train, q=q)
    test_coded = _quantile_code(real_test, q=q)
    synthetic_coded = _quantile_code(synthetic, q=q)

    n = min(len(test_coded), len(train_coded))
    members = train_coded.sample(n=n, random_state=random_state).copy()
    nonmembers = test_coded.sample(n=n, random_state=random_state).copy()

    members["_member"] = 1
    nonmembers["_member"] = 0

    attacker = pd.concat([members, nonmembers], ignore_index=True)
    attacker = attacker.sample(frac=1, random_state=random_state).reset_index(drop=True)

    features = [c for c in attacker.columns if c != "_member"]
    results: dict[str, dict[str, float]] = {}

    for threshold in thresholds:
        precision_values = []
        accuracy_values = []

        for proportion in proportions:
            k = max(1, int(len(attacker) * proportion))
            subset = attacker.iloc[:k]
            true_labels = subset["_member"].to_numpy()

            predicted = [
                int(
                    _identified_record(
                        row,
                        synthetic_coded[features],
                        threshold,
                    )
                )
                for row in subset[features].to_numpy()
            ]

            precision_values.append(
                precision_score(true_labels, predicted, zero_division=0)
            )
            accuracy_values.append(accuracy_score(true_labels, predicted))

        results[str(threshold)] = {
            "mean_precision_across_attacker_proportions": float(
                np.mean(precision_values)
            ),
            "mean_accuracy_across_attacker_proportions": float(
                np.mean(accuracy_values)
            ),
        }

    return results
