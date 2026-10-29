"""Detector principal: Isolation Forest em features log1p + RobustScaler (Spec 06).

Treino transdutivo (sem split/rotulagem); rótulos ficam para a avaliação.
Contribuição por feature (RF-07): perturbação para a mediana de treino —
no espaço escalado a mediana é 0; contribuição = score original - score
com a feature na mediana; magnitude rankeia as Top-N.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler

from users_anomaly_detection import config

N_ESTIMATORS = 200


def fit(feature_matrix: np.ndarray) -> tuple[RobustScaler, IsolationForest]:
    scaler = RobustScaler().fit(feature_matrix)
    model = IsolationForest(
        n_estimators=N_ESTIMATORS, random_state=config.RANDOM_SEED, n_jobs=-1
    )
    model.fit(scaler.transform(feature_matrix))
    return scaler, model


def anomaly_score(
    scaler: RobustScaler, model: IsolationForest, feature_matrix: np.ndarray
) -> np.ndarray:
    """Anomalia = -score_samples (quanto maior, mais anômalo)."""
    return -model.score_samples(scaler.transform(feature_matrix))


def _contributions(
    row_scaled: np.ndarray, model: IsolationForest
) -> np.ndarray:
    base = -model.score_samples(row_scaled[None, :])[0]
    out = np.empty(row_scaled.shape[0])
    for i in range(row_scaled.shape[0]):
        perturred = row_scaled.copy()
        perturred[i] = 0.0  # mediana no espaço escalado
        out[i] = base - (-model.score_samples(perturred[None, :])[0])
    return out


def explain(
    row_scaled: np.ndarray,
    features: list[str],
    model: IsolationForest,
    top: int = 2,
) -> list[str]:
    """Features mais contribuintes de UMA linha pré-processada (scaled)."""
    contribs = np.abs(_contributions(row_scaled, model))
    order = np.argsort(-contribs)[:top]
    return [features[i] for i in order]


def explain_batch(
    rows_scaled: np.ndarray,
    features: list[str],
    model: IsolationForest,
    top: int = 2,
) -> list[list[str]]:
    return [explain(row, features, model, top) for row in rows_scaled]
