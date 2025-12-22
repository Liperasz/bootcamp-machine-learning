# importa a DAG e o BashOperator
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# lidar com os tempos
from datetime import datetime, timedelta

# funções de callback para sucesso e falha
def on_success_task(dict):
    print("on_success_task")
    print(dict)

def on_failure_task(dict):
    print("on_failure_task")
    print(dict)

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2025, 1, 1), # data de inicio do DAG
    'owner': 'Airflow', # dono do DAG
    'retries': 3, # numero de tentativas
    'retry_delay': timedelta(seconds=60), # tempo de espera entre as tentativas
    'emails': ['owner@test.com'], # email generico
    'email_on_failure': True, # envia email se falhar
    'email_on_retry': False, # nao envia email se tentar novamente
    'on_success_callback': on_success_task, # função de callback para sucesso
    'on_failure_callback': on_failure_task, # função de callback para falha
    'exec_timeout': timedelta(seconds=60) # tempo maximo de execucao da tarefa
}

# funções de callback para sucesso e falha do DAG
def on_success_dag(dict):
    print("on_success_dag")
    print(dict)

def on_failure_dag(dict):
    print("on_failure_dag")
    print(dict)

# definicao do DAG
with DAG(dag_id='alert_dag', # id do DAG
         schedule_interval="0 0 * * *", # executa diariamente a meia noite
         default_args=default_args, # argumentos padrão
         catchup=True, # nao executa tarefas passadas
         dagrun_timeout=timedelta(seconds=75), # tempo maximo de execucao do DAG
        on_success_callback=on_success_dag, # função de callback para sucesso do DAG
         on_failure_callback=on_failure_dag) as dag: # função de callback para falha do DAG
    
    # Task 1
    t1 = BashOperator(task_id='t1', bash_command="exit 1")
    
    # Task 2
    t2 = BashOperator(task_id='t2', bash_command="echo 'second task'")

    # define a ordem de execucao das tarefas
    t1 >> t2