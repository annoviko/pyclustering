"""!

@brief Test runner for unit and integration tests in the project.

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

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.suite_holder import suite_holder


class pyclustering_integration_tests(suite_holder):
    def __init__(self):
        super().__init__()
        pyclustering_integration_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(integration_suite):
        integration_suite.addTests(unittest.TestLoader().discover(".", "it_*.py"))


class pyclustering_unit_tests(suite_holder):
    def __init__(self):
        super().__init__()
        pyclustering_unit_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(unit_suite):
        unit_suite.addTests(unittest.TestLoader().discover(".", "ut_*.py"))


class pyclustering_tests(suite_holder):
    def __init__(self):
        super().__init__()
        pyclustering_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(pyclustering_suite):
        pyclustering_integration_tests.fill_suite(pyclustering_suite)
        pyclustering_unit_tests.fill_suite(pyclustering_suite)
