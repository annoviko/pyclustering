"""!

@brief Test runner for unit and integration tests of utils module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

from pyclustering.utils.tests.unit import utils_unit_tests;


class utils_tests(suite_holder):
    def __init__(self):
        super().__init__();
        utils_tests.fill_suite(self.get_suite());


    @staticmethod
    def fill_suite(tsp_suite):
        utils_unit_tests.fill_suite(tsp_suite);


if __name__ == "__main__":
    utils_tests().run();