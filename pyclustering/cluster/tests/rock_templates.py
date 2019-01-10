"""!

@brief Test templates for ROCK clustering module.

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


from pyclustering.cluster.rock import rock;

from pyclustering.utils import read_sample;

from random import random;


class RockTestTemplates:
    @staticmethod
    def templateLengthProcessData(path_to_file, radius, cluster_numbers, threshold, expected_cluster_length, ccore):
        sample = read_sample(path_to_file);
        
        rock_instance = rock(sample, radius, cluster_numbers, threshold, ccore);
        rock_instance.process();
        clusters = rock_instance.get_clusters();
        
        length = sum([len(cluster) for cluster in clusters]);
        assert len(sample) == length;
        
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        
        assert obtained_cluster_sizes == expected_cluster_length;


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
        
        rock_instance = rock(input_data, 1, 4, 0.5, ccore_flag);
        rock_instance.process();
        clusters = rock_instance.get_clusters();
        
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
