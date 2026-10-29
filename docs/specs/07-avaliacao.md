# Spec 07 — Avaliação

## Preparação

- Rankear todos os pares (user, day) pelo score do modelo; juntar com o
  ground truth do CERT r4.2 (pares `user`, `day` que tiveram incidente).
- Cada par marcado no ground truth conta uma vez; `(user, day)` que não está
  lá entra como "não incidente".

## Métricas

| Métrica | Definição | Por quê |
|---|---|---|
| **Recall@100** | incidentes presentes no top-100 do ranking ÷ total de incidentes | analista humano olha ~3 dias de fila; janela do CERT é dia |
| Recall@1% | idem, top-1% do ranking | referência escala com dataset |
| Precision@100 | incidentes ÷ 100 no top-100 | custo de atenção do analista |
| PR-AUC | área sob precision-recall | desbalanceamento extremo |
| ROC-AUC | área sob ROC | apenas referência entre modelos, nunca primária |

Incidentes são raros (~2% dos user-days). **Accuracy nunca é reportada.**

## Protocolo de comparação

- Baseline (z-score) e Isolation Forest — e candidato, se rodar — usam as
  **mesmas** features, o mesmo dataset completo.
- Não há split treino/teste supervisionado: modelo não supervisionado
  pontua o próprio dataset. Reportar no resultado que rótulos nunca foram
  usados para treino.
- Saída obrigatória além de métricas: tabela top-20 do ranking com as 2
  features mais contribuintes (Spec 06) para checagem manual contra os
  cenários de insider do CERT.
- Referência de literatura: papers e tutoriais de insider threat sobre o CERT
  relatam recall@100 tipicamente entre 50% e 80%. Usar apenas como sanity
  check, não como meta.

## Saída

`data/output/`:

- `scores.parquet` — user, day, score, rank
- `metrics.json` — métricas por modelo
- `report.md` — narrativa curta: tabela de métricas por modelo, top-20 com
  features principais, observações e limitações
