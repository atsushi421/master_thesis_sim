import copy
import os
from typing import List

import networkx as nx
from src.dag_formatter import DAGFormatter
from src.dag_reader import DAGReader


def get_test_dags_dir_path() -> str:
    return f'{os.path.dirname(__file__)}/test_dags'


def get_read_dags() -> List[nx.DiGraph]:
    read_dags = DAGReader.read(get_test_dags_dir_path(), 'dot')

    return read_dags


class TestDAGFormatter:

    def test_format_us(self):
        dags = get_read_dags()
        before_dag0 = copy.deepcopy(dags[0])

        DAGFormatter.format(dags, 'us')
        for dag in dags:
            assert len(dag.pred) >= 1 or len(dag.succ) >= 1
            assert isinstance(dag.Ti, int)
            assert dag.Ti >= 1000
            assert isinstance(dag.Pi, int)
            assert dag.Pi >= 1000 or dag.Pi == 0
            assert isinstance(dag.Ci, int)
            assert dag.Ci >= 1000
            assert isinstance(dag.Di, int)
            assert dag.Di >= 1000
            assert isinstance(dag.Li, int)
            assert dag.Li >= 1000

        after_dag0 = dags[0]
        for node_i in after_dag0:
            np = after_dag0.nodes[node_i].keys()
            assert ('Execution_time' not in np and
                    'Period' not in np and
                    'Offset' not in np)
            assert (before_dag0.nodes[node_i]['Execution_time']*1000 ==
                    (after_dag0.nodes[node_i]['exec']
                     + after_dag0.nodes[node_i]['write']
                     + after_dag0.nodes[node_i]['read'])
                    )
            assert (before_dag0.nodes[node_i]['Execution_time']*1000 ==
                    after_dag0.nodes[node_i]['WCET'])
            if before_period := before_dag0.nodes[node_i].get('Period'):
                assert before_period*1000 == after_dag0.nodes[node_i]['period']
            if before_offset := before_dag0.nodes[node_i].get('Offset'):
                assert before_offset*1000 == after_dag0.nodes[node_i]['offset']

    def test_random_add_edges(self):
        connection = DAGFormatter._random_add_edges(get_read_dags())
        assert connection.is_directed()
        assert not connection.is_multigraph()

    def test_ensure_weakly_connected(self):
        read_dags = get_read_dags()
        connection = DAGFormatter._random_add_edges(read_dags)
        connection = DAGFormatter._ensure_weakly_connected(
            read_dags, connection)
        assert len(list(nx.weakly_connected_components(connection))) == 1
