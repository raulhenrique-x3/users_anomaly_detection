"""Baixa o CERT Insider Threat Dataset (r4.2) via kagglehub e copia para data/raw/.

Uso: python scripts/fetch_dataset.py
"""

import shutil
from pathlib import Path

import kagglehub

DATASET = "andrihjonior/cert-insider-threat-dataset-r4-2"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Baixando {DATASET} (cache do kagglehub)...")
    path = Path(kagglehub.dataset_download(DATASET))
    print(f"Cache em: {path}")

    print(f"Copiando para {RAW_DIR} ...")
    shutil.copytree(path, RAW_DIR, dirs_exist_ok=True)
    print("Concluído.")


if __name__ == "__main__":
    main()
