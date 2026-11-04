"""Domínio Getnet — FERRAMENTAS do Customer Support: registro TOOLS e caminho offline do records.

Contrato lido pelo motor: TOOLS, ELIGIBLE_STATUS, LABELS, records(), needs_for(), records_offline().
A identidade (`user_id`) vem sempre do servidor, nunca do schema. Registro de outro cliente = "não encontrado".
Totais, datas de depósito e significado de código de recusa são calculados aqui (o LLM não soma).
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, timedelta
from functools import lru_cache

from app import clock
from app.config import data_dir

PERIODS = ["yesterday", "today", "last_7_days"]
DEFAULT_PERIOD = "last_7_days"
REASONS = ["sem_conexao", "sem_sinal", "erro_transacao"]

DECLINE_CODES = {
    "51": {"pt": "saldo insuficiente", "en": "insufficient funds"},
    "05": {"pt": "não autorizada pelo emissor", "en": "not authorized by the issuer"},
}
METHODS = {"pix": "Pix", "debit": "débito", "credit": "crédito"}

LABELS = {
    "sem_conexao": {"pt": "sem conexão", "en": "no connection"},
    "sem_sinal": {"pt": "sem sinal", "en": "no signal"},
    "erro_transacao": {"pt": "erro de transação", "en": "transaction error"},
    "last_7_days": {"pt": "últimos 7 dias", "en": "last 7 days"},
    "yesterday": {"pt": "ontem", "en": "yesterday"},
    "today": {"pt": "hoje", "en": "today"},
    "reason": {"pt": "motivo", "en": "reason"},
    "period": {"pt": "período", "en": "period"},
    "status": {"pt": "situação", "en": "status"},
    "approved": {"pt": "aprovadas", "en": "approved"},
    "declined": {"pt": "recusadas", "en": "declined"},
    "all": {"pt": "todas", "en": "all"},
    "amount": {"pt": "valor", "en": "amount"},
    "terminal_id": {"pt": "maquininha", "en": "card machine"},
    "pix": {"pt": "Pix", "en": "Pix"},
    "debit": {"pt": "débito", "en": "debit"},
    "credit": {"pt": "crédito", "en": "credit"},
    "wifi": {"pt": "Wi-Fi", "en": "Wi-Fi"},
    "chip": {"pt": "chip", "en": "SIM chip"},
    "ok": {"pt": "ok", "en": "ok"},
    "get_deposit_schedule": {"pt": "agenda de depósitos", "en": "deposit schedule"},
    "list_transactions": {"pt": "consulta de vendas", "en": "transaction list"},
    "get_terminal_status": {"pt": "situação da maquininha", "en": "card machine status"},
    "request_receivables_advance": {"pt": "antecipação dos recebíveis", "en": "receivables advance"},
    "open_support_ticket": {"pt": "chamado técnico", "en": "support ticket"},
}

TERMINAL_NEED = {"agent": "faq", "why": "maquininha offline: o passo a passo vem do manual de conexão",
                 "hint": "maquininha não conecta wi-fi chip sinal manual de conexão"}
DECLINE_NEED = {"agent": "faq", "why": "venda recusada: o que fazer vem da central de ajuda",
                "hint": "transação recusada código de recusa"}


# --- adaptador do CRM ------------------------------------------------------------------------------------
@lru_cache(maxsize=4)
def _load(path: str) -> dict:
    return json.loads(open(path, encoding="utf-8").read())


def records() -> dict:
    """Adaptador do sistema de registro: hoje data/crm/crm.json; em produção, a API do CRM (mesma assinatura)."""
    return _load(str(data_dir() / "crm" / "crm.json"))


def _customer(user_id: str) -> dict:
    return records()["customers"].get(user_id) or {"terminals": [], "transactions": []}


def _next_business_day(d: date) -> date:
    d += timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def deposit_date(method: str, sale: date) -> date:
    if method == "pix":
        return sale
    if method == "debit":
        return _next_business_day(sale)
    return sale + timedelta(days=30)


def _money(v: float) -> float:
    return round(v + 0.0, 2)


def _brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _period_range(period: str) -> tuple[date, date]:
    today = clock.today()
    if period == "today":
        return today, today
    if period == "yesterday":
        y = today - timedelta(days=1)
        return y, y
    return today - timedelta(days=6), today


def _transactions(user_id: str, period: str) -> list[dict]:
    start, end = _period_range(period)
    today = clock.today()
    out = []
    for tx in _customer(user_id)["transactions"]:
        d = today + timedelta(days=tx["day_offset"])
        if start <= d <= end:
            row = {k: v for k, v in tx.items() if k != "day_offset"}
            row["date"] = d.isoformat()
            if tx["status"] == "declined" and tx.get("decline_code"):
                meaning = DECLINE_CODES.get(tx["decline_code"], {"pt": "código desconhecido", "en": "unknown code"})
                row["decline_meaning"] = meaning["pt"]
                row["decline_meaning_en"] = meaning["en"]
            out.append(row)
    return sorted(out, key=lambda r: (r["date"], r["time"]))


# --- tools -----------------------------------------------------------------------------------------------
def _deposit_schedule(user_id: str, period: str = DEFAULT_PERIOD) -> dict:
    if period not in PERIODS:
        return {"ok": False, "error": "invalid_period"}
    approved = [t for t in _transactions(user_id, period) if t["status"] == "approved"]
    by_method: dict[str, dict] = {}
    by_date: dict[str, float] = {}
    for t in approved:
        dep = deposit_date(t["method"], date.fromisoformat(t["date"])).isoformat()
        m = by_method.setdefault(t["method"], {"method": t["method"], "count": 0, "total": 0.0,
                                               "transactions": [], "deposit_dates": []})
        m["count"] += 1
        m["total"] = _money(m["total"] + t["amount"])
        m["transactions"].append(t["transaction_id"])
        if dep not in m["deposit_dates"]:
            m["deposit_dates"].append(dep)
        by_date[dep] = _money(by_date.get(dep, 0.0) + t["amount"])
    rule = {"pix": "D+0", "debit": "D+1 útil", "credit": "D+30"}
    for m in by_method.values():
        m["rule"] = rule[m["method"]]
    return {"ok": True, "data": {
        "period": period, "today": clock.today().isoformat(),
        "by_method": list(by_method.values()),
        "by_deposit_date": [{"deposit_date": d, "total": v} for d, v in sorted(by_date.items())],
        "count": len(approved), "total": _money(sum(t["amount"] for t in approved)),
    }}


def _list_transactions(user_id: str, status: str = "all", period: str = DEFAULT_PERIOD) -> dict:
    if period not in PERIODS or status not in ("approved", "declined", "all"):
        return {"ok": False, "error": "invalid_argument"}
    rows = [t for t in _transactions(user_id, period) if status == "all" or t["status"] == status]
    declined = [t for t in rows if t["status"] == "declined"]
    approved = [t for t in rows if t["status"] == "approved"]
    data = {"period": period, "status": status, "today": clock.today().isoformat(), "transactions": rows,
            "count": len(rows), "approved_count": len(approved),
            "approved_total": _money(sum(t["amount"] for t in approved)),
            "declined_count": len(declined), "declined_total": _money(sum(t["amount"] for t in declined))}
    result = {"ok": True, "data": data}
    if declined:
        result["needs"] = [dict(DECLINE_NEED)]
    return result


def _terminal_status(user_id: str, terminal_id: str | None = None) -> dict:
    terms = _customer(user_id)["terminals"]
    if terminal_id:
        terms = [t for t in terms if t["terminal_id"] == terminal_id]
        if not terms:
            return {"ok": False, "error": "not_found"}
    out = []
    for t in terms:
        row = {k: v for k, v in t.items() if k != "last_contact_minutes_ago"}
        last = clock.now() - timedelta(minutes=t["last_contact_minutes_ago"])
        row["last_contact"] = last.isoformat(timespec="minutes")
        if not t["online"]:
            row["offline_for_hours"] = round(t["last_contact_minutes_ago"] / 60, 1)
        out.append(row)
    result = {"ok": True, "data": {"terminals": out, "count": len(out),
                                   "offline_count": sum(1 for t in out if not t["online"])}}
    if any(not t["online"] for t in out):
        result["needs"] = [dict(TERMINAL_NEED)]
    return result


def _open_ticket(user_id: str, terminal_id: str, reason: str) -> dict:
    if reason not in REASONS:
        return {"ok": False, "error": "invalid_reason"}
    found = _terminal_status(user_id, terminal_id)
    if not found["ok"]:
        return found
    key = f"{user_id}|{terminal_id}|{reason}|{clock.today().isoformat()}".encode()
    proto = "CH" + str(int(hashlib.sha256(key).hexdigest(), 16) % 10**8).zfill(8)
    before = found["data"]["terminals"][0]
    return {"ok": True, "data": {"protocol": proto, "terminal_id": terminal_id, "reason": reason,
                                 "status": "aberto", "before": before, "after": {**before, "ticket": proto}}}


def _advance(user_id: str, amount: float) -> dict:
    if not isinstance(amount, (int, float)) or amount <= 0:
        return {"ok": False, "error": "invalid_amount"}
    return {"ok": True, "data": {"amount": _money(float(amount)), "status": "pendente_aprovacao",
                                 "requested_on": clock.today().isoformat()}}


_PERIOD = {"type": "string", "enum": PERIODS, "default": DEFAULT_PERIOD,
           "description": "Período (padrão: últimos 7 dias)"}
_TERMINAL = {"type": "string", "pattern": r"^[A-Za-z0-9]{2,16}$", "description": "Id da maquininha (ex.: T1988B)"}
TOOLS = {
    "get_deposit_schedule": {
        "description": "Vendas aprovadas por modalidade e quando cada valor cai (Pix D+0, débito D+1 útil, "
                       "crédito D+30), com totais calculados.", "write": False,
        "input_schema": {"type": "object", "properties": {"period": _PERIOD}, "additionalProperties": False},
        "fn": _deposit_schedule},
    "list_transactions": {
        "description": "Transações do cliente com código de recusa e o significado dele.", "write": False,
        "input_schema": {"type": "object", "properties": {
            "status": {"type": "string", "enum": ["approved", "declined", "all"], "default": "all"},
            "period": _PERIOD}, "additionalProperties": False},
        "fn": _list_transactions},
    "get_terminal_status": {
        "description": "Situação das maquininhas do cliente (modelo, conexão, online; há quanto tempo offline).",
        "write": False,
        "input_schema": {"type": "object", "properties": {"terminal_id": _TERMINAL}, "additionalProperties": False},
        "fn": _terminal_status},
    "open_support_ticket": {
        "description": "Abre chamado técnico para uma maquininha. Exige confirmação do cliente.", "write": True,
        "input_schema": {"type": "object", "properties": {
            "terminal_id": _TERMINAL, "reason": {"type": "string", "enum": REASONS}},
            "required": ["terminal_id", "reason"], "additionalProperties": False},
        "fn": _open_ticket},
    # risco alto: move dinheiro → confirmação do dono E aprovação de um operador com chave pessoal
    "request_receivables_advance": {
        "description": "Pede antecipação de recebíveis. Exige confirmação do cliente e aprovação de um atendente.",
        "write": True, "risk": "high",
        "input_schema": {"type": "object", "properties": {
            "amount": {"type": "number", "exclusiveMinimum": 0, "description": "Valor em reais"}},
            "required": ["amount"], "additionalProperties": False},
        "fn": _advance},
}
# Chamado técnico só faz sentido para maquininha offline.
ELIGIBLE_STATUS: dict[str, set[str]] = {}


# --- achados (needs) ---------------------------------------------------------------------------------------
_SYMPTOM = re.compile(r"(conect|internet|wi-?fi|sinal|signal|offline|chip|connect|recus|declin|erro|error)",
                      re.IGNORECASE)


def needs_for(result, ctx) -> list[dict]:
    """Junta o `needs` de TODOS os resultados de tool do records (terminal E transação)."""
    if result.agent != "records":
        return []
    out: list[dict] = []
    for item in result.evidence:
        try:
            data = json.loads(item)
        except ValueError:
            continue
        if not isinstance(data, dict):
            continue
        for need in data.get("needs") or []:
            if need not in out:
                out.append(dict(need))
    return out if _SYMPTOM.search(ctx.text or "") else []


# --- caminho offline do agente records (sem LLM / provedor fora) -------------------------------------------
_TERM_ID = re.compile(r"\b(T\d{4}[A-Z])\b", re.IGNORECASE)
_TX_ID = re.compile(r"\b(TX\d{4})\b", re.IGNORECASE)
_AMOUNT = re.compile(r"R\$\s*([\d.]+(?:,\d{1,2})?)|\b(\d+(?:[.,]\d{1,2})?)\s*(?:reais|BRL)", re.IGNORECASE)
_ADVANCE = re.compile(r"(antecip|advance)", re.IGNORECASE)
_TICKET = re.compile(r"(chamado|ticket|suporte t[eé]cnico)", re.IGNORECASE)
_TERMINAL_Q = re.compile(r"(maquininha|terminal|card machine|conect|internet|wi-?fi|sinal|signal|offline|online)",
                         re.IGNORECASE)
_DECLINE_Q = re.compile(r"(recus|declin|negad|c[oó]digo|code)", re.IGNORECASE)
_DEPOSIT_Q = re.compile(r"(dep[oó]sit|cai|caem|receb|money|dinheiro|payout)", re.IGNORECASE)
_TX_Q = re.compile(r"(venda|vendas|transa[cç]|sales|sale|transaction)", re.IGNORECASE)


def _period_of(text: str) -> str:
    if re.search(r"\b(ontem|yesterday)\b", text, re.IGNORECASE):
        return "yesterday"
    if re.search(r"\b(hoje|today)\b", text, re.IGNORECASE):
        return "today"
    return DEFAULT_PERIOD


def _amount_of(text: str) -> float | None:
    m = _AMOUNT.search(text)
    if not m:
        return None
    raw = m.group(1) or m.group(2)
    raw = raw.replace(".", "").replace(",", ".") if "," in raw else raw
    try:
        return float(raw)
    except ValueError:
        return None


def _lbl(ctx, value: str) -> str:
    entry = LABELS.get(value)
    if not entry:
        return value.replace("_", " ")
    return entry["en"] if getattr(ctx, "language", "pt") == "en" else entry["pt"]


def records_offline(ctx, a):
    """Atendimento determinístico do agente records. `a` = módulo app.agents (AgentResult, run_tool, _t...)."""
    AgentResult, run_tool, t = a.AgentResult, a.run_tool, a._t
    text = ctx.text or ""
    calls: list = []
    ev: list[str] = []

    def call(name, args):
        res, c = run_tool(name, args, ctx.user_id, ctx.conversation_id)
        calls.append(c)
        ev.append(json.dumps(res, ensure_ascii=False))
        return res

    def pending(res, what_pt, what_en):
        aid = res["action_id"]
        extra_pt = " Depois da sua confirmação, um atendente aprova." if res.get("risk") == "high" else ""
        extra_en = " After you confirm, a human agent approves it." if res.get("risk") == "high" else ""
        return AgentResult("records", "ok", tool_calls=calls, pending_action=aid, evidence=ev,
                           text=t(ctx, f"Proposta de {what_pt}: confirme a ação {aid}.{extra_pt} Nada foi feito ainda.",
                                  f"Proposed {what_en}: confirm action {aid}.{extra_en} Nothing has been done yet."))

    if _ADVANCE.search(text):
        amount = _amount_of(text)
        if amount is None:
            return AgentResult("records", "ok", text=t(ctx, "Qual valor você quer antecipar?",
                                                       "How much would you like to advance?"))
        res = call("request_receivables_advance", {"amount": amount})
        if res.get("needs_confirmation"):
            return pending(res, f"antecipação dos recebíveis de {_brl(amount)}",
                           f"receivables advance of {_brl(amount)}")
        if not res.get("ok"):
            return AgentResult("records", "error", tool_calls=calls, reason="tool_error", evidence=ev)

    term = _TERM_ID.search(text)
    if _TICKET.search(text):
        if not term:
            return AgentResult("records", "ok", text=t(ctx, "Para qual maquininha devo abrir o chamado?",
                                                       "Which card machine should the ticket be for?"))
        tid = term.group(1).upper()
        st = call("get_terminal_status", {"terminal_id": tid})
        if st.get("error") == "not_found":
            return AgentResult("records", "ok", tool_calls=calls, evidence=ev, facts={"record_not_found": tid},
                               text=t(ctx, f"Não encontrei a maquininha {tid} na sua conta.",
                                      f"I couldn't find card machine {tid} in your account."))
        reason = "erro_transacao" if _DECLINE_Q.search(text) else (
            "sem_sinal" if st.get("ok") and st["data"]["terminals"][0].get("signal") == "sem_sinal" else "sem_conexao")
        res = call("open_support_ticket", {"terminal_id": tid, "reason": reason})
        if res.get("needs_confirmation"):
            return pending(res, f"chamado técnico para a maquininha {tid} ({_lbl(ctx, reason)})",
                           f"support ticket for card machine {tid} ({LABELS[reason]['en']})")
        if not res.get("ok"):
            return AgentResult("records", "error", tool_calls=calls, reason="tool_error", evidence=ev)

    parts_pt: list[str] = []
    parts_en: list[str] = []
    facts: dict = {}
    if _DECLINE_Q.search(text) or _TX_ID.search(text):
        res = call("list_transactions", {"status": "declined", "period": DEFAULT_PERIOD})
        if res.get("ok"):
            rows = res["data"]["transactions"]
            txid = _TX_ID.search(text)
            if txid:
                rows = [r for r in rows if r["transaction_id"] == txid.group(1).upper()]
            if not rows:
                parts_pt.append("Não encontrei vendas recusadas nos últimos 7 dias.")
                parts_en.append("I found no declined sales in the last 7 days.")
            for r in rows:
                parts_pt.append(f"{r['transaction_id']} ({METHODS[r['method']]}, {_brl(r['amount'])}, {r['date']}): "
                                f"recusada com código {r['decline_code']} — {r['decline_meaning']}.")
                parts_en.append(f"{r['transaction_id']} ({LABELS[r['method']]['en']}, {_brl(r['amount'])}, "
                                f"{r['date']}): declined with code {r['decline_code']} — {r['decline_meaning_en']}.")
            facts["declined"] = [r["transaction_id"] for r in rows]
    elif _TERMINAL_Q.search(text) or term:
        args = {"terminal_id": term.group(1).upper()} if term else {}
        res = call("get_terminal_status", args)
        if res.get("error") == "not_found":
            tid = args["terminal_id"]
            return AgentResult("records", "ok", tool_calls=calls, evidence=ev, facts={"record_not_found": tid},
                               text=t(ctx, f"Não encontrei a maquininha {tid} na sua conta.",
                                      f"I couldn't find card machine {tid} in your account."))
        if res.get("ok"):
            for r in res["data"]["terminals"]:
                conn = _lbl(ctx, r["connection"])
                if r["online"]:
                    parts_pt.append(f"A maquininha {r['terminal_id']} ({r['model']}, {conn}) está online.")
                    parts_en.append(f"Card machine {r['terminal_id']} ({r['model']}, "
                                    f"{LABELS[r['connection']]['en']}) is online.")
                else:
                    sig_pt = f", {_lbl(ctx, r['signal'])}" if r.get("signal") in LABELS else ""
                    sig_en = f", {LABELS[r['signal']]['en']}" if r.get("signal") in LABELS else ""
                    parts_pt.append(f"A maquininha {r['terminal_id']} ({r['model']}, {conn}) está offline{sig_pt} "
                                    f"há cerca de {r['offline_for_hours']} h.")
                    parts_en.append(f"Card machine {r['terminal_id']} ({r['model']}, "
                                    f"{LABELS[r['connection']]['en']}) is offline{sig_en} for about "
                                    f"{r['offline_for_hours']} h.")
            facts["terminals"] = [r["terminal_id"] for r in res["data"]["terminals"]]
    elif _DEPOSIT_Q.search(text) or _TX_Q.search(text):
        period = _period_of(text)
        res = call("get_deposit_schedule", {"period": period})
        if res.get("ok"):
            d = res["data"]
            for m in d["by_method"]:
                dates = ", ".join(m["deposit_dates"])
                parts_pt.append(f"{METHODS[m['method']].capitalize()}: {_brl(m['total'])} ({m['count']} venda(s)), "
                                f"cai em {dates} ({m['rule']}).")
                parts_en.append(f"{LABELS[m['method']]['en'].capitalize()}: {_brl(m['total'])} ({m['count']} sale(s)), "
                                f"deposited on {dates} ({m['rule'].replace('útil', 'business day')}).")
            parts_pt.insert(0, f"Vendas aprovadas ({_lbl(ctx, period)}): total {_brl(d['total'])}.")
            parts_en.insert(0, f"Approved sales ({LABELS[period]['en']}): total {_brl(d['total'])}.")
            facts["total"] = d["total"]
    else:
        return AgentResult("records", "ok", text=t(ctx, "Posso consultar depósitos, vendas e maquininhas. O que você "
                                                        "quer ver?", "I can check deposits, sales and card machines. "
                                                                     "What would you like to see?"))
    if calls and not parts_pt:
        return AgentResult("records", "error", tool_calls=calls, reason="tool_error", evidence=ev)
    needs: list[dict] = []
    for item in ev:
        for need in (json.loads(item).get("needs") or []):
            if need not in needs:
                needs.append(dict(need))
    return AgentResult("records", "ok", tool_calls=calls, evidence=ev, facts=facts, needs=needs,
                       text=t(ctx, " ".join(parts_pt), " ".join(parts_en)))
