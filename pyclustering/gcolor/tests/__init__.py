"""!

@brief Unit-test runner for tests of graph coloring algorithms.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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

import unittest;

from pyclustering.tests.suite_holder import suite_holder;

from pyclustering.gcolor.tests                   import dsatur_tests        as gcolor_dsatur_unit_tests;
from pyclustering.gcolor.tests                   import hysteresis_tests    as gcolor_hysteresis_unit_tests;
from pyclustering.gcolor.tests                   import sync_tests          as gcolor_sync_unit_tests;


class gcolor_tests(suite_holder):
    def __init__(self):
        super().__init__();
        gcolor_tests.fill_suite(self.get_suite());

    @staticmethod
    def fill_suite(gcolor_tests):
        gcolor_tests.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_dsatur_unit_tests));
        gcolor_tests.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_hysteresis_unit_tests));
        gcolor_tests.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_sync_unit_tests));


if __name__ == "__main__":
    gcolor_tests().run();