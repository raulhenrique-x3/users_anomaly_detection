"""Métricas contra o ground truth (Spec 07).

Sobre o ranking global user-day: recall@100 (primária), recall@1%,
precision@100, PR-AUC e ROC-AUC (referência). Accuracy nunca reportada.
"""

import numpy as np
import polars as pl
from sklearn.metrics import average_precision_score, roc_auc_score


def _ranking_metrics(labels: np.ndarray, scores: np.ndarray, top_n: int) -> dict:
    total_positives = int(labels.sum())
    order = np.argsort(-scores, kind="stable")
    top_labels = labels[order[:top_n]]
    top1pct = labels[order[: max(1, int(len(labels) * 0.01))]]
    return {
        f"recall@{top_n}": float(top_labels.sum() / total_positives),
        "recall@1pct": float(top1pct.sum() / total_positives),
        f"precision@{top_n}": float(top_labels.sum() / top_n),
        # nº de incidentes dentro do topo (valor absoluto do recall@N)
        f"incidents@{top_n}": int(top_labels.sum()),
        "pr_auc": float(average_precision_score(labels, scores)),
        "roc_auc": float(roc_auc_score(labels, scores)),
    }


def evaluate(
    scores: pl.DataFrame, positives: pl.DataFrame, score_cols: list[str]
) -> tuple[pl.DataFrame, int]:
    """Métrica por coluna de score + nº total de positivos no dataset.

    scores: user | day | <score_cols...>
    positives: user | day | label  (par (user, day) do CERT)
    """
    labeled = scores.join(positives, on=["user", "day"], how="left").with_columns(
        pl.col("label").fill_null(False)
    )
    y = labeled["label"].to_numpy().astype(int)
    rows = [
        {"score": name, **_ranking_metrics(y, labeled[name].to_numpy(), top_n=100)}
        for name in score_cols
    ]
    return pl.DataFrame(rows), int(y.sum())
