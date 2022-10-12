import os
from typing import List

import networkx as nx
from src.dag_formatter import DAGFormatter
from src.dag_reader import DAGReader
from src.federated_scheduling import FederatedScheduling


def get_test_dags_dir_path() -> str:
    return f'{os.path.dirname(__file__)}/test_dags'


def get_formatted_dags() -> List[nx.DiGraph]:
    dags = DAGReader.read(get_test_dags_dir_path(), 'dot')
    DAGFormatter.format(dags, 'us')

    return dags


class TestFederatedScheduling:

    def test_classify_dags(self):
        dags = get_formatted_dags()
        heavy_dags, light_dags = FederatedScheduling.classify_dags(dags)
        for h_dag in heavy_dags:
            assert h_dag.Ui > 1.0
            assert h_dag.classification == 'heavy'
        for l_dag in light_dags:
            assert l_dag.Ui <= 1.0
            assert l_dag.classification == 'light'
