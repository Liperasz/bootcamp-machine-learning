# ESSA FUNÇÃO SERÁ EXECUTADA NO CÓDIGO DO "tamplate_dag.py"

import pandas as pd
from datetime import datetime

# a função recebe **context, que é a forma de aceitar um número
# variável de argumentos cujo nome é kwargs. No airflow, como usamos 
# provide_context = true no python operator,o Airflow injeta automaticamente um
# dicionario gigante com informações sobre a execução nesta variável
def process_logs_func(**context):

    # extrai o caminho do diretório da log
    log_dir = context['templates_dict']['log_dir']
    # nome do arquivo
    filename = context['params']['filename']

    # imprime os valores no console
    print("Log dir: {}".format(log_dir))
    print("Filename: {}".format(filename))

    # formatação do arquivo csv e salvamento
    logs = pd.read_csv(log_dir + "/" + filename, sep=";")
    logs.drop("index", axis=1, inplace=True)
    logs['timestamp'] = logs['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
    logs.rename(
            columns={
                'timestamp': 'processing_time',
                'ds_airflow': 'etl_execution_time'
                },
            inplace=True
            )
    logs.to_csv(log_dir + "/processed_log.csv", sep=";", index=False)