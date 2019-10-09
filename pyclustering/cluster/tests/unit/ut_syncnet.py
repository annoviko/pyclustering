"""!

@brief Unit-tests for Sync algorithm.

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


from pyclustering.nnet import initial_type, conn_represent, solve_type

from pyclustering.cluster.tests.syncnet_templates import SyncnetTestTemplates
from pyclustering.cluster.syncnet import syncnet, syncnet_visualizer

from pyclustering.utils import read_sample

from numpy import pi

from pyclustering.samples.definitions import SIMPLE_SAMPLES


class SyncnetUnitTest(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5], False);

    def testClusteringSampleSimple1ListRepr(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.LIST, [5, 5], False);

    def testClusteringSampleSimple2(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 8, 10], False);
     
    def testClusteringSampleSimple2ListRepr(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.LIST, [5, 8, 10], False);     

    def testClusteringSampleSimple3(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [10, 10, 10, 30], False);
  
    def testClusteringSampleSimple3ListRepr(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.LIST, [10, 10, 10, 30], False);

    def testClusteringSampleSimple4(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [15, 15, 15, 15, 15], False); 

    def testClusteringSampleSimple5(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [15, 15, 15, 15], False);


    def testClusteringTheSameData1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [10, 20], False);

    def testClusteringTheSameData2(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5, 5], False);


    def testClusterAllocationHighToleranceSampleSimple1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, conn_represent.MATRIX, [10], False);

    def testClusterAllocationHighToleranceSampleSimple2(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, conn_represent.MATRIX, [23], False);

    def testClusterAllocationHighToleranceSampleSimple3(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, conn_represent.MATRIX, [60], False);

    def testClusterAllocationHighToleranceSampleSimple4(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, conn_represent.MATRIX, [75], False);

    def testClusterAllocationHighToleranceSampleSimple5(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 2 * pi, conn_represent.MATRIX, [60], False);


    def testClusterAllocationConnWeightSampleSimple1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, conn_represent.MATRIX, [5, 5], False);
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, conn_represent.MATRIX, [10], False);
     
    def testClusterAllocationConnWeightSampleSimple2(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, conn_represent.MATRIX, [5, 8, 10], False);
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, True, 0.05, conn_represent.MATRIX, [23], False);


    def testClusteringWithoutDynamicCollectingSampleSimple1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [5, 5], False);

    def testClusteringWithoutDynamicCollectingSampleSimple2(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [5, 8, 10], False);

    def testClusteringWithoutDynamicCollectingSampleSimple3(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [10, 10, 10, 30], False);


    def testClusteringRandomInitialSampleSimple1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5], False);

    def testClusteringRandomInitialSampleSimple2(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, solve_type.FAST, initial_type.RANDOM_GAUSSIAN, False, False, 0.05, conn_represent.MATRIX, [5, 8, 10], False);


    def testClusteringSolverRK4SampleSimple1(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, solve_type.RK4, initial_type.RANDOM_GAUSSIAN, True, False, 0.05, conn_represent.MATRIX, [5, 5], False);


    def testClusteringOneDimensionDataSampleSimple7(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 0.999, solve_type.FAST, initial_type.EQUIPARTITION, True, False, 0.05, conn_represent.MATRIX, [10, 10], False);

    def testClusteringOneDimensionDataSampleSimple9(self):
        SyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 0.999, solve_type.FAST, initial_type.EQUIPARTITION, True, False, 0.05, conn_represent.MATRIX, [20, 10], False);


    def testShowNetwork2DimensionMatrixRepr(self):
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, conn_represent.MATRIX, False);
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2.0, conn_represent.MATRIX, False);

    def testShowNetwork2DimensionListRepr(self):
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, conn_represent.LIST, False);
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2.0, conn_represent.LIST, False);

    def testShowNetwork3DimensionMatrixRepr(self):
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1.0, conn_represent.MATRIX, False);

    def testShowNetwork3DimensionListRepr(self):
        SyncnetTestTemplates.templateShowNetwork(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1.0, conn_represent.LIST, False);


    def testConnectionApi(self):
        SyncnetTestTemplates.templateConnectionApi(conn_represent.MATRIX, False);
        SyncnetTestTemplates.templateConnectionApi(conn_represent.LIST, False);


    def testVisualizerNoFailure(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        network = syncnet(sample, 1.0, ccore=False)

        analyser = network.simulate(25, 5, solve_type.FAST, True)
        syncnet_visualizer.animate_cluster_allocation(sample, analyser)

    def test_incorrect_data(self):
        self.assertRaises(ValueError, syncnet, [], 0.5)
