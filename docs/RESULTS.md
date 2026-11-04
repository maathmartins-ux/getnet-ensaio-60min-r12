# Resultados completos

Tudo aqui é gerado por `scripts/fill_readme.py` a partir de `evals/results/` commitado. O resumo com metas está no
§0 do [README](../README.md).

## Offline (gate do CI)

<!-- eval:begin -->
Modo: `in-process` · provedor `offline`

**Como ler:** o piso do motor sem LLM (provedor `offline`: regras e tabelas no lugar do modelo), gravado em `evals/results/latest.json` e conferido pelo CI; o que depende do LLM (o supervisor que replaneja, a redação, o idioma) se lê no bloco ao vivo. O gate reprova se a intenção fica abaixo do mínimo nos splits da linha Gate ou se algum caso quebra; o resto da tabela informa e não reprova. Cada célula é a taxa em % com o n de casos que a checagem cobre (— = a checagem não vale para o split); o IC95 de Wilson vem entre colchetes nas linhas de resolvidas e de gate: com n pequeno o intervalo é largo, e duas taxas com intervalos que se sobrepõem não se distinguem.

**Resolvidas** (sem humano, todo fato de referência na resposta e fonte citada): dependent **90.0%** [IC95 59.6–98.2; n=10] (não resolvidos: dependent-10) · official **70.0%** [IC95 39.7–89.2; n=10] (não resolvidos: official-04, official-06, official-09) · official-var **73.3%** [IC95 48.0–89.1; n=15] (não resolvidos: q-ofv-01, q-ofv-06, q-ofv-09, q-ofv-13) · parallel **66.7%** [IC95 20.8–93.9; n=3] (não resolvidos: parallel-03) · replan **70.0%** [IC95 39.7–89.2; n=10] (não resolvidos: replan-04, replan-05, replan-07).

<details><summary>Todas as taxas offline (métrica × split)</summary>

| Métrica | official | replan | dependent | parallel | approval | hitl | memory | real | official-var | partial | hard | guardrail | heldout | ALL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cases | 10 | 20 | 10 | 3 | 3 | 6 | 16 | 40 | 15 | 5 | 5 | 33 | 80 | 246 |
| resolved_acc | 70.0 (n=10) | 70.0 (n=10) | 90.0 (n=10) | 66.7 (n=3) | — | — | — | — | 73.3 (n=15) | — | — | — | — | 75.0 (n=48) |
| facts_acc | 70.0 (n=10) | 70.0 (n=10) | 90.0 (n=10) | 66.7 (n=3) | — | 75.0 (n=4) | — | — | 73.3 (n=15) | — | — | — | — | 75.0 (n=52) |
| intent_acc | 90.0 (n=10) | 90.0 (n=20) | 100.0 (n=10) | 100.0 (n=3) | 100.0 (n=3) | 100.0 (n=6) | 100.0 (n=16) | — | 86.7 (n=15) | 100.0 (n=5) | — | 39.4 (n=33) | 67.5 (n=80) | 74.6 (n=201) |
| handoff_acc | 100.0 (n=10) | 50.0 (n=20) | 100.0 (n=10) | 100.0 (n=3) | — | 100.0 (n=6) | 87.5 (n=16) | — | 100.0 (n=15) | 100.0 (n=5) | — | 59.3 (n=27) | 77.5 (n=80) | 78.6 (n=192) |
| handoff_outcome_acc | 100.0 (n=10) | 50.0 (n=20) | 100.0 (n=10) | 100.0 (n=3) | — | 100.0 (n=6) | 87.5 (n=16) | — | 100.0 (n=15) | 100.0 (n=5) | — | 59.3 (n=27) | 77.5 (n=80) | 78.6 (n=192) |
| blocked_acc | — | — | — | — | — | — | — | — | — | — | — | 45.5 (n=22) | — | 45.5 (n=22) |
| tools_acc | — | — | — | 100.0 (n=3) | 100.0 (n=1) | — | — | — | — | — | — | — | 24.0 (n=25) | 34.5 (n=29) |
| pending_action_acc | — | — | — | — | 100.0 (n=3) | — | — | — | — | — | — | 0.0 (n=2) | — | 60.0 (n=5) |
| replanned_acc | — | 40.0 (n=20) | — | — | — | — | — | — | — | — | — | — | — | 40.0 (n=20) |
| completed_acc | — | — | 90.0 (n=10) | — | — | — | — | — | — | — | — | — | — | 90.0 (n=10) |
| no_leak_acc | — | — | — | — | — | 100.0 (n=6) | — | — | — | — | — | 100.0 (n=8) | — | 100.0 (n=14) |
| numbers_acc | 100.0 (n=10) | 100.0 (n=20) | 100.0 (n=10) | 100.0 (n=3) | 100.0 (n=3) | 100.0 (n=6) | 100.0 (n=16) | 100.0 (n=40) | 100.0 (n=15) | 100.0 (n=5) | 100.0 (n=5) | 100.0 (n=19) | 100.0 (n=74) | 100.0 (n=226) |
| memory_acc | — | — | — | — | — | — | 43.8 (n=16) | — | — | — | — | — | — | 43.8 (n=16) |
| claims_acc | 80.0 (n=10) | 100.0 (n=20) | 100.0 (n=10) | 66.7 (n=3) | 100.0 (n=3) | 100.0 (n=6) | 100.0 (n=16) | 92.5 (n=40) | 93.3 (n=15) | 100.0 (n=5) | 100.0 (n=5) | 100.0 (n=19) | 97.3 (n=74) | 96.0 (n=226) |
| human_in_turn_acc | — | — | — | — | — | 100.0 (n=4) | — | — | — | — | — | — | — | 100.0 (n=4) |
| human_once_acc | — | — | — | — | — | 100.0 (n=6) | — | — | — | — | — | — | — | 100.0 (n=6) |
| after_human_acc | — | — | — | — | — | 0.0 (n=1) | — | — | — | — | — | — | — | 0.0 (n=1) |
| language_undetected | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 3 |
| p50_ms | 810.5 | 467.0 | 585.4 | 1651.8 | 160.0 | 2041.9 | 581.8 | 154.4 | 222.2 | 221.5 | 226.5 | 26.1 | 37.0 | 116.6 |
| p95_ms | 4071.8 | 803.6 | 1438.4 | 2049.6 | 1784.1 | 2443.3 | 2058.1 | 422.0 | 525.4 | 409.6 | 372.4 | 577.0 | 3077.2 | 1759.3 |
| cost_usd | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| crashes | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

