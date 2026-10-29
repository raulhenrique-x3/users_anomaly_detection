# Spec 06 — Modelos de detecção

## Formulação

Não supervisionado, granularidade usuário-dia: dado o vetor de features do
usuário `u` no dia `d`, o score diz "quão anômalo é esse dia, comparado ao
padrão global (e/ou ao próprio usuário no restante da série)". Saída não é
classe, é **score**; o ranking global é construído sobre todos os pares
(user, day).

## Modelos em duas faixas

1. **Baseline (sempre roda, referência):** z-score simples por atributo com
   média/σ global; score = média dos z-scores. Custo quase zero. Serve para
   saber se o modelo maior realmente agrega.
2. **Modelo principal — Isolation Forest (sklearn, a instalar):** padrão de
   mercado em anomalia tabular, rápido, robusto a outliers. Score =
   `-decision_function`. CPU, não precisa GPU.
3. **Candidato experimental (torch + GPU RTX 5060 Ti):** autoencoder
   feed-forward em pytorch-lightning; score = erro de reconstrução. É
   hipótese, não aposta segura: com ~30 features tabulares, nem sempre há
   estrutura profunda relevante. Só entra no comparativo se os dois primeiros
   ficarem fracos.

## Pré-processamento

Contagens de telemetria são distorcidas com cauda longa e outliers.
Padrão: `log1p` nas contagens + `RobustScaler` (mediana/IQR). Ajustado no
split de treino, aplicado em qualquer inferência.

## Explicabilidade mínima (RF-07)

Contribuição por feature calculada por perturbação: score original menos score
com a feature centralizada à mediana de treino. |contribuição| rankeia as duas
melhores features por usuário-dia. Funciona para os três modelos, não exige
biblioteca de interpretação externa.

## Regras

- Rótulos do CERT (user, day) entram **somente** na avaliação (Spec 07).
  Nenhuma decisão de treino ou seleção de feature usa rótulos.
- Seed fixa em config para toda fase de treino (RNF-05).

## Artefatos

- `data/models/baseline.pkl`
- `data/models/iforest.pkl`
- `data/models/autoencoder.pt` (só se aprovado no comparativo)
- Scores completos em `data/output/scores.parquet`
