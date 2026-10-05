import argparse
from pathlib import Path
from urllib.request import urlretrieve

from .config import PIMA, RAW_DIR


def _download(url: str, destination: Path, force: bool = False) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print(f"[skip] {destination} already exists")
        return destination

    print(f"[download] {url}")
    urlretrieve(url, destination)
    print(f"[saved] {destination}")
    return destination


def download_pima(force: bool = False) -> tuple[Path, Path]:
    train_path = RAW_DIR / PIMA.train_filename
    test_path = RAW_DIR / PIMA.test_filename
    _download(PIMA.train_url, train_path, force=force)
    _download(PIMA.test_url, test_path, force=force)
    return train_path, test_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the published Pima train/test split."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite files if they already exist.",
    )
    args = parser.parse_args()
    download_pima(force=args.force)


if __name__ == "__main__":
    main()
