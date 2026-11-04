# Arquitetura

Descreve só o que o código faz. Cada caixa traz o arquivo. O domínio (`src/app/domain/challenge/`) segue a
[SPEC](SPEC.md): taxonomia de intents e tools com nomes congelados.

## 1. Agentes

```mermaid
flowchart TD
  C["Cliente: POST /chat<br/>src/app/api.py"] --> P["pipeline.handle<br/>src/app/pipeline.py"]
  P --> G["Guardrails (inseguro, sensível, fora de escopo)<br/>src/app/guardrails.py"]
  G -- "blocked" --> R0["Resposta de recusa<br/>src/app/pipeline.py"]
  G -- "ok" --> RT["Router: intent, plano, standalone<br/>src/app/router.py + src/app/domain/challenge/flow.py"]
  RT --> S["Supervisor: executa o plano, aceita needs, replaneja, orçamento<br/>src/app/supervisor.py"]
  S --> K["Knowledge (faq_agent, RAG)<br/>src/app/agents.py + src/app/rag.py"]
  S --> CS["Customer Support (records_agent)<br/>src/app/agents.py + src/app/domain/challenge/tools.py"]
  S --> GE["General (weather_forecast, currency_rate, web_search)<br/>src/app/agents.py + src/app/live_data.py"]
  S --> H["Human Escalation (escalation_agent)<br/>src/app/agents.py + src/app/cases.py"]
  CS -- "needs → faq" --> S
  K --> CH["Checagem: grounding, claims, idioma<br/>src/app/grounding.py + src/app/claims.py + src/app/pipeline.py"]
  CS --> CH
  GE --> CH
  H --> CH
  CH --> OUT["ChatResponse<br/>src/app/schemas.py"]
```

- O Router é o único leitor do histórico; os especialistas recebem a pergunta reescrita (`standalone`)
  ([ADR 0007](adr/0007-especialistas-sem-estado.md)).
- O Supervisor roda em todo turno ([ADR 0005](adr/0005-supervisor-em-todo-turno.md)) com teto de chamadas, custo e
  tempo por nó (`max_model_calls`, `max_turn_usd`, `node_timeout_s` em `src/app/supervisor.py`).
- `general` nunca escala (`no_escalation` em `src/app/supervisor.py`).
- Escritas (`open_support_ticket`, `request_receivables_advance`) passam por confirmação e aprovação em
  `src/app/actions.py` (`/actions/{id}/confirm|approve|reject` em `src/app/api.py`).

Taxonomia (SPEC): `knowledge` → `["faq"]`; `support` → `["records"]`; `troubleshoot` → `["records"]` + `needs` → faq;
`general` → `["general"]`; `multi` → `["faq","records"]`; `human_request` → `["escalation"]`; `blocked` → guardrail.

## 2. RAG

```mermaid
flowchart LR
  SRC["Fontes permitidas<br/>data/sources.json"] --> ING["Ingestão: extração HTML, tabelas, chunking<br/>src/app/ingest.py"]
  ING --> KB["Corpus em disco<br/>data/knowledge/"]
  KB --> IDX["Índice: load_docs, dedupe, vetores (cache)<br/>src/app/rag.py"]
  Q["Pergunta + standalone + glossário<br/>src/app/agents.py (plan_queries, expand_query)"] --> RET["Busca: denso + cross-encoder (híbrido opcional)<br/>src/app/rag.py (get_retriever)"]
  IDX --> RET
  RET --> GATE["Portão de cobertura: ok / partial / insufficient<br/>src/app/agents.py (covered_hits, coverage_of)"]
  GATE --> GEN["Geração com citação<br/>src/app/agents.py (_faq_write) + src/app/llm.py"]
  GEN --> GR["Verificação na fonte<br/>src/app/grounding.py + src/app/claims.py"]
```

Escolha do buscador: [ADR 0004](adr/0004-buscador-denso-com-teto-de-ram.md); o que foi medido e ficou de fora:
[ADR 0008](adr/0008-considerado-e-nao-feito.md).

## 3. HITL (humano no laço)

```mermaid
sequenceDiagram
  participant Cl as Cliente (src/app/api.py /chat)
  participant Sp as Supervisor (src/app/supervisor.py)
  participant Es as Human Escalation (src/app/agents.py)
  participant Cs as Caso / fila (src/app/cases.py, src/app/store.py)
  participant No as Aviso (src/app/notify.py)
  participant Op as Operador (/operator, /handoffs em src/app/api.py)
  participant Hs as Espera curta (src/app/hitl_sync.py)
  participant Re as Retomada (src/app/resume.py)
  Cl->>Sp: pergunta não resolvida / pedido de humano
  Sp->>Es: plano ["escalation"]
  Es->>Cs: abre caso com resumo
  Cs->>No: avisa operador
  Sp->>Hs: espera a resposta dentro do turno
  Op->>Cs: POST /handoffs/{id}/reply
  alt respondeu a tempo
    Hs-->>Sp: resposta do operador
  else expirou
    Sp-->>Cl: caso aberto, resposta virá depois
  end
  Re->>Sp: retoma o plano após o humano (resume_table)
  Sp-->>Cl: resposta final
```

Quando escalar: só quando não resolve ([ADR 0006](adr/0006-humano-so-quando-nao-resolve.md)). SLA dos casos:
`POST /handoffs/sla-check` em `src/app/api.py`.
