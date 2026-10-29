"""Estágio 5 (Spec 04): scores + ground truth -> métricas + relatório.

Uso: python scripts/evaluate.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from users_anomaly_detection import config
from users_anomaly_detection.data.ground_truth import positive_pairs
from users_anomaly_detection.evaluation import report
from users_anomaly_detection.evaluation.metrics import evaluate
from users_anomaly_detection.models import detector


SCORE_COLS = ["score_baseline", "score_iforest"]
ACTIVE_MODEL = "score_iforest"  # modelo principal do relatório


def main() -> None:
    scores = pl.read_parquet(config.OUTPUT_DIR / "scores.parquet")
    positives = positive_pairs()
    metrics_df, total_positives = evaluate(scores, positives, SCORE_COLS)
    print(metrics_df)

    # top-20 do modelo ativo com explicabilidade (RF-07)
    import pickle

    iforest = pickle.load((config.MODELS_DIR / "iforest.pkl").open("rb"))
    top20 = (
        scores.sort(ACTIVE_MODEL, descending=True)
        .head(20)
        .with_row_index("rank", offset=1)
    )
    feature_rows = pl.read_parquet(config.FEATURES_DIR / "users.parquet").join(
        top20.select("user", "day"), on=["user", "day"], how="inner"
    )
    features = [c for c in feature_rows.columns if c not in ("user", "day")]
    X = np.log1p(feature_rows.select(features).to_numpy().astype(float))
    scaled = iforest["scaler"].transform(X)
    hints = detector.explain_batch(scaled, features, iforest["model"], top=2)
    top20 = top20.with_columns(
        feature_1=pl.Series([h[0] for h in hints], dtype=pl.String),
        feature_2=pl.Series([h[1] for h in hints], dtype=pl.String),
    ).with_columns(pl.col(ACTIVE_MODEL).alias("score"))

    report.write_report(
        metrics_df=metrics_df,
        top20=top20,
        total_positives=total_positives,
        n_rows=len(scores),
        out_metrics=config.OUTPUT_DIR / "metrics.json",
        out_md=config.OUTPUT_DIR / "report.md",
    )
    print(f"relatório -> {config.OUTPUT_DIR / 'report.md'}")


if __name__ == "__main__":
    main()
