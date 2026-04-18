# Importando as classes principais do Airflow
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator # operadores para chamada de api
from airflow.operators.bash_operator import BashOperator # rodar comandos no terminal

from datetime import datetime

# configuração padrão para todas as tarefas da dag
default_args = {
    'start_date': datetime(2019, 1, 1), # data de inicio
    'owner': 'Airflow', # dono da dag
    'email': 'owner@test.com' # email de contato
}

# definindo a Dag
with DAG(dag_id='pool_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # requisição da api para cotação do Euro
    get_forex_rate_EUR = SimpleHttpOperator( 
        task_id='get_forex_rate_EUR', 
        method='GET',
        priority_weight=1, # prioridade
        pool='forex_api_pool', # define o pool que a tarefa pertence
        http_conn_id='forex_api',
        endpoint='/latest?base=EUR',
        xcom_push=True # salvar a resposta da API no bd interno
    )
 
    # mesma coisa mas para o Dólar
    get_forex_rate_USD = SimpleHttpOperator(
        task_id='get_forex_rate_USD',
        method='GET',
        priority_weight=2,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=USD',
        xcom_push=True
    )
 
    # Mesma coisa mas para o JPY (Yen japones)
    get_forex_rate_JPY = SimpleHttpOperator(
        task_id='get_forex_rate_JPY',
        method='GET',
        priority_weight=3,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=JPY',
        xcom_push=True
    )
 
    # template de comando bash com os macros
    bash_command="""
        {% for task in dag.task_ids %}
            echo "{{ task }}"
            echo "{{ ti.xcom_pull(task) }}"
        {% endfor %}
    """

    # Executa o script do bash command
    show_data = BashOperator(
        task_id='show_result',
        bash_command=bash_command
    )

    # Dependências de uma tarefa para outra
    # as tarefas podem rodar em paralelo, mas respeitando o limite do pool
    # show_data só vai rodar após as outras 3 terminarem
    [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data