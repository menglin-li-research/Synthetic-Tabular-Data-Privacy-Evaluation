import argparse
from pathlib import Path
from urllib.request import urlretrieve

from .config import DATASETS, RAW_DIR, DatasetSpec


def _download(url: str, destination: Path, force: bool = False) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print(f"[skip] {destination} already exists")
        return destination

    print(f"[download] {url}")
    urlretrieve(url, destination)
    print(f"[saved] {destination}")
    return destination


def download_dataset(spec: DatasetSpec, force: bool = False) -> tuple[Path, Path]:
    train_path = RAW_DIR / spec.train_filename
    test_path = RAW_DIR / spec.test_filename
    _download(spec.train_url, train_path, force=force)
    _download(spec.test_url, test_path, force=force)
    return train_path, test_path


def download_all(force: bool = False) -> None:
    for spec in DATASETS:
        download_dataset(spec, force=force)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the published train/test splits used in the reproduction."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite files if they already exist.",
    )
    args = parser.parse_args()
    download_all(force=args.force)


if __name__ == "__main__":
    main()
