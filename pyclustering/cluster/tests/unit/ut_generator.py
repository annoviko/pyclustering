"""!

@brief Unit-tests for cluster generator.

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

from pyclustering.cluster.generator import data_generator

from pyclustering.tests.assertion import assertion


class generator_unit_tests(unittest.TestCase):
    def assert_dimension(self, data, expected_dimension):
        for point in data:
            assertion.eq(expected_dimension, len(point))


    def assert_distribution(self, data, sizes, centers, widths):
        index_cluster = 0
        index_cluster_point = 0

        actual_means = [[0.0 for _ in range(len(data[0])) ] for _ in range(len(sizes))]

        for index_point in range(len(data)):
            for index_dimension in range(len(data[0])):
                actual_means[index_cluster][index_dimension] += data[index_point][index_dimension]

            index_cluster_point += 1
            if index_cluster_point == sizes[index_cluster]:
                index_cluster_point = 0
                index_cluster += 1

        for index_cluster in range(len(actual_means)):
            for index_dimension in range(len(data[0])):
                actual_means[index_cluster][index_dimension] /= sizes[index_cluster]
                assertion.ge(centers[index_cluster][index_dimension], actual_means[index_cluster][index_dimension] - widths[index_cluster])
                assertion.le(centers[index_cluster][index_dimension], actual_means[index_cluster][index_dimension] + widths[index_cluster])


    def test_generate_one_dimension(self):
        data = data_generator(2, 1, [10, 10]).generate()
        assertion.eq(20, len(data))
        self.assert_dimension(data, 1)


    def test_generate_two_dimension(self):
        data = data_generator(2, 2, [10, 15]).generate()
        assertion.eq(25, len(data))
        self.assert_dimension(data, 2)


    def test_generate_one_cluster(self):
        data = data_generator(1, 10, 20).generate()
        assertion.eq(20, len(data))
        self.assert_dimension(data, 10)


    def test_generate_similar_clusters(self):
        data = data_generator(10, 2, 10).generate()
        assertion.eq(100, len(data))
        self.assert_dimension(data, 2)


    def test_generate_with_centers(self):
        data = data_generator(3, 1, [5, 10, 15], [[0.0], [-5.0], [5.0]]).generate()
        assertion.eq(30, len(data))
        self.assert_distribution(data, [5, 10, 15], [[0.0], [-5.0], [5.0]], [1.0, 1.0, 1.0])
