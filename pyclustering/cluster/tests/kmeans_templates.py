"""!

@brief Test templates for K-Means clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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


from pyclustering.cluster.encoder import type_encoding, cluster_encoder;
from pyclustering.cluster.kmeans import kmeans;

from pyclustering.utils import read_sample;

from random import random;


class KmeansTestTemplates:
    @staticmethod
    def templateLengthProcessData(path_to_file, start_centers, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        
        kmeans_instance = kmeans(sample, start_centers, 0.025, ccore);
        kmeans_instance.process();
        
        clusters = kmeans_instance.get_clusters();
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        if (expected_cluster_length != None):
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            assert obtained_cluster_sizes == expected_cluster_length;


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
        
        kmeans_instance = kmeans(input_data, [ [0.0], [3.0], [5.0], [8.0] ], 0.025, ccore_flag);
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
        
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;


    @staticmethod
    def templateEncoderProcedures(sample, initial_centers, number_clusters, ccore_flag):
        sample = read_sample(sample);
        
        cure_instance = kmeans(sample, initial_centers, 0.025, ccore_flag);
        cure_instance.process();
        
        clusters = cure_instance.get_clusters();
        encoding = cure_instance.get_cluster_encoding();
        
        encoder = cluster_encoder(encoding, clusters, sample);
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        encoder.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        
        assert number_clusters == len(clusters);
