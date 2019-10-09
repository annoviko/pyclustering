"""!

@brief Unit-tests for center-initializer set.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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

from pyclustering.cluster.tests.kmeans_templates import KmeansTestTemplates
from pyclustering.cluster.tests.kmedoids_templates import kmedoids_test_template

from pyclustering.cluster.center_initializer import random_center_initializer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils import read_sample

from pyclustering.tests.assertion import assertion


class RandomCenterInitializerUnitTest(unittest.TestCase):
    def templateRandomCenterInitializer(self, data, amount):
        centers = random_center_initializer(data, amount).initialize()

        self.assertEqual(amount, len(centers))

        for center in centers:
            self.assertEqual(len(data[0]), len(center))

    def test1DimensionDataOneCenter(self):
        self.templateRandomCenterInitializer([[0.0], [1.0], [2.0], [3.0]], 1)
    
    def test2DimensionDataOneCenter(self):
        self.templateRandomCenterInitializer([[0.0, 0.5], [1.0, 1.5], [2.0, 2.5], [3.0, 3.5]], 1)

    def testGenerateTwoCenters(self):
        self.templateRandomCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 2)

    def testGenerateThreeCenters(self):
        self.templateRandomCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 3)

    def testGenerateFourCenters(self):
        self.templateRandomCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 4)

    def testGenerateTwoCentersIntData(self):
        self.templateRandomCenterInitializer([[0], [-1], [-2], [-3]], 2)


class KmeansPlusPlusInitializerUnitTest(unittest.TestCase):
    def templateKmeasPlusPlusCenterInitializer(self, data, amount, candidates=None):
        centers = kmeans_plusplus_initializer(data, amount, candidates).initialize()

        assertion.eq(amount, len(centers))

        for center in centers:
            assertion.eq(len(data[0]), len(center))

        return centers

    def test1DimensionDataOneCenter(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [1.0], [2.0], [3.0]], 1)
    
    def test2DimensionDataOneCenter(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0, 0.5], [1.0, 1.5], [2.0, 2.5], [3.0, 3.5]], 1)

    def testGenerateTwoCenters(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 2)

    def testGenerateThreeCenters(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 3)

    def testGenerateFourCenters(self):
        self.templateKmeasPlusPlusCenterInitializer([[0.0], [-1.0], [-2.0], [-3.0]], 4)

    def testGenerateTwoCentersIntData(self):
        self.templateKmeasPlusPlusCenterInitializer([[0], [-1], [-2], [-3]], 2)

    def testGenerateCentersIdenticalData1(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2], [1.2], [1.2], [1.2]], 2)

    def testGenerateCentersIdenticalData2(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2], [1.2], [1.2], [1.2]], 4)

    def testGenerateCentersThreeDimensionalData(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2, 1.3, 1.4], [1.2, 1.3, 1.4], [2.3, 2.3, 2.4], [2.1, 4.2, 1.1]], 3)

    def testGenerateCentersOnePoint(self):
        self.templateKmeasPlusPlusCenterInitializer([[1.2, 1.3, 1.4]], 1)

    def testTwoSimilarPointsTwoCenters1(self):
        self.templateKmeasPlusPlusCenterInitializer([[0], [0]], 2, "farthest")

    def testTwoSimilarPointsTwoCenters2(self):
        self.templateKmeasPlusPlusCenterInitializer([[20], [20]], 2, "farthest")

    def templateKmeansPlusPlusForClustering(self, path_sample, amount, expected_clusters_length):
        result_success = True
        for _ in range(3):
            try:
                sample = read_sample(path_sample)
                start_centers = kmeans_plusplus_initializer(sample, amount).initialize()
                KmeansTestTemplates.templateLengthProcessData(path_sample, start_centers, expected_clusters_length, False)
            
            except AssertionError:
                continue
            
            break
        
        self.assertTrue(result_success)


    def testInitializerForKmeansSampleSimple01(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5])

    def testInitializerForKmeansSampleSimple01TenCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, None)

    def testInitializerForKmeansSampleSimple02(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8])

    def testInitializerForKmeansSampleSimple03(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30])

    def testInitializerForKmeansSampleSimple04(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, [15, 15, 15, 15, 15])

    def testInitializerForKmeansTotallySimilarObjectsTwoCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, None)

    def testInitializerForKmeansTotallySimilarObjectsFiveCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, None)

    def testInitializerForKmeansTotallySimilarObjectsTenCenters(self):
        self.templateKmeansPlusPlusForClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 10, None)


    def templateKmeasPlusPlusCenterInitializerIndexReturn(self, data, amount):
        centers = kmeans_plusplus_initializer(data, amount).initialize(return_index=True)

        assertion.eq(amount, len(centers))

        for center_index in centers:
            assertion.gt(len(data), center_index)
            assertion.le(0, center_index)
            assertion.eq(1, centers.count(center_index))

        return centers

    def testSimple01ReturnIndex(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        for amount in range(1, len(sample)):
            self.templateKmeasPlusPlusCenterInitializerIndexReturn(sample, amount)

    def testSimple02ReturnIndex(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        for amount in range(1, len(sample)):
            self.templateKmeasPlusPlusCenterInitializerIndexReturn(sample, amount)

    def testSimple03ReturnIndex(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        for amount in range(1, len(sample)):
            self.templateKmeasPlusPlusCenterInitializerIndexReturn(sample, amount)

    def test1DimensionDataOneCenterReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[0.0], [1.0], [2.0], [3.0]], 1)

    def test2DimensionDataOneCenterReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[0.0, 0.5], [1.0, 1.5], [2.0, 2.5], [3.0, 3.5]], 1)

    def testGenerateTwoCentersReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[0.0], [-1.0], [-2.0], [-3.0]], 2)

    def testGenerateThreeCentersReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[0.0], [-1.0], [-2.0], [-3.0]], 3)

    def testGenerateFourCentersReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[0.0], [-1.0], [-2.0], [-3.0]], 4)

    def testGenerateTwoCentersIntDataReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[0], [-1], [-2], [-3]], 2)

    def testGenerateCentersIdenticalData1ReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[1.2], [1.2], [1.2], [1.2]], 2)

    def testGenerateCentersIdenticalData2ReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[1.2], [1.2], [1.2], [1.2]], 4)

    def testGenerateCentersThreeDimensionalDataReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn(
            [[1.2, 1.3, 1.4], [1.2, 1.3, 1.4], [2.3, 2.3, 2.4], [2.1, 4.2, 1.1]], 3)

    def testGenerateCentersOnePointReturnIndex(self):
        self.templateKmeasPlusPlusCenterInitializerIndexReturn([[1.2, 1.3, 1.4]], 1)

    def templateKmeansPlusPlusForKmedoidsClustering(self, path_sample, amount, expected_clusters_length):
        result_success = True
        for _ in range(3):
            try:
                sample = read_sample(path_sample)
                start_medoids = kmeans_plusplus_initializer(sample, amount).initialize(return_index=True)
                kmedoids_test_template.templateLengthProcessData(path_sample, start_medoids, expected_clusters_length,
                                                              False)

            except AssertionError:
                continue
            break

        assert result_success is True;

    def testInitializerForKmedoidsSampleSimple01(self):
        self.templateKmeansPlusPlusForKmedoidsClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5])

    def testInitializerForKmedoidsSampleSimple01TenCenters(self):
        self.templateKmeansPlusPlusForKmedoidsClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, None)

    def testInitializerForKmedoidsSampleSimple02(self):
        self.templateKmeansPlusPlusForKmedoidsClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8])

    def testInitializerForKmedoidsSampleSimple03(self):
        self.templateKmeansPlusPlusForKmedoidsClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30])

    def testInitializerForKmedoidsSampleSimple04(self):
        self.templateKmeansPlusPlusForKmedoidsClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, [15, 15, 15, 15, 15])


    def templateKmeansPlusPlusUnique(self, path_sample, amount, candidates):
        sample = read_sample(path_sample)
        start_medoids = kmeans_plusplus_initializer(sample, amount, candidates).initialize(return_index=True)

        unique_mediods = set(start_medoids)
        self.assertEqual(len(unique_mediods), len(start_medoids))

    def testKmeansPlusPlusUniqueCentersSimple01(self):
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, 1)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 1)

    def testKmeansPlusPlusUniqueCentersSeveralCandidatesSimple01(self):
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 5)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, 5)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 5)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 5)

    def testKmeansPlusPlusUniqueCentersFarthestCandidatesSimple01(self):
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 'farthest')
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, 'farthest')
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 'farthest')
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 'farthest')

    def testKmeansPlusPlusUniqueCentersSimple02(self):
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 1)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 23, 1)

    def testKmeansPlusPlusUniqueCentersSeveralCandidatesSimple02(self):
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 10)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 10)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 10)
        self.templateKmeansPlusPlusUnique(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 23, 10)


    def templateKmeansPlusPlusSeveralRuns(self, path_sample, amount, candidates):
        sample = read_sample(path_sample)

        attempts = 10
        for _ in range(attempts):
            medoids = kmeans_plusplus_initializer(sample, amount, candidates).initialize(return_index=True)
            medoids += kmeans_plusplus_initializer(sample, amount, candidates).initialize(return_index=True)
            medoids += kmeans_plusplus_initializer(sample, amount, candidates).initialize(return_index=True)

            unique_medoids = set(medoids)
            if len(unique_medoids) != len(medoids):
                continue

            return

        self.assertTrue(False, "K-Means++ does not return unique medoids during %d attempts." % attempts)

    def templateKmeansPlusPlusVariousCentersSimple01(self):
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1)
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1)

    def templateKmeansPlusPlusVariousCentersSeveralCandidatesSimple01(self):
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 3)

    def templateKmeansPlusPlusVariousCentersFarthestCandidatesSimple01(self):
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 'farthest')

    def templateKmeansPlusPlusVariousCentersSimple02(self):
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1)
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 1)

    def templateKmeansPlusPlusVariousCentersSimple03(self):
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 4, 1)
        self.templateKmeansPlusPlusSeveralRuns(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 8, 1)
