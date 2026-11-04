"""Router do domínio do desafio: intent offline dos casos official e standalone dos casos memory."""
import json
from pathlib import Path

import pytest

from app import domain, router

_LINES = Path("evals/cases.jsonl").read_text(encoding="utf-8").splitlines()
CASES = [json.loads(line) for line in _LINES if line.strip()]
OFFICIAL = [c for c in CASES if c["split"] == "official"]
MEMORY = [c for c in CASES if c["split"] == "memory"]

pytestmark = pytest.mark.usefixtures("domain_data")


def test_contract_constants():
    d = domain.active()
    assert d.DEPENDS == {"faq": {"records"}}
    assert d.NO_ESCALATION == {"general"}
    assert d.OWN_COMPANY == r"\bgetnet\b"
    assert d.PLANS["troubleshoot"] == ["records"]


@pytest.mark.parametrize("case", OFFICIAL, ids=lambda c: c["id"])
def test_official_intent_offline(case):
    got = router.classify_offline(case["message"], []).intent
    if case["expect"]["intent"] != got:
        pytest.xfail(f"offline erra; LLM decide: {got}")  # medido no eval; o gate é a taxa, não cada caso


def test_official_rate_at_least_90():
    ok = sum(router.classify_offline(c["message"], []).intent == c["expect"]["intent"] for c in OFFICIAL)
    assert ok / len(OFFICIAL) >= 0.9


@pytest.mark.parametrize("case", [c for c in MEMORY if c["expect"].get("standalone")], ids=lambda c: c["id"])
def test_memory_cases_declare_standalone(case):
    assert isinstance(case["expect"]["standalone"], (str, list))


def test_own_company_never_general():
    assert router.classify_offline("A Getnet divulga a cotação das ações dela?", []).intent != "general"


def test_human_wins_everything():
    msg = "Minha maquininha está offline, quero falar com um atendente"
    assert router.classify_offline(msg, []).intent == "human_request"
