"""!

@brief Test templates for CURE clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.utils import read_sample;

from pyclustering.cluster.cure import cure;
from pyclustering.cluster.encoder import type_encoding, cluster_encoder;

from random import random;


class CureTestTemplates:
    @staticmethod
    def template_cluster_allocation(path, cluster_sizes, number_cluster, number_represent_points = 5, compression = 0.5, ccore_flag = False):
        sample = read_sample(path);
         
        cure_instance = cure(sample, number_cluster, number_represent_points, compression, ccore = ccore_flag);
        cure_instance.process();
         
        clusters = cure_instance.get_clusters();
        representors = cure_instance.get_representors();
        means = cure_instance.get_means();
 
        assert len(clusters) == number_cluster;
        assert len(representors) == number_cluster;
        assert len(means) == number_cluster;
         
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
         
        total_length = sum(obtained_cluster_sizes);
        assert total_length == len(sample);
         
        cluster_sizes.sort();
        obtained_cluster_sizes.sort();
        assert cluster_sizes == obtained_cluster_sizes;


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [random()] for _ in range(10) ] + [ [random() + 3] for _ in range(10) ] + [ [random() + 5] for _ in range(10) ] + [ [random() + 8] for _ in range(10) ];
         
        cure_instance = cure(input_data, 4, ccore = ccore_flag);
        cure_instance.process();
        clusters = cure_instance.get_clusters();
         
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;


    @staticmethod
    def templateEncoderProcedures(ccore_flag):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        
        cure_instance = cure(sample, 4, 5, 0.5, ccore = ccore_flag);
        cure_instance.process();
        
        clusters = cure_instance.get_clusters();
        encoding = cure_instance.get_cluster_encoding();
        
        encoder = cluster_encoder(encoding, clusters, sample);
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        encoder.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        
        assert 4 == len(clusters);