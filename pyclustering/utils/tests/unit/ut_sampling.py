"""!

Unit-tests for sampling functions.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.utils.tests.sampling_templates import sampling_test_template

from pyclustering.utils.sampling import reservoir_x, reservoir_r


class sampling_unit_test(unittest.TestCase):
    def testReservoirR(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.random_sampling(sample, 10, reservoir_r, 10)

    def testTheSameSizeReservoirR(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.random_sampling(sample, 20, reservoir_r, 10)

    def testOneElementReservoirR(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.random_sampling(sample, 1, reservoir_r, 10)

    def testUniformDistributionReservoirR(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.uniform_distribution(sample, 1, reservoir_r, 2500)

    def testReservoirX(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.random_sampling(sample, 10, reservoir_x, 10)

    def testTheSameSizeReservoirX(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.random_sampling(sample, 20, reservoir_x, 10)

    def testOneElementReservoirX(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.random_sampling(sample, 1, reservoir_x, 10)

    def testUniformDistributionReservoirX(self):
        sample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        sampling_test_template.uniform_distribution(sample, 1, reservoir_x, 2500, 0.3)
