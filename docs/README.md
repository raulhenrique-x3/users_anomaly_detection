# users_anomaly_detection

Modelo de IA para análise de anomalias de comportamento de usuários em sistemas de
software, baseado no [CERT Insider Threat Dataset (r4.2)](https://www.kaggle.com/datasets/andrihjonior/cert-insider-threat-dataset-r4-2).

## Estrutura do projeto

```
docs/          # Especificações (spec-driven development) — LEIA ANTES DE CODAR
  README.md    # Este índice
  plan.md      # Roadmap e marcos
  specs/       # 01 → 07: visão, requisitos, dados, arquitetura, features, modelos, avaliação
  decisions/   # ADRs (decisões arquiteturais com contexto e consequências)
data/
  raw/         # Dataset CERT r4.2 baixado (scripts/fetch_dataset.py)
  interim/     # Dados intermediários processados (alvo de data/ pipeline)
  features/    # Tabelas de atributos consolidadas ( usuário-dia )
src/
  users_anomaly_detection/
    config.py     # Caminhos e hiperparâmetros
    data/         # Carregamento, limpeza, consolidação
    features/     # Engenharia de atributos
    models/       # Detecção de anomalias
    evaluation/   # Métricas e relatórios
scripts/       # Scripts executáveis (fetch, pipeline, treino, avaliação)
```

## Como usar

```bash
# 1. Ambiente (venv já existente em .venv)
source .venv/bin/activate

# 2. Baixar o dataset (~GB, cache do kagglehub)
python scripts/fetch_dataset.py

# 3. Dependências
pip install -r requirements.txt
```

## Processo

Projeto segue spec-driven development: cada etapa de implementação começa por
atualizar sua spec em `docs/specs/`, recebe aprovação rápida, depois vira código.
Mudanças de decisão relevante geram ADR novo em `docs/decisions/`.

## Atalhos de navegação

| Quer saber... | Vá em |
|---|---|
| O que o projeto resolve e métrica de sucesso | `docs/specs/01-visao-e-objetivo.md` |
| Requisitos funcionais / não funcionais | `docs/specs/02-requisitos.md` |
| Dataset, schemas, janela temporal, rótulos | `docs/specs/03-dados.md` |
| Camadas de código, fluxo de dados, CLI | `docs/specs/04-arquitetura.md` |
| Como gerar tabela usuário-dia de features | `docs/specs/05-features.md` |
| Modelos candidatos e hipótese central | `docs/specs/06-modelos.md` |
| Como medir se está funcionando | `docs/specs/07-avaliacao.md` |
| Road por fases | `docs/plan.md` |
