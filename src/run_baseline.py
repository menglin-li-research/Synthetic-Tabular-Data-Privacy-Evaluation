from __future__ import annotations

import json

import pandas as pd

from .config import DATASETS, RAW_DIR, SYNTHETIC_DIR, TABLES_DIR
from .download_data import download_all
from .evaluate import (
    privacy_screening_metrics,
    resemblance_metrics,
    utility_metrics,
)
from .generate import generate_gaussian_multivariate
from .privacy_attacks import upstream_style_membership_inference


def run_dataset(spec) -> dict:
    train_path = RAW_DIR / spec.train_filename
    test_path = RAW_DIR / spec.test_filename

    real_train = pd.read_csv(train_path)
    real_test = pd.read_csv(test_path)

    synthetic, _ = generate_gaussian_multivariate(
        real_train=real_train,
        dataset_name=spec.name,
        n_rows=len(real_train),
        random_state=42,
    )

    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    synthetic_path = SYNTHETIC_DIR / f"{spec.name}_gaussian_multivariate_synthetic.csv"
    synthetic.to_csv(synthetic_path, index=False)

    resemblance = resemblance_metrics(
        real_train=real_train,
        synthetic=synthetic,
        target=spec.target,
    )
    utility = utility_metrics(
        real_train=real_train,
        real_test=real_test,
        synthetic_train=synthetic,
        target=spec.target,
    )
    privacy = privacy_screening_metrics(
        real_train=real_train,
        real_test=real_test,
        synthetic=synthetic,
        target=spec.target,
    )
    membership = upstream_style_membership_inference(
        real_train=real_train,
        real_test=real_test,
        synthetic=synthetic,
    )

    summary = {
        "dataset": spec.name,
        "generator": "GaussianMultivariate (copulas)",
        "n_real_train": int(len(real_train)),
        "n_real_test": int(len(real_test)),
        "n_synthetic": int(len(synthetic)),
        "resemblance": resemblance,
        "utility": utility,
        "privacy_screening": privacy,
        "membership_inference_upstream_style": membership,
        "note": (
            "Nearest-neighbour and upstream-style membership-inference metrics "
            "are empirical diagnostics and do not provide a formal privacy guarantee."
        ),
    }

    json_path = TABLES_DIR / f"{spec.name}_gaussian_baseline_summary.json"
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

    for threshold, metrics in membership.items():
        for metric, value in metrics.items():
            rows.append(
                {
                    "section": f"membership_inference_threshold_{threshold}",
                    "metric": metric,
                    "value": value,
                }
            )

    pd.DataFrame(rows).to_csv(
        TABLES_DIR / f"{spec.name}_gaussian_baseline_metrics.csv",
        index=False,
    )

    return summary


def main() -> None:
    if any(
        not (RAW_DIR / spec.train_filename).exists()
        or not (RAW_DIR / spec.test_filename).exists()
        for spec in DATASETS
    ):
        print("[info] one or more datasets not found; downloading published splits")
        download_all()

    all_results = {}
    for spec in DATASETS:
        print(f"\n=== Running dataset: {spec.name} ===")
        all_results[spec.name] = run_dataset(spec)

    combined_path = TABLES_DIR / "combined_gaussian_baseline_summary.json"
    combined_path.write_text(
        json.dumps(all_results, indent=2),
        encoding="utf-8",
    )

    print("\n=== Multi-dataset baseline complete ===")
    print(json.dumps(all_results, indent=2))
    print(f"\nCombined summary: {combined_path}")


if __name__ == "__main__":
    main()
