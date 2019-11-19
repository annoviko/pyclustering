"""!

@brief Test runner for integration tests and unit-tests for cluster analysis module

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

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
