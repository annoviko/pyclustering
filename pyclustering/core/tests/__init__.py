"""!

@brief Unit-test runner for core wrapper.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest
from pyclustering.tests.suite_holder import suite_holder

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')


from pyclustering.core.tests import ut_package as core_package_unit_tests

import os
import warnings

from pyclustering.core.definitions import PATH_PYCLUSTERING_CCORE_LIBRARY
from pyclustering.core.wrapper import ccore_library


class remove_library(object):
    """!
    @brief Decorator for tests where ccore library should be removed.
    
    """
    def __init__(self, call_object):
        self.call_object = call_object

    def __call__(self, *args):
        test_result = True

        try:
            os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY, PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted")

            warnings.filterwarnings("ignore", category=ResourceWarning)
            ccore_library.initialize()

            self.call_object(args)

        except os.error:
            warnings.warn("Test skipped: no rights to rename C/C++ pyclustering library for testing.")
            return

        except:
            test_result = False

        os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted", PATH_PYCLUSTERING_CCORE_LIBRARY)
        ccore_library.initialize()

        warnings.filterwarnings("default", category=ResourceWarning)

        if test_result is False:
            raise AssertionError("Test failed")


class corrupt_library(object):
    """!
    @brief Decorator for tests where ccore library should be corrupted.
    
    """
    def __init__(self, call_object):
        self.call_object = call_object

    def __create_corrupted_library(self, filepath):
        with open(filepath, 'wb') as binary_file_descriptor:
            binary_file_descriptor.write(bytes("corrupted binary library", 'UTF-8'))

    def __remove_corrupted_library(self, filepath):
        os.remove(filepath)

    def __call__(self, *args):
        try:
            os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY, PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted")
        except os.error:
            warnings.warn("Test skipped: no rights to rename C/C++ pyclustering library for testing.")
            return

        self.__create_corrupted_library(PATH_PYCLUSTERING_CCORE_LIBRARY)

        warnings.filterwarnings("ignore", category=ResourceWarning)
        ccore_library.initialize()
        self.call_object(args)

        self.__remove_corrupted_library(PATH_PYCLUSTERING_CCORE_LIBRARY)
        os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted", PATH_PYCLUSTERING_CCORE_LIBRARY)
        ccore_library.initialize()

        warnings.filterwarnings("default", category=ResourceWarning)


class core_tests(suite_holder):
    def __init__(self):
        super().__init__()
        core_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(core_suite):
        core_suite.addTests(unittest.TestLoader().loadTestsFromModule(core_package_unit_tests))
