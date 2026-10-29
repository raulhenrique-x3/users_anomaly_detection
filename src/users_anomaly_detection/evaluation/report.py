"""Geração do relatório final (Spec 07): metrics.json + report.md."""

import json
from pathlib import Path

import polars as pl


def _md_table(df: pl.DataFrame) -> str:
    """Markdown sem pandas/pyarrow; floats com 4 casas."""
    def fmt(v):
        return f"{v:.4f}" if isinstance(v, float) else str(v)

    cols = df.columns
    lines = ["| " + " | ".join(cols) + " |",
             "| " + " | ".join("---" for _ in cols) + " |"]
    for row in df.iter_rows():
        lines.append("| " + " | ".join(fmt(v) for v in row) + " |")
    return "\n".join(lines)


def write_report(
    metrics_df: pl.DataFrame,
    top20: pl.DataFrame,
    total_positives: int,
    n_rows: int,
    out_metrics: Path,
    out_md: Path,
) -> None:
    metrics_payload = {
        "n_rows": n_rows,
        "total_positives": total_positives,
        "models": metrics_df.to_dicts(),
    }
    out_metrics.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")

    metric_cols = [c for c in metrics_df.columns if c != "score"]
    lines = [
        "# Relatório — Detecção de anomalias (CERT r4.2)",
        "",
        f"- Tabela avaliada: {n_rows} pares (user, day)",
        f"- Incidentes no ground truth (nesse período): {total_positives}",
        "",
        "## Métricas por modelo",
        _md_table(metrics_df.select("score", *metric_cols)),
        "",
        "Legenda: recall@100 = proporção dos incidentes que aparecem no top-100",
        "do ranking global (métrica primária); PR-AUC = confiabilidade geral",
        "sob rótulo raro; ROC-AUC apenas referência; accuracy proibida aqui.",
        "",
        "## Top-20 do ranking (modelo principal)",
        "",
    ]
    for r in top20.iter_rows(named=True):
        lines.append(
            f"{r['rank']}. **{r['user']}** {r['day']} — score {r['score']:.4f}"
            f" | pistas: {r['feature_1']}, {r['feature_2']}"
        )
    lines += [
        "",
        "## Limitações",
        "- Treino transdutivo: score é sobre o próprio dataset; rótulos nunca usados no treino.",
        "- Dataset simulado; recall@100 típico na literatura: 50%-80%.",
        "- Modelo aponta 'incomum', não culpa.",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")
