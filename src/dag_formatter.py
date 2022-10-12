import random
from typing import List

import networkx as nx

from src.dag import DAG


class DAGFormatter:

    @staticmethod
    def format(
        dags: List[DAG],
        unit: str = 'ms',
        comm_ratio_min: float = 0.001,
        comm_ratio_max: float = 0.01
    ) -> None:
        for dag in dags:
            DAGFormatter._convert_unit(dag, unit)
            DAGFormatter._rename_atrr(dag)
            DAGFormatter._divide_wcet(dag, comm_ratio_min, comm_ratio_max)
            DAGFormatter._set_dag_param(dag)
        connection = DAGFormatter._random_add_edges(dags)
        DAGFormatter._ensure_weakly_connected(dags, connection)

    @staticmethod
    def _random_add_edges(dags: List[DAG]) -> nx.DiGraph:
        def _add_edge_lottery() -> bool:
            if random.random() < 2/len(dags):
                return True
            else:
                return False

        connection = nx.DiGraph()
        connection.add_nodes_from([dag.id for dag in dags])
        for dag_p in dags:
            for dag_s in dags:
                if _add_edge_lottery() and dag_p.id < dag_s.id:
                    dag_p.succ.append(dag_s)
                    dag_s.pred.append(dag_p)
                    connection.add_edge(dag_p.id, dag_s.id)

        return connection

    @ staticmethod
    def _ensure_weakly_connected(
        dags: List[DAG],
        connection: nx.DiGraph
    ) -> nx.DiGraph:
        if len(comps := list(nx.weakly_connected_components(connection))) >= 2:
            comps.sort(key=lambda x: len(x))
            target_comp = comps.pop(-1)
            target_nodes = target_comp - \
                {v for v, d in connection.in_degree() if d == 0}
            exit_nodes = {v for v, d in connection.out_degree() if d == 0}
            for comp in comps:
                comp_exits = set(comp) & exit_nodes
                src_i = random.choice(list(comp_exits))
                target_in_degree = \
                    {connection.in_degree(t): t for t in target_nodes}
                target_i = min(target_in_degree.items())[1]

                dags[src_i].succ.append(
                    [dag for dag in dags if dag.id == target_i][0])
                dags[target_i].pred.append(
                    [dag for dag in dags if dag.id == src_i][0])
                connection.add_edge(src_i, target_i)

        return connection

    @ staticmethod
    def _convert_unit(dag: DAG, unit: str) -> None:
        if unit == 'ms':
            factor = 1
        elif unit == 'us':
            factor = 10**3
        elif unit == 'ns':
            factor = 10**6
        else:
            NotImplementedError()

        for node_i in dag.nodes:
            node_properties = dag.nodes[node_i].keys()
            for np in node_properties:
                dag.nodes[node_i][np] = dag.nodes[node_i][np]*factor

    @ staticmethod
    def _rename_atrr(dag: DAG) -> None:
        for node_i in dag.nodes:
            dag.nodes[node_i]['WCET'] = dag.nodes[node_i]['Execution_time']
            del dag.nodes[node_i]['Execution_time']

            if (period := dag.nodes[node_i].get('Period')) is not None:
                dag.nodes[node_i]['period'] = period
                del dag.nodes[node_i]['Period']

            if (offset := dag.nodes[node_i].get('Offset')) is not None:
                dag.nodes[node_i]['offset'] = offset
                del dag.nodes[node_i]['Offset']

    @ staticmethod
    def _divide_wcet(
        dag: DAG,
        comm_ratio_min: float,
        comm_ratio_max: float
    ) -> None:
        for node_i in dag.nodes:
            exec = dag.nodes[node_i]['WCET']
            read = int(exec * random.uniform(comm_ratio_min, comm_ratio_max))
            dag.nodes[node_i]['read'] = read
            write = int(exec * random.uniform(comm_ratio_min, comm_ratio_max))
            dag.nodes[node_i]['write'] = write
            dag.nodes[node_i]['exec'] = exec-read-write

    @ staticmethod
    def _set_dag_param(dag: DAG) -> None:
        timer_i = [node_i for node_i in dag.nodes
                   if 'period' in dag.nodes[node_i].keys()][0]
        dag.Ti = dag.nodes[timer_i]['period']
        dag.Di = dag.Ti
        dag.Pi = dag.nodes[timer_i]['offset']

        dag.Ci = 0
        for node_i in dag.nodes:
            dag.Ci += dag.nodes[node_i]['WCET']

        entry_i = [v for v, d in dag.in_degree() if d == 0][0]
        exit_i = [v for v, d in dag.out_degree() if d == 0][0]
        cp_len = 0
        paths = nx.all_simple_paths(dag, source=entry_i, target=exit_i)
        for path in paths:
            path_len = 0
            for i in range(len(path)):
                path_len += dag.nodes[path[i]]["WCET"]
            if path_len > cp_len:
                cp_len = path_len
        dag.Li = cp_len
