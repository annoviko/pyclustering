"""!

@brief Test runner for integration tests and unit-tests for cluster analysis module

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.tests.suite_holder import suite_holder

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')


from pyclustering.cluster.tests.integration import clustering_integration_tests
from pyclustering.cluster.tests.unit import clustering_unit_tests


class clustering_tests(suite_holder):
    def __init__(self):
        super().__init__()
        clustering_integration_tests.fill_suite(self.get_suite())
        clustering_unit_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(cluster_suite):
        clustering_integration_tests.fill_suite(cluster_suite)
        clustering_unit_tests.fill_suite(cluster_suite)
