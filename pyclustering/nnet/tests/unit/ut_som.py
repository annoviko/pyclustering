"""!

@brief Unit-tests for self-organized feature map.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
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

from pyclustering.nnet.tests.som_templates import SomTestTemplates
from pyclustering.nnet.som import som, type_conn, type_init, som_parameters

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES



class SomUnitTest(unittest.TestCase):
    def testTwoNeuronsTwoClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], False, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], False, False)


    def testTwoNeuronsTwoClustersStoreLoad(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], False, False, store_load=True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], False, False, store_load=True)


    def testAutostopTwoNeuronsTwoClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True, False)


    def testAutostopTwoNeuronsTwoClustersStoreLoad(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True, False, store_load=True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True, False, store_load=True)


    def testThreeNeuronsThreeClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], False, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], False, False)


    def testAutostopThreeNeuronsThreeClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], True, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], True, False)


    def testFourNeuronsFourClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], False, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], False, False)


    def testAutostopFourNeuronsFourClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], True, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], True, False)


    def testTwoNeuronsFourClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], False, False) 


    def testAutostopTwoNeuronsFourClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], True, False) 


    def testSevenNeuronsHeptaClusters(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], False, False) 


    def testAutostopSevenNeuronsHeptaClusters(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], True, False) 


    def testFourNeuronsTetraClusters(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], False, False)


    def testAutostopFourNeuronsTetraClusters(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], True, False)


    def testTwoNeuronsTwoDiamondsClusters(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], False, False)


    def testAutostopTwoNeuronsTwoDiamondsClusters(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], True, False)


    def testFiveNeuronsFiveClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], False, False)


    def testAutostopFiveNeuronsFiveClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], True, False)


    def testFourNeuronsSquareClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], False, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], False, False)


    def testAutostopFourNeuronsSquareClusters(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], True, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], True, False)


    def testOneDimensionSampleSimple7Cluster(self):
        parameters = som_parameters()
        parameters.init_type = type_init.random_surface
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 1, 100, [10, 10], True, False, parameters)


    def testHighEpochs(self):
        epochs = 1000
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, epochs, [5, 5], False, False)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, epochs, [10, 10, 10, 30], False, False)


    def testWinners(self):
        SomTestTemplates.templateTestWinners(False)


    def testDoubleTrain(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        
        parameters = som_parameters()
        network = som(2, 2, type_conn.grid_eight, parameters, ccore = False)
         
        network.train(sample, 100, False)
        network.train(sample, 100, False)
         
        assert sum(network.awards) == len(sample)
         
        total_capture_points = 0
        for points in network.capture_objects:
            total_capture_points += len(points)
         
        assert total_capture_points == len(sample)


    def testSimulateCheckWinnerFuncNeighbor(self):
        SomTestTemplates.templateTestSimulate(type_conn.func_neighbor, False)

    def testSimulateCheckWinnerFuncNeighborStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.func_neighbor, False, store_load=True)

    def testSimulateCheckWinnerGridFour(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_four, False)

    def testSimulateCheckWinnerGridFourStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_four, False, store_load=True)

    def testSimulateCheckWinnerGridEight(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_eight, False)

    def testSimulateCheckWinnerGridEightStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_eight, False, store_load=True)

    def testSimulateCheckWinnerHoneycomb(self):
        SomTestTemplates.templateTestSimulate(type_conn.honeycomb, False)

    def testSimulateCheckWinnerHoneycombStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.honeycomb, False, store_load=True)
