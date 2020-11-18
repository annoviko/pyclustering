"""!

Unit-tests for dimension analyser.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.utils.dimension import dimension_info;


class DimensionUnitTest(unittest.TestCase):
    def testGetDimension(self):
        info = dimension_info([ [1], [2], [3], [4], [5] ]);
        assert 1 == info.get_dimensions();
        
        info = dimension_info([[1, 2], [3, 4]]);
        assert 2 == info.get_dimensions();
