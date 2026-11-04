# Observabilidade

Tudo em `src/app/observability.py`, salvo indicação.

## Traço e log
- Cada turno ganha um `trace_id` (`new_trace_id`) que vai no log JSON (`JsonFormatter`) e na resposta.
- `span(name, **fields)` mede cada etapa (`turn`, `router`, `agent`, `llm`, ...) e alimenta o histograma
  `span_latency_ms`. OpenTelemetry é opcional (`configure_otel`, `otel_enabled`).
- Versão das instruções: `record_prompt` / `prompt_versions` ligam cada resposta ao hash do prompt usado;
  `POST /feedback` (`src/app/api.py`) liga o 👍/👎 ao turno.

## Custo
- `record_llm_usage` e `llm_cost` somam tokens e custo por chamada; `request_usage` / `request_model_calls` dão o
  total do turno, que o supervisor compara com o teto (`max_turn_usd`, `max_model_calls` em `src/app/supervisor.py`).

## Métricas (`GET /metrics`, formato Prometheus)
Contadores principais, com o arquivo que incrementa:

| métrica | arquivo |
|---|---|
| `chat_requests_total`, `guardrail_blocks_total`, `handoffs_total`, `case_escalated_total` | `src/app/pipeline.py` |
| `chat_outcomes_total`, `auth_failures_total`, `feedback_total`, `handoff_replies_total` | `src/app/api.py` |
| `budget_exhausted_total`, `hitl_answer_total`, `actions_on_hold_total` | `src/app/supervisor.py` |
| `escalation_offered_total`, `live_tool_calls_total` | `src/app/agents.py` |
| `guardrail_suspect_total`, `guardrail_llm_unavailable_total` | `src/app/guardrails.py` |
| `llm_errors_total`, `llm_hedged_total` | `src/app/llm.py` |
| `claims_unsupported_total` | `src/app/claims.py` |
| `approvals_requested_total`, `approvals_decided_total` | `src/app/actions.py` |
| `handoff_resumed_total` | `src/app/resume.py` |
| `hitl_sync_total` | `src/app/hitl_sync.py` |

## Saúde
`GET /health` e `GET /ready` (`src/app/api.py`). Painéis e regras: `ops/grafana/`, `ops/prometheus.yml`,
`ops/alerts.yml`; cada alerta tem bloco em [RUNBOOK.md](RUNBOOK.md). `GET /analytics` (`src/app/analytics.py`)
resume os desfechos.

Os números medidos (latência, custo por turno) só aparecem nos blocos gerados por `scripts/fill_readme.py`.
