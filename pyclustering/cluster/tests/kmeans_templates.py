"""!

@brief Test templates for K-Means clustering module.

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

from pyclustering.cluster.encoder import type_encoding, cluster_encoder
from pyclustering.cluster.kmeans import kmeans, kmeans_observer, kmeans_visualizer

from pyclustering.utils import read_sample
from pyclustering.utils.metric import distance_metric, type_metric

from random import random

import numpy


class KmeansTestTemplates:
    @staticmethod
    def templateLengthProcessData(path_to_file, start_centers, expected_cluster_length, ccore, **kwargs):
        sample = read_sample(path_to_file)

        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        itermax = kwargs.get('itermax', 200)
        
        kmeans_instance = kmeans(sample, start_centers, 0.001, ccore, metric=metric, itermax=itermax)
        kmeans_instance.process()
        
        clusters = kmeans_instance.get_clusters()
        centers = kmeans_instance.get_centers()
        wce = kmeans_instance.get_total_wce()

        if itermax == 0:
            assertion.eq(start_centers, centers)
            assertion.eq([], clusters)
            assertion.eq(0.0, wce)
            return

        obtained_cluster_sizes = [len(cluster) for cluster in clusters]
        assertion.eq(len(sample), sum(obtained_cluster_sizes))
        
        assertion.eq(len(clusters), len(centers))
        for center in centers:
            assertion.eq(len(sample[0]), len(center))
        
        if expected_cluster_length is not None:
            obtained_cluster_sizes.sort()
            expected_cluster_length.sort()
            assertion.eq(obtained_cluster_sizes, expected_cluster_length)


    @staticmethod
    def templatePredict(path_to_file, initial_centers, points, expected_closest_clusters, ccore, **kwargs):
        sample = read_sample(path_to_file)

        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        itermax = kwargs.get('itermax', 200)

        kmeans_instance = kmeans(sample, initial_centers, 0.001, ccore, metric=metric, itermax=itermax)
        kmeans_instance.process()

        closest_clusters = kmeans_instance.predict(points)
        assertion.eq(len(expected_closest_clusters), len(closest_clusters))
        assertion.true(numpy.array_equal(numpy.array(expected_closest_clusters), closest_clusters))


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [random()] for _ in range(10) ] + [ [random() + 3] for _ in range(10) ] + [ [random() + 5] for _ in range(10) ] + [ [random() + 8] for _ in range(10) ]
        
        kmeans_instance = kmeans(input_data, [ [0.0], [3.0], [5.0], [8.0] ], 0.025, ccore_flag)
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
        
        assertion.eq(4, len(clusters))
        for cluster in clusters:
            assertion.eq(10, len(cluster))


    @staticmethod
    def templateEncoderProcedures(filename, initial_centers, number_clusters, ccore_flag):
        sample = read_sample(filename)
        
        kmeans_instance = kmeans(sample, initial_centers, 0.025, ccore_flag)
        kmeans_instance.process()
        
        clusters = kmeans_instance.get_clusters()
        encoding = kmeans_instance.get_cluster_encoding()
        
        encoder = cluster_encoder(encoding, clusters, sample)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        encoder.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        
        assertion.eq(number_clusters, len(clusters))


    @staticmethod
    def templateCollectEvolution(filename, initial_centers, number_clusters, ccore_flag):
        sample = read_sample(filename)
        
        observer = kmeans_observer()
        kmeans_instance = kmeans(sample, initial_centers, 0.025, ccore_flag, observer=observer)
        kmeans_instance.process()
        
        assertion.le(1, len(observer))
        for i in range(len(observer)):
            assertion.le(1, len(observer.get_centers(i)))
            for center in observer.get_centers(i):
                assertion.eq(len(sample[0]), len(center))
            
            assertion.le(1, len(observer.get_clusters(i)))


    @staticmethod
    def templateShowClusteringResultNoFailure(filename, initial_centers, ccore_flag):
        sample = read_sample(filename)

        kmeans_instance = kmeans(sample, initial_centers, 0.025, ccore_flag)
        kmeans_instance.process()

        clusters = kmeans_instance.get_clusters()
        centers = kmeans_instance.get_centers()

        kmeans_visualizer.show_clusters(sample, clusters, centers, initial_centers)


    @staticmethod
    def templateAnimateClusteringResultNoFailure(filename, initial_centers, ccore_flag):
        sample = read_sample(filename)

        observer = kmeans_observer()
        kmeans_instance = kmeans(sample, initial_centers, 0.025, ccore_flag, observer=observer)
        kmeans_instance.process()

        kmeans_visualizer.animate_cluster_allocation(sample, observer)