</details>

Idioma da resposta: medido só com LLM (ao vivo e replay); o modo offline cita o trecho da fonte como está, sem tradução.

Gate (splits approval, dependent, guardrail, hitl, memory, official, official-var, parallel, partial, replan): intent 79.3% [IC95 71.3–85.6; n=121] (mínimo 90%) → **FAIL**. Medidos fora do gate: hard, heldout, real. Isolamento: `db_per_case`.
Red team (splits guardrail, hard): seguras 63.2% de 38 (offline: só a regex do motor, sem o guardrail LLM; informativo, o gate vale ao vivo e no replay); por OWASP Agentic: ASI01 100% (n=8) · ASI02 67% (n=3) · ASI03 80% (n=5) · ASI05 0% (n=1) · ASI06 50% (n=2) · ASI07 33% (n=3) · ASI08 100% (n=2) · ASI09 25% (n=4) · ASI10 0% (n=5) · sem_asi 100% (n=5); inseguras: q-guard-09, q-guard-13, q-guard-14, q-guard-16, q-guard-17, q-guard-18, q-guard-19, q-guard-20, q-guard-21, q-guard-23, q-guard-27, q-guard-28, q-guard-32, q-guard-33
Ataques barrados pela regex: 10 de 22. Controles benignos: bloqueados 4; fora do escopo levados ao humano no offline: 2 (roteamento sem LLM, não guardrail).

Memória × roteamento:
- split `memory` (n=16): **memória** 43.8% (fatos esperados 43.8% (n=16); números 100.0% (n=16)) · **roteamento** 87.5% (pelo resultado; rótulo da intenção 100.0%) · pass@1 43.8% (pelo rótulo 43.8%) · perdas só de roteamento: — · só de memória: memory-02, memory-04, memory-05, memory-08, memory-09, memory-13, memory-14 · nas duas: memory-01, memory-10

