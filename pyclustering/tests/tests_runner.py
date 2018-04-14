"""!

@brief Test runner for unit and integration tests in the project.

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


import sys;

from pyclustering.tests.suite_holder import suite_holder;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

# Add path to pyclustering package (much better to set PYTHONPATH), but just to be sure that at least unit-tests can be run.
# import os, sys;
# parent_obtainer = lambda current_folder, level: os.sep.join(current_folder.split(os.sep)[:-level])
# working_folder = parent_obtainer(os.path.abspath(__file__), 3);
# sys.path.insert(0, working_folder);


# Test suits that are used for testing of python implementation.
from pyclustering.cluster.tests                  import clustering_unit_tests, clustering_integration_tests;
from pyclustering.container.tests                import container_unit_tests;
from pyclustering.core.tests                     import core_tests;
from pyclustering.gcolor.tests                   import gcolor_tests;
from pyclustering.nnet.tests                     import nnet_unit_tests, nnet_integration_tests;
from pyclustering.utils.tests                    import utils_unit_tests, utils_integration_tests;



class pyclustering_integration_tests(suite_holder):
    def __init__(self):
        super().__init__();
        pyclustering_integration_tests.fill_suite(self.get_suite());


    @staticmethod
    def fill_suite(integration_suite):
        clustering_integration_tests.fill_suite(integration_suite);
        nnet_integration_tests.fill_suite(integration_suite);



class pyclustering_unit_tests(suite_holder):
    def __init__(self):
        super().__init__();
        pyclustering_unit_tests.fill_suite(self.get_suite());


    @staticmethod
    def fill_suite(unit_suite):
        clustering_unit_tests.fill_suite(unit_suite);
        container_unit_tests.fill_suite(unit_suite);
        core_tests.fill_suite(unit_suite);
        gcolor_tests.fill_suite(unit_suite);
        nnet_unit_tests.fill_suite(unit_suite);
        utils_unit_tests.fill_suite(unit_suite);



class pyclustering_tests(suite_holder):
    def __init__(self):
        super().__init__();
        pyclustering_tests.fill_suite(self.get_suite());


    @staticmethod
    def fill_suite(pyclustering_suite):
        pyclustering_integration_tests.fill_suite(pyclustering_suite);
        pyclustering_unit_tests.fill_suite(pyclustering_suite);



if __name__ == "__main__":
    result = None;
    
    if (len(sys.argv) == 1):
        result = pyclustering_tests().run();

    elif (len(sys.argv) == 2):
        if (sys.argv[1] == "--integration"):
            result = pyclustering_integration_tests().run();
        
        elif (sys.argv[1] == "--unit"):
            result = pyclustering_unit_tests().run();
        
        else:
            print("Unknown type of test is specified '" + str(sys.argv[1]) + "'.");
    
    else:
        print("Too many arguments '" + str(len(sys.argv)) + "' is used.");

    # Get execution result
    execution_testing_result = 0;
     
    if ((result is not None) and (result.wasSuccessful() is True)):
        execution_testing_result = 0;
    else:
        execution_testing_result = 1;
     
    exit(execution_testing_result);

