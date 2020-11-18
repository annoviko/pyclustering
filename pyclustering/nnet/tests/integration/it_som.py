"""!

@brief Integration-tests for self-organized feature map.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.nnet.tests.som_templates import SomTestTemplates
from pyclustering.nnet.som import som, type_conn, type_init, som_parameters

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.core.tests import remove_library


class SomIntegrationTest(unittest.TestCase):
    def testTwoNeuronsTwoClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], False, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], False, True)

    def testTwoNeuronsTwoClustersByCoreStoreLoad(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], False, True, store_load=True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], False, True, store_load=True)


    def testAutostopTwoNeuronsTwoClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True, True)


    def testAutostopTwoNeuronsTwoClustersByCoreStoreLoad(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True, True, store_load=True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True, True, store_load=True)


    def testThreeNeuronsThreeClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], False, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], False, True)


    def testAutostopThreeNeuronsThreeClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], True, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], True, True)


    def testFourNeuronsFourClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], False, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], False, True)


    def testAutostopFourNeuronsFourClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], True, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], True, True)


    def testTwoNeuronsFourClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], False, True)


    def testAutostopTwoNeuronsFourClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], True, True)


    def testSevenNeuronsHeptaClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], False, True)


    def testAutostopSevenNeuronsHeptaClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], True, True)


    def testFourNeuronsTetraClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], False, True)


    def testAutostopFourNeuronsTetraClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], True, True)


    def testTwoNeuronsTwoDiamondsClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], False, True)


    def testAutostopTwoNeuronsTwoDiamondsClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], True, True)


    def testFiveNeuronsFiveClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], False, True)


    def testAutostopFiveNeuronsFiveClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], True, True)


    def testFourNeuronsSquareClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], False, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], False, True)


    def testAutostopFourNeuronsSquareClustersByCore(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], True, True)
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], True, True)


    def testOneDimensionSampleSimple7ClusterByCore(self):
        parameters = som_parameters()
        parameters.init_type = type_init.random_surface
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 1, 100, [10, 10], True, True, parameters)


    def testWinnersByCore(self):
        SomTestTemplates.templateTestWinners(True)


    def testSomVisualizationByCore(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        
        parameters = som_parameters()
        network = som(5, 5, type_conn.grid_eight, parameters, ccore = True)
        network.train(sample, 100, True)
        
        network.show_network()
        network.show_winner_matrix()
        network.show_distance_matrix()
        network.show_density_matrix()


    def testSimulateCheckWinnerFuncNeighborByCore(self):
        SomTestTemplates.templateTestSimulate(type_conn.func_neighbor, True)

    def testSimulateCheckWinnerFuncNeighborByCoreStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.func_neighbor, True, store_load=True)

    def testSimulateCheckWinnerGridFourByCore(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_four, True)

    def testSimulateCheckWinnerGridFourByCoreStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_four, True, store_load=True)

    def testSimulateCheckWinnerGridEightByCore(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_eight, True)

    def testSimulateCheckWinnerGridEightByCoreStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.grid_eight, True, store_load=True)

    def testSimulateCheckWinnerHoneycombByCore(self):
        SomTestTemplates.templateTestSimulate(type_conn.honeycomb, True)

    def testSimulateCheckWinnerHoneycombByCoreStoreLoad(self):
        SomTestTemplates.templateTestSimulate(type_conn.honeycomb, True, store_load=True)

    def testNetwork2x2RandomState5ByCore(self):
        SomTestTemplates.random_state(2, 2, type_conn.honeycomb, 5, True)

    def testNetwork2x2RandomState5FuncNeighborByCore(self):
        SomTestTemplates.random_state(2, 2, type_conn.func_neighbor, 5, True)

    def testNetwork2x2RandomState10ByCore(self):
        SomTestTemplates.random_state(2, 2, type_conn.honeycomb, 10, True)

    def testNetwork2x2RandomState10FuncNeighborByCore(self):
        SomTestTemplates.random_state(2, 2, type_conn.func_neighbor, 10, True)

    def testNetwork2x3RandomState5ByCore(self):
        SomTestTemplates.random_state(2, 3, type_conn.honeycomb, 5, True)

    def testNetwork2x3RandomState10ByCore(self):
        SomTestTemplates.random_state(2, 3, type_conn.honeycomb, 10, True)

    def testNetwork1x8RandomState5ByCore(self):
        SomTestTemplates.random_state(1, 8, type_conn.honeycomb, 5, True)

    def testNetwork1x8RandomState10ByCore(self):
        SomTestTemplates.random_state(1, 8, type_conn.honeycomb, 10, True)

    def testNetwork1x8GridFourByCore(self):
        SomTestTemplates.random_state(1, 8, type_conn.grid_four, 5, True)
        SomTestTemplates.random_state(8, 1, type_conn.grid_four, 5, True)

    def testNetwork1x8GridEightByCore(self):
        SomTestTemplates.random_state(1, 8, type_conn.grid_eight, 5, True)
        SomTestTemplates.random_state(8, 1, type_conn.grid_eight, 5, True)

    def testNetwork1x8FuncNeughborByCore(self):
        SomTestTemplates.random_state(1, 8, type_conn.func_neighbor, 5, True)
        SomTestTemplates.random_state(8, 1, type_conn.func_neighbor, 5, True)


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        SomTestTemplates.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], False, True)
