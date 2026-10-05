from __future__ import annotations

import numpy as np
import pandas as pd
from copulas.multivariate import GaussianMultivariate


PIMA_INTEGER_COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "Age",
]


def _postprocess_pima(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in PIMA_INTEGER_COLUMNS:
        if col in out.columns:
            out[col] = np.rint(out[col]).clip(lower=0).astype(int)

    for col in ["BMI", "DiabetesPedigreeFunction"]:
        if col in out.columns:
            out[col] = out[col].clip(lower=0)

    if "Outcome" in out.columns:
        out["Outcome"] = (out["Outcome"] >= 0.5).astype(int)

    return out


def _postprocess_discrete(
    df: pd.DataFrame,
    real_train: pd.DataFrame,
) -> pd.DataFrame:
    out = df.copy()
    for col in real_train.columns:
        lo = float(real_train[col].min())
        hi = float(real_train[col].max())
        out[col] = np.rint(out[col]).clip(lower=lo, upper=hi).astype(int)
    return out


def generate_gaussian_multivariate(
    real_train: pd.DataFrame,
    dataset_name: str,
    n_rows: int | None = None,
    random_state: int = 42,
) -> tuple[pd.DataFrame, GaussianMultivariate]:
    """Fit a Gaussian multivariate copula and sample synthetic rows."""
    if n_rows is None:
        n_rows = len(real_train)

    np.random.seed(random_state)

    model = GaussianMultivariate()
    model.fit(real_train)
    synthetic = model.sample(n_rows)
    synthetic = synthetic[real_train.columns]

    if dataset_name == "pima":
        synthetic = _postprocess_pima(synthetic)
    elif dataset_name == "contraceptive":
        synthetic = _postprocess_discrete(synthetic, real_train)
    else:
        raise ValueError(f"Unsupported dataset: {dataset_name}")

    return synthetic, model
