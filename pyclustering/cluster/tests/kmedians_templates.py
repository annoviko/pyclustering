"""!

@brief Test templates for K-Medians clustering module.

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


from pyclustering.tests.assertion import assertion

from pyclustering.cluster.kmedians import kmedians

from pyclustering.utils import read_sample, distance_metric, type_metric

from random import random

import numpy


class KmediansTestTemplates:
    @staticmethod
    def templateLengthProcessData(data, start_medians, expected_cluster_length, ccore, **kwargs):
        tolerance = kwargs.get('tolerance', 0.01)
        metric = kwargs.get('metric', None)
        itermax = kwargs.get('itermax', 200)

        if isinstance(data, str):
            sample = read_sample(data)
        else:
            sample = data

        kmedians_instance = kmedians(sample, start_medians, tolerance, ccore, metric=metric, itermax=itermax)
        kmedians_instance.process()
        
        clusters = kmedians_instance.get_clusters()
        medians = kmedians_instance.get_medians()
        wce = kmedians_instance.get_total_wce()

        if itermax == 0:
            assert clusters == []
            assert start_medians == medians
            assert 0.0 == wce
            return

        obtained_cluster_sizes = [len(cluster) for cluster in clusters]
        assert len(sample) == sum(obtained_cluster_sizes)
        assert len(medians) == len(clusters)
        
        if expected_cluster_length is not None:
            obtained_cluster_sizes.sort()
            expected_cluster_length.sort()
            if obtained_cluster_sizes != expected_cluster_length:
                print(obtained_cluster_sizes)
            assert obtained_cluster_sizes == expected_cluster_length


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ]
         
        kmedians_instance = kmedians(input_data, [ [0.0], [3.0], [5.0], [8.0] ], 0.025, ccore)
        kmedians_instance.process()
        clusters = kmedians_instance.get_clusters()
         
        assert len(clusters) == 4
        for cluster in clusters:
            assert len(cluster) == 10


    @staticmethod
    def templateClusterAllocationTheSameObjects(number_objects, number_clusters, ccore_flag):
        value = random()
        input_data = [ [value] ] * number_objects
         
        initial_centers = []
        for i in range(number_clusters):
            initial_centers.append([ random() ])
         
        kmedians_instance = kmedians(input_data, initial_centers, ccore=ccore_flag)
        kmedians_instance.process()
        clusters = kmedians_instance.get_clusters()
         
        object_mark = [False] * number_objects
        allocated_number_objects = 0
         
        for cluster in clusters:
            for index_object in cluster: 
                assert (object_mark[index_object] is False)    # one object can be in only one cluster.
                 
                object_mark[index_object] = True
                allocated_number_objects += 1
             
        assert (number_objects == allocated_number_objects)    # number of allocated objects should be the same.


    @staticmethod
    def templatePredict(path_to_file, initial_medians, points, expected_closest_clusters, ccore, **kwargs):
        sample = read_sample(path_to_file)

        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        itermax = kwargs.get('itermax', 200)

        kmeans_instance = kmedians(sample, initial_medians, 0.001, ccore, metric=metric, itermax=itermax)
        kmeans_instance.process()

        closest_clusters = kmeans_instance.predict(points)
        assertion.eq(len(expected_closest_clusters), len(closest_clusters))
        assertion.true(numpy.array_equal(numpy.array(expected_closest_clusters), closest_clusters))
