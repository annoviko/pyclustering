"""!

@brief Integration-tests for CURE algorithm.

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

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.cluster.cure import cure
from pyclustering.cluster.tests.cure_templates import CureTestTemplates

from pyclustering.core.tests import remove_library


class CureIntegrationTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2, 5, 0.5, True)

    def testClusterAllocationSampleSimple2ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3, 5, 0.5, True)

    def testClusterAllocationSampleSimple3ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4, 5, 0.5, True)

    def testClusterAllocationSampleSimple4ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5, 5, 0.5, True)

    def testClusterAllocationSampleSimple5ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4, 5, 0.5, True)

    def testClusterAllocationSampleTwoDiamondsByCore(self):
        CureTestTemplates.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [399, 401], 2, 5, 0.3, True)

    def testClusterAllocationSampleLsunByCore(self):
        CureTestTemplates.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_LSUN, [100, 101, 202], 3, 5, 0.3, True)
 
    def testOneClusterAllocationSampleSimple1ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1, 5, 0.5, True)

    def testOneClusterAllocationSampleSimple2ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1, 5, 0.5, True)

    def testOneClusterAllocationSampleSimple3ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1, 5, 0.5, True)

    def testOneClusterAllocationSampleSimple4ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [75], 1, 5, 0.5, True)

    def testOneClusterAllocationSampleSimple5ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [60], 1, 5, 0.5, True)


    def testClusterAllocationTheSameData1ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [10, 20], 2, 5, 0.3, True)

    def testClusterAllocationTheSameData2ByCore(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 5, 5], 3, 5, 0.3, True)
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 10], 2, 5, 0.3, True)


    def testClusterAllocationOneDimensionDataByCore(self):
        CureTestTemplates.templateClusterAllocationOneDimensionData(True)


    def testEncoderProcedureByCore(self):
        CureTestTemplates.templateEncoderProcedures(True)


    def testCoreInterfaceIntInputData(self):
        cure_instance = cure([ [1], [2], [3], [20], [21], [22] ], 2, ccore = True)
        cure_instance.process()
        assert len(cure_instance.get_clusters()) == 2;


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2, 5, 0.5, True)
