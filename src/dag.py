from typing import Collection, List

import networkx as nx

from src.common import Location


class DAG(nx.DiGraph):

    def __init__(self, id: int) -> None:
        super().__init__()
        self._id = id
        self.pred: List[DAG] = []
        self.succ: List[DAG] = []

    @property
    def partitioned_locations(self) -> List[Location]:
        return self._partitioned_locations

    @partitioned_locations.setter
    def partitioned_locations(
        self,
        partitioned_locations: Collection[Location]
    ):
        self._partitioned_locations = list(partitioned_locations)

    @property
    def id(self) -> int:
        return self._id

    @property
    def classification(self) -> str:
        return self._classification

    @classification.setter
    def classification(self, classification: str):
        self._classification = classification

    @property
    def Ui(self) -> float:
        return self._Ci / self._Ti

    @property
    def Ti(self) -> int:
        return self._Ti

    @Ti.setter
    def Ti(self, Ti: int):
        self._Ti = Ti

    @property
    def Pi(self) -> int:
        return self._Pi

    @Pi.setter
    def Pi(self, Pi: int):
        self._Pi = Pi

    @property
    def Ci(self) -> int:
        return self._Ci

    @Ci.setter
    def Ci(self, Ci: int):
        self._Ci = Ci

    @property
    def Di(self) -> int:
        return self._Di

    @Di.setter
    def Di(self, Di: int):
        self._Di = Di

    @property
    def Li(self) -> int:
        return self._Li

    @Li.setter
    def Li(self, Li: int):
        self._Li = Li
