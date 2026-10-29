# Spec 05 — Engenharia de features (tabela usuário-dia)

## Granularidade

**Uma linha = (user, day).** Colunas identificadores: `user`, `day`.

Cada fonte gera suas agregações; no final, join externo (`outer`) em
`(user, day)` e zeros onde não houve atividade.

## Features por fonte

### logon

- `logon_count`, `logoff_count`
- `logon_night_count` — logins entre 00h–06h
- `logon_first_time`, `logon_last_time` → `session_span_hours` (span do dia)
- `logon_pc_count` — nº de PCs distintos usados

### device

- `device_connect_count`, `device_disconnect_count`
- `device_pc_count` — PCs distintos com dispositivo

### http

- `http_count` — nº de eventos
- `http_domain_count` — nº de domínios distintos (da coluna `url`)
- `http_job_sites_count` — acessos a sites de busca de emprego / job sites do
  CERT — proxy clássico de insider prestes a sair
- `http_night_count`

### email

- `email_sent_count`
- `email_recipients_total` — soma de destinatários (to + cc + bcc)
- `email_external_count` — destinatário de domínio externo à organização
- `email_size_sum`, `email_size_max`
- `email_attachment_count`
- `email_night_count`

### file

- `file_copy_count`
- `file_pc_count`

## Convenções

- Coluna derivada por evento para reuso entre fontes: `is_weekend` (sáb/dom),
  `is_night` (00h–06h).
- Nomes prefixados pela fonte (ex.: `email_sent_count`) — facilita seguir o
  padrão do dataset e dá a base para explicabilidade.
- Tipos de dados: `str` para user, `Date` para day, `Int32` para contagens,
  `Float32` para medidas (tamanhos, horas).

## Tabela final

```
user | day | logon_count | logon_night_count | ... | email_attachment_count | file_copy_count
```

Coluna `label` (user, day no ground truth) adicionada **apenas** no estágio de
avaliação, nunca no treino — modelo é não supervisionado.

## Persistência

`data/features/users.parquet` (zstd), escritida em uma passada, com
metadados de linhas e colunas registradas.

## Risco

- Features correlacionadas (count vs sum) — podar durante exploração
  inicial, escolha registrada no config.
- Threshold de noite/fim de semana varia por empresa — fixado aqui
  explicitamente (00h–06h; sáb+dom).
