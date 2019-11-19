"""!

@brief Integration-test runner for tests of oscillatory and neural networks.

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

from pyclustering.nnet.tests.integration import it_hhn as nnet_hhn_integration_tests
from pyclustering.nnet.tests.integration import it_legion as nnet_legion_integration_tests
from pyclustering.nnet.tests.integration import it_pcnn as nnet_pcnn_integration_tests
from pyclustering.nnet.tests.integration import it_som as nnet_som_integration_tests
from pyclustering.nnet.tests.integration import it_sync as nnet_sync_integration_tests
from pyclustering.nnet.tests.integration import it_syncpr as nnet_syncpr_integration_tests
from pyclustering.nnet.tests.integration import it_syncsegm as nnet_syncsegm_integration_tests


class nnet_integration_tests(suite_holder):
    def __init__(self):
        super().__init__()
        nnet_integration_tests.fill_suite(self.get_suite())

    @staticmethod
    def fill_suite(integration_nnet_suite):
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hhn_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_legion_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_pcnn_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncpr_integration_tests))
        integration_nnet_suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncsegm_integration_tests))
