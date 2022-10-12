import pytest
from src.clustered_processor import ClusteredProcessor, StaticManager
from src.common import Location
from src.dag import DAG
from src.exceptions import InvalidArgumentError


class TestStaticManager:

    def test_allocate_heavy_invalid_classification_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'id', 0)
        mocker.patch.object(dag_mock, 'classification', 'heavy')

        processor = ClusteredProcessor()
        static_manager = StaticManager(processor)
        with pytest.raises(InvalidArgumentError) as e:
            static_manager.allocate_light(
                dag_mock,
                Location(0, 0)
            )
        assert 'DAG ID: ' in str(e.value)

    def test_allocate_heavy_normal_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'id', 0)
        mocker.patch.object(dag_mock, 'classification', 'heavy')

        processor = ClusteredProcessor()
        static_manager = StaticManager(processor)
        locations = [Location(0, 0), Location(0, 1), Location(0, 2)]
        static_manager.allocate_heavy(dag_mock, locations)

        assert dag_mock.partitioned_locations == locations
        for location in locations:
            core = processor.get_core(location)
            assert core.partitioned_dags == [dag_mock]

    def test_allocate_heavy_already_occupied_case(self, mocker):
        dag_mock0 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock0, 'id', 0)
        mocker.patch.object(dag_mock0, 'classification', 'heavy')
        dag_mock1 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock1, 'id', 1)

        processor = ClusteredProcessor()
        static_manager = StaticManager(processor)
        static_manager.allocate_heavy(
            dag_mock0,
            [Location(0, 0), Location(0, 1), Location(0, 2)]
        )
        with pytest.raises(InvalidArgumentError) as e:
            static_manager.allocate_heavy(
                dag_mock1,
                [Location(0, 0), Location(0, 1), Location(0, 2)]
            )
        assert 'DAG ID: ' in str(e.value)

    def test_allocate_light_invalid_classification_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'id', 0)
        mocker.patch.object(dag_mock, 'classification', 'light')

        processor = ClusteredProcessor(5, 16)
        static_manager = StaticManager(processor)
        with pytest.raises(InvalidArgumentError) as e:
            static_manager.allocate_heavy(
                dag_mock,
                [Location(0, 0), Location(0, 1), Location(0, 2)]
            )
        assert 'DAG ID: ' in str(e.value)

    def test_allocate_light_normal_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'id', 0)

        processor = ClusteredProcessor(5, 16)
        static_manager = StaticManager(processor)
        location = Location(0, 0)
        static_manager.allocate_light(dag_mock, location)
        assert dag_mock.partitioned_locations == [location]
        assert processor.get_core(location).partitioned_dags == [dag_mock]

    def test_allocate_light_multiple_light_case(self, mocker):
        dag_mock0 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock0, 'id', 0)
        mocker.patch.object(dag_mock0, 'classification', 'light')
        dag_mock1 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock1, 'id', 1)
        mocker.patch.object(dag_mock1, 'classification', 'light')

        processor = ClusteredProcessor(5, 16)
        static_manager = StaticManager(processor)
        common_location = Location(0, 0)
        static_manager.allocate_light(dag_mock0, common_location)
        static_manager.allocate_light(dag_mock1, common_location)
        assert dag_mock0.partitioned_locations == [common_location]
        assert dag_mock1.partitioned_locations == [common_location]
        assert (processor.get_core(common_location).partitioned_dags
                == [dag_mock0, dag_mock1])

    def test_allocate_light_already_occupied_case(self, mocker):
        dag_mock0 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock0, 'id', 0)
        mocker.patch.object(dag_mock0, 'classification', 'heavy')
        dag_mock1 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock1, 'id', 1)

        processor = ClusteredProcessor(5, 16)
        static_manager = StaticManager(processor)
        static_manager.allocate_heavy(
            dag_mock0,
            [Location(0, 0), Location(0, 1), Location(0, 2)]
        )
        with pytest.raises(InvalidArgumentError) as e:
            static_manager.allocate_light(
                dag_mock1,
                Location(0, 0)
            )
        assert 'DAG ID: ' in str(e.value)

    def test_get_lowest_utilization_location_single_case(self, mocker):
        dag_mock0 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock0, 'classification', 'light')
        mocker.patch.object(dag_mock0, 'Ui', 0.2)
        dag_mock1 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock1, 'classification', 'light')
        mocker.patch.object(dag_mock1, 'Ui', 0.3)

        processor = ClusteredProcessor(1, 2)
        static_manager = StaticManager(processor)
        static_manager.allocate_light(dag_mock0, Location(0, 0))
        static_manager.allocate_light(dag_mock1, Location(0, 1))
        location, utilization = static_manager.get_lowest_utilization_location()
        assert location == Location(0, 0)
        assert utilization == 0.2

    def test_get_lowest_utilization_location_multiple_case(self, mocker):
        dag_mock0 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock0, 'classification', 'light')
        mocker.patch.object(dag_mock0, 'Ui', 0.2)
        dag_mock1 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock1, 'classification', 'light')
        mocker.patch.object(dag_mock1, 'Ui', 0.2)
        dag_mock2 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock2, 'classification', 'light')
        mocker.patch.object(dag_mock2, 'Ui', 0.3)
        dag_mock3 = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock3, 'classification', 'light')
        mocker.patch.object(dag_mock3, 'Ui', 0.3)

        processor = ClusteredProcessor(1, 2)
        static_manager = StaticManager(processor)
        static_manager.allocate_light(dag_mock0, Location(0, 0))
        static_manager.allocate_light(dag_mock1, Location(0, 0))
        static_manager.allocate_light(dag_mock2, Location(0, 1))
        static_manager.allocate_light(dag_mock3, Location(0, 1))
        location, utilization = static_manager.get_lowest_utilization_location()
        assert location == Location(0, 0)
        assert utilization == 0.4

    def test_get_empty_locations_1cc_normal_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'classification', 'heavy')

        processor = ClusteredProcessor(1, 5)
        static_manager = StaticManager(processor)
        locations = [Location(0, 0), Location(0, 1), Location(0, 2)]
        static_manager.allocate_heavy(dag_mock, locations)

        empty_locations = static_manager.get_empty_locations()
        assert len(empty_locations) == 1
        assert empty_locations[0] == [Location(0, 3), Location(0, 4)]

    def test_get_empty_locations_1cc_full_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'classification', 'heavy')

        processor = ClusteredProcessor(1, 3)
        static_manager = StaticManager(processor)
        locations = [Location(0, 0), Location(0, 1), Location(0, 2)]
        static_manager.allocate_heavy(dag_mock, locations)

        empty_locations = static_manager.get_empty_locations()
        assert len(empty_locations) == 1
        assert not empty_locations[0]

    def test_get_empty_locations_multiple_cc_case(self, mocker):
        dag_mock = mocker.Mock(spec=DAG)
        mocker.patch.object(dag_mock, 'classification', 'heavy')

        processor = ClusteredProcessor(2, 5)
        static_manager = StaticManager(processor)
        locations = [Location(0, 0), Location(0, 1), Location(0, 2)]
        static_manager.allocate_heavy(dag_mock, locations)

        empty_locations = static_manager.get_empty_locations()
        assert len(empty_locations) == 2
        assert empty_locations[0] == [Location(0, 3), Location(0, 4)]
        assert empty_locations[1] == ([Location(1, 0), Location(
            1, 1), Location(1, 2), Location(1, 3), Location(1, 4)])
