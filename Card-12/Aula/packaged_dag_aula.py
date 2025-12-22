from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# chamando as funções do arquivo helpers.py
from functions.helpers_aula import first_task, second_task, third_task

from datetime import datetime

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

# definindo id, agendando todos os dias à meia-noite e passando os argumentos padrão
with DAG(dag_id='packaged_dag', schedule_interval="0 0 * * *", default_args=default_args) as dag:

    # As tarefas chamam as funções importadas do arquivo helpers.py
    # tarefa 1
    python_task_1 = PythonOperator(task_id='python_task_1', python_callable=first_task)

    # tarefa 2
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task)

    # tarefa 3
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)

    # definindo a ordem de execução das tarefas
    python_task_1 >> python_task_2 >> python_task_3