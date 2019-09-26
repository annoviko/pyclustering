"""!

@brief Test templates for X-Means clustering module.

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
import random

from pyclustering.cluster.xmeans import xmeans, splitting_type
from pyclustering.cluster.center_initializer import random_center_initializer

from pyclustering.utils import read_sample, distance_metric, type_metric

from pyclustering.tests.assertion import assertion


class XmeansTestTemplates:
    @staticmethod
    def templateLengthProcessData(input_sample, start_centers, expected_cluster_length, type_splitting, kmax, ccore, **kwargs):
        if isinstance(input_sample, str):
            sample = read_sample(input_sample)
        else:
            sample = input_sample

        xmeans_instance = xmeans(sample, start_centers, kmax, 0.025, type_splitting, ccore, **kwargs)
        xmeans_instance.process()
         
        clusters = xmeans_instance.get_clusters()
        centers = xmeans_instance.get_centers()
        wce = xmeans_instance.get_total_wce()
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters]

        assertion.eq(len(sample), sum(obtained_cluster_sizes))
        assertion.eq(len(clusters), len(centers))
        assertion.le(len(centers), kmax)

        expected_wce = 0.0
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        for index_cluster in range(len(clusters)):
            for index_point in clusters[index_cluster]:
                expected_wce += metric(sample[index_point], centers[index_cluster])

        assertion.eq(expected_wce, wce)

        if expected_cluster_length is not None:
            assertion.eq(len(centers), len(expected_cluster_length))

            obtained_cluster_sizes.sort()
            expected_cluster_length.sort()
            
            assertion.eq(obtained_cluster_sizes, expected_cluster_length)


    @staticmethod
    def templatePredict(path_to_file, initial_centers, points, expected_amount, expected_closest_clusters, ccore, **kwargs):
        sample = read_sample(path_to_file)

        kmax = kwargs.get('kmax', 20)

        xmeans_instance = xmeans(sample, initial_centers, kmax, 0.025, splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore)
        xmeans_instance.process()

        closest_clusters = xmeans_instance.predict(points)
        assertion.eq(expected_amount, len(xmeans_instance.get_clusters()))
        assertion.eq(len(expected_closest_clusters), len(closest_clusters))
        assertion.true(numpy.array_equal(numpy.array(expected_closest_clusters), closest_clusters))


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [[0.0] for _ in range(10)] + [[5.0] for _ in range(10)] + [[10.0] for _ in range(10)] + [[15.0] for _ in range(10)]
            
        xmeans_instance = xmeans(input_data, [[0.5], [5.5], [10.5], [15.5]], 20, 0.025, splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore_flag)
        xmeans_instance.process()
        
        clusters = xmeans_instance.get_clusters()
        centers = xmeans_instance.get_centers()

        assertion.eq(len(clusters), 4)
        assertion.eq(len(centers), len(clusters))
        
        assertion.le(len(clusters), 20)
        for cluster in clusters:
            assertion.eq(len(cluster), 10)


    @staticmethod
    def templateMaxAllocatedClusters(ccore_flag, amount_clusters, size_cluster, offset, kinitial, kmax):
        input_data = []
        for index in range(amount_clusters):
            for _ in range(size_cluster):
                input_data.append([random.random() * index * offset, random.random() * index * offset])
        
        initial_centers = random_center_initializer(input_data, kinitial).initialize()
        xmeans_instance = xmeans(input_data, initial_centers, kmax, 0.025, splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore_flag)
        xmeans_instance.process()
        
        clusters = xmeans_instance.get_clusters()
        centers = xmeans_instance.get_centers()

        if len(clusters) != len(centers):
            print(input_data)
            print(initial_centers)

        assertion.ge(kmax, len(clusters))
        assertion.ge(kmax, len(centers))
        assertion.eq(len(clusters), len(centers))
