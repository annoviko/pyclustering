"""!

@brief Unit-tests for X-Means algorithm.

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

from pyclustering.cluster.tests.xmeans_templates import XmeansTestTemplates;
from pyclustering.cluster.xmeans import splitting_type;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;


class XmeansUnitTest(unittest.TestCase):
    def testBicClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testBicSampleSimple1WithoutInitialCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testBicWrongStartClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testMndlClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, False);

    def testMndlSampleSimple1WithoutInitialCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, False);

    def testBicClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testBicWrongStartClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testMndlClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);

    def testMndlWrongStartClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);

    def testBicClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION);    

    def testBicWrongStartClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION); 

    def testMndlClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);    

    def testBicClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testBicWrongStartClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testMndlClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);

    def testBicClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testBicWrongStartClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testMndlClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);

    def testMndlWrongStartClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);  

    def testBicClusterAllocationSampleTwoDiamonds(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testBicWrongStartClusterAllocationSampleTwoDiamonds(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION);

    def testMndlClusterAllocationSampleTwoDiamonds(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);


    def testClusterAllocationOneDimensionData(self):
        XmeansTestTemplates.templateClusterAllocationOneDimensionData(False);


if __name__ == "__main__":
    unittest.main();