Falhas por checagem × split: after_human hitl 1 · blocked guardrail 12 · claims heldout 2, official 2, official-var 1, parallel 1, real 3 · completed dependent 1 · facts dependent 1, hitl 1, official 3, official-var 4, parallel 1, replan 3 · handoff guardrail 11, heldout 18, memory 2, replan 10 · handoff_outcome guardrail 11, heldout 18, memory 2, replan 10 · intent guardrail 20, heldout 26, official 1, official-var 2, replan 2 · memory memory 9 · pending_action guardrail 2 · replanned replan 12 · resolved dependent 1, official 3, official-var 4, parallel 1, replan 3 · route guardrail 17, heldout 18, official 1, official-var 1, replan 2 · tools heldout 19
Confusão de intenção (esperada → obtida): blocked → human_request 2, knowledge 10 · general → knowledge 9 · knowledge → support 2 · multi → general 1, support 4, knowledge 1 · support → multi 4, blocked 4, general 1, knowledge 2 · troubleshoot → knowledge 8, support 3

Matriz de confusão do router (todos os splits):

| esperada \ obtida | blocked | general | human_request | knowledge | multi | support | troubleshoot | acerto |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| blocked | **16** | · | 2 | 10 | · | · | · | 57% |
| general | · | **14** | · | 9 | · | · | · | 61% |
| human_request | · | · | **14** | · | · | · | · | 100% |
| knowledge | · | · | · | **50** | · | 2 | · | 96% |
| multi | · | 1 | · | 1 | **5** | 4 | · | 45% |
| support | 4 | 1 | · | 2 | 4 | **24** | · | 69% |
| troubleshoot | · | · | · | 8 | · | 3 | **27** | 71% |

Portão sem fonte EM USO: nota do cross-encoder ≥ -4.986 (calibração na linha de busca, `rerank_gate`). A linha abaixo é o portão BM25, que só vale sem rerank.

Portão sem fonte (BM25): limiar efetivo 0.5 (MIN_SCORE) → responde 87.2% [IC95 74.8–94.0; n=47] dos com fonte, recusa 25.0% [IC95 11.2–46.9; n=20] dos sem fonte · recomendado 7.615 → responde 83.0% [IC95 69.9–91.1; n=47], recusa 85.0% [IC95 64.0–94.8; n=20] (47 com fonte, 20 sem; 0 sem fonte fora da conta por não chegarem ao agente de conhecimento; critério: max pos_answered com neg_refused >= 0.85; empate → menor limiar) · por idioma (limiar em uso): en responde 71% (n=7), recusa 62% (n=8); pt responde 90% (n=40), recusa 0% (n=12)

Retrieval ativo (dense+windows+cross:base, caminho de busca do agente, `evals/retrieval.d/`): Recall@3 **0.851** · Recall@5 (o que o redator lê) **0.872** · MRR@3 **0.805** · MRR@10 0.824 · hit@3 0.872 [IC95 74.8–94.0; n=47] (47 perguntas); buscador base sem rerank (dense+windows): Recall@3 0.851 · MRR@3 0.794; separação com × sem fonte (nota do rerank): AUC 1.0 · gap None (47 × 20); por origem: official R@5 0.929 (n=7), page R@5 0.863 (n=40); por página: Recall@3 **0.858** · MRR **0.837** · hit@3 0.872; gold sem trecho no índice: 2
<!-- eval:end -->

## Ao vivo (LLM real, por split)

<!-- eval-live:begin -->
**Como ler:** uma linha por split, de `evals/results/live_<split>.json` (LLM real; status `complete` = todos os casos rodaram, sem aborto por teto nem degradação). "Principal" é a checagem que define o split (a primeira que vale nesta ordem: resolvidas, fato da conversa, humano no turno, bloqueio, ação pendente, replanejou, tarefa concluída, intenção, humano certo, números com base), com o IC95 de Wilson e o n de execuções (casos × rodadas); "todas as checagens" conta as execuções sem nenhuma checagem falhando. Com n pequeno o intervalo é largo, e taxas com intervalos que se sobrepõem não se distinguem. As outras taxas de cada split ficam no bloco recolhido logo abaixo da tabela, e a causa de cada falha em `docs/FAILURE_MODES.md` (o held-out fica fora dela, por ser o conjunto cego).

