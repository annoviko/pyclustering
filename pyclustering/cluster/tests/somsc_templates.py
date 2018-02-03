"""!

@brief Test templates for SOM-SC clustering module.

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


from pyclustering.cluster.somsc import somsc;

from pyclustering.utils import read_sample;

from random import random;


class SyncnetTestTemplates:
    @staticmethod
    def templateLengthProcessData(path_to_file, amount_clusters, expected_cluster_length, ccore):
        sample = read_sample(path_to_file);
        
        somsc_instance = somsc(sample, amount_clusters, 100, ccore);
        somsc_instance.process();
        
        clusters = somsc_instance.get_clusters();

        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        if (expected_cluster_length != None):
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            if (obtained_cluster_sizes != expected_cluster_length):
                print 
            assert obtained_cluster_sizes == expected_cluster_length;


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];

        somsc_instance = somsc(input_data, 4, 100, ccore_flag);
        somsc_instance.process();
        clusters = somsc_instance.get_clusters();

        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;