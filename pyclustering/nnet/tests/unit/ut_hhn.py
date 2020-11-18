"""!

@brief Unit-tests for oscillatory network based on Hodgkin-Huxley model of neuron.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

from pyclustering.nnet.tests.hhn_templates import HhnTestTemplates


class HhnUnitTest(unittest.TestCase):
    def testGlobalSyncWithSameStimulus(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([27, 27, 27], None, 600, 50, [[0, 1, 2]], False);

    def testGlobalSyncWithVariousStimulus(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([26, 26, 27, 27, 26, 25], None, 600, 50, [[0, 1, 2, 3, 4, 5]], False);

    def testPartialSync(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([25, 25, 50, 50], None, 800, 200, [[0, 1], [2, 3]], False);
