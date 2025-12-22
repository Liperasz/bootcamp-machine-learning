from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

# argumentos padrão das tarefas do DAG
default_args = {
    'start_date': datetime(2019, 3, 29, 1),
    'owner': 'Airflow'
}

# definindo id, agendando a cada hora com a função delta e passando os argumentos padrão
with DAG(dag_id='start_and_schedule_dag', schedule_interval=timedelta(hours=1), default_args=default_args) as dag:
    
    # tarefa 1
    dummy_task_1 = DummyOperator(task_id='dummy_task_1')
    
    # tarefa 2
    dummy_task_2 = DummyOperator(task_id='dummy_task_2')
    
    # ordem das tarefas
    dummy_task_1 >> dummy_task_2
    
    # logs deixado para aprendizado

    # calcula os próximos datas de execução do DAG
    run_dates = dag.get_run_dates(start_date=dag.start_date)

    # pega a última data de execução planejada
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None

    # imprime informações do DAG
    print('[DAG:start_and_schedule_dag] start_date: {0} - schedule_interval: {1} - Last execution_date: {2} - next execution_date {3} in UTC'.format(
        dag.default_args['start_date'], 
        dag._schedule_interval, 
        dag.latest_execution_date, 
        next_execution_date
        ))