import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

# adiciona o diretório ao path do sistema
sys.path.insert(1, '/usr/local/airflow/dags/scripts')

# importa a função python que será executada por uma das dags
from scripts.process_logs_aula import process_logs_func

# String pra ser processada pela engine de templates do airflow
TEMPLATED_LOG_DIR = """{{ var.value.source_path }}/data/{{ macros.ds_format(ts_nodash, "%Y%m%dT%H%M%S", "%Y-%m-%d-%H-%M") }}/"""

# argumentos padrões das tarefas da dag
default_args = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1
        }

# criação da dag
with DAG(dag_id="template_dag", schedule_interval="@daily", default_args=default_args) as dag:

        # tarefa bash simples de printar algo no terminal
        t0 = BashOperator(
                task_id="t0",
                bash_command="echo {{ ts_nodash }} - {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}")

        #  task bash que roda o script de geração de logs
        t1 = BashOperator(
                task_id="generate_new_logs",
                bash_command="./scripts/generate_new_logs.sh",
                params={'filename': 'log.csv'})

        # task bash que testa se o arquivo da log existe
        t2 = BashOperator(
                task_id="logs_exist",
                bash_command="test -f " + TEMPLATED_LOG_DIR + "log.csv",
                )

        # task que executa a função ptthon 
        t3 = PythonOperator(
                task_id="process_logs",
                python_callable=process_logs_func,
                provide_context=True,
                templates_dict={'log_dir': TEMPLATED_LOG_DIR},
                params={'filename': 'log.csv'}
                )

        # fluxo de execução das tarefas
        t0 >> t1 >> t2 >> t3