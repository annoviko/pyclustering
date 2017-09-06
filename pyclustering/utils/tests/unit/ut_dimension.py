"""!

Unit-tests for dimension analyser.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import unittest;

from pyclustering.utils.dimension import dimension_info;


class DimensionUnitTest(unittest.TestCase):
    def testGetDimension(self):
        info = dimension_info([ [1], [2], [3], [4], [5] ]);
        assert 1 == info.get_dimensions();
        
        info = dimension_info([[1, 2], [3, 4]]);
        assert 2 == info.get_dimensions();


if __name__ == "__main__":
    unittest.main();