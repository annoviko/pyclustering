"""!

@brief Test runner for unit and integration tests in the project.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import enum
import sys
import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.suite_holder import suite_holder
from pyclustering import __PYCLUSTERING_ROOT_DIRECTORY__

class pyclustering_integration_tests(suite_holder):
    def __init__(self):
        super().__init__()
        pyclustering_integration_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(integration_suite):
        integration_suite.addTests(unittest.TestLoader().discover(__PYCLUSTERING_ROOT_DIRECTORY__, "it_*.py"))


class pyclustering_unit_tests(suite_holder):
    def __init__(self):
        super().__init__()
        pyclustering_unit_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(unit_suite):
        unit_suite.addTests(unittest.TestLoader().discover(__PYCLUSTERING_ROOT_DIRECTORY__, "ut_*.py"))


class pyclustering_tests(suite_holder):
    def __init__(self):
        super().__init__()
        pyclustering_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(pyclustering_suite):
        pyclustering_integration_tests.fill_suite(pyclustering_suite)
        pyclustering_unit_tests.fill_suite(pyclustering_suite)


class exit_code(enum.IntEnum):
    success = 0,
    error_unknown_type_test = -1,
    error_too_many_arguments = -2,
    error_failure = -3


class tests_runner:
    @staticmethod
    def run():
        result = None
        return_code = exit_code.success

        if len(sys.argv) == 1:
            result = pyclustering_tests().run()

        elif len(sys.argv) == 2:
            if sys.argv[1] == "--integration":
                result = pyclustering_integration_tests().run()

            elif sys.argv[1] == "--unit":
                result = pyclustering_unit_tests().run()

            elif sys.argv[1] == "test":
                result = pyclustering_tests().run()

            else:
                print("Unknown type of test is specified '" + str(sys.argv[1]) + "'.")
                return_code = exit_code.error_unknown_type_test

        else:
            print("Too many arguments '" + str(len(sys.argv)) + "' is used.")
            return_code = exit_code.error_too_many_arguments

        # Get execution result
        if result is not None:
            if result.wasSuccessful() is False:
                return_code = exit_code.error_failure

        exit(return_code)
