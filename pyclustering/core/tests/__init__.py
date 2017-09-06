"""!

@brief Unit-test runner for core wrapper.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');


from pyclustering.core.tests            import package_tests as core_package_unit_tests;


class core_tests(suite_holder):
    def __init__(self):
        super().__init__();
        core_tests.fill_suite(self.get_suite());

    @staticmethod
    def fill_suite(core_suite):
        core_suite.addTests(unittest.TestLoader().loadTestsFromModule(core_package_unit_tests));


if __name__ == "__main__":
    core_tests().run();