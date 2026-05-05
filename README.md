# delivery-tipping-experiment-lab

## Português

### Visão geral

`delivery-tipping-experiment-lab` é um projeto de experimentação de produto para marketplace, inspirado em uma pergunta clássica de entrevista: **como medir o sucesso de um novo recurso de gorjetas e decidir se ele deve ser lançado**.

O experimento compara:

- `control`
  - experiência atual de checkout
- `treatment`
  - nudge com âncora de gorjeta mais forte durante o pedido

### Objetivo analítico

O objetivo não é maximizar gorjeta isoladamente. O objetivo correto é medir se o novo recurso:

- aumenta gorjeta por sessão exposta;
- melhora o incentivo econômico do entregador;
- sem prejudicar conversão ou aceitação do pedido.

### Desenho experimental

- unidade de randomização: `checkout_session`
- hipótese principal:
  - o novo nudge aumenta a monetização por gorjeta sem machucar o marketplace

### Métricas

Métrica principal:

- `gross_tip_per_session`

Métricas secundárias:

- `tip_attach_rate`
- `avg_tip_per_completed_order`

Guardrails:

- `checkout_conversion_rate`
- `driver_acceptance_rate`

### Estrutura dos dados

Cada linha representa uma sessão de checkout com campos como:

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

### Técnicas utilizadas

- simulação de experimento A/B
- definição de métrica primária orientada a produto
- lift absoluto e relativo
- intervalo de confiança aproximado por diferença de médias
- análise segmentada por região e tipo de usuário
- recomendação de rollout com guardrails

### Ferramentas e bibliotecas

- `Python`
- `csv`
- `json`
- `math`
- `pathlib`
- `random`
- `unittest`

### Contrato do relatório

O artefato [tipping_experiment_report.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/data/processed/tipping_experiment_report.json) inclui:

- metadados do experimento
- contagem por variante
- primary metric
- secondary metrics
- guardrails
- intervalos de confiança aproximados
- análise segmentada
- recomendação final

### Resultados atuais

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

- o maior ganho está em `gross_tip_per_session`;
- a conversão não piora de forma relevante;
- a aceitação do entregador melhora, mas ainda justificaria acompanhamento em rollout progressivo.

### Arquivos principais

- [main.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/main.py)
- [src/data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/src/data_factory.py)
- [src/modeling.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/src/modeling.py)
- [tests/test_project.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/tests/test_project.py)

### Como executar

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

### Como defender em entrevista

> Eu mediria sucesso de um novo recurso de gorjetas com uma métrica primária que balanceie valor de gorjeta e impacto em conversão, como gross tip per exposed session. Depois olharia tip attach rate e average tip como métricas secundárias, e manteria checkout conversion e driver acceptance como guardrails.

## English

### Overview

`delivery-tipping-experiment-lab` is a marketplace product experimentation project built around a common interview question: **how to measure the success of a new tipping feature and decide whether it should ship**.

The experiment compares:

- `control`
  - current checkout experience
- `treatment`
  - stronger tip-anchor nudge during checkout

### Analytical objective

The goal is not to maximize tip amount in isolation. The correct goal is to measure whether the feature:

- increases tip revenue per exposed session;
- improves courier-side economic incentives;
- without hurting conversion or order acceptance.

### Experimental design

- unit of randomization: `checkout_session`
- core hypothesis:
  - the new nudge increases tip monetization without damaging marketplace health

### Metrics

Primary metric:

- `gross_tip_per_session`

Secondary metrics:

- `tip_attach_rate`
- `avg_tip_per_completed_order`

Guardrails:

- `checkout_conversion_rate`
- `driver_acceptance_rate`

### Data structure

Each row represents a checkout session with fields such as:

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

### Techniques used

- A/B experiment simulation
- product-aligned primary metric design
- absolute and relative lift
- approximate confidence interval using difference in means
- segmented analysis by region and user type
- rollout recommendation based on guardrails

### Tools and libraries

- `Python`
- `csv`
- `json`
- `math`
- `pathlib`
- `random`
- `unittest`

### Report contract

The artifact [tipping_experiment_report.json](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/data/processed/tipping_experiment_report.json) includes:

- experiment metadata
- variant counts
- primary metric
- secondary metrics
- guardrails
- approximate confidence intervals
- segmented analysis
- final recommendation

### Current results

- `dataset_source = synthetic_delivery_tipping_experiment`
- `session_count = 1200`
- `variant_counts = {'control': 600, 'treatment': 600}`
- `primary_metric_gross_tip_per_session absolute_lift = 0.4862`
- `primary_metric_gross_tip_per_session ci = [0.2318, 0.7405]`
- `secondary_metric_tip_attach_rate absolute_lift = 0.0717`
- `guardrail_checkout_conversion_rate absolute_lift = 0.0417`
- `guardrail_driver_acceptance_rate absolute_lift = 0.0483`
- `decision = ship_treatment`

### Main files

- [main.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/main.py)
- [src/data_factory.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/src/data_factory.py)
- [src/modeling.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/src/modeling.py)
- [tests/test_project.py](/Users/flaviagaia/Documents/CV_FLAVIA_CODEX/delivery-tipping-experiment-lab/tests/test_project.py)

### How to run

```bash
python3 main.py
python3 -m unittest discover -s tests -v
python3 -m py_compile main.py src/data_factory.py src/modeling.py tests/test_project.py
```

### Interview framing

> I would measure the success of a new tipping feature with a primary metric that balances tip value and conversion impact, such as gross tip per exposed session. Then I would look at tip attach rate and average tip as secondary metrics, while keeping checkout conversion and driver acceptance as guardrails.
