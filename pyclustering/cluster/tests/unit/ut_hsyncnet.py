"""!

@brief Unit-tests for Hierarchical Sync (HSyncNet) algorithm.

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
