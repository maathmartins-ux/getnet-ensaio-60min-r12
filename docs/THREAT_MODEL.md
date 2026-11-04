# Modelo de ameaças (frente Q)

Escopo: `/chat`, `/mcp`, `/metrics`, CRM (cliente1988, cliente2077), RAG, tools web.

| Ameaça (STRIDE / OWASP LLM 2025 / ASI) | Controle | Arquivo | Teste |
|---|---|---|---|
| S: identidade forjada / token ruim (ASI03) | AUTH_MODE required (JWT); produção recusa AUTH_MODE=demo | src/app/auth.py, src/app/config.py | tests/test_domain_http.py |
| T: injeção direta e indireta (LLM01, ASI01, ASI06) | guardrail antes do router; fonte tratada como dado | src/app/guardrails.py | tests/test_domain_guardrails.py, split guardrail |
| R: ação sem trilha (ASI02, ASI08) | risco alto aprovado só com chave pessoal de OPERATOR_KEYS | src/app/actions.py | split approval |
| I: dado de outro cliente / PII (LLM02, ASI03, ASI07) | escopo por dono no CRM ("não encontrado"); máscara de CPF/cartão | src/app/tools.py, src/app/guardrails.py | casos q-guard ASI03/ASI07 |
| D: abuso e custo (LLM10, ASI10) | limite por IP/usuário, teto de US$ | src/app/api.py | tests/test_auth_modes.py |
| E: tool fora do papel via /mcp (LLM06, ASI02, ASI05) | /mcp com mesma auth e lista fechada de tools | src/app/mcp_server.py | tests/test_mcp.py |
| I: /metrics exposto | Bearer exigido em produção | src/app/observability.py | tests/test_production_ops.py |
| Lavagem de dinheiro / fraude (ASI09) | intent blocked | src/app/guardrails.py | casos q-guard ASI09 |
| Desinformação, fonte velha (LLM09) | juiz com stale_source | evals/judge.py | evals/judge_calibration.d/q.jsonl |
| Cadeia de suprimento (LLM03, ASI04) | versões fixadas | requirements | tests/test_supply_chain.py |
