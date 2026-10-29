# Spec 02 — Requisitos

## Funcionais

| ID | Requisito | Spec detalhada |
|---|---|---|
| RF-01 | Baixar e materializar o dataset CERT r4.2 em `data/raw/` a partir do kagglehub | `01` / `03` |
| RF-02 | Ler cada fonte de log (login, device, http, email, file) com polars, lidando com volume grande (scan lazy, filtro por coluna antes de decodificar totalmente) | `03` |
| RF-03 | Limpeza e validação: tipos corretos, datas parseadas, domínios/valores inválidos descartados com contagem registrada | `03` |
| RF-04 | Consolidar dados por usuário-dia em tabela de features (uma linha = usuário + dia) | `05` |
| RF-05 | Treinar pelo menos um detector de anomalia não supervisionado; output = score por usuário-dia | `06` |
| RF-06 | Ranking global usuário-dia ordenado por score | `06` |
| RF-07 | Explicabilidade: Top-N atributos que mais contribuíram por score do usuário-dia | `06` |
| RF-08 | Avaliar contra rótulos (day.csv de incidentes) com recall@k, PR-AUC, prec@k | `07` |
| RF-09 | Relato final em JSON/CSV+markdown: métricas, tabela top-k, gráfico opcional | `07` |

## Não funcionais

| ID | Requisito | Racional |
|---|---|---|
| RNF-01 | Processamento dos logs completos deve terminar em tempo viável em uma estação local (minutos, não horas) | polars lazy + filtros seletivos; dataset r4.2 é ~ milhares de MB |
| RNF-02 | Cada etapa intermediária gravada em disco (`data/interim/`, `data/features/`) para poder rodar etapa seguinte sem refazer a anterior | iterabilidade; dados grandes não trafegam em memória entre scripts |
| RNF-03 | Código organizado por camada (data → features → models → evaluation), sem lógica de negócio em scripts | legibilidade |
| RNF-04 | Configurações (caminhos, k variáveis, janelas) centralizadas em `config.py`, nenhum hardcoded em módulo | manutenibilidade |
| RNF-05 | Sementes fixáveis (reproducibilidade) e registradas no config | modelos devem reproduzir |
| RNF-06 | Sem pandas; manipulação tabular unicamente via polars | ADR-001 |

## Dependências principais

- `polars` — manipulação/leitura de dados tabulares grandes
- `kagglehub` — obtenção do dataset
- `torch` + `pytorch-lightning` (GPU RTX 5060 Ti) — candidato a modelo neural
- `scikit-learn` — **a instalar**: baseline Isolation Forest/LOF
- `matplotlib` ou similar — a instalar para gráficos da avaliação

Ver lista completa com versões fixadas em `requirements.txt` (freeze do venv).
