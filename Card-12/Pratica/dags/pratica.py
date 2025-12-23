from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta
import requests
import json

# função que pega as informações do clima
def get_weather(ds, **kwargs):

    # como a API utiliza latitude e longitude, coloquei as coordenadas de sao paulo
    lat = "-23.55"
    lon = "-46.63"
    
    # url da API de clima
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={ds}&end_date={ds}&daily=temperature_2m_mean&timezone=America%2FSao_Paulo"
    
    # Faz a requisição GET para a API
    response = requests.get(url)
    # Pega o JSON da resposta
    data = response.json()
    
    # pega a temperatura do dia
    avg_temp = data['daily']['temperature_2m_mean'][0]
    print(f"Data: {ds} | Temperatura: {avg_temp}°C")
    return avg_temp
    

# função que decide se o clima é quente ou frio
def choose_weather(ti):
    # puxa a temperatura retornada pela task anterior via XCom
    temp = ti.xcom_pull(task_ids='get_weather')

    # se a temperatura for maior ou igual a 25 graus, é um dia quente    
    if temp >= 25:
        return 'hot_day' 
    # menor ou igual a 15 graus é um dia frio
    if temp <= 15: 
        return 'cold_day'   
    # entre 15 e 25 graus é um dia agradável
    return 'normal_day' 

# Argumentos da DAG
default_args = {
    'owner': 'Airflow', # dono da DAG
    'start_date': datetime(2025, 12, 10), # data de início
    'retries': 1, # número de tentativas em caso de falha
    'tags':['desafio', 'avancado'] # tags para organização
}

# Definição da DAG
with DAG(dag_id='weather_pipeline', # id
        default_args=default_args, # argumentos padrão
        schedule_interval='@daily', # executa diariamente
        catchup=True) as dag: # Backfill ativado

    # verifica se a API está online
    check_api = HttpSensor(
        task_id='check_api',
        http_conn_id='weather_api',
        endpoint='', # Testa a raiz do site
        poke_interval=5, # intervalo entre tentativas
        timeout=20 # tempo máximo de espera
    )

    # utiliza a função definida para pegar as informações do clima
    get_weather = PythonOperator(
        task_id='get_weather',
        python_callable=get_weather,
    )

    # usa um operador que permite criar branchs no fluxo
    branching = BranchPythonOperator(
        task_id='choose_weather',
        python_callable=choose_weather,
    )

    # 3 operadores bash, um para cada condição de clima
    # o comando ds pega a data de execução da DAG no formato YYYY-MM-DD
    log_hot = BashOperator(
        task_id='hot_day',
        bash_command='echo "DIA QUENTE: {{ ds }}" >> /opt/airflow/logs/historico_clima.txt'
    )

    log_cold = BashOperator(
        task_id='cold_day',
        bash_command='echo "DIA FRIO: {{ ds }}" >> /opt/airflow/logs/historico_clima.txt'
    )

    log_normal = BashOperator(
        task_id='normal_day',
        bash_command='echo "DIA NORMAL: {{ ds }}" >> /opt/airflow/logs/historico_clima.txt'
    )

    # operador vazio para juntar os caminhos do fluxo
    join_tasks = EmptyOperator(
        task_id='finish',
        trigger_rule='none_failed_min_one_success'
    )

    # definindo a ordem das tarefas
    check_api >> get_weather >> branching

    # definindo os caminhos das branchs
    branching >> [log_hot, log_cold, log_normal]

    # juntando os 3 caminhos no final
    [log_hot, log_cold, log_normal] >> join_tasks