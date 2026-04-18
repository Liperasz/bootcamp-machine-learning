import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator

# argumentos padrão
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    }

# avalia a condição 
def conditionally_trigger(context, dag_run_obj):

    # se o parametro é true
    if context['params']['condition_param']: 
        # adiciona um payload que será enviado para a Dag de destino
        dag_run_obj.payload = {
                'message': context['params']['message']
            }
        pp.pprint(dag_run_obj.payload)
        return dag_run_obj

# criação da dag
with DAG(dag_id="triggerdagop_controller_dag", default_args=default_args, schedule_interval="@once") as dag:

    # trigger que adiciona a dag de destino
    trigger = TriggerDagRunOperator(
        task_id="trigger_dag",
        trigger_dag_id="triggerdagop_target_dag", # dag externa que será acionada
        provide_context=True,
        python_callable=conditionally_trigger,
        params={
            'condition_param': True, # é acionado se o parametro for true
            'message': 'Hi from the controller'
        },
    )

    # task final para junção
    last_task = DummyOperator(task_id="last_task")

    # fluxo de tasks
    trigger >> last_task