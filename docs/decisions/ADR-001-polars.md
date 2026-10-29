# ADR-001 — Polars como engine tabular

**Status:** aceito

**Contexto:** os logs do CERT r4.2 somam bilhões de linhas no agregado
(email e http são as maiores fontes). Precisamos consolidar isso numa
estação local, sem cluster. A biblioteca precisa: ler CSV grande com
esquema explícito, executar lazy com pushdown de colunas e filtros, e
agregar por grupo rápido.

**Decisão:** usar **polars** como única engine tabular do projeto. Nenhuma
panda. Leitura com `pl.scan_csv` lazy; persistência intermediária em
parquet (zstd).

**Consequências:**
- + processamento de CSVs grandes dentro da RAM de um PC de trabalho.
- + aggregation e chain de transformações rápidas e expressivas.
- − API difere de pandas; código de referência da internet não copia direto.
- − o time pode precisar de pequena rampa de aprendizado.
