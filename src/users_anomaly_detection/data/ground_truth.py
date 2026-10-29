"""Ground truth do CERT r4.2 (Spec 03/07): answers/insiders.csv -> pares (user, day).

Incidentes: user + janela [start, end] datetimes. Dia do incidente:
todos os dias entre start_date e end_date, inclusivos. Laje de treino nunca
toque nisso; rótulo só para avaliação (RF-08).
"""

import datetime as dt

import polars as pl

from users_anomaly_detection import config


def _parse_date(text: str) -> dt.date:
    """Datas do insiders.csv: '10/23/2010 1:41:56' — sem zero-padding."""
    month, day, year = text.split(" ", 1)[0].split("/")[:3]
    return dt.date(int(year), int(month), int(day))


def incidents() -> pl.DataFrame:
    """70 incidentes da release 4.2 com user, start, end (como date)."""
    return (
        pl.scan_csv(config.ANSWERS_DIR / "insiders.csv")
        .with_columns(pl.col("dataset").cast(pl.String))
        .filter(pl.col("dataset") == config.GROUND_TRUTH_RELEASE)
        .select(
            "scenario",
            "user",
            start="start",
            end="end",
        )
        .collect()
    )


def positive_pairs() -> pl.DataFrame:
    """Uma linha por (user, day) dentro de cada incidente [start.date, end.date]."""
    pairs = []
    for row in incidents().iter_rows(named=True):
        user = row["user"]
        day0, day1 = _parse_date(row["start"]), _parse_date(row["end"])
        day = day0
        while day <= day1:
            pairs.append({"user": user, "day": day})
            day += dt.timedelta(days=1)
    table = pl.DataFrame(pairs).with_columns(pl.col("day").cast(pl.Date)).unique()
    return table.with_columns(label=pl.lit(True))
