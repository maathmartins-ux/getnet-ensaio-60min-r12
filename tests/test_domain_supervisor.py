"""Supervisor do domínio: replan (needs), dependent (DEPENDS) e partial (vira resposta)."""
from pathlib import Path

import pytest

from app import domain

PROMPT = Path("src/app/domain/challenge_prompts/supervisor.md").read_text(encoding="utf-8")

pytestmark = pytest.mark.usefixtures("domain_data")


def test_dependent_faq_waits_for_records():
    assert domain.active().DEPENDS["faq"] == {"records"}


def test_replan_needs_rule_in_prompt():
    assert "se o resultado pedir outro especialista (`needs`), chame-o" in PROMPT


def test_partial_is_answer_not_human():
    assert "nunca chame escalation_agent por um partial" in PROMPT


def test_troubleshoot_starts_with_records_only():
    d = domain.active()
    assert d.PLANS["troubleshoot"] == ["records"]
    assert "records" in d.ALLOWED and "faq" in d.ALLOWED["records"]
