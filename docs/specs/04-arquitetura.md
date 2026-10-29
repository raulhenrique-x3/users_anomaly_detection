# Spec 04 — Arquitetura

## Princípio

Pipeline em estágios com persistência em disco entre eles. Cada estágio lê de
uma pasta e grava em outra. Scripts executáveis fazem só orquestração; a lógica
fica nas camadas. Iteração em uma etapa não reprocessa a anterior.

## Camadas (src/users_anomaly_detection/)

```
config.py       # caminhos, janelas, hiperparâmetros, seeds
data/
  sources.py    # paths dos 5 CSVs por bloco, esquemas polars por fonte
  load.py       # scan lazy dos CSVs -> normalização de datas/columns
  clean.py      # limpeza e validação, contagens de descarte
features/
  build.py      # orquestra: fonte -> agregações -> tabela usuário-dia
  logon.py / http.py / email.py / device.py / file.py   # 1 módulo por fonte,
                # cada um exporta a(s) agregação(ões) da sua fonte (Spec 05)
models/
  baseline.py   # z-score simples nos atributos brutos
  detector.py   # detector principal(es) (Spec 06), fit/score
evaluation/
  metrics.py    # recall@k, PR-AUC, prec@k contra ground truth
  report.py     # gera relatório (markdown/tabela + JSON)
```

## Fluxo

```
kagglehub            polars (lazy)              polars                      sklearn / torch
data/raw/*.csv  →    data/interim/*.parquet  →  data/features/users.parquet →  modelos
                     (1 linha = evento)         (1 linha = usuário-dia)      data/models/*.pkl|pt
                                                                                        │
                                                        avaliação contra gr  ←───────────┘
                                                        data/output/ (rankings, métricas)
```

Estágios:

| Estágio | Script | Entra | Sai |
|---|---|---|---|
| 1. fetch | `scripts/fetch_dataset.py` | kagglehub | `data/raw/` |
| 2. interim | `scripts/build_interim.py` | `data/raw/` | `data/interim/*.parquet` |
| 3. features | `scripts/build_features.py` | `data/interim/` | `data/features/users.parquet` |
| 4. train | `scripts/train_model.py` | `data/features/` | `data/models/`, scores |
| 5. evaluate | `scripts/evaluate.py` | scores + ground truth | `data/output/` |

## Convenções

- leitura de CSVs grandes: sempre `pl.scan_csv` lazy; `collect` só no fim ou
  ao persistir em parquet.
- cada módulo expota funções puras: recebe DataFrame/pl.LazyFrame retorna
  DataFrame; sem I/O escondido na camada de features/models.
- config único; nada de strings mágicas espalhadas.
- nomes de coluna de features: prefixo por fonte (ex.: `logon_count`,
  `http_domains_unique`, `email_size_mean`) — facilita explicabilidade.
- scripts de `scripts/` usam CLI mínimo (`argparse`) com flags `--input`,
  `--output` quando útil; default = caminhos do config.
