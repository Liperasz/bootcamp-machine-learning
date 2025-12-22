# importando dag e operador
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2025, 1, 1),
    'owner': 'Airflow'
}

# definindo id, agendando todos os dias à meia-noite, passando os argumentos padrão e desabilitando o catchup
with DAG(dag_id='backfill', schedule_interval="0 0 * * *", default_args=default_args, catchup=False) as dag:
    
    # Tarefa 1
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'")
    
    # Tarefa 2
    bash_task_2 = BashOperator(task_id='bash_task_2', bash_command="echo 'second task'")

    # definindo a ordem de execução das tarefas
    bash_task_1 >> bash_task_2