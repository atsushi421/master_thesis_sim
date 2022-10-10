import glob
from typing import List

import networkx as nx


class DAGReader:

    @staticmethod
    def read(dag_dir: str, format: str) -> List[nx.DiGraph]:
        if format.lower() == 'dot':
            dags = DAGReader._read_dot(dag_dir)
        else:
            NotImplementedError()

        return dags

    @staticmethod
    def _read_dot(dag_dir: str) -> List[nx.DiGraph]:
        dag_paths = glob.glob(f"{dag_dir}/**/*.dot",
                              recursive=True)

        dag_list: List[nx.DiGraph] = []
        for dag_path in dag_paths:
            tmp_dag = nx.drawing.nx_pydot.read_dot(dag_path)
            tmp_dag = nx.DiGraph(tmp_dag)
            tmp_dag.remove_node('\\n')
            dag_list.append(DAGReader._convert_property_str_to_int(tmp_dag))

        return dag_list

    @staticmethod
    def _convert_property_str_to_int(
        tmp_dag: nx.DiGraph
    ) -> nx.DiGraph:
        dag = nx.DiGraph()
        for node_i in tmp_dag.nodes:
            dag.add_node(int(node_i))
            node_properties = tmp_dag.nodes[node_i].keys()
            for np in node_properties:
                dag.nodes[int(node_i)][np] = int(tmp_dag.nodes[node_i][np])

        for s, t in tmp_dag.edges:
            dag.add_edge(int(s), int(t))
            edge_properties = tmp_dag.edges[s, t].keys()
            for ep in edge_properties:
                dag.edges[int(s), int(t)][ep] = int(tmp_dag.edges[s, t][ep])

        return dag
