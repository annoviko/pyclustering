"""!

@brief Test templates for CURE clustering module.

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

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils import read_sample

from pyclustering.cluster.cure import cure
from pyclustering.cluster.encoder import type_encoding, cluster_encoder

from pyclustering.tests.assertion import assertion

from random import random


class CureTestTemplates:
    @staticmethod
    def template_cluster_allocation(input_data, cluster_sizes, number_cluster, number_represent_points = 5, compression = 0.5, ccore_flag = False, **kwargs):
        if isinstance(input_data, str):
            sample = read_sample(input_data)
        else:
            sample = input_data

        numpy_usage = kwargs.get('numpy_usage', False)
        if numpy_usage is True:
            sample = numpy.array(sample)
         
        cure_instance = cure(sample, number_cluster, number_represent_points, compression, ccore = ccore_flag)
        cure_instance.process()
         
        clusters = cure_instance.get_clusters()
        representors = cure_instance.get_representors()
        means = cure_instance.get_means()

        assertion.eq(len(clusters), number_cluster)
        assertion.eq(len(representors), number_cluster)
        assertion.eq(len(means), number_cluster)
         
        obtained_cluster_sizes = [len(cluster) for cluster in clusters]
         
        total_length = sum(obtained_cluster_sizes)
        assertion.eq(total_length, len(sample))
         
        cluster_sizes.sort()
        obtained_cluster_sizes.sort()
        assertion.eq(cluster_sizes, obtained_cluster_sizes)


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [random()] for _ in range(10) ] + [ [random() + 3] for _ in range(10) ] + [ [random() + 5] for _ in range(10) ] + [ [random() + 8] for _ in range(10) ]
         
        cure_instance = cure(input_data, 4, ccore = ccore_flag)
        cure_instance.process()
        clusters = cure_instance.get_clusters()

        assertion.eq(4, len(clusters))
        for cluster in clusters:
            assertion.eq(10, len(cluster))


    @staticmethod
    def templateEncoderProcedures(ccore_flag):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        
        cure_instance = cure(sample, 4, 5, 0.5, ccore = ccore_flag)
        cure_instance.process()
        
        clusters = cure_instance.get_clusters()
        encoding = cure_instance.get_cluster_encoding()
        
        encoder = cluster_encoder(encoding, clusters, sample)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        encoder.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)

        assertion.eq(4, len(clusters))


    @staticmethod
    def exception(type, input_data, number_cluster, number_represent_points, compression, ccore_flag):
        try:
            if isinstance(input_data, str):
                sample = read_sample(input_data)
            else:
                sample = input_data

            cure_instance = cure(sample, number_cluster, number_represent_points, compression, ccore=ccore_flag)
            cure_instance.process()

        except type:
            return

        except Exception as ex:
            raise AssertionError("Expected: '%s', Actual: '%s'" % (type, type(ex).__name__))

        raise AssertionError("Expected: '%s', Actual: 'None'" % type)
