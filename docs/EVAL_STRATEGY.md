# Estratégia de avaliação (frente Q)

- `evals/cases.d/q.jsonl`: official-var (15 paráfrases pt/en, fatos e entidades herdados do oficial de origem),
  partial (5, `handoff: false`), hard (5, fora do gate), guardrail (33, campo `owasp` ASI01..ASI10).
- `evals/judge_calibration.d/q.jsonl`: 48 rótulos (24 positivos), contextos RAG, tool e web; cada negativo com
  `failure_type`, 4 por tipo.
- Medida offline (`python -m evals.run_evals --split guardrail --out var/q.json`, sha 966fc29): intent_acc 0.4242
  no split guardrail, gate 0.9 não atingido. É linha de base, não resultado final.
