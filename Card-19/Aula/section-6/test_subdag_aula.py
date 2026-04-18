import airflow

# importa a fabrica de subdags
from subdags.subdag_aula import factory_subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.sequential_executor import SequentialExecutor
from airflow.executors.celery_executor import CeleryExecutor

# nome da Deg
DAG_NAME="test_subdag"

# argumentos padrão
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

# cria uma dag
with DAG(dag_id=DAG_NAME, default_args=default_args, schedule_interval="@once") as dag:

    # task de inicio
    start = DummyOperator(
        task_id='start'
    )

    # 2 subdags que executam em sequencia 
    subdag_1 = SubDagOperator(
        task_id='subdag-1',
        subdag=factory_subdag(DAG_NAME, 'subdag-1', default_args),
        executor=SequentialExecutor()
    )

    # task aleatória
    some_other_task = DummyOperator(
        task_id='check'
        )

    subdag_2 = SubDagOperator(
        task_id='subdag-2',
        subdag=factory_subdag(DAG_NAME, 'subdag-2', default_args),
        executor=SequentialExecutor()
    )

    # task final
    end = DummyOperator(
        task_id='final'
    )

    # fluxo de execução sequencial
    start >> subdag_1 >> some_other_task >> subdag_2 >> end