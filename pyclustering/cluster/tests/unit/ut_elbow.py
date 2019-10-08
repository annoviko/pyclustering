"""!

@brief Unit-tests for Elbow method.

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

from pyclustering.cluster.center_initializer import random_center_initializer
from pyclustering.cluster.elbow import elbow

from pyclustering.cluster.tests.elbow_template import elbow_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS


class elbow_unit_test(unittest.TestCase):
    def test_elbow_simple_01(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, 10, False)

    def test_elbow_simple_01_random_initializer(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, 10, False, initializer=random_center_initializer)

    def test_elbow_simple_02(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, 10, False)

    def test_elbow_simple_02_random_initializer(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, 10, False, initializer=random_center_initializer)

    def test_elbow_simple_03(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, 10, False)

    def test_elbow_simple_03_random_initializer(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, 10, False, initializer=random_center_initializer)

    def test_elbow_simple_05(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 1, 10, False)

    def test_elbow_simple_06(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 1, 10, False)

    def test_elbow_simple_10(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 1, 10, False)

    def test_elbow_simple_12(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 1, 10, False)

    def test_elbow_one_dimensional_simple_07(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 1, 10, False)

    def test_elbow_one_dimensional_simple_09(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 1, 10, False)

    def test_elbow_three_dimensional_simple_11(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 1, 10, False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, elbow, [], 1, 5)

    def test_incorrect_kmin(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 0, 2)

    def test_incorrect_difference(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 2)

    def test_incorrect_kmax(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 10)
