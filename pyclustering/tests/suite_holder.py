"""!

@brief Test suite storage

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import sys
import time
import unittest


class suite_holder:
    def __init__(self):
        self.__suite = unittest.TestSuite()

    def get_suite(self):
        return self.__suite

    def run(self, rerun=2):
        print(self.__suite)
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=3).run(self.__suite)
        if result.wasSuccessful() is True:
            return result

        if len(result.errors) > 0:
            return result   # no need to restart in case of errors

        for attempt in range(rerun):
            time.sleep(1)   # sleep 1 second to change current time for random seed.

            print("\n======================================================================")
            print("Rerun failed tests (attempt: %d)." % (attempt + 1))
            print("----------------------------------------------------------------------")

            failure_suite = unittest.TestSuite()
            for failure in result.failures:
                failure_suite.addTest(failure[0])

            result = unittest.TextTestRunner(stream=sys.stdout, verbosity=3).run(failure_suite)
            if result.wasSuccessful() is True:
                return result

        return result

    @staticmethod
    def fill_suite(test_suite):
        pass;