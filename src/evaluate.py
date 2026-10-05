from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    roc_auc_score,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class UtilityResult:
    accuracy: float
    balanced_accuracy: float
    f1: float
    roc_auc: float


def resemblance_metrics(
    real_train: pd.DataFrame,
    synthetic: pd.DataFrame,
    target: str,
) -> dict[str, float]:
    feature_cols = [c for c in real_train.columns if c != target]
    numeric_cols = [
        c for c in feature_cols
        if pd.api.types.is_numeric_dtype(real_train[c])
    ]

    ks_values = []
    smd_values = []

    for col in numeric_cols:
        real = real_train[col].dropna().to_numpy()
        syn = synthetic[col].dropna().to_numpy()
        if len(real) == 0 or len(syn) == 0:
            continue

        ks_values.append(float(ks_2samp(real, syn).statistic))

        pooled_sd = np.sqrt((np.var(real, ddof=1) + np.var(syn, ddof=1)) / 2)
        if pooled_sd > 0:
            smd_values.append(float(abs(np.mean(real) - np.mean(syn)) / pooled_sd))

    real_corr = real_train[numeric_cols].corr().to_numpy()
    syn_corr = synthetic[numeric_cols].corr().to_numpy()
    corr_rmse = float(np.sqrt(np.nanmean((real_corr - syn_corr) ** 2)))

    return {
        "mean_ks_statistic": float(np.mean(ks_values)) if ks_values else np.nan,
        "mean_abs_standardized_mean_difference": (
            float(np.mean(smd_values)) if smd_values else np.nan
        ),
        "correlation_matrix_rmse": corr_rmse,
    }


def _fit_and_score(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    target: str,
) -> UtilityResult:
    x_train = train_df.drop(columns=[target])
    y_train = train_df[target].astype(int)
    x_test = test_df.drop(columns=[target])
    y_test = test_df[target].astype(int)

    numeric_cols = list(x_train.columns)

    preprocess = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_cols,
            )
        ],
        remainder="drop",
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocess),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)

    pred = model.predict(x_test)
    prob = model.predict_proba(x_test)
    classes = np.unique(y_test)

    if len(classes) == 2:
        f1 = f1_score(y_test, pred)
        roc_auc = roc_auc_score(y_test, prob[:, 1])
    else:
        f1 = f1_score(y_test, pred, average="macro")
        roc_auc = roc_auc_score(
            y_test,
            prob,
            multi_class="ovr",
            average="macro",
        )

    return UtilityResult(
        accuracy=float(accuracy_score(y_test, pred)),
        balanced_accuracy=float(balanced_accuracy_score(y_test, pred)),
        f1=float(f1),
        roc_auc=float(roc_auc),
    )


def utility_metrics(
    real_train: pd.DataFrame,
    real_test: pd.DataFrame,
    synthetic_train: pd.DataFrame,
    target: str,
) -> dict[str, dict[str, float]]:
    trtr = _fit_and_score(real_train, real_test, target)
    tstr = _fit_and_score(synthetic_train, real_test, target)

    trtr_dict = asdict(trtr)
    tstr_dict = asdict(tstr)

    ratios = {}
    for metric, real_value in trtr_dict.items():
        syn_value = tstr_dict[metric]
        ratios[metric] = float(syn_value / real_value) if real_value else np.nan

    return {
        "trtr": trtr_dict,
        "tstr": tstr_dict,
        "tstr_to_trtr_ratio": ratios,
    }


def privacy_screening_metrics(
    real_train: pd.DataFrame,
    real_test: pd.DataFrame,
    synthetic: pd.DataFrame,
    target: str,
) -> dict[str, float]:
    feature_cols = [c for c in real_train.columns if c != target]

    scaler = StandardScaler()
    real_train_scaled = scaler.fit_transform(real_train[feature_cols])
    real_test_scaled = scaler.transform(real_test[feature_cols])
    synthetic_scaled = scaler.transform(synthetic[feature_cols])

    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(real_train_scaled)

    syn_dist, _ = nn.kneighbors(synthetic_scaled)
    test_dist, _ = nn.kneighbors(real_test_scaled)

    syn_dist = syn_dist.ravel()
    test_dist = test_dist.ravel()

    rounded_real = {
        tuple(row)
        for row in real_train.round(6).itertuples(index=False, name=None)
    }
    rounded_syn = [
        tuple(row)
        for row in synthetic.round(6).itertuples(index=False, name=None)
    ]
    exact_match_rate = (
        sum(row in rounded_real for row in rounded_syn) / len(rounded_syn)
        if rounded_syn
        else np.nan
    )

    median_test = float(np.median(test_dist))
    median_syn = float(np.median(syn_dist))

    return {
        "synthetic_to_train_median_nn_distance": median_syn,
        "heldout_real_to_train_median_nn_distance": median_test,
        "median_distance_ratio_syn_to_heldout": (
            float(median_syn / median_test) if median_test > 0 else np.nan
        ),
        "synthetic_exact_match_rate": float(exact_match_rate),
    }
