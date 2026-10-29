# ADR-004 — scikit-learn como dependência adicional

**Status:** aceito (sklearn 1.9.1 instalado)

**Contexto:** nenhum pacote de modelos clássicos está instalado hoje
(venv tem torch/polars/numpy, mas não sklearn/matplotlib). Isolation Forest
e RobustScaler são o núcleo do approach tabular detalhado em Spec 06/07.

**Decisão proposta:** instalar `scikit-learn` (e `matplotlib`, para gráfico
precision-recall no relatório). Sem deps além dessas no primeiro ciclo.

**Consequências:**
- + Isolation Forest/RobustScaler/PR-AUC nativos.
- − mais um peso no ambiente (~11 MB) — aceitável.
- matplotlib dispensado: relatório é markdown (RF-09 gráfico é opcional).

**Nota:** a instalar no momento em que se inicia `models/`; requirements.txt
deve ser regenerado (freeze) após isso.
