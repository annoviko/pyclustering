"""!

@brief Integration-tests for double-layer oscillatory network 'syncsegm' for image segmentation based on Kuramoto model.

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

from pyclustering.nnet.tests.syncsegm_templates import SyncsegmTestTemplates

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES


class SyncsegmIntegrationTest(unittest.TestCase):
    def testImageSegmentationSimple13(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE13, 225, 5, 0, 2, 4, False, True)

    def testImageSegmentationSimple15(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE15, 225, 6, 0, 2, 3, False, True)

    def testImageSegmentationSimple16(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE16, 225, 2, 0, 2, 3, True, True)

    def testImageSegmentationSimple17(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE17, 225, 1, 0, 3, 3, False, True)

    def testImageSegmentationSimple18(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE18, 225, 1, 0, 2, 3, False, True)

    def testVisualizeSimple17NoFailure(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE17, 225, 1, 0, 3, 3, False, True)

    def testVisualizeSimple18NoFailure(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE18, 225, 1, 0, 2, 3, False, True)

