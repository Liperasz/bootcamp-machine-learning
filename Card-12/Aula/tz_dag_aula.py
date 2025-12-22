# importando o pendulum, biblioteca de gerenciamento de timezone
import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator

from datetime import timedelta, datetime

# definindo o timezone local como Europa/Paris
local_tz = pendulum.timezone("Europe/Paris")

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2025, 3, 29, 2, tzinfo=local_tz), # define o horario de inicio com o fusio horario especificado
    'owner': 'Airflow',
    'email': 'owner@test.com',
    'retries': 3,
    'retry_delay': timedelta(minutes=5) 
}

# definindo a dag com o agendamento as 2 da manha no fusuo horario especificado
with DAG(dag_id='tz_dag', schedule_interval="0 2 * * *", default_args=default_args) as dag:

    # tarefa 
    dummy_task = DummyOperator(task_id='dummy_task')
    
    # logs deixado para aprendizado

    # calcula os próximos datas de execução do DAG
    run_dates = dag.get_run_dates(start_date=dag.start_date)
    # pega a última data de execução planejada
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None
    
    # imprime informações do DAG
    print('datetime from Python is Naive: {0}'.format(timezone.is_naive(datetime(2019, 9, 19))))
    print('datetime from Airflow is Aware: {0}'.format(timezone.is_naive(timezone.datetime(2019, 9, 19)) == False))
    print('[DAG:tz_dag] timezone: {0} - start_date: {1} - schedule_interval: {2} - Last execution_date: {3} - next execution_date {4} in UTC - next execution_date {5} in local time'.format(
        dag.timezone, 
        dag.default_args['start_date'], 
        dag._schedule_interval, 
        dag.latest_execution_date, 
        next_execution_date,
        local_tz.convert(next_execution_date) if next_execution_date is not None else None
        ))