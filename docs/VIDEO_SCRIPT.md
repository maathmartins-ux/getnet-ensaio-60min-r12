# Roteiro do vídeo

Sem números falados que não estejam nos blocos gerados do README (`scripts/fill_readme.py`).

1. **Abertura.** O problema: lojista pergunta sobre produto, sobre a própria conta ou algo geral, em pt ou en.
2. **Subir.** Um comando (Docker), modo sem chave de LLM. Mostrar `GET /health`.
3. **Knowledge.** Pergunta de comparação de maquininhas: resposta com citação da página oficial; mostrar o
   diagrama RAG em [ARCHITECTURE.md](ARCHITECTURE.md).
4. **Customer Support.** Depósitos de ontem: os totais vêm de `get_deposit_schedule`, calculados no código.
5. **Troubleshoot.** Maquininha sem internet: `get_terminal_status` acha o terminal offline e o `needs` puxa o
   manual pelo supervisor.
6. **General.** Clima e câmbio por tool, nunca escala.
7. **Humano.** Pedido explícito de atendente: caso aberto, operador responde em `/operator`, o plano retoma.
8. **Guardrails.** Pedido inseguro bloqueado, sem abrir caso.
9. **Observabilidade.** `trace_id` no log, `/metrics`, um alerta e o seu bloco no [RUNBOOK](RUNBOOK.md).
10. **Fecho.** Os resultados medidos no README e os limites declarados; ADRs em `docs/adr/`.
