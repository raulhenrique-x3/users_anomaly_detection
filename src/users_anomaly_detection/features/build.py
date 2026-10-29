"""Orquestrador de features (Spec 05): dos parquets interim à tabela usuário-dia.

Uma linha = (user, day). Cada fonte contribui com suas colunas (módulo próprio);
join externo e zeros onde não houve atividade.
"""

import polars as pl

from users_anomaly_detection import config
from users_anomaly_detection.features.device import device_features
from users_anomaly_detection.features.email import email_features
from users_anomaly_detection.features.file import file_features
from users_anomaly_detection.features.http import http_features
from users_anomaly_detection.features.logon import logon_features

FEATURE_MODULES = {
    "logon": logon_features,
    "device": device_features,
    "http": http_features,
    "email": email_features,
    "file": file_features,
}

# contagens viram 0 quando o usuário não teve atividade na fonte naquele dia
COUNT_COLUMNS = [
    "logon_count", "logoff_count", "logon_night_count", "logon_pc_count",
    "session_span_hours",
    "device_connect_count", "device_disconnect_count", "device_pc_count",
    "http_count", "http_domain_count", "http_night_count", "http_job_sites_count",
    "email_sent_count", "email_recipients_total", "email_external_count",
    "email_size_sum", "email_size_max", "email_attachment_count", "email_night_count",
    "file_copy_count", "file_pc_count",
]


def build_user_day_table() -> pl.LazyFrame:
    """Une as features de todas as fontes em uma tabela (user, day)."""
    tables = [
        features(pl.scan_parquet(config.INTERIM_DIR / f"{name}.parquet"))
        for name, features in FEATURE_MODULES.items()
    ]

    table = tables[0]
    for next_table in tables[1:]:
        table = table.join(next_table, on=["user", "day"], how="full", coalesce=True)

    return (
        table
        .with_columns(pl.col(COUNT_COLUMNS).fill_null(0))  # sem atividade = 0
        .sort("user", "day")
    )
