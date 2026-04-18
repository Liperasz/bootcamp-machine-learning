import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# argumentos padrão das dags
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    }

# criação da Dag
with DAG(dag_id="externaltasksensor_dag", default_args=default_args, schedule_interval="@daily") as dag:


    # sensor que monitora uma Dag externa
    sensor = ExternalTaskSensor(
        task_id='sensor',
        external_dag_id='sleep_dag', # nome da Dag que ele está monitorando 
        external_task_id='t2' # id da tarefa especifica que está monitorando
    )

    # tarefa final
    last_task = DummyOperator(task_id="last_task")

    # executa a tarefa final depois que o sensor identificar que a tarefa externa foi concluida
    sensor >> last_task