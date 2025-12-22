# importa OS para criar os diretorios
import os
# importa DagBag para carregar as dags de outros diretorios
from airflow.models import DagBag

# diretorios onde serao criados as dags
dags_dirs = [
                '/usr/local/airflow/project_a', 
                '/usr/local/airflow/project_b'
            ]
# para cada diretorio, carrega as dags e adiciona ao globals
for dir in dags_dirs:
   dag_bag = DagBag(os.path.expanduser(dir))

   if dag_bag:
      for dag_id, dag in dag_bag.dags.items():
         globals()[dag_id] = dag