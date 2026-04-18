import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# argumentos padrão
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    }

# criação da Dag
with DAG(dag_id="sleep_dag", default_args=default_args, schedule_interval="@daily") as dag:

    # task 
    t1 = DummyOperator(task_id="t1")

    # task que coloca o terminal em espera por 30s
    t2 = BashOperator(
            task_id="t2",
            bash_command="sleep 30"
        )
    
    # executa a task 2 depois que a task 1 finaliza
    t1 >> t2 