"""!

@brief Unit-test runner for containers.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest
from pyclustering.tests.suite_holder import suite_holder

from pyclustering.container.tests.unit import ut_cftree as container_cftree_unit_tests
from pyclustering.container.tests.unit import ut_kdtree as container_kdtree_unit_tests


class container_unit_tests(suite_holder):
    def __init__(self):
        super().__init__()
        container_unit_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(unit_container_suite):
        unit_container_suite.addTests(unittest.TestLoader().loadTestsFromModule(container_cftree_unit_tests))
        unit_container_suite.addTests(unittest.TestLoader().loadTestsFromModule(container_kdtree_unit_tests))
