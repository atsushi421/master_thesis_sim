from typing import List, Tuple

from src.dag import DAG


class FederatedScheduling:

    @staticmethod
    def classify_dags(dags: List[DAG]) -> Tuple[List[DAG], List[DAG]]:
        heavy_dags: List[DAG] = []
        light_dags: List[DAG] = []
        for dag in dags:
            if dag.Ui > 1.0:
                heavy_dags.append(dag)
                dag.classification = 'heavy'
            else:
                light_dags.append(dag)
                dag.classification = 'light'

        return heavy_dags, light_dags

    @staticmethod
    def partition(
        heavy_dags: List[DAG],
        light_dags: List[DAG],
        processor
    ) -> None:
        pass
