"""!

@brief Unit-tests for center-initializer set.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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

from pyclustering.cluster.tests.kmeans_templates import KmeansTestTemplates;

from pyclustering.cluster.center_initializer import random_center_initializer;
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.utils import read_sample;

from pyclustering.tests.assertion import assertion;


class RandomCenterInitializerUnitTest(unittest.TestCase):
    def templateRandomCenterInitializer(self, data, amount):
        centers = random_center_initializer(data, amount).initialize();

        self.assertEqual(amount, len(centers));

        for center in centers:
            self.assertEqual(len(data[0]), len(center));

    def test1DimensionDataOneCenter(self):
        self.templateRandomCenterInitializer([[0.0], [1.0], [2.0], [3.0]], 1);
    
    def test2DimensionDataOneCenter(self):
        self.templateRandomCenterInitializer([[0.0, 0.5], [1.0, 1.5], [2.0, 2.5], [3.0, 3.5]], 1);

    def testGenerateTwoCenters(self):
        self.templateRandomCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 2);

    def testGenerateThreeCenters(self):
        self.templateRandomCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 3);

    def testGenerateFourCenters(self):
        self.templateRandomCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 4);

    def testGenerateTwoCentersIntData(self):
        self.templateRandomCenterInitializer([[0], [-1], [-2], [-3]], 2);


class KmeansPlusPlusInitializerUnitTest(unittest.TestCase):
    def templateKmeasPlusPlusCenterInitializer(self, data, amount):
        centers = kmeans_plusplus_initializer(data, amount).initialize();

        assertion.eq(amount, len(centers));

        for center in centers:
            assertion.eq(len(data[0]), len(center));

        return centers;

    def test1DimensionDataOneCenter(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [1.0], [2.0], [3.0]], 1);
    
    def test2DimensionDataOneCenter(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0, 0.5], [1.0, 1.5], [2.0, 2.5], [3.0, 3.5]], 1);

    def testGenerateTwoCenters(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 2);

    def testGenerateThreeCenters(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 3);

    def testGenerateFourCenters(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 4);

    def testGenerateTwoCentersIntData(self):
        self.templateKmeasPlusPlusCenterInitializer([[0], [-1], [-2], [-3]], 2);

    def testGenerateCentersIdenticalData1(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2], [1.2], [1.2], [1.2]], 2);

    def testGenerateCentersIdenticalData2(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2], [1.2], [1.2], [1.2]], 4);

    def testGenerateCentersThreeDimensionalData(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2, 1.3, 1.4], [1.2, 1.3, 1.4], [2.3, 2.3, 2.4], [2.1, 4.2, 1.1]], 3);

    def testGenerateCentersOnePoint(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2, 1.3, 1.4]], 1);

    def templateKmeansPlusPlusForClustering(self, path_sample, amount, expected_clusters_length):
        result_success = True;
        for _ in range(3):
            try:
                sample = read_sample(path_sample);
                start_centers = kmeans_plusplus_initializer(sample, amount).initialize();
                KmeansTestTemplates.templateLengthProcessData(path_sample, start_centers, expected_clusters_length, False);
            
            except AssertionError:
                continue;
            
            break;
        
        assert result_success == True;


    def testInitializerForKmeansSampleSimple01(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5]);

    def testInitializerForKmeansSampleSimple01TenCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, None);

    def testInitializerForKmeansSampleSimple02(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8]);

    def testInitializerForKmeansSampleSimple03(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30]);

    def testInitializerForKmeansSampleSimple04(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, [15, 15, 15, 15, 15]);

    def testInitializerForKmeansTotallySimilarObjectsTwoCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, None);

    def testInitializerForKmeansTotallySimilarObjectsFiveCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, None);

    def testInitializerForKmeansTotallySimilarObjectsTenCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 10, None);


if __name__ == "__main__":
    unittest.main();
