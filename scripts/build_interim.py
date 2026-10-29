"""Estágio 2 do pipeline (Spec 04): raw CSVs -> data/interim/<fonte>.parquet.

Passa 2x por CSV (stats + escrita). No http/email isso é demorado por linha,
aceitável: roda uma vez. Uso: python scripts/build_interim.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from users_anomaly_detection import config
from users_anomaly_detection.data.clean import clean, validation_stats
from users_anomaly_detection.data.load import load_source


def build_source(name: str, force: bool = False) -> dict:
    """Lê, valida, filtra e persiste uma fonte. Retorna resumo do estágio."""
    out = config.INTERIM_DIR / f"{name}.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)

    if out.exists() and not force:
        nrows = pl.scan_parquet(out).select(pl.len()).collect().item()
        return {"source": name, "rows": "?", "bad_date": "?", "null_user": "?",
                "bad_activity": "?", "kept": nrows,
                "parquet_mb": round(out.stat().st_size / 1e6, 1)}

    stats = validation_stats(load_source(name), name).to_dicts()[0]
    df = clean(load_source(name), name).collect(engine="streaming")
    df.write_parquet(out, compression="zstd")

    stats["kept"] = len(df)
    stats["parquet_mb"] = round(out.stat().st_size / 1e6, 1)
    return stats


def main() -> None:
    force = "--force" in sys.argv
    report = pl.DataFrame(
        [build_source(name, force=force) for name in config.DATA_SOURCES]
    )
    print(report)
    assert report["kept"].sum() > 0


if __name__ == "__main__":
    main()
