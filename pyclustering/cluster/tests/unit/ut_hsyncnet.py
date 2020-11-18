"""!

@brief Unit-tests for Hierarchical Sync (HSyncNet) algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.hsyncnet_templates import HsyncnetTestTemplates

from pyclustering.nnet import solve_type

from pyclustering.samples.definitions import SIMPLE_SAMPLES


class HsyncnetUnitTest(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, 5, 0.3, True, False);

    def testClusteringOneAllocationSampleSimple1(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], solve_type.FAST, 5, 0.3, True, False);

    def testClusteringSampleSimple1WithoutCollecting(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, 5, 0.3, False, False);

    def testClusteringSampleSimple2(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8], solve_type.FAST, 5, 0.2, True, False);

    def testClusteringOneAllocationSampleSimple2(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23], solve_type.FAST, 5, 0.2, True, False);

    def testClusteringOneDimensionDataSampleSimple7(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10], solve_type.FAST, 5, 0.3, True, False);

    def testClusteringTheSameData1(self):
        HsyncnetTestTemplates.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 3, [5, 5, 5], solve_type.FAST, 5, 0.3, True, False);

    def testDynamicLengthCollecting(self):
        HsyncnetTestTemplates.templateDynamicLength(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, None, 5, 0.3, True, False);

    def testDynamicLengthWithoutCollecting(self):
        HsyncnetTestTemplates.templateDynamicLength(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, None, 5, 0.3, False, False);
