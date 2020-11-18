"""!

@brief Templates for tests of Self-Organization Map (SOM).

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import pickle

import matplotlib
matplotlib.use('Agg')

from pyclustering.nnet.som import som, type_conn, som_parameters

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES


class SomTestTemplates:
    @staticmethod
    def templateTestAwardNeurons(file, rows, cols, time, expected_result, autostop, ccore_flag, parameters = None, **kwargs):
        store_load = kwargs.get('store_load', False)

        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb]
        sample = read_sample(file)
         
        if parameters is None:
            parameters = som_parameters()
         
        for structure in types:
            network = som(rows, cols, structure, parameters, ccore=ccore_flag)
            if store_load:
                dump_network = pickle.dumps(network)
                network = pickle.loads(dump_network)

            network.train(sample, time, autostop)
            
            winners = network.get_winner_number()
            assert winners == len(expected_result)
            
            if sorted(network.awards) != expected_result:
                network.show_network(awards=True)
                assert sorted(network.awards) == expected_result
             
            total_capture_points = 0
            for points in network.capture_objects:
                total_capture_points += len(points)
             
            assert total_capture_points == sum(expected_result)
         
            del network


    @staticmethod
    def templateTestWinners(ccore_flag):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb]
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
                
        for stucture in types:
            network = som(5, 5, stucture, ccore=ccore_flag)
            network.train(sample, 100)
                    
            assert sum(network.awards) == 60
                    
            points = list()
            for i in range(network.size):
                if network.awards[i] > 0:
                    points += network.capture_objects[i]
                    
            assert len(points) == len(sample)
                    
            points = sorted(points)
            for i in range(len(points)):
                assert points[i] == i


    @staticmethod
    def templateTestSimulate(connections, ccore_flag, **kwargs):
        store_load = kwargs.get('store_load', False)

        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        
        network = som(1, 2, connections, ccore=ccore_flag)
        network.train(sample, 100)

        if store_load:
            dump_network = pickle.dumps(network)
            network = pickle.loads(dump_network)

        expected_winners = [0, 1]
        for i in range(len(sample)):
            index_winner = network.simulate(sample[i])
            if (i == 0) and (index_winner == 1):
                expected_winners = [1, 0]
            
            if i < 5:
                assert expected_winners[0] == index_winner
            else:
                assert expected_winners[1] == index_winner

    @staticmethod
    def random_state(rows, cols, connections, random_state, ccore_flag):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

        params = som_parameters()
        params.random_state = random_state

        network_1 = som(rows, cols, connections, ccore=ccore_flag)
        steps_1 = network_1.train(sample, 100, True)

        network_2 = som(rows, cols, connections, ccore=ccore_flag)
        steps_2 = network_2.train(sample, 100, True)

        assert steps_1 == steps_2
        assert network_1.weights == network_2.weights
        assert network_1.capture_objects == network_2.capture_objects
        assert network_1.awards == network_2.awards
