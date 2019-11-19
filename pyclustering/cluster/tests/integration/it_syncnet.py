"""!

@brief Integration-tests for Sync algorithm.

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

import unittest;

from numpy import pi;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');


from pyclustering.nnet import initial_type, conn_represent, solve_type;

from pyclustering.cluster.tests.syncnet_templates import SyncnetTestTemplates;
from pyclustering.cluster.syncnet import syncnet;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.core.tests import remove_library;


class SyncnetIntegrationTest(unittest.TestCase):
    def testClusteringSampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [5, 5], True);

    def testClusteringSampleSimple2ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [5, 8, 10], True);

    def testClusteringSampleSimple3ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [10, 10, 10, 30], True);

    def testClusteringSampleSimple4ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [15, 15, 15, 15, 15], True);

    def testClusteringSampleSimple5ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [15, 15, 15, 15], True);

    def testClusteringSampleElongateByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [135, 20], True);


    def testClusterAllocationHighToleranceSampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, None, [10], True);

    def testClusterAllocationHighToleranceSampleSimple2ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, None, [23], True);

    def testClusterAllocationHighToleranceSampleSimple3ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, None, [60], True);

    def testClusterAllocationHighToleranceSampleSimple4ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, None, [75], True);

    def testClusterAllocationHighToleranceSampleSimple5ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, None, [60], True);


    def testClusteringTheSameData1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [10, 20], True);

    def testClusteringTheSameData2ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5, 5], True);


    def testClusterAllocationConnWeightSampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, None, [5, 5], True);
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, None, [10], True);
         
    def testClusterAllocationConnWeightSampleSimple2ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, None, [5, 8, 10], True);
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, None, [23], True);


    def testClusteringWithoutDynamicCollectingSampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [5, 5], True);

    def testClusteringWithoutDynamicCollectingSampleSimple2ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [5, 8, 10], True);

    def testClusteringWithoutDynamicCollectingSampleSimple3ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [10, 10, 10, 30], True);


    def testClusteringRandomInitialSampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [5, 5], True);    

    def testClusteringRandomInitialSampleSimple2ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, None, [5, 8, 10], True);


    def testClusteringSolverRK4SampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.RK4, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5], True);

    def testClusteringSolverRKF45SampleSimple1ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.RKF45, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5], True);


    def testClusteringOneDimensionDataSampleSimple7ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 0.999, solve_type.FAST, initial_type.EQUIPARTITION, True, False, 0.05, conn_represent.MATRIX, [10, 10], True);

    def testClusteringOneDimensionDataSampleSimple9ByCore(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 0.999, solve_type.FAST, initial_type.EQUIPARTITION, True, False, 0.05, conn_represent.MATRIX, [20, 10], True);


    def testConnectionApiByCore(self):
        SyncnetTestTemplates.templateConnectionApi(conn_represent.MATRIX, True);
        SyncnetTestTemplates.templateConnectionApi(conn_represent.LIST, True);


    def testShowNetwork2DimensionByCore(self):
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, True);
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2.0, True);
 
    def testShowNetwork3DimensionByCore(self):
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1.0, True);

    def testCoreInterfaceIntInputData(self):
        result = False;
        for _ in range(0, 20, 1):
            syncnet_instance = syncnet([ [1], [2], [3], [20], [21], [22] ], 3, conn_represent.MATRIX, initial_type.EQUIPARTITION, ccore = True);
            analyser = syncnet_instance.process(0.999, solve_type.FAST);
            
            result = (len(analyser.allocate_clusters(0.1)) == 2);
            if (result is True): break;
        
        assert True == result;


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, None, [5, 5], True);
