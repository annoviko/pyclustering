"""!

@brief Unit-tests for CURE algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.cluster.tests.cure_templates import CureTestTemplates


class CureUnitTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2)

    def testClusterAllocationSampleSimple1OneRepresentor(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2, 1, 0.5)

    def testClusterAllocationSampleSimple1NumPy(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2, numpy_usage=True)

    def testClusterAllocationSampleSimple2(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3)

    def testClusterAllocationSampleSimple2NoCompression(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3, 5, 0.0)

    def testClusterAllocationSampleSimple2NumPy(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3, numpy_usage=True)

    def testClusterAllocationSampleSimple3(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4)

    def testClusterAllocationSampleSimple3OneRepresentor(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4, 1, 0.5)

    def testClusterAllocationSampleSimple3NumPy(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4, numpy_usage=True)

    def testClusterAllocationSampleSimple4(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5)

    def testClusterAllocationSampleSimple4NumPy(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5, numpy_usage=True)

    def testClusterAllocationSampleSimple5(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4)

    def testClusterAllocationSampleSimple5NumPy(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4, numpy_usage=True)

    def testClusterAllocationSampleTwoDiamonds(self):
        CureTestTemplates.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [399, 401], 2, 5, 0.3)

    def testClusterAllocationSampleLsun(self):
        CureTestTemplates.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_LSUN, [100, 101, 202], 3, 5, 0.3)

    def testOneClusterAllocationSampleSimple1(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1)

    def testOneClusterAllocationSampleSimple2(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1)

    def testOneClusterAllocationSampleSimple3(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1)

    def testOneClusterAllocationSampleSimple4(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [75], 1)

    def testOneClusterAllocationSampleSimple5(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [60], 1)


    def testClusterAllocationOneDimensionData(self):
        CureTestTemplates.templateClusterAllocationOneDimensionData(False)


    def testClusterAllocationTheSameData1(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [10, 20], 2, 5, 0.3)

    def testClusterAllocationTheSameData2(self):
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 5, 5], 3, 5, 0.3)
        CureTestTemplates.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [5, 10], 2, 5, 0.3)


    def testEncoderProcedure(self):
        CureTestTemplates.templateEncoderProcedures(False)


    def test_argument_invalid_amount_clusters(self):
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0, 5, 0.3, False)
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, -1, 5, 0.3, False)

    def test_argument_invalid_amount_representatives(self):
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0, 0.3, False)
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, -2, 0.3, False)
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, -4, 0.3, False)

    def test_argument_invalid_compression(self):
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 1, -0.3, False)
        CureTestTemplates.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 2, -2.0, False)

    def test_argument_empty_data(self):
        CureTestTemplates.exception(ValueError, [], 3, 5, 0.3, False)
