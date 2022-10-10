from typing import List

import networkx as nx


class DAG(nx.DiGraph):

    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id
        self.pred: List[int] = []
        self.succ: List[int] = []
