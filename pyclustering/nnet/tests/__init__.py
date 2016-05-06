"""!

@brief Unit-test runner for tests of oscillatory and neural networks.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from pyclustering.nnet.tests        import hhn_tests             as nnet_hhn_unit_tests;
from pyclustering.nnet.tests        import hysteresis_tests      as nnet_hysteresis_unit_tests;
from pyclustering.nnet.tests        import legion_tests          as nnet_legion_unit_tests;
from pyclustering.nnet.tests        import nnet_tests            as nnet_unit_tests;
from pyclustering.nnet.tests        import pcnn_tests            as nnet_pcnn_unit_tests;
from pyclustering.nnet.tests        import som_tests             as nnet_som_unit_tests;
from pyclustering.nnet.tests        import sync_tests            as nnet_sync_unit_tests;
from pyclustering.nnet.tests        import syncpr_tests          as nnet_syncpr_unit_tests;
from pyclustering.nnet.tests        import syncsegm_tests        as nnet_syncsegm_unit_tests;

if __name__ == "__main__":
    suite = unittest.TestSuite();

    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hhn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hysteresis_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_legion_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_pcnn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncpr_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncsegm_unit_tests));
    
    unittest.TextTestRunner(verbosity = 2).run(suite);