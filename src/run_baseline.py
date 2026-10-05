from __future__ import annotations

import json

import pandas as pd

from .config import PIMA, RAW_DIR, SYNTHETIC_DIR, TABLES_DIR
from .download_data import download_pima
from .evaluate import (
    privacy_screening_metrics,
    resemblance_metrics,
    utility_metrics,
)
from .generate import generate_gaussian_multivariate


def main() -> None:
    train_path = RAW_DIR / PIMA.train_filename
    test_path = RAW_DIR / PIMA.test_filename

    if not train_path.exists() or not test_path.exists():
        print("[info] data not found; downloading published split")
        download_pima()

    real_train = pd.read_csv(train_path)
    real_test = pd.read_csv(test_path)

    synthetic, _ = generate_gaussian_multivariate(
        real_train=real_train,
        n_rows=len(real_train),
        random_state=42,
    )

    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    synthetic_path = SYNTHETIC_DIR / "pima_gaussian_multivariate_synthetic.csv"
    synthetic.to_csv(synthetic_path, index=False)

    resemblance = resemblance_metrics(
        real_train=real_train,
        synthetic=synthetic,
        target=PIMA.target,
    )
    utility = utility_metrics(
        real_train=real_train,
        real_test=real_test,
        synthetic_train=synthetic,
        target=PIMA.target,
    )
    privacy = privacy_screening_metrics(
        real_train=real_train,
        real_test=real_test,
        synthetic=synthetic,
        target=PIMA.target,
    )

    summary = {
        "dataset": PIMA.name,
        "generator": "GaussianMultivariate (copulas)",
        "n_real_train": int(len(real_train)),
        "n_real_test": int(len(real_test)),
        "n_synthetic": int(len(synthetic)),
        "resemblance": resemblance,
        "utility": utility,
        "privacy_screening": privacy,
        "note": (
            "Privacy metrics are screening diagnostics only and do not provide "
            "a formal privacy guarantee."
        ),
    }

    json_path = TABLES_DIR / "pima_gaussian_baseline_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    rows = []
    for section, values in [
        ("resemblance", resemblance),
        ("privacy_screening", privacy),
    ]:
        for metric, value in values.items():
            rows.append({"section": section, "metric": metric, "value": value})

    for split_name, metrics in utility.items():
        for metric, value in metrics.items():
            rows.append(
                {
                    "section": f"utility_{split_name}",
                    "metric": metric,
                    "value": value,
                }
            )

    pd.DataFrame(rows).to_csv(
        TABLES_DIR / "pima_gaussian_baseline_metrics.csv",
        index=False,
    )

    print("\n=== Baseline complete ===")
    print(json.dumps(summary, indent=2))
    print(f"\nSynthetic data: {synthetic_path}")
    print(f"Summary JSON:   {json_path}")


if __name__ == "__main__":
    main()
