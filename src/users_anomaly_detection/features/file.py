"""Features de cópia de arquivos por usuário-dia (Spec 05).

Cada linha em `file.csv` é uma cópia de arquivo observada no host.
"""

import polars as pl


def file_features(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.group_by("user", "day").agg(
        file_copy_count=pl.len(),
        file_pc_count=pl.col("pc").n_unique(),
    )
