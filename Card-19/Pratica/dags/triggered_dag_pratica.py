from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# argumentos padrão
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1),
    'catchup': False,
}

# função que recebe as variaveis de ambientes passado pelo trigger
def get_values(**kwargs):
    values = kwargs['dag_run'].conf
    print(f"Parâmetros recebidos da DAG 1: {values}")

# criação da Dag
with DAG(dag_id='triggered_dag', default_args=default_args, schedule_interval=None) as dag:

    # task que executa a função de pegar os valores
    task_get_values = PythonOperator(
        task_id='task_get_values',
        python_callable=get_values,
        provide_context=True
    )