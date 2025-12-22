from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2025, 1, 1),
    'email': "owner@test.com"
}

# função para a tarefa 2 que retorna a string 'process'
def process():
    return 'process'


# definindo id, agendando todos os dias à meia-noite, passando os argumentos padrão e desabilitando o catchup
with DAG(dag_id='tst_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # tarefa 1
    task_1 = DummyOperator(task_id='task_1')

    # tarefa 2
    task_2 = PythonOperator(task_id='task_2', python_callable=process)

    # tarefas 3, 4 e 5 criadas em loop
    tasks = [DummyOperator(task_id='task_{0}'.format(t)) for t in range(3, 6)]

    # tarefa 6
    task_6 = DummyOperator(task_id='task_6')

    # definindo a ordem de execução das tarefas
    task_1 >> task_2 >> tasks >> task_6
        