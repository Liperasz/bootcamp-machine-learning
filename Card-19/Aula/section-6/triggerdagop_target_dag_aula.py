import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# argumentos padrão
default_args = {
    "start_date": airflow.utils.dates.days_ago(1), 
    "owner": "Airflow"
}

# imprime as variaveis de ambiente enviados pela task
def remote_value(**context):
    print("Value {} for key=message received from the controller DAG".format(context["dag_run"].conf["message"]))

# cria a dag
with DAG(dag_id="triggerdagop_target_dag", default_args=default_args, schedule_interval=None) as dag:

    # task que usa a função python para printar as variaveis de ambiente
    t1 = PythonOperator(
            task_id="t1",
            provide_context=True,
            python_callable=remote_value, 
        )

    # task executa um comando echo
    t2 = BashOperator(
        task_id="t2",
        bash_command='echo Message: {{ dag_run.conf["message"] if dag_run else "" }}')

    # task que deixa a dag esperando por 30s
    t3 = BashOperator(
        task_id="t3",
        bash_command="sleep 30"
    )