"""Domínio do desafio — FLUXO: taxonomia, planos, FALLBACK, regras do router.

Contrato lido pelo motor: PLANS, FALLBACK, ALLOWED, DEPENDS, NO_ESCALATION, DEFAULT_INTENT,
MULTI_PARTS, states_subject(), clause_intent(), combine().
Teste: tests/test_domain_router.py.
"""
from __future__ import annotations

import re

# --- taxonomia e planos (lidos por router e supervisor) ---------------------------------------------------
# intent → plano inicial. "multi" = duas perguntas independentes no mesmo turno → rodam em paralelo.
PLANS = {
    "knowledge": ["faq"],
    "support": ["records"],
    "troubleshoot": ["records"],  # o manual (faq) vem do achado `needs`, decidido pelo supervisor
    "general": ["faq"],  # o motor despacha o agente geral pela intent
    "multi": ["faq", "records"],
    "human_request": ["escalation"],
}
FALLBACK = {"faq": "escalation", "records": "escalation"}
ALLOWED = {None: {"faq", "records", "escalation"}, "faq": {"records", "escalation"},
           "records": {"faq", "escalation"}, "escalation": set()}
DEPENDS: dict[str, set[str]] = {"faq": {"records"}}
NO_ESCALATION: set[str] = {"general"}
OWN_COMPANY: str | None = r"\bgetnet\b"
OWN_COMPANY_INTENT = "knowledge"
DEFAULT_INTENT = "knowledge"
MULTI_PARTS = {"knowledge", "support"}

# --- regras do router offline -------------------------------------------------------------------------------
_HUMAN = re.compile(r"\b(atendente|humano|pessoa real|falar com algu[eé]m|human|representative|real person"
                    r"|operador|operator)\b", re.IGNORECASE)
_TROUBLE = re.compile(r"(n[aã]o conect|won'?t (connect|go online)|sem (sinal|conex)|no (signal|connection)"
                      r"|offline|lost (its )?internet|recusad|declin|parou de passar|erro de transa)", re.IGNORECASE)
_SUPPORT = re.compile(r"\b(dep[oó]sit\w*|deposited|minhas vendas|my sales|vendas de ontem|yesterday'?s sales"
                      r"|(?:meus|my) receb[ií]ve\w*|(?:meus|my) receivables?"
                      r"|antecip\w* r\$|advance r\$|ticket|chamado|terminal\w*"
                      r"|T\d{4}[A-Z]|c[oó]digo \d+|code \d+|cai o dinheiro)\b", re.IGNORECASE)
_GENERAL = re.compile(r"\b(weather|clima|tempo amanh|previs[aã]o do tempo|forecast|exchange rate|c[aâ]mbio"
                      r"|cota[cç][aã]o|d[oó]lar|euro|not[ií]cia|news|receita|recipe)\b", re.IGNORECASE)
_PRODUCT = re.compile(r"\b(get\s*\w+|pix|credi[aá]rio|link de pagamento|payment link|antecipa\w*|parcelas?|aluguel"
                      r"|installments?|get conta|maquininhas?)\b", re.IGNORECASE)
_OWN = re.compile(r"\bgetnet\b", re.IGNORECASE)
_STATE_FOLLOWUP = re.compile(r"\b(outr[oa]|other|how long|h[aá] quanto tempo|valor|code|c[oó]digo|modelo|model"
                             r"|credit|cr[eé]dito|pix|online|offline|down)\b", re.IGNORECASE)
_FOLLOWUP = re.compile(r"\b(ele|ela|isso|esse|essa|it|that|this one|outr[oa]|other|second one)\b", re.IGNORECASE)


def states_subject(text: str) -> bool:
    """A fala define assunto por REGRA (sem olhar vocabulário)? Usado para achar o assunto da conversa."""
    return bool(_HUMAN.search(text) or _TROUBLE.search(text) or _SUPPORT.search(text) or _GENERAL.search(text))


def clause_intent(text: str, history: list[dict], r) -> str | None:
    """Intenção de UMA cláusula, com os desempates da SPEC. `r` = módulo app.router."""
    if _HUMAN.search(text):  # (1) pedido explícito de humano vence tudo
        return "human_request"
    if _TROUBLE.search(text):  # (3) problema com maquininha/transação
        return "troubleshoot"
    if _SUPPORT.search(text):  # (3) dado da própria conta
        return "support"
    if _GENERAL.search(text) and not _OWN.search(text):  # (6) e (2)
        return "general"
    last = r.topic_intent(history)
    if last in ("support", "troubleshoot", "multi") and _STATE_FOLLOWUP.search(text):  # (5)
        return "support"
    if last == "knowledge" and _FOLLOWUP.search(text):
        return "knowledge"
    if (near := r.knn_intent(text)) is not None:
        if near == "general" and _OWN.search(text):
            return "knowledge"
        return near
    if _OWN.search(text) or _PRODUCT.search(text):
        return "knowledge"
    return DEFAULT_INTENT if r.has_subject(text) else None


def combine(intents: set[str]) -> tuple[str, float]:
    """Intenções das cláusulas → (intent da mensagem, confiança)."""
    if "human_request" in intents:
        return "human_request", 0.95
    if "troubleshoot" in intents and "knowledge" not in intents:
        return "troubleshoot", 0.85
    parts = {"support" if i == "troubleshoot" else i for i in intents}
    if MULTI_PARTS <= parts:
        return "multi", 0.8
    if "support" in intents:
        return "support", 0.85
    intent = min(intents - {DEFAULT_INTENT} or {DEFAULT_INTENT})
    return intent, 0.7
