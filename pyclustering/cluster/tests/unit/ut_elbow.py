"""!

@brief Unit-tests for Elbow method.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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

    def test_elbow_simple_01_step_2(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, 1, 10, False, kstep=2)

    def test_elbow_simple_01_step_3(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 4, 1, 10, False, kstep=3)

    def test_elbow_simple_01_step_4(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 10, False, kstep=4)

    def test_elbow_simple_02(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, 10, False)

    def test_elbow_simple_02_step_2(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, 10, False, kstep=2)

    def test_elbow_simple_02_step_3(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, None, 1, 10, False, kstep=3)

    def test_elbow_simple_02_step_4(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, None, 1, 10, False, kstep=4)

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

    def test_elbow_simple_15(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE15, 5, 1, 20, False, kstep=2)

    def test_elbow_one_dimensional_simple_07(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 1, 10, False)

    def test_elbow_one_dimensional_simple_09(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 1, 10, False)

    def test_elbow_three_dimensional_simple_11(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 1, 10, False)

    def test_elbow_random_state(self):
        elbow_test_template.random_state_fixed(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 10, False, random_state=5)

    def test_elbow_random_state_random_initializer(self):
        elbow_test_template.random_state_fixed(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 10, False, random_state=5, initializer=random_center_initializer)

    def test_elbow_random_state_continuous(self):
        elbow_test_template.random_state_fixed(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 10, False, random_state=5, repeat=10)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, elbow, [], 1, 5)

    def test_incorrect_kmin(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 0, 2)

    def test_incorrect_difference(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 2)

    def test_border_step_1(self):
        elbow_test_template.calculate_elbow(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, 3, False, kstep=1, random_state=1000)

    def test_border_exception_step_2(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 3, kstep=2, random_state=1000)

    def test_border_step_4(self):
        elbow_test_template.random_state_fixed(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 9, False, kstep=4, random_state=1000)

    def test_incorrect_difference_with_kstep(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 10, kstep=5)
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 10, kstep=6)

    def test_incorrect_kmax(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 10)

    def test_incorrect_kstep(self):
        self.assertRaises(ValueError, elbow, [[0], [1], [2]], 1, 3, kstep=0)
