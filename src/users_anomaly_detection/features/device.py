"""Features de dispositivos por usuário-dia (Spec 05)."""

import polars as pl


def device_features(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.group_by("user", "day").agg(
        device_connect_count=(pl.col("activity") == "Connect").sum(),
        device_disconnect_count=(pl.col("activity") == "Disconnect").sum(),
        device_pc_count=pl.col("pc").n_unique(),
    )
