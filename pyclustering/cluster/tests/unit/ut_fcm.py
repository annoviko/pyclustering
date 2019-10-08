"""!

@brief Unit-tests for Fuzzy C-Means algorithm.

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


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.fcm_templates import fcm_test_template

from pyclustering.cluster.fcm import fcm

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FAMOUS_SAMPLES, FCPS_SAMPLES


class fcm_unit_tests(unittest.TestCase):
    def test_cluster_allocation_simple01(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], 2.0, [5, 5], False)

    def test_cluster_allocation_simple01_one_cluster(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], 2.0, [10], False)

    def test_cluster_allocation_simple01_centers_are_points1(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.768699, 5.364477], [6.593196, 7.850364]], 2.0, [5, 5], False)

    def test_cluster_allocation_simple01_centers_are_points2(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.936690, 5.663041], [6.968136, 7.755556]], 2.0, [5, 5], False)

    def test_cluster_allocation_simple01_wrong_amount(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [4.7, 6.5], [3.4, 6.4]], 2.0, [2, 3, 5], False)

    def test_cluster_allocation_simple02(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], 2.0, [10, 5, 8], False)

    def test_cluster_allocation_simple02_wrong_amount(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5], [4.5, 6.2]], 2.0, [4, 5, 6, 8], False)

    def test_cluster_allocation_simple03(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], 2.0, [10, 10, 10, 30], False)

    def test_cluster_allocation_simple04(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], 2.0, [15, 15, 15, 15, 15], False)

    def test_cluster_allocation_simple05(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], 2.0, [15, 15, 15, 15], False)

    def test_cluster_allocation_simple06(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, [[2.0, 6.0], [8.5, 4.5]], 2.0, [20, 21], False)

    def test_cluster_allocation_simple07(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[-3.0], [2.0]], 2.0, [10, 10], False)

    def test_cluster_allocation_simple08(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-4.0], [3.1], [6.1], [12.0]], 2.0, [15, 30, 20, 80], False)

    def test_cluster_allocation_simple09(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [[4.0], [8.0]], 2.0, [10, 20], False)

    def test_cluster_allocation_simple10(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, [[0.426, 0.065 ], [5.462, 6.529], [9.539, 11.379]], 2.0, [11, 11, 11], False)

    def test_cluster_allocation_simple11(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, [[1.0, 0.6, 0.8], [4.1, 4.2, 4.3]], 2.0, [10, 10], False)

    def test_cluster_allocation_simple12(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [[1.0, 1.0], [2.5, 2.5], [4.0, 4.0]], 2.0, [5, 5, 5], False)

    def test_cluster_allocation_simple13(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, [[1.35, 1.21, 0.0], [3.79, 4.21, 0.0]], 2.0, [5, 5], False)

    def test_cluster_allocation_simple14(self):
        fcm_test_template.cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE14, [[5.649, 5.199]], 2.0, [41], False)

    def test_cluster_allocation_famous_oldfaithful(self):
        fcm_test_template.cluster_allocation(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL, [[4.0, 70], [1.0, 48]], 2.0, None, False)

    def test_cluster_allocation_two_diamonds(self):
        fcm_test_template.cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.71 -0.51], [0.99 -0.24]], 2.0, [400, 400], False)

    def test_cluster_allocation_tetra(self):
        fcm_test_template.cluster_allocation(FCPS_SAMPLES.SAMPLE_TETRA, [[1.001, -0.083, -0.681], [-0.811, 0.476, -0.759], [-0.956, -1.427, -0.020], [0.225, 0.560, 1.794]], 2.0, [100, 100, 100, 100], False)

    def test_cluster_allocation_fcps_hepta(self):
        fcm_test_template.cluster_allocation(FCPS_SAMPLES.SAMPLE_HEPTA,
                                             [[-0.06,0.02, 0.02], [2.41, 0.49, 0.03], [-2.69, 0.34, 0.29], [0.49, 2.89, 0.78], [-0.60, -2.31, 0.05], [-0.15, 0.77, 3.23], [-0.50, 0.43, -2.60]],
                                             2.0, [30, 30, 30, 30, 30, 30, 32], False)

    def test_cluster_allocation_fcps_hepta_wrong_amount(self):
        fcm_test_template.cluster_allocation(FCPS_SAMPLES.SAMPLE_HEPTA,
                                             [[-0.06,0.02, 0.02], [2.41, 0.49, 0.03], [-2.69, 0.34, 0.29], [0.49, 2.89, 0.78], [-0.60, -2.31, 0.05], [-0.50, 0.43, -2.60]],
                                             2.0, [30, 30, 30, 30, 30, 62], False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, fcm, [], 1)

    def test_incorrect_centers(self):
        self.assertRaises(ValueError, fcm, [[0], [1], [2]], [])
