import sys
from typing import Collection, List, Tuple

from src.common import Location
from src.dag import DAG
from src.exceptions import InvalidArgumentError


class Core:
    def __init__(
        self,
        core_id: int,
    ) -> None:
        self.id = core_id
        self.partitioned_dags: List[DAG] = []


class Cluster:
    def __init__(
        self,
        cc_id: int,
        num_cores: int
    ) -> None:
        self.id = cc_id
        self.cores = [Core(core_id) for core_id in range(num_cores)]


class ClusteredProcessor:

    def __init__(
        self,
        num_ccs: int = 5,
        num_cores: int = 16
    ) -> None:
        self.num_ccs = num_ccs
        self.num_cores = num_cores
        self.ccs = [Cluster(cc_id, num_cores) for cc_id in range(num_ccs)]

    def get_core(
        self,
        location: Location
    ) -> Core:
        return self.ccs[location.cc_id].cores[location.core_id]


class StaticManager:

    def __init__(
        self,
        processor: ClusteredProcessor
    ) -> None:
        self._processor = processor

    def allocate_light(
        self,
        dag: DAG,
        location: Location
    ) -> None:
        if dag.classification == 'heavy':
            raise InvalidArgumentError(
                f'Invalid heavy DAG inputted. DAG ID: {dag.id}')

        def validate_location(target_core: Core) -> bool:
            if not target_core.partitioned_dags:
                return True
            for partitioned_dag in target_core.partitioned_dags:
                if partitioned_dag.classification == 'heavy':
                    return False
            return True

        target_core = self._processor.get_core(location)
        if validate_location(target_core):
            target_core.partitioned_dags.append(dag)
            dag.partitioned_locations = [location]
        else:
            msg = 'The location has already been allocated a heavy DAG. '
            msg += f'location: {location}. '
            msg += f'DAG ID: {target_core.partitioned_dags + [dag]}'
            raise InvalidArgumentError(msg)

    def allocate_heavy(
        self,
        dag: DAG,
        locations: Collection[Location]
    ) -> None:
        if dag.classification == 'light':
            raise InvalidArgumentError(
                f'Invalid light DAG inputted. DAG ID: {dag.id}')

        for location in locations:
            target_core = self._processor.get_core(location)
            if target_core.partitioned_dags:
                msg = 'The location has already been allocated a heavy DAG. '
                msg += f'location: {location}. '
                msg += f'DAG ID: {target_core.partitioned_dags + [dag]}'
                raise InvalidArgumentError(msg)
            else:
                target_core.partitioned_dags.append(dag)
        dag.partitioned_locations = list(locations)

    def get_empty_locations(self) -> List[List[Location]]:
        empty_locations: List[List[Location]] = []
        for cc in self._processor.ccs:
            empty_locations_per_cc: List[Location] = []
            for core in cc.cores:
                if not core.partitioned_dags:
                    empty_locations_per_cc.append(Location(cc.id, core.id))
            empty_locations.append(empty_locations_per_cc)

        return empty_locations

    def get_lowest_utilization_location(self) -> Tuple[Location, float]:
        lowest_utilization = sys.maxsize
        for cc in self._processor.ccs:
            for core in cc.cores:
                partitioned_dags = core.partitioned_dags
                if not partitioned_dags:
                    return (Location[cc.id, core.id], 0)

                total_utilization = 0
                for dag in partitioned_dags:
                    if dag.classification == 'heavy':
                        continue
                    total_utilization += dag.Ui

                if total_utilization < lowest_utilization:
                    lowest_utilization_location = Location(cc.id, core.id)
                    lowest_utilization = total_utilization

        return lowest_utilization_location, lowest_utilization
