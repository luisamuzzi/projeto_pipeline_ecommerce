# **Pipeline de dados de e-commerce**

### Resumo

Este projeto implementou um pipeline de dados para e-commerce, com foco em análises de vendas e previsão de churn, desde o armazenamento dos dados brutos em banco de dados PostgreSQL, modelagem dos dados em camadas usando dbt, orquestração do pipeline com Apache Airflow (via Astro CLI) e geração de relatórios semanais com envio automatizado via Telegram.

Scripts Python foram usados para:

- Gerar dados fictícios para simulação de dados de e-commerce.

- Gerar relatório semanal com resumo de métricas a ser enviado via Telegram.

O dbt-core foi usado para:

- Realizar transformações nos dados em cada camada. 

O Apache Airflow foi usado para:

- Criação da DAG de orquestração do pipeline.


### Índice

- [1. Ferramentas utilizadas](https://github.com/luisamuzzi/projeto_pipeline_ecommerce?tab=readme-ov-file#1-ferramentas-utilizadas)
- [2. Estrutura do projeto](https://github.com/luisamuzzi/projeto_pipeline_ecommerce?tab=readme-ov-file#2-estrutura-do-projeto)
- [3. Conclusão](https://github.com/luisamuzzi/projeto_pipeline_ecommerce?tab=readme-ov-file#3-conclus%C3%A3o)
- [4. Referências](https://github.com/luisamuzzi/projeto_pipeline_ecommerce?tab=readme-ov-file#4-refer%C3%AAncias)

### 1. Ferramentas utilizadas

**Linguagens:**

- Python: linguagem de programação principal.

- SQL: usada para transformações de dados.

**Bibliotecas Python:**

- `pandas`: usada para manipulações de dados.

- `faker`: usada para gerar dados fictícios.

- `random`: usada no processo de geração dos dados fictícios.

- `datetime`: usada no processo de geração dos dados fictícios e criação da DAG.

- `os`: usada para obter os valores das variáveis de ambiente.

- `dotenv`: usada para gerenciar as variáveis de ambiente.

- `pathlib`: usada para lidar com caminhos.

- `requests`: usada para enviar mensagem via API do bot do Telegram.

- `airflow`: usada para criar a DAG.

- `airflow.operators.bash`: usada para importar o operador bash.

**Banco de dados:**

- PostgreSQL: usado para armazenar os dados brutos em tabelas e os dados transformados em cada camada como views.

**Transformação de dados:**

- dbt (Data build tool): usado para realizar tratamentos/transformações nos dados usando SQL. 

**Envio do relatório semanal:**

- Bot do Telegram: usado para envio dos relatórios.

- API do Telegram: usada para envio da mensagem contendo os dados do relatório.

**Orquestração do Pipeline:**

- Apache Airflow: usado para orquestrar a automação do pipeline de dados.

### 2. Estrutura do projeto

**Geração dos dados:**

O [script python](scripts/generate_fake_data.py) gera os dados fictícios simulando um e-commerce. Os dados gerados são armazenados em arquivos CSV na pasta `dbt_ecommerce/seeds`. Os arquivos gerados são:

- `cancelamentos.csv`: order_id, cancel_reason, cancel_date

- `customers.csv`: customer_id, name, email, signup_date

- `order_items.csv`: order_id, product_id, quantity

- `orders.csv`: order_id, customer_id, order_date, status

- `products.csv`: product_id, name, category, cost, price

**Transformação de dados com dbt:**

O dbt realiza a carga dos dados no banco de dados PostgreSQL e o processamento/transformação, fazendo renomeação de colunas, conversão de tipos de dados e criação de colunas por meio de cálculos adicionais, conforme descrito nos scripts SQL na pasta `dbt_ecommerce/models`:

- Camada staging (`dbt_ecommerce/models/staging`): ajustes simples de tipos de dados e nomes de colunas; criação da coluna de margem de lucro (`price - cost`).

- Camada intermediate (`dbt_ecommerce/models/intermediate`): transformações complexas para criação de fonte de dados para modelos de previsão de churn.

- Camada marts (`dbt_ecommerce/models/marts`): modelagem de dados para consumo por ferramentas de BI e relatórios.  

Em cada camada, foi criado um arquivo `schema.yml` com testes de qualidade e integridade dos dados para colunas pertinentes, como `not_null` e `unique`.

**Geração e envio do relatório:**

O [script python](scripts/generate_report.py) gera um relatório com as principais métricas e o envia por meio de um bot no Telegram. As métricas são:

- Total de pedidos
- Total de pedidos cancelados
- Taxa de cancelamento
- Produto mais caro

**Criação da DAG no Airflow:**

O [script python](dags/ecommerce_dag.py) orquestra o pipeline por meio de uma DAG de execução semanal. As tarefas da DAG são:

- Task 01 - `generate_fake_data`: Executa o script de geração de dados fictícios (`generate_fake_data.py`).

- Task 02 - `dbt_seed`: Executa o comando `dbt seed` para carga dos dados fictícios no banco de dados.

- Task 03 - `dbt_run`: Executa o comando `dbt run` para rodar os modelos dbt de transformação de dados.

- Task 04 - `dbt_test`: Executa o comando `dbt test` para realizar os testes de qualidade de dados descritos nos arquivos `schema.yml`.

- Task 05 - `generate_report`: Executa o script de geração do relatório e envio pelo Telegram (`generate_report.py`).

### 3. Conclusão

Este projeto criou um pipeline de dados para e-commerce por meio de scripts Python, SQL (via dbt) e Apache Airflow. Para tanto, foram utilizadas as bibliotecas `airflow`, `airflow.operators.bash`, `pandas`, `os`, `dotenv`, `requests` e o dbt para realização de transformações nos dados, que foram armazenados no PostgreSQL em camadas por meio de views. O Airflow foi usado para orquestração do pipeline por meio de uma DAG de execução semanal.

### 4. Referências

Esse projeto foi desenvolvido como parte do curso EBA (https://renatabiaggi.com/eba/).