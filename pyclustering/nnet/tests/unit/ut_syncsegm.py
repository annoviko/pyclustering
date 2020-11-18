"""!

@brief Unit-tests for double-layer oscillatory network 'syncsegm' for image segmentation based on Kuramoto model.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet.tests.syncsegm_templates import SyncsegmTestTemplates;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;


class SyncsegmUnitTest(unittest.TestCase):
    def testImageSegmentationSimple17(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE17, 225, 1, 0, 3, 3, False, False);

    def testImageSegmentationSimple17OneObjectDetection(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE17, 225, 5, 0, 3, 3, False, False);

    def testImageSegmentationSimple17OneColorDetection(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE17, float('Inf'), 1, 0, 1, 1, False, False);

    def testImageSegmentationSimple18(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE18, 225, 1, 0, 2, 3, False, False);

    def testImageSegmentationSimple18OneObjectDetection(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE18, 225, 5, 0, 2, 2, False, False);

    def testImageSegmentationSimple18OneColorDetection(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE18, float('Inf'), 2, 0, 1, 1, False, False);

    def testVisualizeSimple17NoFailure(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE17, 225, 1, 0, 3, 3, False, False);

    def testVisualizeSimple18NoFailure(self):
        SyncsegmTestTemplates.templateSyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE18, 225, 1, 0, 2, 3, False, False);