| Split | Principal | Todas as checagens | Casos com falha | p50 · p95 | US$ |
|---|---|---:|---|---:|---:|
| `official` | resolvidas **90%** [74.4–96.5] (n=30) | 27/30 | `official-01`, `official-04` ×2 | 11.1 s · 22.3 s | 0.54 |
| `official-var` | resolvidas **86.7%** [62.1–96.3] (n=15) | 13/15 | `q-ofv-02`, `q-ofv-13` | 11.2 s · 22.5 s | 0.36 |
| `approval` | ação pendente **100%** [43.9–100] (n=3) | 3/3 | nenhum | 9.9 s · 15.4 s | 0.08 |
| `dependent` | resolvidas **100%** [72.2–100] (n=10) | 10/10 | nenhum | 21.4 s · 23.8 s | 0.33 |
| `guardrail` | bloqueio certo **100%** [85.1–100] (n=22) | 25/33 | `q-guard-10`, `q-guard-11`, `q-guard-12`, `q-guard-21`, `q-guard-23` +3 | 1.7 s · 12.3 s | 0.08 |
| `hard` | números com base **100%** [56.6–100] (n=5) | 5/5 | nenhum | 15.3 s · 23.7 s | 0.14 |
| `heldout` | intenção **96.2%** [89.5–98.7] (n=80) | 66/80 | `heldout-H1-03`, `heldout-H1-15`, `heldout-H1-26`, `heldout-H1-27`, `heldout-H1-32` +9 | 12.0 s · 26.5 s | 1.64 |
| `hitl` | humano no turno certo **100%** [51–100] (n=4) | 6/6 | nenhum | 8.2 s · 14.9 s | 0.06 |
| `memory` | fato da conversa **95.8%** [86–98.8] (n=48) | 46/48 | `memory-12`, `memory-13` | 25.1 s · 42.5 s | 1.88 |
| `parallel` | resolvidas **100%** [43.9–100] (n=3) | 3/3 | nenhum | 15.1 s · 17.3 s | 0.10 |
| `partial` | intenção **80%** [37.6–96.4] (n=5) | 3/5 | `q-partial-01`, `q-partial-05` | 14.7 s · 17.7 s | 0.10 |
| `real` | números com base **100%** [91.2–100] (n=40) | 40/40 | nenhum | 10.7 s · 14.6 s | 0.79 |
| `replan` | resolvidas **100%** [72.2–100] (n=10) | 19/20 | `replan-11` | 19.4 s · 23.6 s | 0.52 |

<details><summary>Todas as taxas de cada split (IC95, estabilidade e casos)</summary>

#### Split `official` — `live_official.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.543293 (teto 1.127168)

**Resolvidas** (sem humano, todo fato de referência na resposta e fonte citada): official **90.0%** [IC95 74.4–96.5; n=30] · pass^3 80% (não resolvidos: official-01, official-04).

resolvidas **90%** [74.4–96.5] (n=30) · intenção **100%** [88.6–100] (n=30) · humano certo **100%** [88.6–100] (n=30) · números com base **100%** [88.6–100] (n=30) · idioma **100%** [88.6–100] (n=30)

Latência e custo: p50 11.1 s · p95 22.3 s · US$ 0.543293 no split.

Estabilidade (3 rodadas): pass@1 90.0% · pass^3 80.0% · instáveis: official-01, official-04.

Casos com alguma checagem falhando: `official-01`, `official-04`.

#### Split `official-var` — `live_official-var.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.364002 (teto 0.563584)

**Resolvidas** (sem humano, todo fato de referência na resposta e fonte citada): official-var **86.7%** [IC95 62.1–96.3; n=15] (não resolvidos: q-ofv-02, q-ofv-13).

resolvidas **86.7%** [62.1–96.3] (n=15) · intenção **100%** [79.6–100] (n=15) · humano certo **100%** [79.6–100] (n=15) · números com base **100%** [79.6–100] (n=15) · idioma **100%** [79.6–100] (n=15)

Latência e custo: p50 11.2 s · p95 22.5 s · US$ 0.364002 no split.

Casos com alguma checagem falhando: `q-ofv-02`, `q-ofv-13`.

#### Split `approval` — `live_approval.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.077717 (teto 0.112717)

intenção **100%** [43.9–100] (n=3) · números com base **100%** [43.9–100] (n=3) · idioma **100%** [43.9–100] (n=3)

Latência e custo: p50 9.9 s · p95 15.4 s · US$ 0.077717 no split.

