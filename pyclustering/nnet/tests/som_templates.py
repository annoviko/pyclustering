"""!

@brief Templates for tests of Self-Organization Map (SOM).

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
         
        if (parameters is None):
            parameters = som_parameters()
         
        for stucture in types:
            network = som(rows, cols, stucture, parameters, ccore = ccore_flag)
            if store_load:
                dump_network = pickle.dumps(network)
                network = pickle.loads(dump_network)

            network.train(sample, time, autostop)
            
            winners = network.get_winner_number()
            assert winners == len(expected_result)
            
            if sorted(network.awards) != expected_result:
                network.show_network(awards = True)
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
            network = som(5, 5, stucture, ccore = ccore_flag)
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
        
        network = som(1, 2, connections, ccore = ccore_flag)
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