"""!

@brief Test templates for DBSCAN clustering module.

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


from pyclustering.utils import read_sample;
from pyclustering.cluster.dbscan import dbscan;

from random import random;


class DbscanTestTemplates:
    @staticmethod
    def templateClusteringResults(path, radius, neighbors, expected_length_clusters, ccore = False):
        sample = read_sample(path);
         
        dbscan_instance = dbscan(sample, radius, neighbors, ccore);
        dbscan_instance.process();
         
        clusters = dbscan_instance.get_clusters();
        noise = dbscan_instance.get_noise();
         
        assert sum([len(cluster) for cluster in clusters]) + len(noise) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;


    @staticmethod
    def templateLengthProcessData(path_to_file, radius, min_number_neighbors, max_number_neighbors, ccore = False):
        for _ in range(min_number_neighbors, max_number_neighbors, 1):
            sample = read_sample(path_to_file);
             
            dbscan_instance = dbscan(sample, radius, min_number_neighbors, ccore);
            dbscan_instance.process();
             
            clusters = dbscan_instance.get_clusters();
            noise = dbscan_instance.get_noise();
             
            length = len(noise);
            length += sum([len(cluster) for cluster in clusters]);
         
            assert len(sample) == length;


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        for _ in range(50):
            input_data = [ [random()] for _ in range(10) ] + [ [random() + 3] for _ in range(10) ] + [ [random() + 6] for _ in range(10) ] + [ [random() + 9] for _ in range(10) ];
    
            dbscan_instance = dbscan(input_data, 1.0, 2, ccore_flag);
            dbscan_instance.process();
                
            clusters = dbscan_instance.get_clusters();
                
            assert len(clusters) == 4;
            for cluster in clusters:
                assert len(cluster) == 10;