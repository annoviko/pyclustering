"""!

@brief Unit-tests for K-Medoids algorithm.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.tests.kmedoids_templates import KmedoidsTestTemplates;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.utils import read_sample;


class KmedoidsUnitTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5]);

    def testClusterOneAllocationSampleSimple1(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10]);

    def testClusterAllocationSampleSimple2(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8]);

    def testClusterOneAllocationSampleSimple2(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23]);

    def testClusterAllocationSampleSimple3(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30]);

    def testClusterOneAllocationSampleSimple3(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60]);

    def testClusterAllocationSampleSimple5(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15]);

    def testClusterOneAllocationSampleSimple5(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60]);


    def testClusterAllocationOneDimensionData(self):
        KmedoidsTestTemplates.templateClusterAllocationOneDimensionData();


    def testClusterAllocationTheSameObjectsOneInitialMedoid(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(20, 1, False);

    def testClusterAllocationTheSameObjectsTwoInitialMedoids(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(15, 2, False);

    def testClusterAllocationTheSameObjectsThreeInitialMedoids(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(25, 3, False);


    def testAllocatedRequestedClustersSampleSimple01(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 5, None, False);

    def testAllocatedRequestedClustersSampleSimple02(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 5, None, False);

    def testAllocatedRequestedClustersSampleSimple03(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 5, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 8, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 10, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 15, None, False);

    def testAllocatedRequestedClustersSampleSimple04(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 10, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 25, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 40, None, False);

    def testAllocatedRequestedClustersWithTheSamePoints(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [ [0.0, 0.0], [0.1, 0.1], [0.0, 0.0], [0.1, 0.2] ];
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False);


    def testAllocatedRequestedClustersWithTotallyTheSamePoints(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [ [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0] ];
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False);
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False);


if __name__ == "__main__":
    unittest.main();