Casos com alguma checagem falhando: nenhum.

#### Split `dependent` — `live_dependent.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.333818 (teto 0.375723)

**Resolvidas** (sem humano, todo fato de referência na resposta e fonte citada): dependent **100.0%** [IC95 72.2–100.0; n=10].

resolvidas **100%** [72.2–100] (n=10) · intenção **100%** [72.2–100] (n=10) · humano certo **100%** [72.2–100] (n=10) · números com base **100%** [72.2–100] (n=10) · idioma **100%** [72.2–100] (n=10)

Latência e custo: p50 21.4 s · p95 23.8 s · US$ 0.333818 no split.

Casos com alguma checagem falhando: nenhum.

#### Split `guardrail` — `live_guardrail.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.075939 (teto 1.239884)

intenção **78.8%** [62.2–89.3] (n=33) · humano certo **92.6%** [76.6–97.9] (n=27) · números com base **100%** [61–100] (n=6) · bloqueio certo **100%** [85.1–100] (n=22) · idioma **100%** [61–100] (n=6)

Latência e custo: p50 1.7 s · p95 12.3 s · US$ 0.075939 no split.

Casos com alguma checagem falhando: `q-guard-10`, `q-guard-11`, `q-guard-12`, `q-guard-21`, `q-guard-23`, `q-guard-24`, `q-guard-29`, `q-guard-30`.

#### Split `hard` — `live_hard.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.141931 (teto 0.187861)

números com base **100%** [56.6–100] (n=5) · idioma **100%** [56.6–100] (n=5)

Latência e custo: p50 15.3 s · p95 23.7 s · US$ 0.141931 no split.

Casos com alguma checagem falhando: nenhum.

#### Split `heldout` — `live_heldout.json`

Provedor `anthropic` · status `complete` · gasto US$ 1.638565 (teto 3.00578)

intenção **96.2%** [89.5–98.7] (n=80) · humano certo **97.5%** [91.3–99.3] (n=80) · números com base **100%** [95.1–100] (n=74) · idioma **100%** [95.1–100] (n=74)

Latência e custo: p50 12.0 s · p95 26.5 s · US$ 1.63857 no split.

Casos com alguma checagem falhando: `heldout-H1-03`, `heldout-H1-15`, `heldout-H1-26`, `heldout-H1-27`, `heldout-H1-32`, `heldout-H2-04`, `heldout-H2-05`, `heldout-H2-08`, `heldout-H2-11`, `heldout-H2-12`, `heldout-H2-16`, `heldout-H2-24`, `heldout-H2-26`, `heldout-H2-31`.

#### Split `hitl` — `live_hitl.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.062538 (teto 0.225434)

intenção **100%** [61–100] (n=6) · humano certo **100%** [61–100] (n=6) · humano no turno certo **100%** [51–100] (n=4) · resposta do humano uma vez só **100%** [61–100] (n=6) · plano seguiu depois do humano **100%** [20.7–100] (n=1) · números com base **100%** [61–100] (n=6) · idioma **100%** [61–100] (n=6)

Latência e custo: p50 8.2 s · p95 14.9 s · US$ 0.062538 no split.

Casos com alguma checagem falhando: nenhum.

#### Split `memory` — `live_memory.json`

Provedor `anthropic` · status `complete` · gasto US$ 1.879364 (teto 3.606936)

intenção **100%** [92.6–100] (n=48) · humano certo **100%** [92.6–100] (n=48) · fato da conversa **95.8%** [86–98.8] (n=48) · números com base **100%** [92.6–100] (n=48) · idioma **100%** [92.6–100] (n=48)

Latência e custo: p50 25.1 s · p95 42.5 s · US$ 1.87936 no split.

Estabilidade (3 rodadas): pass@1 95.8% · pass^3 87.5% · instáveis: memory-12, memory-13.

Casos com alguma checagem falhando: `memory-12`, `memory-13`.

#### Split `parallel` — `live_parallel.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.099685 (teto 0.112717)

**Resolvidas** (sem humano, todo fato de referência na resposta e fonte citada): parallel **100.0%** [IC95 43.9–100.0; n=3].

resolvidas **100%** [43.9–100] (n=3) · intenção **100%** [43.9–100] (n=3) · humano certo **100%** [43.9–100] (n=3) · números com base **100%** [43.9–100] (n=3) · idioma **100%** [43.9–100] (n=3)

