# Regra do dono: melhoria contínua a cada rodada

Pedido do dono (03/11/2026): "a cada nova rodada você precisa pegar os pontos bons e reforçá-los e os pontos ruins e
melhorá-los, pesquisando na web se possível, no git, no bench etc. Precisa ser melhora contínua; senão só estamos
gastando dinheiro e tokens à toa."

## O ciclo (obrigatório em toda rodada: ensaio, avaliação simulada, bateria ao vivo, produção)

1. **Medir com o avaliador** (régua cega calibrada) logo depois de cada mudança relevante. Rodar bateria ao vivo não
   é avaliar: a nota só muda quando a régua roda de novo sobre o commit novo. Nunca repetir a nota antiga como se
   fosse atual.
2. **Ler o resultado inteiro**: as perdas (TOP8), os ganhos (TOP5) e os números citados (arquivo:linha).
3. **Pontos ruins → corrigir na raiz**, do maior peso para o menor. Para cada um: causa no código/evidência, correção,
   teste que prova, e o número que deve mudar na próxima rodada.
4. **Pontos bons → reforçar**: deixar mais visível no README/RESULTS, com prova commitada; não deixar regredir
   (teste ou checagem do `check.py`).
5. **Pesquisar antes de inventar**: web (desafios e práticas parecidas), git (o que já funcionou nas rodadas e
   tentativas anteriores, `docs/kit/CHANGELOG.md`), benches (Skywalker 10, nelsondell 9,5), feedbacks reais.
   Só ideias; nada de copiar código ou texto (fonte em PROCEDENCIA).
6. **Registrar a rodada**: nota por critério antes → depois, o que mudou, o que não mudou e por quê. Se a nota não
   subiu, a próxima rodada começa explicando o motivo, não repetindo a mesma receita.
7. **Não gastar à toa**: nenhuma bateria ao vivo ou avaliação sem uma hipótese do que ela vai mostrar; rodar só os
   splits afetados pela mudança; parar o que ficou velho (código mudou) em vez de deixar terminar.

## Diretriz 2 do dono (03/11/2026): o kit de produção é atualizado a cada rodada até bater a meta

"Com essas melhorias você atualiza o kit que rodará em produção de forma recorrente até batermos a nota mínima ou
superá-la." Toda correção entra primeiro no kit (`kit-v5.4.0`, testes verdes), depois no ensaio, e a rodada
seguinte mede o kit atualizado. O ciclo só para quando a meta é batida.

**Meta para ir à produção: ver "Ordem do dono" no fim (vale a última: ≥ 9,0 na nossa régua, ensaio e cronometrado).**
Antes (03/11, à noite) foi ≥ 8,9
(calibração: 8,73 no simulador = 9,5 real do nelsondell; 8,9 ≈ 9,8 real). Ao bater, avisar o dono na hora.
Abaixo disso não se roda produção (é desperdício). Limite da tentativa: 58 min.

## Diretriz 3 do dono (03/11/2026): rodadas rápidas, errar rápido para corrigir rápido

"Busque ser mais eficiente e mais rápido nas correções e nas rodadas... errar rápido para corrigir rápido."

Como (estratégias do loop curto; a régua completa só no fim de cada lote):
- **Loop interno de minutos, não de horas**: mudança → teste focado → rescore das respostas GRAVADAS (sem LLM) →
  bateria ao vivo só do split afetado, repeat 1, poucos casos → régua. A bateria integral (US$ ~17, ~25 min) só
  antes da avaliação final do lote.
- **Medir em paralelo com a correção**: enquanto um split roda ao vivo, corrigir o próximo item; nunca esperar ocioso.
- **Pré-régua mecânica** (`scripts/check.py` + checagens das deduções já conhecidas) antes de gastar a régua cega:
  evidência ao vivo do commit atual, oficiais com fato, sem tarja, sem split abortado, sem escalada desnecessária.
- **Evidência sempre do código atual**: código mudou → só os splits afetados são re-rodados na hora; nada de medir
  commit velho e esperar.
- **Uma sessão de bateria por vez, com relatório curto**; a sessão-mãe não fica parada esperando.

## Texto do dono, palavra por palavra (03/11/2026) — seguir a partir de agora, em toda sessão

> a cada nova rodada você precisa pegar os pontos bons e reforça-los e os pontos ruins e melhora-los, pesquisando na
> web se possivel, no git, no bench e etc. precisa ser uma coisa de melhora continua se não só estamos gastando
> dinheiro e tokens a toa. Salve isso na sua memória persistente. E com essas melhorias você atualiza o kit que rodará
> em produção de forma recorrente até batermos a nota mínima ou supera-la. Não entendo porquê de tanta dificuldade,
> estamos trabalhando nisso a dias já. salve essas duas diretrizes na sua memória persistente, para rodarmos o teste
> em produção ainda hoje com uma nota do nosso avaliado igual ou maior que 9. Além disso busque ser mais eficiente e
> mais rápido nas correções e nas rodadas, estamos perdendo muito tempo, deve haver estratégias de código na WEB, no
> git ou no bench que reduza, todo esse tempo que levamos entre rodadas, precisa ser uma coisa mais rápida, errar
> rápido para corrigir rápido. salve isso tambem.

Depois disso o dono disse: "Vamos tentar chegar em 8,9 ainda hoje. Não importa o horário, e ai você me manda um
lembrete quando alcançar esse patamar." → meta em vigor: ≥ 8,9 no nosso avaliador; avisar o dono quando bater.

## Ordem do dono (03/11/2026, noite) — gate em 3 passos, tudo cabendo em 60 min

1. O ensaio (sem relógio) precisa dar **≥ 9,0 na NOSSA régua** (média de 2 réguas cegas por rodada).
2. Só então roda o **ensaio cronometrado de 60 min** do kit (domínio NÃO vai pré-montado no kit: o kit leva o
   motor, os scripts que automatizam os passos e o checklist do domínio em docs/kit; o domínio é montado no relógio).
3. Produção só se o cronometrado também der **≥ 9,0 na nossa régua**, dentro de 60 min no máximo.
