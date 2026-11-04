"""Frente Q: oficial pela API HTTP nos dois AUTH_MODE; token ruim = 401."""
from fastapi.testclient import TestClient

from app.api import app
from app.auth import issue_token

client = TestClient(app)
MSG = {"message": "When will the money from yesterday's sales be deposited?", "user_id": "cliente1988"}


def test_required_with_token_answers():
    r = client.post("/chat", json=MSG, headers={"Authorization": f"Bearer {issue_token('cliente1988')}"})
    assert r.status_code == 200 and r.json()["answer"]


def test_required_bad_token_is_401():
    assert client.post("/chat", json=MSG, headers={"Authorization": "Bearer cliente1988.ruim"}).status_code == 401


def test_demo_answers(monkeypatch):
    monkeypatch.setenv("AUTH_MODE", "demo")
    r = client.post("/chat", json=MSG)
    assert r.status_code == 200 and r.json()["answer"]
