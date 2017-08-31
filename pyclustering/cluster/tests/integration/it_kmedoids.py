"""!

@brief Integration-tests for K-Medoids algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

from pyclustering.cluster.tests.kmedoids_templates import KmedoidsTestTemplates;
from pyclustering.cluster.kmedoids import kmedoids;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class KmedoidsIntegrationTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True);

    def testClusterOneAllocationSampleSimple1ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], True);

    def testClusterAllocationSampleSimple2ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], True);

    def testClusterOneAllocationSampleSimple2ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], True);

    def testClusterAllocationSampleSimple3ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], True);

    def testClusterOneAllocationSampleSimple3ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60], True);

    def testClusterAllocationSampleSimple5ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], True);

    def testClusterOneAllocationSampleSimple5ByCore(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60], True);


    def testClusterAllocationTheSameObjectsOneInitialMedoidByCore(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(20, 1, True);

    def testClusterAllocationTheSameObjectsTwoInitialMedoidsByCore(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(15, 2, True);

    def testClusterAllocationTheSameObjectsThreeInitialMedoidsByCore(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(25, 3, True);

    def testCoreInterfaceIntInputData(self):
        kmedoids_instance = kmedoids([ [1], [2], [3], [20], [21], [22] ], [ 2, 5 ], 0.025, True);
        kmedoids_instance.process();
        assert len(kmedoids_instance.get_clusters()) == 2;


if __name__ == "__main__":
    unittest.main();
