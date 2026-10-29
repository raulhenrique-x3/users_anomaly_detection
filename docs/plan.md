# Road — plan.md

Ordem de implementação, uma fase por vez, cada fase começa deixando a spec
dela atualizada e termina com o estágio rodando ponta a ponta.

## FASE 0 — Fundação *(feito nesta sessão)*

- [x] Estrutura de docs no padrão spec-driven (specs/ + decisions/ + plan)
- [x] requirements.txt por freeze do venv
- [x] Script de download do dataset (scripts/fetch_dataset.py)
- [x] Download em execução → data/raw/

## FASE 1 — Conhecer os dados *(feito)*

- [x] Download completo e copiado para `data/raw/` (r4.2/ + answers/).
- [x] Schemas validados com polars lazy; datas `MM/DD/YYYY HH:MM:SS`.
- [x] `03-dados.md` atualizado com layout real — CSVs únicos (não blocos),
      ground truth em `answers/insiders.csv` (70 incidentes dataset 4.2).

## FASE 2 — interim *(código pronto; parquets em data/interim/)*

- [x] `src/.../data/{sources,load,clean}.py` + `scripts/build_interim.py`
      (lazy, validação com contagem de descartes, parquet zstd).
- [x] Smoke-test logon (854k linhas limpas, sem bad_date/null_user).

## FASE 3 — features *(feito)*

- [x] `src/.../features/{logon,device,http,email,file,build}.py`
- [x] `scripts/build_features.py` — join completo das fontes
- [x] `data/features/users.parquet` (zstd): 330.452 user-days × 23 colunas,
      1.000 usuários, 2010-01-02 .. 2011-05-17; sem null em user/day;
      sanity: hits de job-site em 63.996 dias, atividade noturna em 9.513.
- [ ] Exploratório inicial (jupytext) para podar features correlacionadas —
      levar para Fase 4 antes de treinar.

## FASE 4 — modelos *(feito)*

- [x] scikit-learn 1.9.1 instalado (ADR-004) + requirements regenerado.
- [x] `src/.../data/ground_truth.py` — 70 incidentes → 1.364 usados (user,
      day) de `answers/insiders.csv`.
- [x] `models/baseline.py` (z-score robusto, guarda mean/std)
- [x] `models/detector.py` (IsolationForest 200 árvores, seed 42;
      plot explicativo por perturbação = mediana)
- [x] `scripts/train_model.py` → `data/models/` + `data/output/scores.parquet`

## FASE 5 — avaliação *(feita; resultados do 0-iteration)*

- [x] `evaluation/metrics.py` (recall@100/1%, precision@100, PR-AUC, ROC-AUC —
      accuracy omitida de propósito)
- [x] `evaluation/report.py` — `metrics.json` + `report.md` (tabela markdown
      sem pandas/pyarrow), Top-20 com 2 features-pista
- [x] `scripts/evaluate.py`

### Resultado do primeiro ciclo (baseline honesto)

| modelo | recall@100 | prec@100 | PR-AUC | ROC-AUC |
|---|---|---|---|---|
| baseline (z) | **2,7%** (37 in.) | 0,37 | 0,038 | 0,80 |
| Isolation Forest | 0,15% (2 in.) | 0,02 | 0,016 | 0,85 |

- **Isolation Forest sobrevivente pior que o baseline no topo** — o código
  funciona, os sinais de features ainda são genéricos demais. É o ponto de
  partida; melhoria esperada vem de (a) feat. mais específicas (uploads/
  downloads por tamanho, domínios raros, pendrive fora de expediente),
  (b) comparação com o mesmo usuário no tempo (seu próprio histórico),
  (c) ajuste de hiperparâmetros e (d) autoencoder como candidato (ADR-003).
- Lift de baseline já é sólido; próximo passo é o notebook exploratório da
  Fusão de features + candidato 2.

## Metas de guardrail

- RNF-01: cada estágio em minutos, não horas (bench na execução).
- Toda fase lida de parquet anterior; nada reprocessa o raw sem ordem.
- Specs atualizadas *antes* de codar a fase (spec-driven).
