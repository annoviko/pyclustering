"""!

@brief Unit-tests for ROCK algorithm.

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

from pyclustering.cluster.rock import rock
from pyclustering.cluster.tests.rock_templates import RockTestTemplates

from pyclustering.samples.definitions import SIMPLE_SAMPLES


class RockUnitTest(unittest.TestCase):  
    def testClusterAllocationSampleSimple1(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5], False)
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 0.5, [10], False)
        
    def testClusterAllocationSampleSimple2(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 0.5, [10, 5, 8], False)
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1, 0.5, [23], False)
        
    def testClusterAllocationSampleSimple3(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 0.5, [10, 10, 10, 30], False)
        
    def testClusterAllocationSampleSimple3WrongRadius(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.7, 4, 0.5, [10, 10, 10, 30], False)
        
    def testClusterAllocationSampleSimple4(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 0.5, [15, 15, 15, 15, 15], False)

    def testClusterAllocationSampleSimple4WrongRadius(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.5, 5, 0.5, [15, 15, 15, 15, 15], False)

    def testClusterAllocationSampleSimple5(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 0.5, [15, 15, 15, 15], False)

    def testClusterTheSameData1(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, 2, 0.5, [10, 20], False)

    def testClusterTheSameData2(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 2, 0.5, [5, 5, 5], False)


    def testClusterAllocationIncorrectNumberClusters(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 4, 0.5, [15, 15, 15, 15, 15], False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, rock, [], 0.1, 2)

    def test_incorrect_eps(self):
        self.assertRaises(ValueError, rock, [[0], [1], [2]], -1.0, 2)

    def test_incorrect_minpts(self):
        self.assertRaises(ValueError, rock, [[0], [1], [2]], 0.5, 0)

    def test_incorrect_amount_clusters(self):
        self.assertRaises(ValueError, rock, [[0], [1], [2]], 0.5, 1, -0.1)
        self.assertRaises(ValueError, rock, [[0], [1], [2]], 0.5, 1, 1.1)
