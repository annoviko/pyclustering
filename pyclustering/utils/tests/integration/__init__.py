"""!

@brief Integration-test runner for utils.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.suite_holder import suite_holder

from pyclustering.utils.tests.integration import it_metric as utils_metric_integration_tests


class utils_integration_tests(suite_holder):
    def __init__(self):
        super().__init__()
        utils_integration_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(integration_nnet_suite):
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(utils_metric_integration_tests))
