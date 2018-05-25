"""!

@brief Unit-tests for BANG algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.bang_templates import bang_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES


class bsas_unit_test(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0.0, [5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 7, 0.0, [5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 0.0, [5, 5], 0, False)

    def testClusteringSampleSimple1OneCluster(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.0, [10], 0, False)

    def testClusteringSampleSimple1NoiseOnly(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 1000.0, [], 10, False)

    def testClusteringSampleSimple2(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 7, 0.0, [5, 8, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 0.0, [5, 8, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.0, [23], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 500.0, [], 23, False)

    def testClusteringSampleSimple3(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 7, 0.0, [10, 10, 10, 30], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 8, 0.0, [10, 10, 10, 30], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.0, [60], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 6, 500.0, [], 60, False)

    def testClusteringSampleSimple3HalfNoise(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 2.5, [30], 30, False)


if __name__ == "__main__":
    unittest.main()