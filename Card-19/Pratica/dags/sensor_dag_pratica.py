from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

# argumentos padrão para as tarefas
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1),
    'catchup': False,
}

# criação da Dag
with DAG(dag_id='sensor_dag', default_args=default_args, schedule_interval=None) as dag:

    # task que fica com um sensor na tarefa do triggered dag
    task_sensor = ExternalTaskSensor(
        task_id='task_sensor',
        external_dag_id='triggered_dag',
        external_task_id='task_get_values',
    )

    # task final
    final = BashOperator(
        task_id='final',
        bash_command='echo "Triggered Dag finalizada! Sensor liberado."'
    )

    # fluxo das tasks
    task_sensor >> final