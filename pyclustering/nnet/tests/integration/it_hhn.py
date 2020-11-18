"""!

@brief Integration-tests for Hodgkin-Huxley oscillatory network.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

from pyclustering.nnet.tests.hhn_templates import HhnTestTemplates

from pyclustering.core.tests import remove_library


class HhnIntegrationTest(unittest.TestCase):
    def testGlobalSyncWithSameStimulus(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([27, 27, 27], None, 600, 50, [[0, 1, 2]], True);

    def testGlobalSyncWithVariousStimulus(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([26, 26, 27, 27, 26, 25], None, 600, 50, [[0, 1, 2, 3, 4, 5]], True);

    def testPartialSync(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([25, 25, 50, 50], None, 800, 200, [[0, 1], [2, 3]], True);

    def testThreeEnsembles(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([0, 0, 25, 25, 47, 47], None, 2400, 600, [[0, 1], [2, 3], [4, 5]], True);

    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([27, 27, 27], None, 600, 50, [[0, 1, 2]], True);
