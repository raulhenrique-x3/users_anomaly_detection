# Spec 03 — Dados: CERT Insider Threat Dataset r4.2

> **Status:** schema validado contra o download real (kagglehub, relayout do
> maintainer — CSVs únicos, não blocos por semana).

## Layout real em `data/raw/`

```
r4.2/
  logon.csv    (id, date, user, pc, activity)
  device.csv   28M   (id, date, user, pc, activity: Connect/Disconnect)
  file.csv     185M  (id, date, user, pc, filename, content)
  email.csv    1.3G  (id, date, user, pc, to, cc, bcc, from, size, attachments, content)
  http.csv     8.3G  (id, date, user, pc, url, content)
  LDAP/        (org info por mês — não usado nesta iteração)
answers/
  insiders.csv (dataset, scenario, details, user, start, end)  ← ground truth
  r4.2-1..3/   (CSVs detalhados por incidente — observáveis)
```

- `date`: texto `MM/DD/YYYY HH:MM:SS` (parse strict=False + drop de nulos).
- `content` (email/http/file): texto ofuscado (bag of words) — não vai para
  features; jogamos fora já no `scan_csv` (projection pushdown).
- `id`: GUID — descartado.
- Domínio "da empresa" nos e-mails: `@dtaa.com`.

## Ground truth real

`answers/insiders.csv`, 70 linhas `dataset == "4.2"` → incidentes com
`user`, `start`, `end` (datetime). Dias positivos: cada (user, day) dentro
do intervalo `[start, end]`. Métricas por user-day (Spec 07).

## Visão geral

O CERT Insider Threat Dataset simula logs de telemetria de uma organização
fictícia (~1000 funcionários) ao longo de ~517 dias. Incidentes de insider
threat são "plantados" em cenários, e o ground truth vem junto (`answers/`).
Cada linha de log = **evento** (usuário faz algo, num PC, num instante).

| Fonte | Evento logado | Colunas úteis (id/content fora) |
|---|---|---|
| `logon.csv` | sessões de login/logout | `date`, `user`, `pc`, `activity` (Logon/Logoff) |
| `device.csv` | pendrive/CD/impressora | `date`, `user`, `pc`, `activity` (Connect/Disconnect) |
| `http.csv` | navegação web | `date`, `user`, `pc`, `url` |
| `email.csv` | e-mails (proxy) | `date`, `user`, `pc`, `from`, `to`, `cc`, `bcc`, `size`, `attachments` |
| `file.csv` | cópia de arquivos | `date`, `user`, `pc`, `filename` |

## Ground truth

`answers/insiders.csv` — uma linha por incidente: `dataset`, `scenario`,
`details`, `user`, `start`, `end`. Filtrar `dataset == "4.2"` (70 incidentes).
Dias positivos = todos os (user, day) com `start ≤ day ≤ end` — derivado na
camada `evaluation/`, nunca em treino.

## Decisão: r4.2 (não r6.2)

r4.2 tem ground truth simples (70 incidentes declarados) e volume suficiente.
r6.2 é maior e com rótulos mais fragmentados. Ver `ADR-002-cert-r42.md`.

## Estratégia de ingestão

1. `kagglehub.dataset_download(...)` → cache local → copiar para `data/raw/`.
2. Ler cada fonte com `pl.scan_csv(..., columns=[...])` — só as colunas úteis
   (deixa `id`/`content` no CSV: pushdown de projeção corteja leitura).
3. `date` texto → `pl.Datetime` (`MM/DD/YYYY HH:MM:SS`, strict=False);
   descartar linhas não parseáveis/null em `user`, com contagem registrada.
4. Derivar `day = date.dt.date()` (grânulo padrão do dataset).
5. Persistir cada fonte em `data/interim/<fonte>.parquet` (zstd). http/email
   são os gigantes — parquet compacto é obrigatório.

## Tratamento por fonte

- `logon.csv` — `activity` é direção (Logon/Logoff); features derivam nº de
  logins/logoffs, night count, nº de PCs e span de sessão.
- `device.csv` — Connect/Disconnect por sessão → contagens + nº de PCs.
- `http.csv` — domínio extraído de `url` (por `://` e primeiro `/`);
  contagens + nº de domínios + night + sites de emprego.
- `email.csv` — destinatários de `to`/`cc`/`bcc` (split por `;`);
  externo = domínio ≠ `@dtaa.com`; `size`, `attachments` entram direto.
- `file.csv` — toda linha é cópia → contagem + nº de PCs.

## Riscos

- http.csv (8.3G): nunca materializar inteiro; scan com `columns=` + parquet
  interim resolve memória.
- `date` pode ter linhas malformadas / `user` nulo: filtrar e reportar contagem.
- Rótulos são pares (user, day) derivados de start/end; sem inferir mais.
