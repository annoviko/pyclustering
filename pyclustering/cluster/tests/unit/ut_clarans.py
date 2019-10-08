"""!

@brief Unit-tests for CLARANS algorithm.

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

import matplotlib
matplotlib.use('Agg')

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils import read_sample

from pyclustering.cluster.clarans import clarans


class ClaransUnitTest(unittest.TestCase):
    def templateClusterAllocation(self, path, cluster_sizes, number_clusters, iterations, maxneighbors):
        result_testing = False
        
        # it's randomized algorithm therefore attempts are required
        for _ in range(0, 5, 1):
            sample = read_sample(path)
            
            clarans_instance = clarans(sample, number_clusters, iterations, maxneighbors)
            clarans_instance.process()
            clusters = clarans_instance.get_clusters()
    
            obtained_cluster_sizes = [len(cluster) for cluster in clusters]
            
            total_length = sum(obtained_cluster_sizes)
            if total_length != len(sample):
                continue
            
            cluster_sizes.sort()
            obtained_cluster_sizes.sort()
            if cluster_sizes != obtained_cluster_sizes:
                continue
            
            result_testing = True
            break
        
        assert result_testing == True


    def testClusterAllocationSampleSimple1(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2, 10, 3)

    def testClusterAllocationSampleSimple2(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3, 10, 3)

    def testClusterAllocationSampleSimple3(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4, 10, 3)
       
    def testClusterAllocationSampleSimple5(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4, 10, 5)
       
    def testClusterAllocationSampleSimple7(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [10, 10], 2, 10, 5)
       
    def testClusterAllocationSampleSimple8(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [15, 30, 20, 80], 4, 15, 5)


    def testClusterAllocationTheSameData1(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [10, 20], 2, 15, 5)

    def testClusterAllocationTheSameData2(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 10], 2, 15, 5)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, clarans, [], 1, 0, 0)

    def test_incorrect_amount_clusters(self):
        self.assertRaises(ValueError, clarans, [[0], [1], [2]], 0, 0, 0)

    def test_incorrect_local_minima(self):
        self.assertRaises(ValueError, clarans, [[0], [1], [2]], 1, -1, 0)

    def test_incorrect_max_neighbors(self):
        self.assertRaises(ValueError, clarans, [[0], [1], [2]], 1, 0, -1)
