"""Features de navegação web por usuário-dia (Spec 05)."""

import polars as pl

from users_anomaly_detection import config


def http_features(lf: pl.LazyFrame) -> pl.LazyFrame:
    night = (pl.col("date").dt.hour() >= config.NIGHT_START) & (
        pl.col("date").dt.hour() < config.NIGHT_END
    )
    domain = (
        pl.col("url")
        .str.to_lowercase()
        .str.split("//")
        .list.last()
        .str.split("/")
        .list.first()
    )
    job_flag = (
        pl.lit(False).or_(
            *[
                pl.col("url").str.to_lowercase().str.contains(p, literal=True)
                for p in config.JOB_SITE_PATTERNS
            ]
        )
    )

    return lf.with_columns(
        domain.alias("domain"),
    ).group_by("user", "day").agg(
        http_count=pl.len(),
        http_domain_count=pl.col("domain").n_unique(),
        http_night_count=night.sum(),
        http_job_sites_count=job_flag.sum(),
    )
