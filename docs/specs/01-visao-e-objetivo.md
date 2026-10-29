# Spec 01 — Visão e Objetivo

## Problema

Detectar ameaças internas (insider threat): usuários legítimos de uma organização
que, por intenção (roubo de dados, sabotagem) ou negligência (comprometimento de
conta), passam a se comportar de forma anômala no sistema — downloads em massa,
acessos fora do expediente, uso de pendrives, logins impossíveis, etc.

Não é classificação supervisionada: ataques são raríssimos (~2% dos user-days
do CERT) e os rótulos são parcos. O modelo aprende o comportamento "normal" e
sinaliza o que foge dele.
**Detector de anomalias não supervisionado, por usuário.**

## Objetivo

Construir pipeline end-to-end que:

1. Ingestiona os logs de telemetria do CERT r4.2 (5 fontes), limpa e consolida.
2. Deriva, por usuário e por dia, um vetor de atributos de comportamento.
3. Treina detector(es) de anomalia não supervisionados.
4. Produz ranking de risco diário por usuário, com explicabilidade (quais
   atributos puxaram o score).
5. Avalia contra o ground truth de incidentes do r4.2 (pares user+day),
   medindo recall@k e derivadas.

## Métrica de sucesso

- **Primária:** recall@100 (nº de incidentes do ground truth presentes no
  top-100 do ranking global usuário-dia).
- **Secundárias:** recall@1%, PR-AUC, prec@100 — anomalias são raras, accuracy
  e ROC-AUC são inúteis aqui.
- Baseline empírica: score z simples sobre 3-5 atributos brutos; o ganho do
  modelo deve ser demonstrado contra essa linha.

## Escopo

**Dentro:** pipeline de dados em polars, features por usuário-dia, detecção
não supervisionada, avaliação contra rótulos do CERT, relatório de resultados.

**Fora:** inferência em tempo real, alerta em produção, interface gráfica,
retreino automático, análise forense individual por caso.

## Consequências da visão (por que esses formatos)

- Ranking de risco, não classificação binária: no mundo real, analista humano
  olha os N primeiros. A métrica precisa refletir isso.
- Score por usuário-dia, não por evento: granularidade natural do CERT e do
  SOAR; permite agregação simples.
