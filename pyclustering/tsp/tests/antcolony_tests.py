"""!

@brief Unit-tests for ant colony based algorithm for travelling salesman problem.

@authors Andrei Novikov (pyclustering@yandex.ru)
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


class Test(unittest.TestCase):
    def templateTspSolving(self, parameters, object_locations, expected_length, expected_order):
        if (parameters is None):
            # default parameters
            parameters = antcolony_parameters();
        
        algorithm = antcolony(parameters);
        result = algorithm.process(object_locations);
        
        assert result.shortest_length == expected_length;
        
        print(result.object_sequence);
        if (expected_order != None):
            assert result.object_sequence == expected_order;


    def testSixObjects(self):
        self.templateTspSolving(None, [[0.0, 1.0], [1.0, 1.0], [2.0, 1.0], [0.0, 0.0], [1.0, 0.0], [2.0, 0.0]], 6.0, None);
    
    
    def testSimpleSixObjectsSequence(self):
        self.templateTspSolving(None, [[0.0, 0.0], [0.0, 1.0], [0.0, 2.0], [0.0, 3.0], [0.0, 4.0], [0.0, 5.0]], 10.0, [0, 1, 2, 3, 4, 5]);


if __name__ == "__main__":
    unittest.main();