"""!

@brief Integration-tests for ROCK algorithm.

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


import unittest;

import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.tests.rock_templates import RockTestTemplates;
from pyclustering.cluster.rock import rock;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.core.tests import remove_library;


class RockIntegrationTest(unittest.TestCase):  
    def testClusterAllocationByCore(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 0.5, [10], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 0.5, [10, 5, 8], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1, 0.5, [23], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 0.5, [10, 10, 10, 30], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.7, 4, 0.5, [10, 10, 10, 30], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 0.5, [15, 15, 15, 15, 15], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.5, 5, 0.5, [15, 15, 15, 15, 15], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 0.5, [15, 15, 15, 15], True); 

    def testClusterAllocationByCoreIncorrectNumberOfClusters(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 4, 0.5, [15, 15, 15, 15, 15], True);

    def testClusterTheSameData1ByCore(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, 2, 0.5, [10, 20], True);

    def testClusterTheSameData2ByCore(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 2, 0.5, [5, 5, 5], True);

    def testClusterAllocationOneDimensionDataByCore(self):
        RockTestTemplates.templateClusterAllocationOneDimensionData(True);

    def testCoreInterfaceIntInputData(self):
        optics_instance = rock([ [1], [2], [3], [20], [21], [22] ], 3, 2, 0.5, True);
        optics_instance.process();
        assert len(optics_instance.get_clusters()) == 2;


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5], True);
