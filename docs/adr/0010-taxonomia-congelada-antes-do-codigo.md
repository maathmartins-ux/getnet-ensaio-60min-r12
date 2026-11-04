# ADR 0010 — Taxonomia de intents e nomes de tools congelados antes do código

Status: aceito.

**Contexto.** Cinco frentes escrevem o domínio em paralelo (`OWNERSHIP.json`). Router, tools, casos e docs precisam
do mesmo vocabulário.

**Decisão.** A taxonomia (`knowledge`, `support`, `troubleshoot`, `general`, `multi`, `human_request`, `blocked`) e os
nomes das tools (`get_deposit_schedule`, `list_transactions`, `get_terminal_status`, `open_support_ticket`,
`request_receivables_advance`) ficam em `docs/SPEC.md`, congelada. O manual do `troubleshoot` vem do achado `needs`
decidido pelo supervisor (`src/app/supervisor.py`), não de um plano fixo de dois passos.

**Alternativa descartada.** Deixar cada frente nomear e alinhar no merge. Motivo: o desalinhamento só aparece na
integração, quando não há tempo para corrigir.

**Consequência.** Mudar uma intent ou tool exige mudar a SPEC na sessão principal.
