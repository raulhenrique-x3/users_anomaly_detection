"""Estágio 3 do pipeline (Spec 04): interim parquets -> data/features/users.parquet.

Uso: python scripts/build_features.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import polars as pl

from users_anomaly_detection import config
from users_anomaly_detection.features.build import build_user_day_table


def main() -> None:
    out = config.FEATURES_DIR / "users.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)

    table = build_user_day_table().collect(engine="streaming")
    table.write_parquet(out, compression="zstd")

    # sanity-check do estágio (Spec 05): shape, escopo e ausência buracos
    n_users = table["user"].n_unique()
    day_min, day_max = table["day"].min(), table["day"].max()
    checks = {
        "linhas": len(table),
        "colunas": len(table.columns),
        "usuários": n_users,
        "período": f"{day_min} .. {day_max}",
        "parquet_mb": round(out.stat().st_size / 1e6, 1),
    }
    for k, v in checks.items():
        print(f"{k:>12}: {v}")

    assert len(table) > 0
    assert n_users > 0
    assert table["user"].null_count() == 0 and table["day"].null_count() == 0
    assert (table["logon_count"] >= 0).all()


if __name__ == "__main__":
    main()
