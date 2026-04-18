from airflow import DAG
from airflow.operators.bash_operator import BashOperator # executar comando shell
from airflow.operators.python_operator import PythonOperator # executar funções python

from datetime import datetime

# argumentos padrão para todas as tarefas da dag
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# função que printa o parametro e retorna feito
def process(p1):
    print(p1)
    return 'done'

# criando a dag
with DAG(dag_id='parallel_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # Tarefas criadas dinamicamente (de 1 a 3)
    tasks = [BashOperator(task_id='task_{0}'.format(t), bash_command='sleep 5'.format(t)) for t in range(1, 4)]

    # task com a função python criada
    task_4 = PythonOperator(task_id='task_4', python_callable=process, op_args=['my super parameter'])

    # task que printa uma frase
    task_5 = BashOperator(task_id='task_5', bash_command='echo "pipeline done"')

    # a lista de tasks rodara em parelo, porém a task 4 só inicia quando as task 1 2 e 3 terminar
    tasks >> task_4 >> task_5
        