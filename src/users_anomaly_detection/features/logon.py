"""Features de logon por usuário-dia (Spec 05).

Entrada: LazyFrame interim com colunas day, date, user, pc, activity.
Saída: LazyFrame uma linha por (user, day), colunas prefixadas `logon_`.
"""

import polars as pl

from users_anomaly_detection import config


def logon_features(lf: pl.LazyFrame) -> pl.LazyFrame:
    night = (pl.col("date").dt.hour() >= config.NIGHT_START) & (
        pl.col("date").dt.hour() < config.NIGHT_END
    )
    return lf.group_by("user", "day").agg(
        logon_count=(pl.col("activity") == "Logon").sum(),
        logoff_count=(pl.col("activity") == "Logoff").sum(),
        logon_night_count=((pl.col("activity") == "Logon") & night).sum(),
        logon_pc_count=pl.col("pc").n_unique(),
        # span do dia: primeiro ao último evento de sessão
        session_span_hours=(
            (pl.col("date").max() - pl.col("date").min()).dt.total_seconds() / 3600
        ),
    )
