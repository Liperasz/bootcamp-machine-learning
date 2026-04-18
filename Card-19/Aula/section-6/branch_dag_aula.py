import airflow
import requests # requisições
from airflow.models import DAG # Dag
from airflow.operators.dummy_operator import DummyOperator # task vazia, apenas estruturação

# branch python operator permite criar ramificações de tarefas, e o python operator para executar função python
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator 

# argumentos padrões
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

# apis para cada local
IP_GEOLOCATION_APIS = {
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json'
}

# Função para verificar as APIs
def check_api():

    # Tenta receber o código do país de cada API
    apis = []
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        # Se conseguir, a API é retornada e a próxima task correspondente a essa API será executada
        try:
            data = r.json()
            if data and 'country' in data and len(data['country']):
                apis.append(api)
        except ValueError:
            pass
    return apis if len(apis) > 0 else 'none'

# criação da Dag
with DAG(dag_id='branch_dag', 
    default_args=default_args, 
    schedule_interval="@once") as dag:

    # A pŕoxima task depende do retorno da função check_api
    check_api = BranchPythonOperator(
        task_id='check_api',
        python_callable=check_api
    )

    # task vazia, executada se nenhuma API estiver funcionando
    none = DummyOperator(
        task_id='none'
    )

    # task vazia para juntar o fluxo novamente
    save = DummyOperator(task_id='save', trigger_rule='one_success') 

    # caso de falha total
    check_api >> none >> save

    # cria as tasks dinamicamente 
    for api in IP_GEOLOCATION_APIS:
        process = DummyOperator(
            task_id=api
        )

        # o trigger 'one success' faz com que caso pelo menos uma das branchings tenha que finalizar para a task ser ativada
        check_api >> process >> save