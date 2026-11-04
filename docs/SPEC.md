# Spec — Getnet Multi-Agent Support System

Commitada antes de qualquer código do domínio. Congelada (OWNERSHIP.json): mudança aqui é decisão da sessão principal.

## Problema
Lojistas da Getnet escrevem em pt ou en perguntando sobre produtos (maquininhas, Pix, Link de Pagamento,
crediário, antecipação), sobre a própria conta (depósitos, recusas, terminais) e coisas gerais (clima, câmbio).
Um Router decide o agente (Knowledge com RAG sobre o site oficial, Customer Support com tools sobre o CRM, agente
geral com dado ao vivo) e o supervisor encadeia/replaneja; o que não se resolve com confiança vai a um humano.

## Requisitos

| ID | Requisito (do enunciado) | Módulo | Teste / eval |
|---|---|---|---|
| FR-01 | Router: entrada única, decide agente ou sequência | `src/app/router.py`, `src/app/domain/challenge/flow.py` | `tests/test_domain_router.py`, split `official` |
| FR-02 | Knowledge: RAG sobre site da Getnet + busca web para geral | `src/app/agents.py`, `data/sources.json` | `scripts/official_check.py`, bloco `retrieval` |
| FR-03 | Customer Support: lê o dado do cliente, ≥ 2 tools | `src/app/domain/challenge/tools.py` | `tests/test_tools.py` |
| FR-04 | `POST /chat` com `{"message","user_id"}` → JSON | `src/app/api.py` | `tests/test_domain_http.py` |
| FR-05 | Humano (4º agente): escalonamento e retomada | `src/app/hitl.py` | split `hitl` |
| FR-06 | Guardrails: inseguro, sensível, fora de escopo | `src/app/guardrails.py` | split `guardrail` |
| NFR-01 | Sobe com um comando (Docker) | `Dockerfile` | `scripts/check.py --docker` |
| NFR-02 | Funciona sem chave de LLM (modo offline) | `config.py` | CI |
| NFR-03 | Identidade: `AUTH_MODE` demo (payload literal do enunciado) e required (JWT) (ADR 0001) | `api.py` | `tests/test_auth_modes.py` |

## Cenários de aceite (copiados do enunciado, um por linha; todos `user_id` = `cliente1988`, idioma en)

`expect.facts` = regex sem caixa que a RESPOSTA e o TRECHO da fonte (ou o dado da tool) têm de conter. Escritas
antes do código. Nenhuma é eco da pergunta.

| ID | Mensagem | intent | Fatos de referência (regex) | Entidades | Parcial aceitável |
|---|---|---|---|---|---|
| official-01 | What's the difference between the Get Clássica and the Get Smart? | knowledge | `79[,.]90` (aluguel Clássica) · `129[,.]90` (aluguel Smart) · recurso da Smart (`estoque\|stock\|inventory\|nota fiscal\|invoice\|aplicativo\|apps?\|android\|tela\|screen`) | Get Clássica, Get Smart | se a fonte não lista recursos da Clássica, diz isso e responde o resto; sem humano |
| official-02 | What's the weather forecast in Porto Alegre tomorrow? | general | `°C\|graus\|degrees` · `chuva\|rain\|precipita` | — | nunca escala; tool `weather_forecast` (Open-Meteo, 2ª fonte wttr.in) |
| official-03 | When will the money from yesterday's sales be deposited? | support | `205[,.]50` (débito) · `480[,.]00` (crédito) · `60[,.]00` (Pix) | — | tool devolve totais e datas; o LLM não soma |
| official-04 | Do I need a bank account to receive my sales via Pix? | knowledge | `Get\s*Conta` | Pix, Get Conta | responde com a Get Conta; sem humano |
| official-05 | My card machine won't connect to the internet, what should I do? | troubleshoot | `T1988B` (terminal offline do CRM) · `chip\|wi-?fi\|sinal\|signal` | — | records → (needs) faq com o manual |
| official-06 | How does receivables advance (antecipação) work with Getnet? | knowledge | `taxa\|fee\|rate\|custo\|cost` · `autom[aá]tic\|pontual\|one-?off\|on demand\|sob demanda\|quando quiser\|whenever` | Antecipação | página de antecipação certa (não a Reserva Financeira) |
| official-07 | What's the euro exchange rate today? | general | `PTAX` · `R\$\s*\d+[,.]\d{2,4}` | — | nunca escala; tool `currency_rate` (BCB PTAX, com a data do boletim) |
| official-08 | My card machine is showing a transaction decline error. | troubleshoot | `\b51\b` · `\b05\b` (códigos de recusa do CRM, com significado calculado no código) | — | records (transações recusadas + terminal) → faq se `needs` |
| official-09 | How many installments can I split a sale into with the crediário? | knowledge | `48\s*x\|48 (parcelas\|installments)` | Crediário | — |
| official-10 | Can I sell through WhatsApp using the Payment Link? | knowledge | `e-?mail\|SMS\|redes sociais\|social` | Link de Pagamento | — |

### Dados do CRM que os oficiais de support/troubleshoot leem (frente T grava em `data/crm/`, datas relativas a hoje em America/Sao_Paulo)

- `cliente1988`: terminais `T1988A` (Get Smart, Wi-Fi, online) e `T1988B` (Get Clássica, chip, offline, sem sinal,
  último contato há ~190 min). Vendas de ONTEM aprovadas: débito R$ 205,50 (duas: TX1001 R$ 120,00 + TX1003
  R$ 85,50; cai D+1 útil), crédito R$ 480,00 (TX1002, D+30), Pix R$ 60,00 (TX1005, D+0). Recusadas de hoje: TX1007
  crédito R$ 210,00 código 51 (saldo insuficiente), TX1008 débito R$ 75,00 código 05 (não autorizada pelo emissor).
- 2º cliente `cliente2077` (outro dono; registro dele pedido por `cliente1988` = "não encontrado").
