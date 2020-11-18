"""!

@brief Test runner for unit and integration tests of utils module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.suite_holder import suite_holder

from pyclustering.utils.tests.integration import utils_integration_tests
from pyclustering.utils.tests.unit import utils_unit_tests


class utils_tests(suite_holder):
    def __init__(self):
        super().__init__()
        utils_tests.fill_suite(self.get_suite())


    @staticmethod
    def fill_suite(utils_suite):
        utils_unit_tests.fill_suite(utils_suite)
        utils_integration_tests.fill_suite(utils_suite)
