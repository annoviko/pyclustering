"""!

@brief Unit-test runner for tests of graph coloring algorithms.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

from pyclustering.tests.suite_holder import suite_holder

from pyclustering.gcolor.tests import ut_dsatur as gcolor_dsatur_unit_tests
from pyclustering.gcolor.tests import ut_hysteresis as gcolor_hysteresis_unit_tests
from pyclustering.gcolor.tests import ut_sync as gcolor_sync_unit_tests


class gcolor_tests(suite_holder):
    def __init__(self):
        super().__init__()
        gcolor_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(gcolor_tests):
        gcolor_tests.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_dsatur_unit_tests))
        gcolor_tests.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_hysteresis_unit_tests))
        gcolor_tests.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_sync_unit_tests))
