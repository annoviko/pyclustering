"""!

@brief Unit-tests for CURE algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from pyclustering.cluster.tests.cure_templates import CureTestTemplates;


class CureUnitTest(unittest.TestCase): 
    def testClusterAllocationSampleSimple1(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2);

    def testClusterAllocationSampleSimple2(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3);

    def testClusterAllocationSampleSimple3(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4);

    def testClusterAllocationSampleSimple4(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5);

    def testClusterAllocationSampleSimple5(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4);

    def testClusterAllocationSampleTwoDiamonds(self):
        CureTestTemplates.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [400, 400], 2, 5, 0.3);

    def testClusterAllocationSampleLsun(self):
        CureTestTemplates.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_LSUN, [100, 101, 202], 3, 5, 0.3);

    def testOneClusterAllocationSampleSimple1(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1);

    def testOneClusterAllocationSampleSimple2(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1);

    def testOneClusterAllocationSampleSimple3(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1);

    def testOneClusterAllocationSampleSimple4(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [75], 1);

    def testOneClusterAllocationSampleSimple5(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [60], 1);


    def testClusterAllocationOneDimensionData(self):
        CureTestTemplates.templateClusterAllocationOneDimensionData(False);


    def testClusterAllocationTheSameData1(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [10, 20], 2, 5, 0.3);

    def testClusterAllocationTheSameData2(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 5, 5], 3, 5, 0.3);
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 10], 2, 5, 0.3);


    def testEncoderProcedure(self):
        CureTestTemplates.templateEncoderProcedures(False);


if __name__ == "__main__":
    unittest.main();