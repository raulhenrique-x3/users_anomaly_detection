# Detecção de Anomalias em Usuários

Um sistema que aprende a rotina digital de cada pessoa de uma empresa e aponta,
todo dia, quem está agindo de forma estranha — antes que o estranho vire perda
de dados ou dinheiro.

## O problema

Cada pessoa em uma empresa tem o seu "jeito" de usar os computadores: os
horários em que entra, os sites que visita, os e-mails que manda, quantos
arquivos transfere. Em certos casos, alguém passa a agir bem diferente disso.
É o que chamamos de ameaça interna: um exemplo comum é um funcionário que vai
sair da empresa e, dias antes, começa a baixar relatórios confidenciais fora
do expediente e a mandá-los para o e-mail pessoal.

Como é impossível vigiar todos manualmente, a defesa mais prática é saber
**quais dias saíram do padrão** — porque a maioria dos incidentes é precedida
por dias de comportamento incomum, vistos tarde demais ou nunca.

## O que o projeto faz

1. **Lê os registros da empresa** — logins, e-mails, sites acessados, uso de
   pendrives, tudo com data e hora.
2. **Resume o comportamento** de cada pessoa por dia, em números
   ("no dia 12, o usuário acessou 63 sites, 12 fora do horário").
3. **Aprende o que é rotina normal** e atribui, a cada pessoa/dia, uma nota
   de quanto aquele dia fugiu do padrão.
4. **Devolve uma lista rankeada** para a equipe de segurança: começa pelos
   dias mais suspeitos. Fila pequena e priorizada, no lugar de um oceano de
   logs.

Importante: apontar suspeita não é acusar ninguém. A lista existe para direcionar
a atenção humana — e para cada suspeita, o sistema mostra as pistas que levaram
à nota.

## Os dados

Usamos um dataset público da CERT/SEI (Carnegie Mellon), o principal
referencial mundial para esse tipo de sistema. Ele simula, por cerca de 17
meses, a rotina digital de uma empresa fictícia de ~1000 funcionários — com
ataques "plantados" de propósito, para verificarmos se o sistema também os
encontra. É o padrão de testes antes de aplicar modelos em dados reais.

## Como rodar

Precisa de Python 3.12 instalado e de conta no Kaggle para baixar o dataset.
(Dica: configure a conta Kaggle uma única vez, seguindo o passo oficial de
API token.)

```bash
# 1. Ambiente, uma única vez
python3 -m venv .venv
source .venv/bin/activate

# 2. Dependências
pip install -r requirements.txt

# 3. Baixar o dataset (alguns GB; vai direto para data/raw/)
python scripts/fetch_dataset.py
```

Depois disso, os próximos passos (fases do projeto) rodam o pipeline completo:
consolidar os logs, montar os comportamentos, treinar o detector e gerar a
lista final de alertas.

## Quão bom ele precisa ser (métricas)

Como os dias "suspeitos" de verdade são raros (~2% da lista), dizer "acertou
em 98%" significa muito pouco — nunca olhamos os 98%. Por isso medimos de
outro jeito:

| Métrica | Em palavras |
|---|---|
| **Recall** | De todos os incidentes reais, quantos apareceram no topo da lista do dia. |
| **Recall@100** | Nos 100 primeiros da fila, quantos são de verdade. É a fase de triagem humana em números. |
| **Precisão** | Das linhas mostradas, quantas foram realmente suspeitas — o quanto a fila "não engana". |
| **F1-score** | Meio termo entre recall e precisão. Aparece no relatório, mas não é nossa estrela. |
| **PR-AUC** | A qualidade global do modelo em toda a escala do ranking, sem se perder no raro. |

## Qual confiar

- **Métrica primária:** recall@100 — é o que mostra se a fila é usável no
  dia a dia.
- **Métrica de confiabilidade (a mais honesta):** PR-AUC. Ela avalia o modelo
  em toda a escala (não só o topo) e não é distorcida pelo rótulo raro.
- **Base de comparação (baseline):** um modelo simples de regras ("alerte
  quando a atividade do usuário estiver bem acima da média do dia") que a
  solução precisa derrotar com folga — senão ela não valeu o esforço.

## O que queremos alcançar

Trabalhos na literatura, sobre este mesmo dataset, reportam **50% a 80%** de
recall@100, dependendo do esforço do modelo e das features escolhidas. Nossa
meta imediata: bater o baseline. Meta mais ambiciosa: **recall@100 ≥ 50%**.
O relatório final sempre registra onde o modelo ainda erra, para manter
honestidade.

## Limites honestos

- O sistema aponta "incomum", não culpa — quem decide é a pessoa analista.
- Ações de insider sem pegada nos logs usados aqui passam despercebidas.
- Dataset é simulado; os números não se traduzem literalmente para uma
  empresa real.
