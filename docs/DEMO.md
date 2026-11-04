# Respostas reais — split `official`

Geradas de `evals/results/live_official.json` (provedor `anthropic`, status `complete`, gasto US$ 0.54); respostas medidas no commit `5bf537e` (2026-11-04T11:41:27Z), página gerada no commit `b9f2ddc` em 04/11/2026 11:51 UTC. Nada aqui foi escrito à mão: é a saída do `POST /chat` com o LLM ligado, 1ª rodada de cada caso.

Estabilidade em 3 rodadas: pass@1 0.9, pass^3 0.8; instáveis: official-01, official-04.

Em cada passo, **decidido por** diz quem pôs o agente no turno: o supervisor LLM (tool call); o plano do router (o router LLM, ou a regra que o substitui: seguimento herdado, guarda da própria empresa, queda do LLM), quando o supervisor LLM não foi consultado (rodado pelo atalho de 1 passo ou pelo motor de tabela); o código, com a regra entre parênteses (`supervisor.CODE_WHY`); ou a operadora que respondeu o caso. "não registrado" = passo gravado sem o campo `decided_by`.

| caso | intenção | rota | ferramentas | handoff | veredito automático |
|---|---|---|---|---|---|
| `official-01` | knowledge | router → faq | — | não | OK |
| `official-02` | general | router → faq | weather_forecast | não | OK |
| `official-03` | support | router → records | get_deposit_schedule | não | OK |
| `official-04` | knowledge | router → faq | — | não | falhou: facts, resolved |
| `official-05` | troubleshoot | router → records → faq | get_terminal_status | não | OK |
| `official-06` | knowledge | router → faq | — | não | OK |
| `official-07` | general | router → faq | currency_rate | não | OK |
| `official-08` | troubleshoot | router → records → faq | list_transactions, get_terminal_status | não | OK |
| `official-09` | knowledge | router → faq | — | não | OK |
| `official-10` | knowledge | router → faq | — | não | OK |

## official-01

**Pergunta:** What's the difference between the Get Clássica and the Get Smart?

**Intenção:** knowledge (esperada knowledge) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0199 · **latência:** 14.9 s

**Resposta:**

> The Get Clássica costs R$ 0,00/month and the Get Smart costs R$ 129,90/month [prod-maquininhas-04]. The Get Smart also has built-in management features.
>
> - **Get Smart:** You can control stock, place orders, close tabs, load menus and issue invoices on the device, and it can integrate with your establishment's system [sup-duvidas-get-smart-10]. It works as a computer and a fiscal printer, so you need neither at the counter. It also reconciles payments in credit, debit, store credit (crediário), QR Code and cash [sup-duvidas-get-smart-08].
> - **Get Clássica:** The sources list no features for it beyond the price.
> - **Other price:** One listing also shows R$ 79,90/month, but it doesn't say which product that price belongs to [prod-maquininhas-04].
>
> The sources don't cover the Get Clássica's technical features or a rate comparison between the two machines. I can hand you to a human agent if you'd like those details.

**Passos:**

1. **faq** · partial · motivo `partial_coverage` · 4847 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/duvidas/get-smart/>; <https://site.getnet.com.br/duvidas/get-smart/>; <https://site.getnet.com.br/todas-as-maquininhas/>; <https://site.getnet.com.br/todas-as-maquininhas/>; <https://site.getnet.com.br/get-tap/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-02

**Pergunta:** What's the weather forecast in Porto Alegre tomorrow?

**Intenção:** general (esperada general) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0319 · **latência:** 8.7 s

**Resposta:**

