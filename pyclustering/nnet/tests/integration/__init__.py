"""!

@brief Integration-test runner for tests of oscillatory and neural networks.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest
from pyclustering.tests.suite_holder import suite_holder

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.nnet.tests.integration import it_hhn as nnet_hhn_integration_tests
from pyclustering.nnet.tests.integration import it_legion as nnet_legion_integration_tests
from pyclustering.nnet.tests.integration import it_pcnn as nnet_pcnn_integration_tests
from pyclustering.nnet.tests.integration import it_som as nnet_som_integration_tests
from pyclustering.nnet.tests.integration import it_sync as nnet_sync_integration_tests
from pyclustering.nnet.tests.integration import it_syncpr as nnet_syncpr_integration_tests
from pyclustering.nnet.tests.integration import it_syncsegm as nnet_syncsegm_integration_tests


class nnet_integration_tests(suite_holder):
    def __init__(self):
        super().__init__()
        nnet_integration_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(integration_nnet_suite):
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hhn_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_legion_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_pcnn_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncpr_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncsegm_integration_tests))
