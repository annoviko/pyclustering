import unittest;

from clustering.cure                import tests as cluster_cure_unit_tests;
from clustering.dbscan              import tests as cluster_dbscan_unit_tests;
from clustering.hierarchical        import tests as cluster_hierarchical_unit_tests;
from clustering.hsyncnet            import tests as cluster_hsyncnet_unit_tests;
from clustering.kmeans              import tests as cluster_kmeans_unit_tests;
from clustering.optics              import tests as cluster_optics_unit_tests;
from clustering.rock                import tests as cluster_rock_unit_tests;
from clustering.syncnet             import tests as cluster_syncnet_unit_tests;
from clustering.syncsom             import tests as cluster_syncsom_unit_tests;
from clustering.xmeans              import tests as cluster_xmeans_unit_tests;

from gcolor.dsatur                  import tests as gcolor_dsatur_unit_tests;
from gcolor.hysteresis              import tests as gcolor_hysteresis_unit_tests;
from gcolor.sync                    import tests as gcolor_sync_unit_tests;

from nnet.hhn                       import tests as nnet_hhn_unit_tests;
from nnet.hysteresis                import tests as nnet_hysteresis_unit_tests;
from nnet.legion                    import tests as nnet_legion_unit_tests;
from nnet.pcnn                      import tests as nnet_pcnn_unit_tests;
from nnet.som                       import tests as nnet_som_unit_tests;
from nnet.sync                      import tests as nnet_sync_unit_tests;
from nnet                           import tests as nnet_unit_tests;

from support.cftree                 import tests as support_cftree_unit_tests;
from support.kdtree                 import tests as support_kdtree_unit_tests;
from support                        import tests as support_unit_tests;



if __name__ == "__main__":
    suite = unittest.TestSuite();
    
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_cure_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_dbscan_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_hierarchical_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_hsyncnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_kmeans_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_optics_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_rock_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_syncnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_syncsom_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(cluster_xmeans_unit_tests));
     
    suite.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_dsatur_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_hysteresis_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(gcolor_sync_unit_tests));
 
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hhn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_hysteresis_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_legion_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_pcnn_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_som_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(nnet_sync_unit_tests));
    
    suite.addTests(unittest.TestLoader().loadTestsFromModule(support_cftree_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(support_kdtree_unit_tests));
    suite.addTests(unittest.TestLoader().loadTestsFromModule(support_unit_tests));
    
    unittest.TextTestRunner(verbosity = 2).run(suite);
    