# ADR-003 — PyTorch + GPU como runtime de neural nets

**Status:** aceito

**Contexto:** anomalia em dados tabulares. Ambiente já tem `torch == 2.15.0`
e `pytorch-lightning == 2.6.6`; GPU NVIDIA RTX 5060 Ti detectada com CUDA
disponível. Isolation Forest (sklearn) roda em CPU.

**Decisão:** autoencoder pytorch-lightning como modelo experimental apenas,
após comparativo contra Isolation Forest. Não é aposta inicial.

**Consequências:**
- + GPU aproveitada; treino rápido se usado.
- − autoencoder em features tabulares de ~40 colunas nem sempre supera
  métodos clássicos; custo de inferência mais alto.
- − nada de redes de série temporal nesta iteração (LSTM sobre sequência
  bruta): features são agregadas por usuário-dia.
