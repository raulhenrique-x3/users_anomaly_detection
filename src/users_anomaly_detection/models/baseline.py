"""Baseline de referência (z-score), Spec 06.

Aposto desprezível por design: z (média/σ global) sobre atributos log1p,
score = média dos |z| por linha. Serve de régua mínima — o modelo principal
precisa superá-la.
"""

import numpy as np
import polars as pl


def zscore_scores(feature_matrix: np.ndarray) -> tuple[np.ndarray, dict]:
    """Média dos |z| por linha; guarda mean/std para reproducibilidade."""
    mean = feature_matrix.mean(axis=0)
    std = feature_matrix.std(axis=0)
    std_safe = np.where(std == 0, 1.0, std)
    z = np.abs(feature_matrix - mean) / std_safe
    params = {"mean": mean.tolist(), "std": std_safe.tolist()}
    return z.mean(axis=1), params


def explain_from_z(z_matrix: np.ndarray, features: list[str], top: int = 2) -> list[list[str]]:
    """Mesma semântica de contribuição: variável com maior |z| por linha."""
    return [[features[i] for i in np.argsort(-row)[:top]] for row in z_matrix]