> Tomorrow (2026-11-05) in Porto Alegre, the forecast is a low of 17 °C and a high of 25 °C. The chance of rain is up to 43%, with light drizzle expected (source: Open-Meteo, https://open-meteo.com/).

**Passos:**

1. **faq** · ok · 3731 ms · decidido por: supervisor LLM (tool call)
   - `weather_forecast` {"city": "Porto Alegre", "day": "amanhã"} → ok

**Fontes:** <https://open-meteo.com/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-03

**Pergunta:** When will the money from yesterday's sales be deposited?

**Intenção:** support (esperada support) · **rota:** router → records · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0157 · **latência:** 9.6 s

**Resposta:**

> Yesterday's approved sales came to R$ 745.50 across 4 transactions. R$ 265.50 has already been deposited, and R$ 480.00 is still to come.
>
> | Method | Amount | Deposit date | Status |
> |---|---|---|---|
> | Pix (1 sale) | R$ 60.00 | 2026-11-03 | Already deposited |
> | Debit (2 sales) | R$ 205.50 | 2026-11-04 | Already deposited |
> | Credit (1 sale) | R$ 480.00 | 2026-12-03 | Not yet deposited |
>
> The R$ 480.00 credit sale is due to be deposited on 2026-12-03.

**Passos:**

1. **records** · ok · 3894 ms · decidido por: supervisor LLM (tool call)
   - `get_deposit_schedule` {"period": "yesterday"} → ok · `{"ok": true, "data": {"period": "yesterday", "today": "2026-11-04", "by_method": [{"method": "debit", "count": 2, "total": 205.5, "transact…`

**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-04

**Pergunta:** Do I need a bank account to receive my sales via Pix?

**Intenção:** knowledge (esperada knowledge) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0182 · **latência:** 12.2 s

**Resposta:**

> To receive Pix sales, you first enable Pix in the Getnet Brasil app or the Minha Conta portal. Then you choose Pix on the terminal and your customer scans the QR Code [sup-pix-venda-01].
>
> In general, Pix works between different banks using a checking account, a savings account or a prepaid payment account [sup-duvidas-57]. That passage describes Pix in general, not the requirements for a merchant to receive sales.
>
> The sources don't say whether a bank account is required to receive Pix sales. I can pass your question to a human agent if you'd like.

**Passos:**

1. **faq** · partial · motivo `partial_coverage` · 5868 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/get-ajuda-pix/como-habilitar-o-recebimento-de-vendas-via-pix-no-aplicativo-getnet-brasil/>; <https://site.getnet.com.br/get-ajuda-pix/como-fazer-uma-venda-com-pix-na-maquininha/>; <https://site.getnet.com.br/duvidas/>; <https://site.getnet.com.br/get-ajuda-pix/como-habilitar-o-recebimento-de-vendas-via-pix-no-aplicativo-getnet-brasil/>; <https://site.getnet.com.br/duvidas/pix-mais-respostas/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': False, 'resolved': False}

## official-05

**Pergunta:** My card machine won't connect to the internet, what should I do?

**Intenção:** troubleshoot (esperada troubleshoot) · **rota:** router → records → faq · **replanos:** ['records:need->faq (maquininha offline: o passo a passo vem do manual de conexão)'] · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0338 · **latência:** 20.5 s

**Resposta:**

> Your machine T1988B (Get Clássica) is offline. It connects by chip, shows no signal, and has been offline for 3.2 hours. The last contact was at 05:26. Your other machine, T1988A (Get Smart), is online on Wi‑Fi.
>
> Steps for a chip connection (these are general and don't name the Get Clássica):
> 1. With the machine off, open the back cover. [sup-duvidas-05]
> 2. Insert the chip in the slot marked SIM1 or SIM2, metal side facing down. [sup-duvidas-05]
> 3. Close the cover, turn the machine on and wait for the data network to connect. [sup-duvidas-05]
> 4. When the screen shows a connected network (2G or 3G), the machine is ready. [sup-duvidas-05]
> 5. Run a communication test to check the chip's connectivity. [sup-duvidas-05]
>
> If the chip still shows no signal, you can use Wi‑Fi instead. On the home screen tap "Wi-Fi", then "Procurar Redes". Pick your network, enter the password and confirm. [sup-wifi-02][sup-wifi-01]
>
> I can propose a support ticket for T1988B with the reason "no signal". It is only opened after you confirm, and the proposal expires after 15 minutes. Do you want me to propose it?
>
> The sources don't include the communication test steps or a Get Clássica-specific procedure. I can also hand your case to a human agent if you'd like.

**Passos:**

1. **records** · ok · 3133 ms · decidido por: supervisor LLM (tool call)
   - `get_terminal_status` {} → ok · `{"ok": true, "data": {"terminals": [{"terminal_id": "T1988A", "model": "Get Smart", "connection": "wifi", "online": true, "signal": "ok", "…`
2. **faq** · partial · motivo `partial_coverage` · 6704 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/duvidas/>; <https://site.getnet.com.br/get-ajuda-configuracoes/como-configurar-o-wi-fi-na-sua-maquininha-getnet/>; <https://site.getnet.com.br/get-ajuda-erros-maquininha/erro-adq-4-83/>; <https://site.getnet.com.br/get-ajuda-configuracoes/como-configurar-o-wi-fi-na-sua-maquininha-getnet/>; <https://site.getnet.com.br/todas-as-maquininhas/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-06

**Pergunta:** How does receivables advance (antecipação) work with Getnet?

**Intenção:** knowledge (esperada knowledge) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0225 · **latência:** 12.4 s

**Resposta:**

> Getnet lets you advance credit sales, paid in full or in installments, through the Getnet Brasil app on Android and iOS. You log in with your username and password and then tap the Services menu [sup-antecipar-app-01].
>
> - **Default timing:** Debit sales are available the next day. For credit sales, you can choose to receive everything in 2 days, in 30 days, or month by month according to the card installments [sup-duvidas-antecipacao-de-vendas-13].
> - **Automatic Advance:** This is a condition for getting an exemption if you choose the "Receba Conforme suas Vendas" receiving plan. It goes through credit approval, and Getnet decides contract by contract whether to grant it [sup-duvidas-100].
> - **Registry rules:** Since June 7, 2021, Central Bank Resolution 4.734 and Circular 3.952 have set conditions for using card receivables in credit operations. Receivables must be registered with a registry so they can be negotiated [sup-duvidas-antecipacao-de-vendas-08].
> - **Lien (gravame):** This is a guarantee you give Getnet for a loan. Your sales on Getnet and other acquirers are paid into your Get Conta, up to the loan's outstanding balance [sup-duvidas-antecipacao-de-vendas-05].
>
> I can also request an advance for you. You would need to confirm it, and then a human agent would have to approve it before it runs.
>
> The sources don't give the advance fee or rate, or the app steps after the Services menu. I can hand you to a human agent for those details if you'd like.

**Passos:**

1. **faq** · partial · motivo `partial_coverage` · 4724 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/get-ajuda-antecipacao-de-venda/como-antecipar-sua-vendas-pelo-app/>; <https://site.getnet.com.br/duvidas/>; <https://site.getnet.com.br/duvidas/antecipacao-de-vendas/>; <https://site.getnet.com.br/duvidas/antecipacao-de-vendas/>; <https://site.getnet.com.br/duvidas/antecipacao-de-vendas/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-07

**Pergunta:** What's the euro exchange rate today?

**Intenção:** general (esperada general) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0144 · **latência:** 8.8 s

**Resposta:**

> The euro is R$ 6.1482 to buy and R$ 6.1500 to sell, according to Banco Central do Brasil (PTAX). That is the closing quote from 2026-11-03, not today's. There is no PTAX bulletin for 2026-11-04 yet, so this is the latest quote available.
>
> Source: https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes

**Passos:**

1. **faq** · ok · 4088 ms · decidido por: supervisor LLM (tool call)
   - `currency_rate` {"currency": "EUR", "date": "2026-11-04"} → ok

**Fontes:** <https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-08

**Pergunta:** My card machine is showing a transaction decline error.

**Intenção:** troubleshoot (esperada troubleshoot) · **rota:** router → records → faq · **replanos:** ['records:need->faq (venda recusada: o que fazer vem da central de ajuda; maquininha offline: o passo)'] · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0324 · **latência:** 17.6 s

**Resposta:**

> Your last 7 days show 2 declined transactions, totaling R$ 285.00. Both were on terminal T1988A.
> - TX1007: today at 09:20, credit, R$ 210.00. Code 51 means insufficient funds.
> - TX1008: today at 09:45, debit, R$ 75.00. Code 05 means not authorized by the issuer.
>
> T1988A is online on wifi with good signal. Your other terminal, T1988B, has been offline with no signal for 3.2 hours. The data doesn't link T1988B to these declines.
>
> I can propose a support ticket for T1988B for "no signal". Nothing runs until you confirm. I can also hand your case to a human agent if you'd like.

**Passos:**

1. **records** · ok · 3942 ms · decidido por: supervisor LLM (tool call)
   - `list_transactions` {"status": "declined", "period": "last_7_days"} → ok · `{"ok": true, "data": {"period": "last_7_days", "status": "declined", "today": "2026-11-04", "transactions": [{"transaction_id": "TX1007", "…`
   - `get_terminal_status` {} → ok · `{"ok": true, "data": {"terminals": [{"terminal_id": "T1988A", "model": "Get Smart", "connection": "wifi", "online": true, "signal": "ok", "…`
2. **faq** · insufficient · motivo `not_in_sources` · 6418 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/get-ajuda-erros-maquininha/erro-adq-4-91/>; <https://site.getnet.com.br/duvidas/>; <https://site.getnet.com.br/crediario/>; <https://site.getnet.com.br/get-ajuda-erros-maquininha/erro-adq-4-83/>; <https://site.getnet.com.br/todas-as-maquininhas/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-09

**Pergunta:** How many installments can I split a sale into with the crediário?

**Intenção:** knowledge (esperada knowledge) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0159 · **latência:** 12.7 s

**Resposta:**

> You can split a sale into up to 48 installments with the Crediário. The maximum term and the interest rate depend on the card issuer, and each issuer sets its own installment limit under its credit policies [prod-crediario-02][prod-crediario-01][sup-duvidas-crediario-03].
>
> To see the interest for a specific purchase, run a simulation on the card machine:
> 1. Insert the card.
> 2. Enter the amount.
> 3. Choose credit > crediário.
>
> You can print the simulation receipt for the customer. The simulation is for reference only. It is subject to credit analysis, and the issuer approves the transaction when the customer contracts it [sup-duvidas-crediario-03].
>
> You receive the full sale amount within 2 business days, with a single fee and no anticipation cost [prod-crediario-02].

**Passos:**

1. **faq** · ok · 4204 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/crediario/>; <https://site.getnet.com.br/crediario/>; <https://site.getnet.com.br/duvidas/crediario/>; <https://site.getnet.com.br/crediario/>; <https://site.getnet.com.br/duvidas/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}

## official-10

**Pergunta:** Can I sell through WhatsApp using the Payment Link?

**Intenção:** knowledge (esperada knowledge) · **rota:** router → faq · **replanos:** nenhum · **caminho:** supervisor LLM (laço de tool use) · **custo:** US$ 0.0181 · **latência:** 10.7 s

**Resposta:**

> Yes, you can sell through WhatsApp with the Payment Link. You send the link to customers on WhatsApp, social media, email or SMS. They click it, choose a payment method and complete the purchase [sup-duvidas-link-de-pagamento-12, prod-link-de-pagamento-01].
>
> To create the link [prod-link-de-pagamento-04]:
> 1. Log in to the Minha Conta portal or the Getnet Brasil app.
> 2. Go to Products and Services, select Payment Link, then Create Payment Link.
> 3. Fill in the product, shipping and payment options.
> 4. Click share or copy, then send the link wherever you like.
>
> You pay for the plan you subscribed to, plus the card fee. The card fee depends on the number of installments and how many days you want to wait for the money [sup-duvidas-link-de-pagamento-12]. Every Payment Link transaction goes through the antifraud check [sup-duvidas-link-de-pagamento-07].

**Passos:**

1. **faq** · ok · 4522 ms · decidido por: supervisor LLM (tool call)

**Fontes:** <https://site.getnet.com.br/duvidas/link-de-pagamento/>; <https://site.getnet.com.br/link-de-pagamento/>; <https://site.getnet.com.br/link-de-pagamento/>; <https://site.getnet.com.br/pagamentos-pelo-whatsapp/>; <https://site.getnet.com.br/duvidas/link-de-pagamento/>
**Checagens:** {'intent': True, 'route': True, 'handoff': True, 'handoff_outcome': True, 'language': True, 'numbers': True, 'claims': True, 'facts': True, 'resolved': True}
