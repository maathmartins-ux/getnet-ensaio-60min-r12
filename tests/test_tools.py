from app.domain.challenge import tools as T


def test_schemas_closed_and_identity_not_in_schema(domain_data):
    for spec in T.TOOLS.values():
        sch = spec["input_schema"]
        assert sch["additionalProperties"] is False
        assert "user_id" not in sch["properties"]
        p = sch["properties"].get("period")
        if p:
            assert p["enum"] == ["yesterday", "today", "last_7_days"] and p["default"] == "last_7_days"
    assert T.TOOLS["open_support_ticket"]["write"] and T.TOOLS["request_receivables_advance"]["risk"] == "high"
    assert not any(k in T.TOOLS for k in ("lookup_record", "cancel_record", "refund_record"))


def test_deposit_yesterday_totals_in_code(domain_data):
    d = T._deposit_schedule("cliente1988", "yesterday")["data"]
    totals = {m["method"]: m["total"] for m in d["by_method"]}
    assert totals == {"debit": 205.5, "credit": 480.0, "pix": 60.0}
    assert d["total"] == 745.5


def test_declines_with_meaning(domain_data):
    rows = T._list_transactions("cliente1988", "declined", "today")["data"]["transactions"]
    assert {(r["decline_code"], r["decline_meaning"]) for r in rows} == {
        ("51", "saldo insuficiente"), ("05", "não autorizada pelo emissor")}


def test_terminal_offline_hours_only_when_offline_and_needs(domain_data):
    res = T._terminal_status("cliente1988")
    by = {t["terminal_id"]: t for t in res["data"]["terminals"]}
    assert "offline_for_hours" not in by["T1988A"] and by["T1988B"]["offline_for_hours"] > 3
    assert res["needs"][0]["agent"] == "faq"


def test_other_owner_is_not_found(domain_data):
    assert T._terminal_status("cliente1988", "T2077A") == {"ok": False, "error": "not_found"}
    assert T._terminal_status("cliente1988", "T9999Z") == {"ok": False, "error": "not_found"}


def test_labels_cover_closed_values(domain_data):
    for v in T.PERIODS + T.REASONS + ["reason", "period", "request_receivables_advance", "open_support_ticket"]:
        assert set(T.LABELS[v]) == {"pt", "en"}
