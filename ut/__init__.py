import unittest;

from ants           import tests as ants_unit_tests;
from cure           import tests as cure_unit_tests;
from dbscan         import tests as dbscan_unit_tests;
from hierarchical   import tests as hierarchical_unit_tests;
from hsyncnet       import tests as hsyncnet_unit_tests;
from kmeans         import tests as kmeans_unit_tests;
from nnet.som       import tests as nnet_som_unit_tests;
from nnet.sync      import tests as nnet_sync_unit_tests;
from support        import tests as support_unit_tests;
from syncnet        import tests as syncnet_unit_tests;


if __name__ == "__main__":
    suite = unittest.TestSuite();
    
    # suite.addTests(unittest.TestLoader().loadTestsFromModule(ants_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cure_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(dbscan_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(hierarchical_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(hsyncnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(support_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(syncnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(kmeans_unit_tests));
    
    unittest.TextTestRunner(verbosity = 2).run(suite);
    