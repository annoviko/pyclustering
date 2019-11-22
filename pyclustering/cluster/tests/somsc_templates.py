"""!

@brief Test templates for SOM-SC clustering module.

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


import numpy
import unittest

from pyclustering.cluster.somsc import somsc

from pyclustering.utils import read_sample

from random import random


class SyncnetTestTemplates(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, amount_clusters, expected_cluster_length, ccore):
        sample = read_sample(path_to_file)
        
        somsc_instance = somsc(sample, amount_clusters, 100, ccore)
        somsc_instance.process()
        
        clusters = somsc_instance.get_clusters()

        obtained_cluster_sizes = [len(cluster) for cluster in clusters]
        self.assertEqual(len(sample), sum(obtained_cluster_sizes))
        
        if expected_cluster_length is not None:
            obtained_cluster_sizes.sort()
            expected_cluster_length.sort()
            self.assertEqual(obtained_cluster_sizes,expected_cluster_length)


    def templateClusterAllocationOneDimensionData(self, ccore_flag):
        input_data = [[random()] for i in range(10)] + [[random() + 3] for i in range(10)] + \
                     [[random() + 5] for i in range(10)] + [[random() + 8] for i in range(10)]

        somsc_instance = somsc(input_data, 4, 100, ccore_flag)
        somsc_instance.process()
        clusters = somsc_instance.get_clusters()

        self.assertEqual(len(clusters), 4)
        for cluster in clusters:
            self.assertEqual(len(cluster), 10)


    def predict(self, path_to_file, amount_clusters, points, expected_closest_clusters, ccore):
        sample = read_sample(path_to_file)

        somsc_instance = somsc(sample, amount_clusters, 100, ccore)
        somsc_instance.process()

        closest_clusters = somsc_instance.predict(points)
        self.assertEqual(len(expected_closest_clusters), len(closest_clusters))
        self.assertTrue(numpy.array_equal(numpy.array(expected_closest_clusters), closest_clusters))