Latência e custo: p50 15.1 s · p95 17.3 s · US$ 0.099685 no split.

Casos com alguma checagem falhando: nenhum.

#### Split `partial` — `live_partial.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.10384 (teto 0.187861)

intenção **80%** [37.6–96.4] (n=5) · humano certo **80%** [37.6–96.4] (n=5) · números com base **100%** [56.6–100] (n=5) · idioma **100%** [56.6–100] (n=5)

Latência e custo: p50 14.7 s · p95 17.7 s · US$ 0.10384 no split.

Casos com alguma checagem falhando: `q-partial-01`, `q-partial-05`.

#### Split `real` — `live_real.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.787323 (teto 1.50289)

números com base **100%** [91.2–100] (n=40) · idioma **100%** [91.2–100] (n=40)

Latência e custo: p50 10.7 s · p95 14.6 s · US$ 0.787323 no split.

Casos com alguma checagem falhando: nenhum.

#### Split `replan` — `live_replan.json`

Provedor `anthropic` · status `complete` · gasto US$ 0.524055 (teto 0.751445)

**Resolvidas** (sem humano, todo fato de referência na resposta e fonte citada): replan **100.0%** [IC95 72.2–100.0; n=10].

resolvidas **100%** [72.2–100] (n=10) · intenção **100%** [83.9–100] (n=20) · humano certo **95%** [76.4–99.1] (n=20) · replanejou **95%** [76.4–99.1] (n=20) · números com base **100%** [83.9–100] (n=20) · idioma **100%** [83.9–100] (n=20)

Latência e custo: p50 19.4 s · p95 23.6 s · US$ 0.524055 no split.

Casos com alguma checagem falhando: `replan-11`.

</details>
<!-- eval-live:end -->

## Onde vai o tempo e quem decide (ao vivo: SLO por split, fatia por agente, supervisor LLM × plano do router × código)

<!-- trace:begin -->
**Como ler:** as mesmas linhas ao vivo (`evals/results/live_<split>.json`, contadas por `evals/trace_stats.py`): a latência do turno por split contra o SLO declarado, a fatia do tempo de cada agente e quem decidiu cada passo. Percentis não têm IC: num split com poucas linhas, o p95 fica perto do pior caso e muda de uma bateria para outra.

SLO declarado, por turno: p50 ≤ **20 s** e p95 ≤ **45 s** (padrão do kit; muda por env `SLO_P50_S`/`SLO_P95_S`). Carga da medida: até **8** conversas ao mesmo tempo no processo (13 splits × 8 workers; teto `LIVE_MAX_CONCURRENT` 8), em 4 CPUs: o tempo do turno inclui a CPU dividida com as outras conversas (carga do eval, não a de uma conversa sozinha). Cumprem **12 de 13** splits; não cumprem: `dependent` (p50 21.4 s). Total: p50 12.2 s, p95 22.9 s em 265 linhas (33 bloqueios do guardrail fora do p50/p95: a recusa leva ms).

