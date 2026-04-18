from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime
import random

# argumentos padrão para as tarefas
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1),
    'catchup': False,
}

# Função que simula um processamento e envia uma mensagem com True ou False
def processing(**kwargs):
    status = random.choice([True, False])
    print(f"Status gerado: {status}")
    kwargs['ti'].xcom_push(key='processing_status', value=status)

# Função que cria uma ramificação
def branching(**kwargs):

    # verifica o valor dos tatus que foi enviado pela task_processing
    status = kwargs['ti'].xcom_pull(task_ids='task_processing', key='processing_status')

    # Se recebeu True, retorna o id da próxima dag a ser ativada
    if status == True :
        return 'task_trigger' 
    else:
        # se recebeu False, retorna o id da task que reporta um erro
        return 'task_fail'

with DAG(dag_id='controller_dag', default_args=default_args, schedule_interval=None) as dag:


    # Bash Operator para imprimir a data de execução da tarefa e uma variável criada na interface do airflow
    task_templating = BashOperator(

        task_id='task_templating',
        bash_command='echo "Data de Execução: {{ ds }} | Sistema: {{ var.json.secret_config.id }}"'
    )

    # Task que executa a função processing
    task_processing = PythonOperator(
        task_id='task_processing',
        python_callable=processing,
        provide_context=True
    )

    # Executa uma ramificação a ser seguida com base em um status obitido da task processing
    task_branching = BranchPythonOperator(
        task_id='task_branching',
        python_callable=branching,
        provide_context=True
    )

    # ramificação 1: task que aciona a triggered dag
    task_trigger = TriggerDagRunOperator(
        task_id='task_trigger',
        trigger_dag_id='triggered_dag',
        conf={'mensagem': 'Iniciado com sucesso pela DAG 1!', 'id_lote': 42}
    )

    # ramificação 2: task simulando um print de falha
    task_fail = BashOperator(
        task_id='task_fail',
        bash_command='echo "O processamento falhou. Encerrando fluxo base."'
    )

    # Fluxo das dependências
    task_templating >> task_processing >> task_branching
    task_branching >> [task_trigger, task_fail]

