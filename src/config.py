from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
RESULTS_DIR = ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    train_url: str
    test_url: str
    train_filename: str
    test_filename: str
    target: str


PIMA = DatasetSpec(
    name="pima",
    train_url=(
        "https://raw.githubusercontent.com/Vicomtech/"
        "STDG-evaluation-metrics/main/REAL%20DATASETS/TRAIN%20DATASETS/"
        "E_PimaIndiansDiabetes_Real_Train.csv"
    ),
    test_url=(
        "https://raw.githubusercontent.com/Vicomtech/"
        "STDG-evaluation-metrics/main/REAL%20DATASETS/TEST%20DATASETS/"
        "E_PimaIndiansDiabetes_Real_Test.csv"
    ),
    train_filename="E_PimaIndiansDiabetes_Real_Train.csv",
    test_filename="E_PimaIndiansDiabetes_Real_Test.csv",
    target="Outcome",
)
