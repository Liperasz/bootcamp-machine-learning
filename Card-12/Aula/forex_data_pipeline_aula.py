# Importa a classe principal do airflow
from airflow import DAG

# lidar com os tempos 
from datetime import datetime, timedelta 

# importa os operadores e sensores
from airflow.sensors.http_sensor import HttpSensor 
from airflow.contrib.sensors.file_sensor import FileSensor 
from airflow.operators.python_operator import PythonOperator 
from airflow.operators.bash_operator import BashOperator 
from airflow.operators.hive_operator import HiveOperator 
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator 
from airflow.operators.email_operator import EmailOperator 
from airflow.operators.slack_operator import SlackAPIPostOperator

# importando outras bibliotecas necessárias para o processo
import json
import csv
import requests
import os
from dotenv import load_dotenv

# argumentos utilizados nas tarefas da DAG
default_args = {
    "owner": "airflow", # dono da tarefa
    "start_date": datetime(2025, 12, 15), # data inicial da tarefa
    "depend_on_past": False, # nao depende da tarefa anterior para executar novamente
    "email_on_failure": False, # nao envia email se falhar
    "email_on_retry": False, # nao envia email se tentar novamente
    "email": "fonseca.2006@alunos.utfpr.edu.br", # email que vai enviar
    "retries": 1, # numero de tentativas
    "retry_delay": timedelta(minutes=5) # tempo de espera entre as tentativas
}

# função para baixar as taxas de câmbio
def download_rates():
    # abre o arquivo csv com as moedas
    with open('/usr/local/airflow/dags/files/forex_currencies.csv') as forex_currencies:

        # le o arquivo csv
        reader = csv.DictReader(forex_currencies, delimiter=';')

        # para cada linha (moeda base)
        for row in reader:

            # pega a moeda e as moedas com as quais comparar
            base = row['base']
            with_pairs = row['with_pairs'].split(' ')

            # faz a requisição para a API
            indata = requests.get('https://api.exchangeratesapi.io/latest?base=' + base).json()

            # cria o dicionário de saida (vazio, onde vão ser colocados os dados)
            outdata = {'base': base, 'rates': {}, 'last_update': indata['date']}

            # para cada moeda com a qual comparar
            for pair in with_pairs:
                # adiciona a taxa de câmbio ao dicionario de saída
                outdata['rates'][pair] = indata['rates'][pair]

            # escreve os dados no arquivo json
            with open('/usr/local/airflow/dags/files/forex_rates.json', 'a') as outfile:
                json.dump(outdata, outfile)
                outfile.write('\n')

# cria uma DAG
with DAG(dag_id="forex_data_pipeline", # id
         schedule_interval="@daily", # intervalo diário
         default_args=default_args, # argumentos criados anteriormente
         catchup=False) as dag: # não executa tarefas passadas
    
    # sensor http: verifica se a API está disponível
    is_forex_api_available = HttpSensor(

         # id da tarefa
        task_id="is_forex_rates_available",
         # método da requisição
        method="GET",
        # conexão http criada no Airflow
        http_conn_id="forex_api", 
        # caminho final da url
        endpoint="latest", 

        # função que verifica se a resposta contém as taxas de câmbio
        response_check=lambda response: "rates" in response.text,
        # intervalo entre as tentativas
        poke_interval=5,
        # tempo máximo de espera
        timeout=20
    )

    # sensor de arquivos: verifica se o csv está disponivel
    is_forex_currencies_file_available = FileSensor(

        # id da tarefa
        task_id="is_forex_currencies_file_available",
        # id da conexão do sistema de arquivos criada no Airflow
        fs_conn_id="forex_path",
        # caminho do arquivo
        filepath="forex_currencies.csv",

        # intervalo entre as tentativas e tempo maximo de espera
        poke_interval=5,
        timeout=20
    )
    
    # operador do python: executa a função criada no inicio
    download_rates = PythonOperator(
        # id da tarefa
        task_id="download_rates",
        # função a ser executada
        python_callable=download_rates
    )

    # Operador bash: executa comandos bash no hdfs
    saving_rates = BashOperator(
        # id da tarefa
        task_id="saving_rates",
        # comandos bash a serem executados (o primeiro cria o diretório, o segundo envia o arquivo)
        bash_command="""
            hdfs dfs -mkdir -p /forex_data/ && \
            hdfs dfs -put -f %AIRFLOW_HOME/dags/files/forex_rates.json /forex
        """
    )

    # Operador hive: cria a estrutura da tabela no hive
    creating_forex_rates_table = HiveOperator(
        # id da tarefa
        task_id="creating_forex_rates_table",
        # conexão hive criada no Airflow
        hive_cli_conn_id="hive_conn",
        # comando hql para criar a tabela (semelhante ao sql)
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
    )

    # operador spark: executa o spark para executar um arquivo
    forex_processing = SparkSubmitOperator(
        # id da tarefa
        task_id="forex_processing",
        # conexão spark criada no Airflow
        conn_id="spark_conn",
        # caminho do script spark a ser executado
        application="/usr/local/airflow/dags/scripts/forex_processing.py",
        # reduz os logs 
        verbose=False
    )

    # operador pra enviar email
    sending_email_notification = EmailOperator(
        # id da tarefa
        task_id="sending_email",
        # email que vai enviar
        to="airflow_course@yopmail.com",
        # assunto do email
        subject="forex_data_pipeline",
        # conteudo do email
        html_content="<h3>forex_data_pipeline succeded</h3>"
    )

    # carrega as variaveis de ambiente do .env (criado por mim pra colocar a api do token. Motivo: github não deixou eu subir o arquivo com a api key)
    load_dotenv()

    # operador para enviar mensagem no slack
    sending_slack_notification = SlackAPIPostOperator(
        # id da tarefa
        task_id="sending_slack",
        # token de autenticação (pego do .env)
        token=os.getenv("SLACK_API_TOKEN"),
        # nome de usuário que vai enviar a mensagem
        username='airflow',
        # canal que vai enviar a mensagem e a mensagem
        text='DAG forex_data_pipeline: DONE',
        channel='#airflow-exploit'
    )

    # fluxo das tarefas, primeiro o sensor http, depois o sensor de arquivos, depois o download, depois salvar no hdfs, depois criar a tabela no hive, depois processar com spark, depois enviar email e por fim enviar mensagem no slack
    is_forex_api_available >> is_forex_currencies_file_available >> download_rates >> saving_rates >> creating_forex_rates_table >> forex_processing >> sending_email_notification >> sending_slack_notification