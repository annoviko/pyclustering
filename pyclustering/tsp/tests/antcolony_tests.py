"""!

@brief Unit-tests for ant colony based algorithm for travelling salesman problem.

@authors Andrei Novikov, Alexey Kukushkin (pyclustering@yandex.ru)
@date 2014-2016
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

from pyclustering.tsp.antcolony import antcolony, antcolony_parameters;
import pyclustering.core.antcolony_tsp_wrapper as wrapper;

from pyclustering.utils import euclidean_distance;


class Test(unittest.TestCase):
    def getCityDistance(self, result, object_locations, citiesDistRepresent):
        visited_objects = [False] * len(result.object_sequence);
        current_distance = 0.0;
        
        for i in range(len(result.object_sequence)):
            assert visited_objects[i] == False;
            
            index1 = result.object_sequence[i];
            index2 = result.object_sequence[(i + 1) % len(result.object_sequence)];
            
            if citiesDistRepresent == wrapper.CITIES_DISTANCE_SET_BY_MATRIX:
                current_distance += object_locations[index1][index2];
            else:
                current_distance += euclidean_distance(object_locations[index1], object_locations[index2]);
        
        return current_distance
        
    
    def templateTspSolving(self, parameters, object_locations, expected_length, citiesDistRepresent = wrapper.CITIES_DISTANCE_SET_BY_LIST_OF_COORDINATES):
        if (parameters is None):
            # default parameters
            parameters = antcolony_parameters();
        
        algorithm = antcolony(parameters);
        
        if citiesDistRepresent == wrapper.CITIES_DISTANCE_SET_BY_MATRIX:
            result = algorithm.process_by_matrix(object_locations);
        else:
            result = algorithm.process(object_locations);
        
        assert result.shortest_length == expected_length;
        
        assert len(result.object_sequence) == len(object_locations);
        
        current_distance = self.getCityDistance(result, object_locations, citiesDistRepresent)
        assert current_distance == expected_length;
        

    def testSixObjects(self):
        self.templateTspSolving(None, [[0.0, 1.0], [1.0, 1.0], [2.0, 1.0], [0.0, 0.0], [1.0, 0.0], [2.0, 0.0]], 6.0);
    
    
    def testSimpleSixObjectsSequence(self):
        self.templateTspSolving(None, [[0.0, 0.0], [0.0, 1.0], [0.0, 2.0], [0.0, 3.0], [0.0, 4.0], [0.0, 5.0]], 10.0);
    
    
    def testSmallestPathFourCitiesByMatrix(self):
        matrix = [[ 0.0,  1.0, 30.0, 99.0],
                  [ 1.0,  0.0,  1.0, 30.0],
                  [30.0,  1.0,  0.0,  1.0],
                  [99.0, 30.0,  1.0,  0.0],]
        
        self.templateTspSolving(None, matrix, 62.0, wrapper.CITIES_DISTANCE_SET_BY_MATRIX)



if __name__ == "__main__":
    unittest.main();