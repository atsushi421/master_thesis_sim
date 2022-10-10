from typing import List

import networkx as nx


class DAG(nx.DiGraph):

    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id
        self.pred: List[int] = []
        self.succ: List[int] = []

    @property
    def Ti(self):
        return self._Ti

    @Ti.setter
    def Ti(self, Ti: int):
        self._Ti = Ti

    @property
    def Pi(self):
        return self._Pi

    @Pi.setter
    def Pi(self, Pi: int):
        self._Pi = Pi

    @property
    def Ci(self):
        return self._Ci

    @Ci.setter
    def Ci(self, Ci: int):
        self._Ci = Ci

    @property
    def Di(self):
        return self._Di

    @Di.setter
    def Di(self, Di: int):
        self._Di = Di

    @property
    def Li(self):
        return self._Li

    @Li.setter
    def Li(self, Li: int):
        self._Li = Li
