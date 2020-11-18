"""!

@brief Unit-test runner for utils module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.suite_holder import suite_holder

from pyclustering.utils.tests.unit import ut_dimension as dimension_unit_tests
from pyclustering.utils.tests.unit import ut_metric as metric_unit_tests
from pyclustering.utils.tests.unit import ut_sampling as sampling_unit_tests
from pyclustering.utils.tests.unit import ut_utils as utils_general_unit_tests


class utils_unit_tests(suite_holder):
    def __init__(self):
        super().__init__()
        utils_unit_tests.fill_suite(self.get_suite())


    @staticmethod
    def fill_suite(utils_suite):
        utils_suite.addTests(unittest.TestLoader().loadTestsFromModule(dimension_unit_tests))
        utils_suite.addTests(unittest.TestLoader().loadTestsFromModule(metric_unit_tests))
        utils_suite.addTests(unittest.TestLoader().loadTestsFromModule(sampling_unit_tests))
        utils_suite.addTests(unittest.TestLoader().loadTestsFromModule(utils_general_unit_tests))
