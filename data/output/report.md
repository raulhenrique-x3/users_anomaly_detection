# Relatório — Detecção de anomalias (CERT r4.2)

- Tabela avaliada: 330452 pares (user, day)
- Incidentes no ground truth (nesse período): 1364

## Métricas por modelo
| score | recall@100 | recall@1pct | precision@100 | incidents@100 | pr_auc | roc_auc |
| --- | --- | --- | --- | --- | --- | --- |
| score_baseline | 0.0271 | 0.0711 | 0.3700 | 37 | 0.0382 | 0.7999 |
| score_iforest | 0.0015 | 0.0528 | 0.0200 | 2 | 0.0156 | 0.8468 |

Legenda: recall@100 = proporção dos incidentes que aparecem no top-100
do ranking global (métrica primária); PR-AUC = confiabilidade geral
sob rótulo raro; ROC-AUC apenas referência; accuracy proibida aqui.

## Top-20 do ranking (modelo principal)

1. **BSS0369** 2010-02-03 — score 0.7835 | pistas: device_disconnect_count, logon_pc_count
2. **HDS0367** 2010-07-08 — score 0.7835 | pistas: logon_pc_count, logoff_count
3. **IBB0359** 2010-04-23 — score 0.7727 | pistas: logoff_count, device_disconnect_count
4. **HDS0367** 2010-12-30 — score 0.7706 | pistas: logoff_count, logon_pc_count
5. **AJF0370** 2010-09-13 — score 0.7653 | pistas: logoff_count, logon_pc_count
6. **WDD0366** 2010-06-10 — score 0.7505 | pistas: logon_pc_count, session_span_hours
7. **AJF0370** 2010-11-15 — score 0.7504 | pistas: logon_pc_count, device_pc_count
8. **IBB0359** 2011-01-21 — score 0.7490 | pistas: logoff_count, logon_pc_count
9. **EIS0041** 2010-03-16 — score 0.7487 | pistas: logoff_count, logon_pc_count
10. **AJF0370** 2010-10-12 — score 0.7465 | pistas: logoff_count, logon_pc_count
11. **BSS0369** 2010-09-30 — score 0.7463 | pistas: device_pc_count, logon_pc_count
12. **MPM0220** 2010-04-28 — score 0.7463 | pistas: email_size_sum, logon_pc_count
13. **BAL0044** 2011-03-25 — score 0.7458 | pistas: logoff_count, logon_pc_count
14. **BAL0044** 2011-04-29 — score 0.7451 | pistas: email_size_sum, logoff_count
15. **AJF0370** 2010-09-14 — score 0.7451 | pistas: email_size_sum, session_span_hours
16. **AJF0370** 2011-04-11 — score 0.7448 | pistas: email_size_sum, logoff_count
17. **BAL0044** 2011-02-21 — score 0.7444 | pistas: email_size_sum, logon_pc_count
18. **AJF0370** 2010-12-08 — score 0.7440 | pistas: logon_pc_count, device_disconnect_count
19. **BAL0044** 2011-02-25 — score 0.7437 | pistas: logon_pc_count, device_pc_count
20. **AJF0370** 2011-03-24 — score 0.7437 | pistas: logon_pc_count, logoff_count

## Limitações
- Treino transdutivo: score é sobre o próprio dataset; rótulos nunca usados no treino.
- Dataset simulado; recall@100 típico na literatura: 50%-80%.
- Modelo aponta 'incomum', não culpa.