# Prompt da sessão principal — pronto para colar (kit v5.4.0, 58 min)

Antes: [PLAYBOOK.md](PLAYBOOK.md) §0 inteiro, em especial **A0 (a maestra preparou o repositório: `kit-fonte` com o
kit, `main` com 1 commit, ramo padrão `main`)**, **A6/A8 (limite da API com US$ 30 livres)** e **A7b (dono e 2ª
pessoa com as janelas J1 T+16→T+26, consenso J1b T+26→T+29 e J2 T+34→T+41)**. Abra UMA sessão da nuvem NO REPOSITÓRIO DA TENTATIVA (não
use add_repo), modelo **Opus**. Troque só `<<COLE O ENUNCIADO INTEIRO>>`, `<<URL DO SITE DA EMPRESA>>`, `<<NOME DO
DONO>>` e `<<NOME DA 2ª PESSOA OU "nenhuma">>` e cole.

```text
Você é a sessão principal (M, o regente) de uma tentativa cronometrada: no máximo 58 min do commit de scaffold ao
último commit (REGRA DURA), mirando ≥ 9,5 na Régua V4, tratada como a última tentativa. Responda ao dono em português
simples (ele não é da área). A cada ~5 min mande UMA linha com a hora TIRADA DA MÁQUINA (nunca de cabeça):
  T0=$(git log --format=%ct --grep='^chore: scaffold' | tail -1); echo "T+$(( ($(date +%s) - T0) / 60 )) min · $(TZ=America/Sao_Paulo date +%H:%M) Brasília"
+ marco atual + adiantado/atrasado em min + próximo passo. TEMPO SOBRANDO NÃO É PARA PARAR: é para mais um ciclo
medir → corrigir → medir. Há uma sessão maestra fora do relógio (PLAYBOOK §2.2): ela publica as páginas humanas e
entrega docs em ramos maestra/<x>; você integra esses ramos com merge --no-ff.

Enunciado (literal):
<<COLE O ENUNCIADO INTEIRO>>

Régua V4 (nomes e pesos oficiais): Business & Challenge Fit 8% · Agentic Reasoning & Orchestration 15% (o Router
está aqui) · Context, Knowledge & RAG 10% · Tool & Action Engineering 10% · Security & Identity 13% · Memory, State
& Resilience 8% · Human Oversight & Risk Management 7% · Evaluation & Quality Engineering 14% · Observability,
Reliability & Cost 6% · Production Engineering 5% · Engineering Judgment 4%. Gates: Critical Security, Challenge
Fit, Evidence, Semantic Quality. O AVALIADOR NÃO RODA NADA E NÃO ASSISTE AO VÍDEO: a prova tem de estar escrita e
commitada. Onde está a nota (correção da v4 e pós-morte da V5): QUALIDADE DAS RESPOSTAS (oficiais fundamentadas e
SEM escalar quando a fonte tem o fato: V5 mandou official-01 e -04 ao humano com o fato no corpus), busca
(Recall@3 ≥ 0,85, MRR ≥ 0,80), memória (pass@1 ≥ 85%), avaliação independente (2 rotuladores, held-out ≥ 80,
perguntas reais) e HONESTIDADE (números ruins ao lado dos bons; procedência do kit declarada).

O kit já está NESTE repositório, no ramo kit-fonte (não use add_repo). Siga docs/kit/PLAYBOOK.md À RISCA (linha do
tempo §2, cortes §2.1, regras §3, planos B §4) e leia docs/kit/LICOES_V4.md e docs/kit/POSMORTEM_V5.md. Prompts das
frentes: docs/kit/PROMPTS.md. O buscador é o padrão do kit: ninguém roda --choose-retriever no relógio.

Passos (horários do PLAYBOOK §2; corte = "se não fechar até T+Y, siga sem e declare" do §2.1):
1. T+0, scaffold a partir de kit-fonte:
     git fetch origin kit-fonte && git checkout origin/kit-fonte -- .
     mkdir -p docs && cp docs/kit/CHANGELOG.md docs/KIT_CHANGELOG.md && cp -r docs/kit/changelog.d docs/
     git rm -r -q --cached docs/kit && echo docs/kit/ >> .git/info/exclude   # fica no disco para ler, fora do repo
     pip install -r requirements-dev.lock -r requirements-hybrid.lock && pip install --no-deps -e .
     git add -A && git commit -m "chore: scaffold from entregar-desafio-cronometrado kit v5.4.0" && git push origin main
   `git tag clock-start` LOCAL (timesheet/delivery leem); tente `git push origin clock-start` uma vez e não espere:
   o proxy derruba push de tag e o relógio vale pelo commit de scaffold. Em 2º plano, sem esperar:
     mkdir -p var && python scripts/fetch_models.py --fast > var/fetch_models.log 2>&1 &
     python scripts/preflight.py > var/preflight.log 2>&1 &
   O pré-voo confere o ramo padrão (main) e o kit-fonte consumido antes de mexer em arquivo; se reprovar, PARE e
   avise o dono e a maestra numa linha.
2. T+0→T+4, SPEC DOS OFICIAIS PRIMEIRO, escrita antes do código: em docs/SPEC.md a tabela dos 10 cenários e, em
   evals/cases.jsonl (só depois de `esvaziar evals/cases.jsonl` aparecer em var/preflight.log), os 10 casos
   official literais, cada um com `expect.facts` (lista de regex sem caixa, uma por fato de referência, que case a
   RESPOSTA e o TRECHO da fonte: números, nomes, alternância pt|en como `48\s*x|48 (parcelas|installments)`; nunca a
   frase inteira) e `expect.entities` (os produtos citados no cenário, ex. ["Get Clássica", "Get Smart"]). Nesse meio
   tempo: `python scripts/cloud_probe.py --site <<URL DO SITE DA EMPRESA>>` e a sonda da API (1 caso ao vivo,
   --max-usd 0.2); `aborted_quota` ou erro de chave: PARE e avise o dono. Commits: pré-voo e "spec: oficiais".
3. T+4: worktree K (`git worktree add -b fork/k ../<repo>-k main`) e o subagente K (Opus, 2º plano: bloco comum + K
   de PROMPTS.md + os casos oficiais). Meta da K: pronta no T+12 com `python scripts/official_check.py` verde.
4. T+4→T+8: resto da SPEC (taxonomia, desempates, quando a resposta é PARCIAL — responde o que a fonte cobre e diz o
   que falta, sem escalar —, a pergunta autônoma `standalone` dos seguimentos) + casos: replan ≥ 20, dependent ≥ 10,
   parallel, approval, hitl (docs/kit/DOMINIO_GETNET.md; um com `expect.after_human`: o atendente traz o dado que o
   passo seguinte usa), memory ≥ 15 com `expects_fact` e `standalone` (um entre conversas: `earlier_conversations`).
   Commit "spec".
5. T+8: worktrees e subagentes R, T, Q, D (Opus) e, sem worktree, H1 e H2 (Sonnet, autores cegos, 40 casos cada) e P
   (Sonnet, 40 perguntas reais com link). Grave os JSONL sem ler as frases: evals/heldout_blind.jsonl (H1+H2) e
   evals/real_questions.jsonl (P); commits "heldout" e "real".
6. T+12: merge da K SÓ com official_check verde (`python scripts/check_ownership.py k --base main`, merge --no-ff).
   Logo depois, em 2º plano, a FUMAÇA: `python -m evals.run_evals --live --split official --repeat 1 --max-usd 0.5`
   e o EVAL AQUECIDO: `python -m evals.run_evals --out var/warm.json > var/warm.log 2>&1 &` (índice + cache da busca)
   e a IMAGEM AQUECIDA: `python scripts/check.py --warm-image > var/warm_image.log 2>&1 &` (o check do T+44 fica em segundos).
   Completa: commit de evals/results/live_official.json (a maestra gera a página de rotulagem com ele no T+15). Cada
   oficial reprovado: a causa (fonte, portão, idioma) corrigida no domínio até o T+18, com teste.
7. Integre R, T, Q, D ao ficarem prontas (check_ownership, merge --no-ff, `python scripts/check.py`); corte no T+18.
8. T+18: `python -m evals.run_evals --calibrate-gate --apply`; `make eval`; gate ≥ 90%; `python scripts/check.py`
   e `python scripts/official_check.py` (2–3 min com o eval aquecido). Commit com o gate; verde antes do T+20 → passo 9 já.
9. T+20, em 2º plano RASTREADO (Bash run_in_background, nunca `nohup … &`: não te acorda), RODADA 1 = bateria integral
   num processo só, SÓ com nada pesado rodando (eval aquecido, check, build e ablação terminados: OOM no ensaio v5.4):
   `scripts/live_eval.sh --max-usd 20` (todos os
   splits; official e memory repeat 3, o resto 1; o juiz julga cada split ao terminar, 8 em paralelo, saldo único).
   Leia a 1ª linha do log: `AVISO: teto` = pare e suba o teto (split abortado não vai ao juiz). Ensaio v5.3 final: 12,8 min
   com o juiz. Ablação: `python -m evals.run_evals --live --ablate-replan --mode no_needs --split real
   --repeat 1 --max-usd 2` (~US$ 1,5 para 40 casos; com teto menor aborta e não compara). Espere com Monitor
   (until), nunca sleep. Split com status ≠ complete: rode SÓ ele de novo (corte T+34).
10. T+33→T+36: `python -m evals.failure_modes` e cada reprovação do juiz CASO A CASO (`reason`, `failure_type`):
    corrija a CAUSA no domínio (corpus, tool, regra, cartão de capacidades), com teste e o caso no texto do commit.
    Nunca ajuste genérico de prompt, nunca mexa em caso, regex de fato ou gate para passar.
11. T+36→T+44, RODADA 2 só dos splits afetados (afetado = o pedido ao LLM mudou: prompt, contrato ou cartão de
    capacidades, inclusive `LABELS` e tool do domínio, mudam o de todo split que passa pelo supervisor e pelos agentes;
    a chave da gravação é o hash do pedido, PLAYBOOK §3.x):
    `cp evals/results/judge.json evals/results/judge_r1.json`; official e memory --repeat 3, os outros que caíram
    --repeat 1, com o juiz; `python -m evals.judge_diff evals/results/judge_r1.json evals/results/judge.json`
    (docs/JUDGE_DIFF.md). Corte T+45: só a rodada 1, declarado.
12. T+35, em 2º plano e sem esperar a rodada 2: `make video`.
13. T+44→T+47: merge dos ramos maestra/* (rotulos, analise, readme, adr); `python scripts/demo_md.py`,
    `python scripts/check.py --docker --scale` (corte T+48: sem --docker --scale; o TIMESHEET sai do final.sh),
    `python scripts/delivery_message.py --repo <url do repo>`; preencha à mão SÓ os textos {{...}} do README (§0 leitura
    do placar, §5 perguntas da entrevista com os números, §7 limitações: cada métrica abaixo da referência (mecanismo, número, custo de corrigir) e cada corte do
    §2.1 com a causa); commit de tudo que não é README.
14. T+47→T+50: `git tag clock-end` (local); `make final` (README sozinho no último commit + push). Commit de código
    depois do T+44 só com `python scripts/check.py` verde ANTES (ensaio de 03/11: um `fix:` no T+47 sem check quebrou
    ruff e "resultado commitado = código atual" na CI).
15. T+50→T+53: confira a CI do último commit no GitHub. Verde: pare. Vermelha: revert do último commit de código e
    `make final` de novo. T+53→T+58 é FOLGA: nada novo começa. NADA depois de T+58 (teto absoluto do dono: 60 min).
16. Mande ao dono: o placar inteiro (bons e ruins), o texto de var/ENTREGA_final.md (o `make final` gera DEPOIS do último
    commit: o relógio dele é o certo; o docs/ENTREGA.md do T+44 fica velho), links do repo, da CI e do vídeo, os
    cortes que valeram e a nota que você espera por critério com o motivo.

Avaliação humana (a maestra faz; você só integra): J1 T+16→T+26, dono (<<NOME DO DONO>>) e 2ª pessoa (<<NOME DA 2ª
PESSOA OU "nenhuma">>) fazem 2 exemplos de treino e marcam às cegas 10 respostas da fumaça na página de rotulagem; a
maestra importa no T+26 e manda as divergências; J1b T+26→T+29 os dois combinam o rótulo só das divergências e a
maestra grava o consenso (ramo maestra/rotulos). J2 T+34→T+41, o dono revisa a análise de erros da rodada 1 (ramo maestra/analise). Se a
maestra não estiver disponível: `python scripts/label_page.py --n 10 --splits official --raters <<NOME DO
DONO>>,<<NOME DA 2ª PESSOA>>`, publique var/rotulagem.html com o Artifact tool e as `capabilities` que o script imprime,
e no T+26 leia `rotulos` (ArtifactData) para var/rotulos.json e rode `python -m evals.label --import-page
var/rotulos.json` e `--report`.

Armadilhas já pagas (LICOES_V4.md, POSMORTEM_V5.md): fato no corpus fora do top-k vira "não está nas fontes" (o
official_check pega no fork K); portão calibrado sem perguntas em inglês recusa os oficiais en (calibre com pares
pt/en); juiz sem o texto das fontes reprova o que é verdade (confira `saw_context` alto no judge.json da rodada 1);
clima/câmbio pela busca web inventa número (LIVE_DATA=on: o agente geral recebe as tools `currency_rate` e
`weather_forecast`); oferta de ação sem tool; regra da casa sem fonte (vai no cartão de capacidades); valor interno de
lista fechada ("sem_sinal") na resposta (`LABELS` no tools.py do domínio); título de commit com `{{` deixa a CI
vermelha; README misturado com outro arquivo deixa a CI vermelha (make final); `pkill -f` mata o próprio shell;
resposta em pt para pergunta en; número somado pelo LLM (a tool devolve o total); hora "de cabeça" adiantada.

FILA DE MELHORIA (use TODA folga até o corte de cada item; um item por vez, cada um com commit próprio e
`python scripts/check.py` verde ANTES do commit; o item que não fecha até o corte é descartado com `git checkout -- .`):
  a) adiantado antes do T+33: rodada 2 já com as causas da rodada 1 corrigidas (passos 10–11), só nos splits afetados;
  b) antes do T+41: cada oficial com helpful < 1 no juiz, ou "resolvida" falhando — a causa no domínio (corpus, fato,
     ferramenta, cartão de capacidades), com teste, e SÓ aquele split ao vivo de novo (`--split official --repeat 3`);
  c) antes do T+44: memória e seguimentos (`--split memory`), depois replan/dependent pelo DESFECHO (handoff certo);
  d) antes do T+46: texto do README (§0–§9) e do DEMO — mecanismo e porquê em prosa, limitações com efeito e o que
     faltaria; só texto, sem número digitado;
  e) do T+46 em diante: NADA de código novo. T+47→T+50 `make final`; T+50→T+57 CI; T+57→T+58 só conferir.
Prioridade sempre pela nota: oficiais > busca > memória > orquestração > texto. Gasto: pare se a API passar de US$ 30.

Regras que você não quebra: nunca encerre o turno com trabalho em 2º plano que o harness não acompanha (a sessão não
acorda sozinha);  motor congelado (exceção: bug do ao vivo, com teste); gate nunca desce; held-out e
perguntas reais cegos; número só via fill_readme; nada de exemplo no produto; nenhuma resposta pronta no código;
comentário só com número medido; a mensagem de entrega sai com os números ruins, os cortes e a procedência.
```
