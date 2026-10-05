from __future__ import annotations

import numpy as np
import pandas as pd
from copulas.multivariate import GaussianMultivariate


INTEGER_COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "Age",
]


def _postprocess_pima(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in INTEGER_COLUMNS:
        if col in out.columns:
            out[col] = np.rint(out[col]).clip(lower=0).astype(int)

    for col in ["BMI", "DiabetesPedigreeFunction"]:
        if col in out.columns:
            out[col] = out[col].clip(lower=0)

    if "Outcome" in out.columns:
        out["Outcome"] = (out["Outcome"] >= 0.5).astype(int)

    return out


def generate_gaussian_multivariate(
    real_train: pd.DataFrame,
    n_rows: int | None = None,
    random_state: int = 42,
) -> tuple[pd.DataFrame, GaussianMultivariate]:
    """Fit a Gaussian multivariate copula and sample synthetic rows.

    This is a compact Stage-1 baseline. It is not yet an exact port of every
    preprocessing step in the upstream study.
    """
    if n_rows is None:
        n_rows = len(real_train)

    np.random.seed(random_state)

    model = GaussianMultivariate()
    model.fit(real_train)
    synthetic = model.sample(n_rows)

    synthetic = synthetic[real_train.columns]
    synthetic = _postprocess_pima(synthetic)
    return synthetic, model
