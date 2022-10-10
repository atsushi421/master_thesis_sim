import os

import networkx as nx
from src.dag_reader import DAGReader


def get_test_dags_dir_path() -> str:
    return f'{os.path.dirname(__file__)}/test_dags'


class TestDAGReader:
    def test_read_dot(self):
        dags = DAGReader.read(get_test_dags_dir_path(), 'dot')

        assert isinstance(dags, list)
        for dag in dags:
            assert isinstance(dag, nx.DiGraph)

        dag0 = dags[0]
        for value in dag0.nodes[0].values():
            isinstance(value, int)
        for value in dag0.edges[0, 1].values():
            isinstance(value, int)
