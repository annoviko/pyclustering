"""!

@brief Unit-test runner for tests of clustering algorithms.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.tests               import agglomerative_tests as cluster_agglomerative_unit_tests;
from pyclustering.cluster.tests               import birch_tests         as cluster_birch_unit_tests;
from pyclustering.cluster.tests               import clarans_tests       as cluster_clarans_unit_tests;
from pyclustering.cluster.tests               import cure_tests          as cluster_cure_unit_tests;
from pyclustering.cluster.tests               import dbscan_tests        as cluster_dbscan_unit_tests;
from pyclustering.cluster.tests               import general_tests       as cluster_general_unit_tests;
from pyclustering.cluster.tests               import hsyncnet_tests      as cluster_hsyncnet_unit_tests;
from pyclustering.cluster.tests               import kmeans_tests        as cluster_kmeans_unit_tests;
from pyclustering.cluster.tests               import kmedians_tests      as cluster_kmedians_unit_tests;
from pyclustering.cluster.tests               import kmedoids_tests      as cluster_kmedoids_unit_tests;
from pyclustering.cluster.tests               import optics_tests        as cluster_optics_unit_tests;
from pyclustering.cluster.tests               import rock_tests          as cluster_rock_unit_tests;
from pyclustering.cluster.tests               import syncnet_tests       as cluster_syncnet_unit_tests;
from pyclustering.cluster.tests               import syncsom_tests       as cluster_syncsom_unit_tests;
from pyclustering.cluster.tests               import xmeans_tests        as cluster_xmeans_unit_tests;


if __name__ == "__main__":
    suite = unittest.TestSuite();
    
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_agglomerative_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_birch_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_clarans_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_cure_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_dbscan_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_general_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_hsyncnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_kmeans_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_kmedians_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_kmedoids_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_optics_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_rock_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_syncnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_syncsom_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_xmeans_unit_tests));
    
    unittest.TextTestRunner(verbosity = 2).run(suite);