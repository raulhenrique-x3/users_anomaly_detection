"""Estágio 4 (Spec 04): data/features/users.parquet -> modelos + scores.

Treino transdutivo: baseline z-score e Isolation Forest sobre o mesmo dataset.
Sem rótulos. Uso: python scripts/train_model.py
"""

import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import polars as pl

from users_anomaly_detection import config
from users_anomaly_detection.models import baseline, detector


def main() -> None:
    features_path = config.FEATURES_DIR / "users.parquet"
    df = pl.read_parquet(features_path)
    features = [c for c in df.columns if c not in ("user", "day")]
    X = np.log1p(df.select(features).to_numpy().astype(float))  # Spec 06: log1p

    # baseline (referência) + detector principal (Isolation Forest)
    baseline_scores, baseline_params = baseline.zscore_scores(X)
    scaler, model = detector.fit(X)
    iforest_scores = detector.anomaly_score(scaler, model, X)

    scores = pl.DataFrame(
        {
            "user": df["user"],
            "day": df["day"],
            "score_baseline": np.round(baseline_scores, 6),
            "score_iforest": np.round(iforest_scores, 6),
        }
    )
    out = config.OUTPUT_DIR / "scores.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    scores.write_parquet(out, compression="zstd")

    pickle.dump(baseline_params, (config.MODELS_DIR / "baseline.pkl").open("wb"))
    pickle.dump({"scaler": scaler, "model": model}, (config.MODELS_DIR / "iforest.pkl").open("wb"))

    print(f"rows={len(scores)}  features={len(features)}")
    print(f"scores -> {out}")


if __name__ == "__main__":
    main()
