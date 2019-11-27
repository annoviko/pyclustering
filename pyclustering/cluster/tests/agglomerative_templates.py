"""!

@brief Test templates for agglomerative clustering module.

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


from pyclustering.cluster.agglomerative import agglomerative;
from pyclustering.utils import read_sample;

from random import random;


class AgglomerativeTestTemplates:
    @staticmethod
    def templateClusteringResults(path, number_clusters, link, expected_length_clusters, ccore_flag):
        sample = read_sample(path)
        
        agglomerative_instance = agglomerative(sample, number_clusters, link, ccore_flag)
        agglomerative_instance.process()
        
        clusters = agglomerative_instance.get_clusters()
        
        assert sum([len(cluster) for cluster in clusters]) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;

    @staticmethod
    def templateClusterAllocationOneDimensionData(link, ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ]
        
        agglomerative_instance = agglomerative(input_data, 4, link, ccore_flag)
        agglomerative_instance.process()
        clusters = agglomerative_instance.get_clusters()
        
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;

    @staticmethod
    def templateClusterAllocationTheSameObjects(number_objects, number_clusters, link, ccore_flag):
        input_data = [ [random()] ] * number_objects
        
        agglomerative_instance = agglomerative(input_data, number_clusters, link, ccore_flag)
        agglomerative_instance.process()
        clusters = agglomerative_instance.get_clusters()
        
        assert len(clusters) == number_clusters;
        
        object_mark = [False] * number_objects
        allocated_number_objects = 0
        
        for cluster in clusters:
            for index_object in cluster: 
                assert (object_mark[index_object] == False);    # one object can be in only one cluster.
                
                object_mark[index_object] = True
                allocated_number_objects += 1
            
        assert (number_objects == allocated_number_objects);    # number of allocated objects should be the same.
