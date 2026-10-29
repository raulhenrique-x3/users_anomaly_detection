"""Features de e-mail por usuário-dia (Spec 05).

Destinatários em `to`/`cc`/`bcc` vêm como listas separadas por `;`.
Externo = destinatário com domínio != org (config.ORG_DOMAIN).
"""

import polars as pl

from users_anomaly_detection import config


def _recipients(field: str) -> pl.Expr:
    return (
        pl.col(field)
        .fill_null("")
        .str.split(";")
        .list.eval(pl.element().str.strip_chars())
        .list.eval(pl.element().filter(pl.element() != ""))
    )


def _has_external(field: str) -> pl.Expr:
    return _recipients(field).list.eval(
        pl.element().str.contains("@") & ~pl.element().str.ends_with(config.ORG_DOMAIN)
    ).list.any()


def email_features(lf: pl.LazyFrame) -> pl.LazyFrame:
    night = (pl.col("date").dt.hour() >= config.NIGHT_START) & (
        pl.col("date").dt.hour() < config.NIGHT_END
    )
    n_recipients = _recipients("to").list.len() + _recipients("cc").list.len() + _recipients("bcc").list.len()

    return lf.group_by("user", "day").agg(
        email_sent_count=pl.len(),
        email_recipients_total=n_recipients.sum(),
        email_external_count=(_has_external("to") | _has_external("cc") | _has_external("bcc")).sum(),
        email_size_sum=pl.col("size").sum(),
        email_size_max=pl.col("size").max(),
        email_attachment_count=pl.col("attachments").sum(),
        email_night_count=night.sum(),
    )
