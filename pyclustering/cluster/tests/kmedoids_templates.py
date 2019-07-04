"""!

@brief Test templates for K-Medoids clustering module.

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


import math
import numpy

from pyclustering.tests.assertion import assertion

from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

from pyclustering.utils import read_sample, calculate_distance_matrix
from pyclustering.utils.metric import distance_metric, type_metric

from random import random, randint


class kmedoids_test_template:
    @staticmethod
    def templateLengthProcessData(path_to_file, initial_medoids, expected_cluster_length, ccore_flag, **kwargs):
        kmedoids_test_template.templateLengthProcessWithMetric(path_to_file, initial_medoids, expected_cluster_length, None, ccore_flag, **kwargs)


    @staticmethod
    def templateLengthProcessWithMetric(path_to_file, initial_medoids, expected_cluster_length, metric, ccore_flag, **kwargs):
        sample = read_sample(path_to_file)
        data_type = kwargs.get('data_type', 'points')
        input_type = kwargs.get('input_type', 'list')
        initialize_medoids = kwargs.get('initialize_medoids', None)
        itermax = kwargs.get('itermax', 200)

        if metric is None:
            metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)

        input_data = sample
        if data_type == 'distance_matrix':
            input_data = calculate_distance_matrix(sample)

            if input_type == 'numpy':
                input_data = numpy.array(input_data)

        testing_result = False
        testing_attempts = 1
        if initialize_medoids is not None:  # in case center initializer randomization appears
            testing_attempts = 10

        for _ in range(testing_attempts):
            if initialize_medoids is not None:
                initial_medoids = kmeans_plusplus_initializer(sample, initialize_medoids).initialize(return_index=True)

            kmedoids_instance = kmedoids(input_data, initial_medoids, 0.001, ccore_flag, metric=metric, data_type=data_type, itermax=itermax)
            kmedoids_instance.process()

            clusters = kmedoids_instance.get_clusters()
            medoids = kmedoids_instance.get_medoids()

            if itermax == 0:
                assertion.eq([], clusters)
                assertion.eq(medoids, initial_medoids)
                return

            if len(clusters) != len(medoids):
                continue

            if len(set(medoids)) != len(medoids):
                continue

            obtained_cluster_sizes = [len(cluster) for cluster in clusters]
            if len(sample) != sum(obtained_cluster_sizes):
                continue

            if expected_cluster_length is not None:
                obtained_cluster_sizes.sort()
                expected_cluster_length.sort()
                if obtained_cluster_sizes != expected_cluster_length:
                    continue

            testing_result = True

        assertion.true(testing_result)


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [[random()] for i in range(10)] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ]
         
        kmedoids_instance = kmedoids(input_data, [ 5, 15, 25, 35 ], 0.025, ccore_flag)
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()
         
        assertion.eq(4, len(clusters))
        for cluster in clusters:
            assertion.eq(10, len(cluster))


    @staticmethod
    def templateAllocateRequestedClusterAmount(data, amount_clusters, initial_medoids, ccore_flag):
        if initial_medoids is None:
            initial_medoids = []
            for _ in range(amount_clusters):
                index_point = randint(0, len(data) - 1)
                while (index_point in initial_medoids):
                    index_point = randint(0, len(data) - 1)
                
                initial_medoids.append(index_point)
            
        kmedoids_instance = kmedoids(data, initial_medoids, 0.025, ccore = ccore_flag)
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()
        
        assertion.eq(len(clusters), amount_clusters)
        amount_objects = 0
        for cluster in clusters:
            amount_objects += len(cluster)
        
        assertion.eq(amount_objects, len(data))


    @staticmethod
    def templateClusterAllocationTheSameObjects(number_objects, number_clusters, ccore_flag = False):
        value = random()
        input_data = [ [value] ] * number_objects
        
        initial_medoids = []
        step = int(math.floor(number_objects / number_clusters))
        for i in range(number_clusters):
            initial_medoids.append(i * step)
        
        kmedoids_instance = kmedoids(input_data, initial_medoids, ccore=ccore_flag)
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()
        medoids = kmedoids_instance.get_medoids()

        assertion.eq(len(clusters), len(medoids))
        assertion.eq(len(set(medoids)), len(medoids))
        
        object_mark = [False] * number_objects
        allocated_number_objects = 0
        
        for cluster in clusters:
            for index_object in cluster: 
                assertion.eq(False, object_mark[index_object])    # one object can be in only one cluster.
                
                object_mark[index_object] = True
                allocated_number_objects += 1
            
        assertion.eq(number_objects, allocated_number_objects)    # number of allocated objects should be the same.


    @staticmethod
    def templatePredict(path_to_file, initial_medoids, points, expected_closest_clusters, ccore, **kwargs):
        sample = read_sample(path_to_file)

        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        itermax = kwargs.get('itermax', 200)

        kmedoids_instance = kmedoids(sample, initial_medoids, 0.001, ccore, metric=metric, itermax=itermax)
        kmedoids_instance.process()

        closest_clusters = kmedoids_instance.predict(points)
        assertion.eq(len(expected_closest_clusters), len(closest_clusters))
        assertion.true(numpy.array_equal(numpy.array(expected_closest_clusters), closest_clusters))
