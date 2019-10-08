"""!

@brief Unit-tests for EMA algorithm.

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

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.ema import ema, ema_observer, ema_initializer, ema_init_type, ema_visualizer
from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES, FAMOUS_SAMPLES


class EmaUnitTest(unittest.TestCase):
    def templateDataClustering(self, sample_path, 
                               amount_clusters, 
                               expected_clusters_sizes, 
                               init_type = ema_init_type.KMEANS_INITIALIZATION):
        testing_result = False
        attempts = 10
        
        for _ in range(attempts):
            sample = read_sample(sample_path)
            
            means, variances = None, None
            if init_type is not ema_init_type.KMEANS_INITIALIZATION:
                means, variances = ema_initializer(sample, amount_clusters).initialize(init_type)
            
            ema_instance = ema(sample, amount_clusters, means, variances)
            ema_instance.process()
            
            clusters = ema_instance.get_clusters()
            centers = ema_instance.get_centers()
            covariances = ema_instance.get_covariances()
            probabilities = ema_instance.get_probabilities()
            
            assert len(centers) == len(clusters)
            assert len(covariances) == len(clusters)
            assert len(probabilities) == len(clusters)
            
            for cluster_probability in probabilities:
                assert len(cluster_probability) == len(sample)
            
            for index_point in range(len(sample)):
                total_probability = 0.0
                for cluster_probability in probabilities:
                    total_probability += cluster_probability[index_point]
                
                assert abs(total_probability - 1.0) <= 0.00001
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters]
            if len(sample) != sum(obtained_cluster_sizes):
                continue
            
            if expected_clusters_sizes is not None:
                obtained_cluster_sizes.sort()
                expected_clusters_sizes.sort()
                if obtained_cluster_sizes != expected_clusters_sizes:
                    continue
            
            testing_result = True
            break
        
        assert testing_result is True


    def testClusteringSampleSimple01(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5])

    def testClusteringSampleSimple01RandomInit(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], ema_init_type.RANDOM_INITIALIZATION)

    def testClusteringSampleSimple01OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10])

    def testClusteringSampleSimple01OneClusterRandomInit(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], ema_init_type.RANDOM_INITIALIZATION)

    def testClusteringSampleSimple01ThreeCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None)

    def testClusteringSampleSimple01ThreeClusterRandomInit(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None, ema_init_type.RANDOM_INITIALIZATION)

    def testClusteringSampleSimple01TenCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, None)

    def testClusteringSampleSimple01SevenCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 7, None)

    def testClusteringSampleSimple02(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [5, 8, 10])

    def testClusteringSampleSimple02OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23])

    def testClusteringSampleSimple02ThreeCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None)

    def testClusteringSampleSimple03(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30])

    def testClusteringSampleSimple03OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, [60])

    def testClusteringSampleSimple05(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, [15, 15, 15, 15])

    def testClusteringSampleSimple05OneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, [60])

    def testClusteringCommonOldFaithful(self):
        self.templateDataClustering(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL, 2, [97, 175])

    def testClusteringFcpsLsun(self):
        self.templateDataClustering(FCPS_SAMPLES.SAMPLE_LSUN, 3, [100, 101, 202])

    def testClusteringOneDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10])

    def testClusteringOneDimensionalDataRandomInit(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10], ema_init_type.RANDOM_INITIALIZATION)

    def testClusteringOneDimensionalDataOneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1, [20])

    def testClusteringThreeDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, [10, 10])

    def testClusteringThreeDimensionalDataOneCluster(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, [20])

    def testClusteringTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, None)

    def testClusteringTotallySimilarObjectsTwoClusters(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, None)

    def testClusteringTotallySimilarObjectsThreeClustersRandonInit(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 3, None, ema_init_type.RANDOM_INITIALIZATION)

    def testClusteringTotallySimilarObjectsFiveClusters(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, None)

    def testClusteringTotallySimilarObjectsFiveClustersRandomInit(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, None, ema_init_type.RANDOM_INITIALIZATION)


    def testObserver(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        
        means, variances = ema_initializer(sample, 3).initialize(ema_init_type.RANDOM_INITIALIZATION)
        
        observer_instance = ema_observer()
        ema_instance = ema(sample, 3, means, variances, observer_instance)
        ema_instance.process()
        
        observer_length = len(observer_instance)
        assert observer_length > 0
        assert observer_length == len(observer_instance.get_evolution_clusters())
        assert observer_length == len(observer_instance.get_evolution_covariances())
        assert observer_length == len(observer_instance.get_evolution_means())
        assert observer_length == observer_instance.get_iterations()


    def testVisualizerNoFailures(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        
        means, variances = ema_initializer(sample, 4).initialize(ema_init_type.RANDOM_INITIALIZATION)
        
        observer_instance = ema_observer()
        ema_instance = ema(sample, 4, means, variances, observer_instance)
        ema_instance.process()
        
        clusters = ema_instance.get_clusters()
        means = ema_instance.get_centers()
        covariances = ema_instance.get_covariances()
        
        ema_visualizer.show_clusters(clusters, sample, covariances, means)
        ema_visualizer.animate_cluster_allocation(sample, observer_instance)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, ema, [], 2)

    def test_incorrect_amount_clusters(self):
        self.assertRaises(ValueError, ema, [[0], [1], [2]], 0)
