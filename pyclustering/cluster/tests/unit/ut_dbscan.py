"""!

@brief Unit-tests for DBSCAN algorithm.

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

from pyclustering.cluster.tests.dbscan_templates import DbscanTestTemplates

from pyclustering.cluster.dbscan import dbscan

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS
from pyclustering.samples.definitions import FCPS_SAMPLES


class DbscsanUnitTest(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], False)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 2, [10], False)

    def testClusteringSampleSimple1Randomize(self):
        DbscanTestTemplates.templateClusteringResultsRandomize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], False)

    def testClusteringSampleSimple1DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], False)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 2, [10], False)

    def testClusteringSampleSimple2(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], False)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 2, [23], False)

    def testClusteringSampleSimple2Randomize(self):
        DbscanTestTemplates.templateClusteringResultsRandomize(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], False)

    def testClusteringSampleSimple2DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], False)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 2, [23], False)

    def testClusteringSampleSimple3(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], False)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 3, [60], False)

    def testClusteringSampleSimple3Randomize(self):
        DbscanTestTemplates.templateClusteringResultsRandomize(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], False)

    def testClusteringSampleSimple3DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], False)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 3, [60], False)

    def testClusteringSampleSimple4(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], False)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 3, [75], False)

    def testClusteringSampleSimple4DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], False)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 3, [75], False)

    def testClusteringSampleSimple5(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], False)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 3, [60], False)

    def testClusteringSampleSimple5DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], False)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 3, [60], False)

    def testClusteringHepta(self):
        DbscanTestTemplates.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, [30, 30, 30, 30, 30, 30, 32], False)
        DbscanTestTemplates.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 5, 3, [212], False)

    def testClusteringTheSameData1(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 3, [10, 20], False)

    def testClusteringTheSameData1DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 3, [10, 20], False)

    def testClusteringTheSameData2(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 2, [5, 5, 5], False)

    def testClusteringTheSameData2DistanceMatrix(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 2, [5, 5, 5], False)


    def testLengthProcessedSampleSimple1(self):
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10, False)

    def testLengthProcessedSampleSimple1DistanceMatrix(self):
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10, False)

    def testLengthProcessedSampleSimple2(self):    
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15, False)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15, False)

    def testLengthProcessedSampleSimple2DistanceMatrix(self):
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15, False)
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15, False)

    def testLengthProcessedSampleSimple3(self):
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20, False)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20, False)

    def testLengthProcessedSampleSimple3DistanceMatrix(self):
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20, False)
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20, False)

    def testLengthProcessedSampleSimple4(self):
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75, False)

    def testLengthProcessedSampleSimple4DistanceMatrix(self):
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75, False)

    def testLengthProcessedSampleSimple5(self):
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10, False)

    def testLengthProcessedSampleSimple5DistanceMatrix(self):
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10, False)
        DbscanTestTemplates.templateLengthProcessDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10, False)


    def testPermutationSampleSimple14(self):
        DbscanTestTemplates.templateClusteringWithAnswers(SIMPLE_SAMPLES.SAMPLE_SIMPLE14,
                                                          SIMPLE_ANSWERS.ANSWER_SIMPLE14, 1.0, 5, False,
                                                          random_order=True,
                                                          repeat=20)


    def testClusterAllocationOneDimensionData(self):
        DbscanTestTemplates.templateClusterAllocationOneDimensionData(False)

    def testClusterAllocationOneDimensionDistanceMatrix(self):
        DbscanTestTemplates.templateClusterAllocationOneDimensionDistanceMatrix(False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, dbscan, [], 0.1, 1)

    def test_incorrect_eps(self):
        self.assertRaises(ValueError, dbscan, [[0], [1], [2]], -1.0, 1)