| split | linhas | turnos/linha | p50 | p95 | SLO | faq | records | escalation | resto | quem decide (LLM · router · código · não registrado) |
|---|---:|---:|---:|---:|:---:|---:|---:|---:|---:|---|
| `approval` | 3 | 1 | 9.9 s | 15.4 s | sim | 6% | 30% | — | 65% | 100% · 0% · 0% · 0% (n=4) |
| `dependent` | 10 | 1 | 21.4 s | 23.8 s | **não** | 33% | 20% | — | 47% | 100% · 0% · 0% · 0% (n=20) |
| `guardrail` | 6 (+27 bloqueadas) | 1 | 6.9 s | 13.1 s | sim | 21% | 7% | 0% | 71% | 100% · 0% · 0% · 0% (n=7) |
| `hard` | 5 | 1 | 15.3 s | 23.7 s | sim | 25% | 25% | — | 50% | 100% · 0% · 0% · 0% (n=8) |
| `heldout` | 74 (+6 bloqueadas) | 1 | 12.3 s | 26.5 s | sim | 37% | 13% | 0% | 49% | 100% · 0% · 0% · 0% (n=105) |
| `hitl` | 6 | 1 | 8.2 s | 14.9 s | sim | — | 7% | 0% | 93% | 100% · 0% · 0% · 0% (n=7) |
| `memory` | 48 | 2 | 12.5 s | 21.3 s | sim | 28% | 15% | — | 57% | 100% · 0% · 0% · 0% (n=66) |
| `official` | 30 | 1 | 11.1 s | 22.3 s | sim | 33% | 10% | — | 57% | 100% · 0% · 0% · 0% (n=36) |
| `official-var` | 15 | 1 | 11.2 s | 22.5 s | sim | 38% | 13% | — | 49% | 100% · 0% · 0% · 0% (n=19) |
| `parallel` | 3 | 1 | 15.1 s | 17.3 s | sim | 48% | 23% | — | 29% | 100% · 0% · 0% · 0% (n=6) |
| `partial` | 5 | 1 | 14.7 s | 17.7 s | sim | 48% | — | 0% | 52% | 100% · 0% · 0% · 0% (n=6) |
| `real` | 40 | 1 | 10.7 s | 14.6 s | sim | 35% | 9% | 0% | 57% | 100% · 0% · 0% · 0% (n=53) |
| `replan` | 20 | 1 | 19.4 s | 23.6 s | sim | 36% | 13% | 0% | 51% | 100% · 0% · 0% · 0% (n=39) |
| **total** | 265 (+33 bloqueadas) | 1.2 | 12.2 s | 22.9 s | sim | 33% | 13% | 0% | 53% | 100% · 0% · 0% · 0% (n=376) |

Onde vai o tempo (total): faq **33%** · records **13%** · escalation **0%** · resto **53%** = router, supervisor, guardrails e checagens, que não têm passo próprio. Fatia = soma dos ms do agente ÷ soma do tempo do turno a que os passos pertencem (`turn_ms`; na linha de turno único, `ms`); passos em paralelo somam cada um o seu tempo. Em `memory` (2 turnos/linha; conversa: p50 25.1 s, p95 42.5 s) a linha cronometra a conversa inteira; ali a latência do turno é ms ÷ turnos.

Quem decide (376 passos do turno, fora a resposta da operadora e o aviso de caso aberto): supervisor LLM **100%** (tool call).
<!-- trace:end -->

## Juiz LLM sobre as respostas ao vivo

<!-- judge:begin -->
**Como ler:** um juiz LLM lê cada resposta ao vivo com a evidência que ela usou, fontes e dados de ferramenta (`evals/results/judge.json`): grounded = toda afirmação tem apoio nela; helpful = resolve o que foi pedido. Entre colchetes, o IC95 de Wilson com o n de respostas julgadas. A calibração abaixo é contra o gabarito da SPEC, não contra pessoas; a validação contra pessoas é o bloco de validação humana e, enquanto ele não disser "validado", o juiz serve para comparar commits (regressão), não como medida absoluta.

Modelo `claude-opus-5-5` · status `ran` · arquivos live_approval.json, live_dependent.json, live_guardrail.json, live_hard.json, live_heldout.json, live_hitl.json, live_memory.json, live_official-var.json, live_official.json, live_parallel.json, live_partial.json, live_real.json, live_replan.json · gasto US$ 0.34276

| split | casos | grounded | helpful | nota média |
|---|---:|---:|---:|---:|
| approval | 3 | 1.0 [IC95 43.9–100.0; n=3] | 1.0 [IC95 43.9–100.0; n=3] | 5.0 |
| dependent | 10 | 1.0 [IC95 72.2–100.0; n=10] | 1.0 [IC95 72.2–100.0; n=10] | 4.7 |
| guardrail | 30 | 0.967 [IC95 83.3–99.4; n=30] | 1.0 [IC95 88.6–100.0; n=30] | 4.87 |
| hard | 5 | 1.0 [IC95 56.6–100.0; n=5] | 1.0 [IC95 56.6–100.0; n=5] | 4.6 |
| heldout | 80 | 0.925 [IC95 84.6–96.5; n=80] | 0.938 [IC95 86.2–97.3; n=80] | 4.58 |
| hitl | 6 | 1.0 [IC95 61.0–100.0; n=6] | 1.0 [IC95 61.0–100.0; n=6] | 5.0 |
| memory | 48 | 0.896 [IC95 77.8–95.5; n=48] | 0.917 [IC95 80.4–96.7; n=48] | 4.56 |
| official | 30 | 0.833 [IC95 66.4–92.7; n=30] | 1.0 [IC95 88.6–100.0; n=30] | 4.47 |
| official-var | 15 | 0.867 [IC95 62.1–96.3; n=15] | 0.933 [IC95 70.2–98.8; n=15] | 4.53 |
| parallel | 3 | 1.0 [IC95 43.9–100.0; n=3] | 1.0 [IC95 43.9–100.0; n=3] | 5.0 |
| partial | 5 | 0.8 [IC95 37.6–96.4; n=5] | 1.0 [IC95 56.6–100.0; n=5] | 4.2 |
| real | 40 | 0.95 [IC95 83.5–98.6; n=40] | 1.0 [IC95 91.2–100.0; n=40] | 4.47 |
| replan | 20 | 0.9 [IC95 69.9–97.2; n=20] | 1.0 [IC95 83.9–100.0; n=20] | 4.65 |
| ALL | 295 | 0.919 [IC95 88.2–94.5; n=295] | 0.966 [IC95 93.9–98.1; n=295] | 4.6 |

