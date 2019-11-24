"""!

@brief Test suite storage

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

        for attempt in range(rerun):
            time.sleep(1)   # sleep 1 second to change current time for random seed.

            print("\n======================================================================")
            print("Rerun failed tests (attempt: %d)." % (attempt + 1))
            print("----------------------------------------------------------------------")

            failure_suite = unittest.TestSuite()
            for failure in result.failures:
                failure_suite.addTest(failure[0])

            result = unittest.TextTestRunner(stream=sys.stdout, verbosity=3).run(failure_suite)

        return result

    @staticmethod
    def fill_suite(test_suite):
        pass;