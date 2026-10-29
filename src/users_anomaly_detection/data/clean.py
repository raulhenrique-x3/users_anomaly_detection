"""Validação e limpeza por fonte: contagem de descartes e filtros de domínio.

Funções puras sobre LazyFrame; podem ser encadeadas ou usadas para auditoria.
Uma única passada colectiva por consultoria (streaming engine).
"""

import polars as pl

from users_anomaly_detection.data.sources import VALID_ACTIVITIES


def validation_stats(lf: pl.LazyFrame, name: str) -> pl.DataFrame:
    """Contagens de problemas *antes* do filtro final: linhas totais,
    datas não parseadas, usuários nulos e activity fora do domínio.

    Para http/email/file a checagem de activity é pulada (sem coluna).
    """
    row = lf.select(
        rows=pl.len(),
        bad_date=pl.col("date").is_null().sum(),
        null_user=pl.col("user").is_null().sum(),
    ).collect(engine="streaming").row(0)

    out = {"source": name, "rows": row[0], "bad_date": row[1], "null_user": row[2]}

    if name in VALID_ACTIVITIES:
        out["bad_activity"] = (
            lf.filter(~pl.col("activity").is_in(sorted(VALID_ACTIVITIES[name])))
            .select(pl.len())
            .collect(engine="streaming")
            .item()
        )
    else:
        out["bad_activity"] = None
    return pl.DataFrame(out)


def clean(lf: pl.LazyFrame, name: str) -> pl.LazyFrame:
    """Filtra linhas fora do domínio de activity (logon/device)."""
    if name in VALID_ACTIVITIES:
        lf = lf.filter(
            pl.col("activity").is_in(sorted(VALID_ACTIVITIES[name]))
        )
    return lf
