"""!

@brief Integration-tests for K-Medians algorithm.

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

from pyclustering.cluster.tests.kmedians_templates import KmediansTestTemplates;

from pyclustering.cluster.kmedians import kmedians;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class KmediansIntegrationTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True);

    def testClusterOneAllocationSampleSimple1Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], True);

    def testClusterAllocationSampleSimple2Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True);

    def testClusterOneAllocationSampleSimple2Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], True);

    def testClusterAllocationSampleSimple3Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True);

    def testClusterOneAllocationSampleSimple3Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], True);

    def testClusterAllocationSampleSimple5Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], True);

    def testClusterOneAllocationSampleSimple5Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], True);

    def testClusterAllocationSample1WrongInitialNumberCenters1Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.8, 9.5], [3.5, 6.6], [1.3, 4.0]], None, True);

    def testClusterAllocationSample1WrongInitialNumberCenters2Core(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.8, 9.5], [3.5, 6.6], [1.3, 4.0], [1.2, 4.5]], None, True);

    def testClusterAllocationSample2WrongInitialNumberCentersCore(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5], [7.3, 4.5], [3.1, 5.4]], None, True);


    def testClusterAllocationOneDimensionDataCore(self):
        KmediansTestTemplates.templateClusterAllocationOneDimensionData(True);


    def testClusterAllocationTheSameObjectsOneInitialCenterCore(self):
        KmediansTestTemplates.templateClusterAllocationTheSameObjects(20, 1, True);

    def testClusterAllocationTheSameObjectsTwoInitialCentersCore(self):
        KmediansTestTemplates.templateClusterAllocationTheSameObjects(15, 2, True);

    def testClusterAllocationTheSameObjectsThreeInitialCentersCore(self):
        KmediansTestTemplates.templateClusterAllocationTheSameObjects(25, 3, True);

    def testClusterAllocationSampleRoughMediansSimple10ByCore(self):
        initial_medians = [[0.0772944481804071, 0.05224990900863469], [1.6021689021213712, 1.0347579135245601], [2.3341008076636096, 1.280022869739064]];
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, initial_medians, None, True);

    def testCoreInterfaceIntInputData(self):
        kmedians_instance = kmedians([ [1], [2], [3], [20], [21], [22] ], [ [2], [21] ], ccore=True);
        kmedians_instance.process();
        assert len(kmedians_instance.get_clusters()) == 2;


if __name__ == "__main__":
    unittest.main();