import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.bash import BashOperator

# Carregar variáveis de ambiente do aequivo .env
load_dotenv()

# Armazenar variáveis de ambiente
SCRIPTS_PATH = os.getenv('SCRIPTS_PATH')
DBT_DIR = os.getenv('DBT_DIR')

default_args = {
    'owner': 'Luisa',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'ecommerce_analytics_dag',
    default_args=default_args,
    start_date=datetime(2025, 12, 15),
    schedule='@weekly',
    catchup=False,
    tags=['ecommerce', 'analytics', 'dbt', 'churn']
) as dag:
    #--------------- task 01: gerar os dados fake ---------------
    t1_generate_data = BashOperator(
        task_id = 'generate_fake_data',
        bash_command = f'python {os.path.join(SCRIPTS_PATH, 'generate_fake_data.py')}'
    )

    #--------------- task 02: executar o dbt seed ---------------
    t2_dbt_seed = BashOperator(
        task_id = 'dbt_seed',
        bash_command = f'cd {DBT_DIR} && dbt seed --profiles-dir /usr/local/airflow/include/.dbt'
    )

    #--------------- task 03: executar o dbt run --------------- 
    t3_dbt_run = BashOperator(
        task_id = 'dbt_run',
        bash_command = f'cd {DBT_DIR} && dbt run --profiles-dir /usr/local/airflow/include/.dbt'
    )

    #--------------- task 04: executar o dbt test --------------- 
    t4_dbt_test = BashOperator(
        task_id = 'dbt_test',
        bash_command = f'cd {DBT_DIR} && dbt test --profiles-dir /usr/local/airflow/include/.dbt'
    )

    #--------------- task 05: gerar o relatorio --------------- 
    t5_generate_report = BashOperator(
        task_id = 'generate_report',
        bash_command = f'python {os.path.join(SCRIPTS_PATH, 'generate_report.py')}'
    )

    # Definir a ordem de execução das tasks
    t1_generate_data >> t2_dbt_seed >> t3_dbt_run >> t4_dbt_test >> t5_generate_report