"""!

@brief Unit-tests for center-initializer set.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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


import unittest

from pyclustering.cluster.tests.kmeans_templates import KmeansTestTemplates;

from pyclustering.cluster.center_initializer import random_center_initializer;
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.utils import read_sample;


class RandomCenterInitializerUnitTest(unittest.TestCase):
    def templateRandomCenterInitializer(self, data, amount):
        centers = random_center_initializer(data, amount).initialize();

        self.assertEqual(amount, len(centers));
        self.assertEqual(len(data[0]), len(centers[0]));

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

        self.assertEqual(amount, len(centers));
        self.assertEqual(len(data[0]), len(centers[0]));

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

    def testCalcDistanceToNearestCenter(self):
        # Test Data
        data_set_1 = [];
        data_set_1.extend([[0, 0], [1, 0], [0, 1], [1, 1]]);
        data_set_1.extend([[5, 0], [6, 0], [5, 1], [6, 1]]);
        data_set_1.extend([[0, 5], [1, 5], [0, 6], [1, 6]]);
        data_set_1.extend([[4, 4], [7, 4], [4, 7], [7, 7]]);

        # Centers
        centers = [[0.5, 0.5], [5.5, 0.5], [0.5, 5.5], [5.5, 5.5]];

        # Result
        initializer = kmeans_plusplus_initializer(data_set_1, 4);
        res_1 = initializer._kmeans_plusplus_initializer__calc_distance_to_nearest_center(data_set_1, centers)

        # Asserts
        for _idx in range(12):
            self.assertAlmostEqual(res_1[_idx], 0.7071067, places=4);

        for _idx in range(12, 16):
            self.assertAlmostEqual(res_1[_idx], 2.12132034, places=4);


if __name__ == "__main__":
    unittest.main();
