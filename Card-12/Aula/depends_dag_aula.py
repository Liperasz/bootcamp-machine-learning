from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2025, 1, 1),
    'owner': 'Airflow'
}

# funções das tarefas 2 e 3
# a linha comentada serve para simular uma falha na tarefa
def second_task():
    print('Hello from second_task')
    # raise ValueError('This will turns the python task in failed state')

def third_task():
    print('Hello from third_task')
    # aise ValueError('This will turns the python task in failed state')

with DAG(dag_id='depends_task', schedule_interval="0 0 * * *", default_args=default_args) as dag:
    
    # tarefa 1
    # wait for downstream faz com que a tarefa espere todas as tarefas dependentes serem concluídas antes de marcar como concluída
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'", wait_for_downstream=True)
    
    # tarefa 2
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task)

    # tarefa 3
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)

    bash_task_1 >> python_task_2 >> python_task_3