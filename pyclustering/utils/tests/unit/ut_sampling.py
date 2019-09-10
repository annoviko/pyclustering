"""!

Unit-tests for sampling functions.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
