"""!

@brief Test templates for X-Means clustering module.

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

import random;

from pyclustering.cluster.xmeans import xmeans, splitting_type;
from pyclustering.cluster.center_initializer import random_center_initializer;

from pyclustering.utils import read_sample;

from pyclustering.tests.assertion import assertion;


class XmeansTestTemplates:
    @staticmethod
    def templateLengthProcessData(input_sample, start_centers, expected_cluster_length, type_splitting, kmax, ccore):
        sample = None;
        if (isinstance(input_sample, str)):
            sample = read_sample(input_sample);
        else:
            sample = input_sample;
        
        #clusters = xmeans(sample, start_centers, 20, ccore);
        xmeans_instance = xmeans(sample, start_centers, kmax, 0.025, type_splitting, ccore);
        xmeans_instance.process();
         
        clusters = xmeans_instance.get_clusters();
        centers = xmeans_instance.get_centers();
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];

        assert len(sample) == sum(obtained_cluster_sizes);
        assert len(clusters) == len(centers);
        assert len(centers) <= kmax;
        
        if (expected_cluster_length is not None):
            assert len(centers) == len(expected_cluster_length);
            
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            
            assert obtained_cluster_sizes == expected_cluster_length;


    @staticmethod
    def templateClusterAllocationOneDimensionData(ccore_flag):
        input_data = [ [0.0] for _ in range(10) ] + [ [5.0] for _ in range(10) ] + [ [10.0] for _ in range(10) ] + [ [15.0] for _ in range(10) ];
            
        xmeans_instance = xmeans(input_data, [ [0.5], [5.5], [10.5], [15.5] ], 20, 0.025, splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore_flag);
        xmeans_instance.process();
        
        clusters = xmeans_instance.get_clusters();
        centers = xmeans_instance.get_centers();

        assert len(clusters) == 4;
        assert len(centers) == len(clusters);
        
        assert len(clusters) <= 20;
        for cluster in clusters:
            assert len(cluster) == 10;


    @staticmethod
    def templateMaxAllocatedClusters(ccore_flag, amount_clusters, size_cluster, offset, kinitial, kmax):
        input_data = [];
        for index in range(amount_clusters):
            input_data.append([random.random() * index * offset, random.random() * index * offset]);
        
        initial_centers = random_center_initializer(input_data, kinitial).initialize();
        xmeans_instance = xmeans(input_data, initial_centers, kmax, 0.025, splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore_flag);
        xmeans_instance.process();
        
        clusters = xmeans_instance.get_clusters();
        centers = xmeans_instance.get_centers();

        if (len(clusters) != len(centers)):
            print(input_data);
            print(initial_centers);

        assertion.ge(kmax, len(clusters));
        assertion.ge(kmax, len(centers));
        assertion.eq(len(clusters), len(centers));