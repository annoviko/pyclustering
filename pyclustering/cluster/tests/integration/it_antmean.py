"""!

@brief Unit-tests for ant means algorithm.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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


import unittest;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.cluster.antmean import antmean, antmean_clustering_params;

from pyclustering.utils import read_sample;


class AntmeanIntegrationTest(unittest.TestCase):
    def templateSimpleClustering(self, path, count_clusters, expected_length_clusters, iterations, count_ants, pheramone_init, ro):
        attempts = 15;

        params = antmean_clustering_params();
        params.iterations = iterations;
        params.count_ants = count_ants;
        params.pheramone_init = pheramone_init;
        params.ro = ro;

        sample = read_sample(path);
        
        testing_result = False;
        for _ in range(attempts):
            algo = antmean(sample, count_clusters, params);
            
            algo.process();
    
            clusters = algo.get_clusters();
            if (sum([len(cluster) for cluster in clusters]) != len(sample)):
                continue;
            
            if (len(clusters) != len(expected_length_clusters)):
                continue;
            
            if (sum([len(cluster) for cluster in clusters]) != sum(expected_length_clusters)):
                continue;
            
            if (sorted([len(cluster) for cluster in clusters]) != sorted(expected_length_clusters)):
                continue;
            
            testing_result = True;
            break;
        
        assert testing_result == True;


    def testClusteringSampleSimple01(self):
        self.templateSimpleClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], 50, 100, 0.1, 0.9);

    def testClusteringSampleSimple02(self):
        self.templateSimpleClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [5, 8, 10], 400, 500, 0.1, 0.9);

    def testClusteringOneDimensionalData(self):
        self.templateSimpleClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10], 400, 500, 0.1, 0.9);


if __name__ == "__main__":
    unittest.main()
