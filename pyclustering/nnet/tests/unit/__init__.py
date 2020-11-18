"""!

@brief Unit-test runner for tests of oscillatory and neural networks.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest
from pyclustering.tests.suite_holder import suite_holder

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.nnet.tests.unit import ut_cnn as nnet_cnn_unit_tests
from pyclustering.nnet.tests.unit import ut_dynamic_visualizer as nnet_dynamic_visualizer_unit_tests
from pyclustering.nnet.tests.unit import ut_fsync as nnet_fsync_unit_tests
from pyclustering.nnet.tests.unit import ut_hhn as nnet_hhn_unit_tests
from pyclustering.nnet.tests.unit import ut_hysteresis as nnet_hysteresis_unit_tests
from pyclustering.nnet.tests.unit import ut_legion as nnet_legion_unit_tests
from pyclustering.nnet.tests.unit import ut_nnet as nnet_network_unit_tests
from pyclustering.nnet.tests.unit import ut_pcnn as nnet_pcnn_unit_tests
from pyclustering.nnet.tests.unit import ut_som as nnet_som_unit_tests
from pyclustering.nnet.tests.unit import ut_sync as nnet_sync_unit_tests
from pyclustering.nnet.tests.unit import ut_syncpr as nnet_syncpr_unit_tests
from pyclustering.nnet.tests.unit import ut_syncsegm as nnet_syncsegm_unit_tests


class nnet_unit_tests(suite_holder):
    def __init__(self):
        super().__init__()
        nnet_unit_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(unit_nnet_suite):
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_cnn_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_dynamic_visualizer_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_fsync_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hhn_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hysteresis_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_legion_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_network_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_pcnn_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncpr_unit_tests))
        unit_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncsegm_unit_tests))