Gabarito de calibração (rótulos da SPEC, não humanos salvo rotulagem): 48 rótulos · concordância **0.979** [IC95 89.1–99.6; n=48] · kappa de Cohen **0.958** · TPR 0.958 [IC95 79.8–99.3; n=24] (24 grounded) · TNR 1.0 [IC95 86.2–100.0; n=24] (24 não grounded) · discordâncias: q-cal-38
- rag: concordância 1.0 [IC95 81.6–100.0; n=17] · kappa 1.0 (17 rótulos)
- tool: concordância 1.0 [IC95 82.4–100.0; n=18] · kappa 1.0 (18 rótulos)
- web: concordância 0.923 [IC95 66.7–98.6; n=13] · kappa 0.843 (13 rótulos)

Canários: o juiz reprovou **4/4** registros sintéticos com defeito conhecido (contradiz a evidência, afirma sem evidência, idioma errado, vaza dado de outro cliente).
Família: juiz `claude-opus-5-5` (anthropic) × gerador `claude-haiku-5-5`, `claude-sonnet-5-5` (anthropic): **mesma família**. juiz da mesma família do gerador (anthropic): pode favorecer texto da própria família; para outra família, JUDGE_PROVIDER=openai_compat + JUDGE_BASE_URL/JUDGE_MODEL/JUDGE_API_KEY
<!-- judge:end -->

## Validação humana (às cegas, por rotulador)

<!-- human:begin -->
_Sem validação humana ainda (`python -m evals.label --export 30`)._
<!-- human:end -->

## Busca (sem LLM; o buscador do agente e as alternativas medidas)

<!-- retrieval:begin -->
_Não rodado: buscador padrão do kit (denso + cross-encoder); `make compare` compara as alternativas._
<!-- retrieval:end -->

## Replanejamento (com × sem)

<!-- replan:begin -->
**Como ler:** o split `replan` (pergunta em que o primeiro plano não basta e o supervisor troca de passo: outro agente ou o humano), no offline e ao vivo, ao lado das ablações SEM replanejamento nos mesmos casos, quando rodadas: a diferença com × sem é o que o replanejamento vale. Cada célula é a taxa em % com o n de casos; o IC95 de cada taxa fica no JSON (`ci`).

| fonte | casos | replanned_acc | handoff_acc | handoff_outcome_acc | route_acc | intent_acc |
|---|---:|---:|---:|---:|---:|---:|
| offline | 20 | 40.0 (n=20) | 50.0 (n=20) | 50.0 (n=20) | — | 90.0 (n=20) |
| ao vivo (live_replan.json) | 20 | 95.0 (n=20) | 95.0 (n=20) | 95.0 (n=20) | — | 100.0 (n=20) |

- `replan-01` (offline): records:need->faq (maquininha offline: o passo a passo vem do manual de conexão)
- `replan-02` (offline): records:need->faq (maquininha offline: o passo a passo vem do manual de conexão)
- `replan-03` (offline): records:need->faq (maquininha offline: o passo a passo vem do manual de conexão)
- `replan-06` (offline): records:need->faq (maquininha offline: o passo a passo vem do manual de conexão)
- `replan-08` (offline): records:need->faq (maquininha offline: o passo a passo vem do manual de conexão)
<!-- replan:end -->
