# Importando as classes principais do Airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator # Estruturação apenas
from airflow.operators.bash_operator import BashOperator # rodar comandos no terminal

from datetime import datetime

# argumentos padrão para todas as tarefas da Dag
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# criação da Dag
with DAG(dag_id='queue_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # task para a fila ssd
    t_1_ssd = BashOperator(task_id='t_1_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    t_2_ssd = BashOperator(task_id='t_2_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    t_3_ssd = BashOperator(task_id='t_3_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    # task para a fila cpu
    t_4_cpu = BashOperator(task_id='t_4_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')

    t_5_cpu = BashOperator(task_id='t_5_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')

    # task para a fila spart
    t_6_spark = BashOperator(task_id='t_6_spark', bash_command='echo "Spark dependency task"', queue='worker_spark')

    # task final para agrupar o termino das outras tarefas
    task_7 = DummyOperator(task_id='task_7')

    # todas as tarefas da lista são independentes, podem rodar 
    # desde que consigam rodar em suas filas
    # task 7 só roda depois que todas as outras terminarem
    [t_1_ssd, t_2_ssd, t_3_ssd, t_4_cpu, t_5_cpu, t_6_spark] >> task_7
        