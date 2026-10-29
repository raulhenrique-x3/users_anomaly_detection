# ADR-002 — Dataset CERT r4.2 (e não r6.2)

**Status:** aceito

**Contexto:** existem duas gerações: r4.2 e r6.2 (a mais nova, com ~55 dias
por subcenário e logs mais densos). O usuário indicou r4.2 via kagglehub
(`andrihjonior/cert-insider-threat-dataset-r4-2`).

**Decisão:** r4.2.

**Racional:**
- ground truth day-level mais simples (pares user+day);
- volume alto o suficiente para o problema, menor custo de ingestão;
- indíicado como requisito do usuário.

**Consequências:**
- + menor tempo por iteração, pipeline mais simples.
- − r6.2 tem mais incidentes e cenários modernos; migração futura é possível,
  já que pipeline consome "conjunto de CSVs de log + lista de incidentes".
  O estágio interim abstrai o formato.
