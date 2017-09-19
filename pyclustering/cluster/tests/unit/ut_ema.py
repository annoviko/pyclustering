"""!

@brief Unit-tests for EMA algorithm.

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

import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.ema import ema, ema_observer, ema_initializer, ema_init_type, ema_visualizer;
from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;


class EmaUnitTest(unittest.TestCase):
    def templateDataClustering(self, sample_path, 
                               amount_clusters, 
                               expected_clusters_sizes, 
                               init_type = ema_init_type.KMEANS_INITIALIZATION):
        testing_result = False;
        
        for _ in range(3):
            sample = read_sample(sample_path);
            
            means, variances = None, None;
            if (init_type is not ema_init_type.KMEANS_INITIALIZATION):
                means, variances = ema_initializer().initialize(init_type);
            
            ema_instance = ema(sample, amount_clusters, means, variances);
            ema_instance.process();
            
            clusters = ema_instance.get_clusters();
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters];
            if (len(sample) != sum(obtained_cluster_sizes)):
                continue;
            
            if (expected_clusters_sizes != None):
                obtained_cluster_sizes.sort();
                expected_clusters_sizes.sort();
                if (obtained_cluster_sizes != expected_clusters_sizes):
                    continue;
            
            testing_result = True;
            break;
        
        assert testing_result == True;


    def testClusteringSampleSimple01(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5]);

    def testClusteringSampleSimple01OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10]);

    def testClusteringSampleSimple01ThreeCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None);

    def testClusteringSampleSimple01TenCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, None);

    def testClusteringSampleSimple01SevenCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 7, None);

    def testClusteringSampleSimple02(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [5, 8, 10]);

    def testClusteringSampleSimple02OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23]);

    def testClusteringSampleSimple02ThreeCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None);

    def testClusteringSampleSimple03(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30]);

    def testClusteringSampleSimple03OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, [60]);

    def testClusteringSampleSimple04(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, [15, 15, 15, 15, 15]);

    def testClusteringSampleSimple04OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, [75]);

    def testClusteringSampleSimple05(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, [15, 15, 15, 15]);

    def testClusteringSampleSimple05OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, [60]);

    def testClusteringOneDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10]);

    def testClusteringOneDimensionalDataOneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1, [20]);

    def testClusteringThreeDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, [10, 10]);

    def testClusteringThreeDimensionalDataOneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, [20]);

    def testClusteringTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, None);

    def testClusteringTotallySimilarObjectsTwoClusters(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, None);

    @unittest.skip("Wait for correction in kmeans++")
    def testClusteringTotallySimilarObjectsFiveClusters(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, None);


if __name__ == "__main__":
    unittest.main();