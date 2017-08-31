"""!

@brief Unit-test runner that runs all unit-tests in the project.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

# Add path to pyclustering package (much better to set PYTHONPATH), but just to be sure that at least unit-tests can be run.
# import os, sys;
# parent_obtainer = lambda current_folder, level: os.sep.join(current_folder.split(os.sep)[:-level])
# working_folder = parent_obtainer(os.path.abspath(__file__), 3);
# sys.path.insert(0, working_folder);


# Test suits that are used for testing of python implementation.
from pyclustering.cluster.tests                  import clustering_tests;

from pyclustering.gcolor.tests                   import dsatur_tests        as gcolor_dsatur_unit_tests;
from pyclustering.gcolor.tests                   import hysteresis_tests    as gcolor_hysteresis_unit_tests;
from pyclustering.gcolor.tests                   import sync_tests          as gcolor_sync_unit_tests;

from pyclustering.nnet.tests                     import cnn_tests           as nnet_cnn_unit_tests;
from pyclustering.nnet.tests                     import fsync_tests         as nnet_fsync_unit_tests;
from pyclustering.nnet.tests                     import hhn_tests           as nnet_hhn_unit_tests;
from pyclustering.nnet.tests                     import hysteresis_tests    as nnet_hysteresis_unit_tests;
from pyclustering.nnet.tests                     import legion_tests        as nnet_legion_unit_tests;
from pyclustering.nnet.tests                     import nnet_tests          as nnet_unit_tests;
from pyclustering.nnet.tests                     import pcnn_tests          as nnet_pcnn_unit_tests;
from pyclustering.nnet.tests                     import som_tests           as nnet_som_unit_tests;
from pyclustering.nnet.tests                     import sync_tests          as nnet_sync_unit_tests;
from pyclustering.nnet.tests                     import syncpr_tests        as nnet_syncpr_unit_tests;
from pyclustering.nnet.tests                     import syncsegm_tests      as nnet_syncsegm_unit_tests;

from pyclustering.container.tests                import cftree_tests        as container_cftree_unit_tests;
from pyclustering.container.tests                import kdtree_tests        as container_kdtree_unit_tests;

from pyclustering.core.tests                     import package_tests       as core_package_unit_tests;

from pyclustering.tsp.tests                      import antcolony_tests     as tsp_antcolony_unit_tests;

from pyclustering.utils.tests                    import utils_tests         as utils_unit_tests;


if __name__ == "__main__":
    suite = unittest.TestSuite();

    clustering_tests.fill_suite(suite);

    suite.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_dsatur_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_hysteresis_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_sync_unit_tests));

    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_cnn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_fsync_unit_tests))
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hhn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hysteresis_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_legion_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_pcnn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncpr_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_syncsegm_unit_tests));

    suite.addTests(unittest.TestLoader().loadTestsFromModule(container_cftree_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(container_kdtree_unit_tests));

    suite.addTests(unittest.TestLoader().loadTestsFromModule(core_package_unit_tests));

    suite.addTests(unittest.TestLoader().loadTestsFromModule(tsp_antcolony_unit_tests));

    suite.addTests(unittest.TestLoader().loadTestsFromModule(utils_unit_tests));

    result = unittest.TextTestRunner(verbosity = 2).run(suite);

    # Get execution result
    execution_testing_result = 0;
    
    if (result.wasSuccessful() is True):
        execution_testing_result = 0;
    else:
        execution_testing_result = 1;
    
    exit(execution_testing_result);

