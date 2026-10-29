"""Leitura lazy das fontes do CERT r4.2 e normalização de datas.

Cada função retorna um pl.LazyFrame com colunas
    day (Date) | date (Datetime) | user (str) | pc (str) | <colunas da fonte>
Sem I/O escondido: quem chama decide materializar.
"""

import polars as pl

from users_anomaly_detection import config
from users_anomaly_detection.data.sources import LOG_COLUMNS


def _parse_date(col: str) -> pl.Expr:
    """Texto MM/DD/YYYY HH:MM:SS -> Datetime; inválidos viram null."""
    return pl.col(col).str.strptime(
        pl.Datetime, format=config.DATETIME_FORMAT, strict=False
    )


def load_source(name: str, raw_dir: "str | None" = None) -> pl.LazyFrame:
    """Scan lazy do CSV da fonte, parseia data, deriva `day` e limpa colunas."""
    csv_path = (raw_dir or config.RAW_DIR_CERT) / f"{name}.csv"
    keep = LOG_COLUMNS[name]

    lf = pl.scan_csv(csv_path).select(keep).with_columns(
        _parse_date("date").alias("date")
    ).with_columns(
        pl.col("date").dt.date().alias("day"),
    )
    return lf.drop_nulls(subset=["date", "user"])
