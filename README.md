# delivery-tipping-experiment-lab

## Português

`delivery-tipping-experiment-lab` é um projeto de **cientista de dados de marketplace** inspirado em perguntas comuns de entrevista da DoorDash: **como medir o sucesso de um novo recurso de gorjetas e como decidir se vale a pena lançar a mudança**.

O projeto simula um experimento A/B em checkout para testar uma nova estratégia de gorjetas:

- `control`
  - experiência atual de checkout
- `treatment`
  - nudge com âncora de gorjeta mais forte durante o pedido

## Objetivo analítico

O objetivo não é maximizar gorjeta isoladamente. O objetivo correto é medir se o novo recurso:

- aumenta a gorjeta total capturada pela plataforma por sessão exposta;
- melhora a experiência e o incentivo econômico dos entregadores;
- sem prejudicar conversão de checkout ou aceitação do pedido.

Essa é a lógica de produto que normalmente separa uma boa resposta de entrevista de uma resposta superficial.

## Base de dados

O runtime do projeto usa uma **base sintética** de sessões de checkout porque dados públicos de experimentos de gorjeta em delivery quase nunca existem em nível de produto.

Referência pública usada no projeto:

- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

Papel da referência:

- inspirar sinais comportamentais de marketplace envolvendo:
  - tempo
  - região
  - valor da corrida/pedido
  - gorjeta

Observação importante:

- o projeto **não afirma** que dados de táxi são equivalentes a delivery;
- a referência pública existe para apoiar a plausibilidade dos sinais;
- a análise executável é inteiramente sintética e voltada para experimentação de produto.

## O que o projeto faz

1. gera uma base local de `checkout_sessions`;
2. randomiza sessões entre `control` e `treatment`;
3. calcula métricas primárias, secundárias e guardrails;
4. estima lift absoluto, lift relativo e intervalo de confiança aproximado;
5. compara impacto por:
   - região
   - segmento de usuário
6. devolve uma recomendação final:
   - `ship_treatment`
   - ou `needs_iteration`

## Desenho experimental

### Unidade de randomização

- `checkout_session`

### Hipótese de produto

- um nudge com âncora de gorjeta mais forte pode aumentar a monetização via tips;
- mas só deve ser lançado se esse ganho não vier às custas de conversão ou da saúde de supply.

### Leitura causal esperada

O projeto foi estruturado para responder:

- o tratamento aumentou a propensão a dar gorjeta?
- o tratamento aumentou o valor de gorjeta por sessão exposta?
- o tratamento mudou a probabilidade de o pedido ser aceito?
- o tratamento prejudicou o checkout?

## Métrica principal

A métrica principal do experimento é:

- `gross_tip_per_session`

Por que ela é melhor do que olhar só `avg_tip`:

- incorpora o efeito de gorjeta;
- mas também penaliza queda de conversão;
- então evita otimizar uma UX que aumenta gorjeta apenas entre quem ainda conclui pedido.

## Métricas secundárias

- `tip_attach_rate`
- `avg_tip_per_completed_order`

## Guardrails

- `checkout_conversion_rate`
- `driver_acceptance_rate`

Esses guardrails existem porque, em um marketplace, uma mudança de tipping pode:

- ajudar o entregador;
- mas piorar conversão;
- ou afetar oferta/aceitação de forma indireta.

## Estrutura dos dados

Cada linha da amostra local representa uma sessão de checkout com campos como:

- `session_id`
- `user_id`
- `region`
- `user_segment`
- `device`
- `variant`
- `peak_hour`
- `rainy_weather`
- `basket_size`
- `order_subtotal`
- `delivery_fee`
- `converted_order`
- `tipped`
- `tip_pct`
- `tip_amount`
- `driver_accepted`

Semântica analítica dos campos principais:

- `converted_order`
  - se a sessão terminou em pedido
- `tipped`
  - se houve gorjeta
- `tip_pct`
  - percentual de gorjeta sobre subtotal
- `tip_amount`
  - valor absoluto da gorjeta
- `driver_accepted`
  - proxy de impacto do incentivo econômico no lado da oferta

## Técnicas utilizadas

- simulação de experimento A/B
- definição de métrica primária orientada a produto
- cálculo de `absolute lift`
- cálculo de `relative lift`
- intervalo de confiança aproximado por diferença de médias
- análise segmentada por região e tipo de usuário
- recomendação de lançamento baseada em guardrails

## Ferramentas e bibliotecas

- `Python`
- `csv`
- `json`
- `math`
- `pathlib`
- `random`
- `unittest`

O projeto foi mantido propositalmente sem dependências pesadas para continuar leve e reproduzível.

## Contrato do relatório

O artefato [tipping_experiment_report.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/data/processed/tipping_experiment_report.json) traz:

- metadados do experimento
- contagem por variante
- primary metric
- secondary metrics
- guardrails
- intervalos de confiança aproximados
- análise segmentada
- recomendação final de rollout

## Arquivos principais

- [main.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/main.py)
- [src/data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/src/data_factory.py)
- [src/modeling.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/src/modeling.py)
- [tests/test_project.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/tests/test_project.py)

## Resultados esperados do MVP

O treatment foi desenhado para:

- aumentar `gross_tip_per_session`;
- aumentar `tip_attach_rate`;
- manter `checkout_conversion_rate` praticamente estável;
- melhorar `driver_acceptance_rate`.

## Resultados atuais

- `dataset_source = synthetic_delivery_tipping_experiment`
- `session_count = 1200`
- `variant_counts = {'control': 600, 'treatment': 600}`
- `primary_metric_gross_tip_per_session absolute_lift = 0.4862`
- `primary_metric_gross_tip_per_session ci = [0.2318, 0.7405]`
- `secondary_metric_tip_attach_rate absolute_lift = 0.0717`
- `guardrail_checkout_conversion_rate absolute_lift = 0.0417`
- `guardrail_driver_acceptance_rate absolute_lift = 0.0483`
- `decision = ship_treatment`

Leitura honesta:

- o maior ganho está em `gross_tip_per_session`, que é a métrica mais alinhada à decisão de produto;
- a conversão não piora de forma relevante neste sample;
- a aceitação do entregador melhora, mas com intervalo de confiança que ainda justificaria acompanhamento em rollout progressivo.

## Artefatos gerados

- [data/raw/checkout_sessions.csv](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/data/raw/checkout_sessions.csv)
- [data/raw/public_dataset_reference.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/data/raw/public_dataset_reference.json)
- [data/processed/tipping_experiment_report.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/data/processed/tipping_experiment_report.json)

## Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

## Como defender em entrevista

> Eu mediria sucesso de um novo recurso de gorjetas com uma métrica primária que balanceie valor de gorjeta e impacto em conversão, como gross tip per exposed session. Depois olharia tip attach rate e average tip como métricas secundárias, e manteria checkout conversion e driver acceptance como guardrails. Esse projeto mostra exatamente esse raciocínio, incluindo segmentação e recomendação final de rollout.

## English

`delivery-tipping-experiment-lab` is a marketplace experimentation project designed around a common DoorDash-style product question: **how to measure the success of a new tipping feature and decide whether it should ship**.

The repository simulates a checkout A/B test, evaluates a product-aligned primary metric, tracks secondary metrics and guardrails, and returns a final launch recommendation. It is intentionally lightweight, reproducible, and centered on product experimentation rather than on generic ML modeling.
