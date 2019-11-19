"""!

@brief Unit-tests for chaotic neural network (CNN).

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

from pyclustering.nnet.cnn import type_conn, cnn_network, cnn_visualizer

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils import read_sample


class CnnUnitTest(unittest.TestCase):
    def templateSyncEnsembleAllocation(self, stimulus, steps, connection, amount_neighbors, analysed_iterations, expected_length_ensembles):
        testing_result = True;
        
        for _ in range(3):
            network_instance = cnn_network(len(stimulus), connection, amount_neighbors);
            assert len(stimulus) == len(network_instance);
            
            output_dynamic = network_instance.simulate(steps, stimulus);
            
            ensembles = output_dynamic.allocate_sync_ensembles(analysed_iterations);
            obtained_ensemble_sizes = [len(ensemble) for ensemble in ensembles];
    
            # critical checks - always determined
            assert len(stimulus) == len(network_instance);
            assert len(stimulus) == sum(obtained_ensemble_sizes);
            
            if (expected_length_ensembles != None):
                obtained_ensemble_sizes.sort();
                expected_length_ensembles.sort();
                
                if (obtained_ensemble_sizes != expected_length_ensembles):
                    continue;

        assert testing_result == True;

    
    def testClusteringPhenomenonSimpleSample01(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.ALL_TO_ALL, 3, 10, [5, 5]);

    def testGlobalSynchronizationSimpleSample01(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.ALL_TO_ALL, 9, 10, [10]);

    def testDelaunayTriangulationSimpleSample01(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.TRIANGULATION_DELAUNAY, 3, 10, None);

    def testClusteringPhenomenonSimpleSample02(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.ALL_TO_ALL, 3, 10, [10, 5, 8]);

    def testGlobalSynchronizationSimpleSample02(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.ALL_TO_ALL, 22, 10, [10, 5, 8]);

    def testDelaunayTriangulationSimpleSample02(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.TRIANGULATION_DELAUNAY, 22, 10, None);

    def testClusteringPhenomenonSimpleSample03(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.ALL_TO_ALL, 3, 10, [10, 10, 10, 30]);

    def testClusteringPhenomenonSimpleSample04(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
        self.templateSyncEnsembleAllocation(stimulus, 200, type_conn.ALL_TO_ALL, 10, 10, [15, 15, 15, 15, 15]);

    def testClusteringPhenomenonSimpleSample05(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE5);
        self.templateSyncEnsembleAllocation(stimulus, 100, type_conn.ALL_TO_ALL, 5, 10, [15, 15, 15, 15]);

    def testChaoticNeuralNetwork2DVisualization(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        network_instance = cnn_network(len(stimulus));
        
        output_dynamic = network_instance.simulate(100, stimulus);
        
        network_instance.show_network();
        
        cnn_visualizer.show_dynamic_matrix(output_dynamic);
        cnn_visualizer.show_observation_matrix(output_dynamic);
        cnn_visualizer.show_output_dynamic(output_dynamic);

    def testChaoticNeuralNetwork3DVisualization(self):
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE11);
        network_instance = cnn_network(len(stimulus));
        
        output_dynamic = network_instance.simulate(10, stimulus);
        
        network_instance.show_network();
        
        cnn_visualizer.show_dynamic_matrix(output_dynamic);
        cnn_visualizer.show_observation_matrix(output_dynamic);
        cnn_visualizer.show_output_dynamic(output_dynamic);
