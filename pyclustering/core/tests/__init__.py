"""!

@brief Unit-test runner for core wrapper.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import unittest
from pyclustering.tests.suite_holder import suite_holder

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')


from pyclustering.core.tests import ut_package as core_package_unit_tests

import os

from pyclustering.core.definitions import PATH_PYCLUSTERING_CCORE_LIBRARY
from pyclustering.core.wrapper import ccore_library


class remove_library(object):
    """!
    @brief Decorator for tests where ccore library should be removed.
    
    """
    def __init__(self, call_object):
        self.call_object = call_object

    def __call__(self, *args):
        print("[TEST] Ignore next print related to problems with pyclustering ccore")
        test_result = True

        try:
            os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY, PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted")
            ccore_library.initialize()

            self.call_object(args)

        except:
            test_result = False

        os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted", PATH_PYCLUSTERING_CCORE_LIBRARY)
        ccore_library.initialize()

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
        os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY, PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted")
        self.__create_corrupted_library(PATH_PYCLUSTERING_CCORE_LIBRARY)
        
        ccore_library.initialize()

        self.call_object(args)

        self.__remove_corrupted_library(PATH_PYCLUSTERING_CCORE_LIBRARY)
        os.rename(PATH_PYCLUSTERING_CCORE_LIBRARY + "_corrupted", PATH_PYCLUSTERING_CCORE_LIBRARY)
        ccore_library.initialize()


class core_tests(suite_holder):
    def __init__(self):
        super().__init__()
        core_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(core_suite):
        core_suite.addTests(unittest.TestLoader().loadTestsFromModule(core_package_unit_tests))
