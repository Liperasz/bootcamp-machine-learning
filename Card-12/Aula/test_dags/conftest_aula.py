# pytest é um framework de testes para Python
import pytest
from airflow.models import DagBag

# define uma fixture chamada dagbag que carrega todas as DAGs para os testes
@pytest.fixture(scope="session")
def dagbag():
    return DagBag()