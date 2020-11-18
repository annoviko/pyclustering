"""!

@brief Test templates for hSyncNet clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.nnet import initial_type, solve_type;

from pyclustering.utils import read_sample;

from pyclustering.cluster.hsyncnet import hsyncnet;


class HsyncnetTestTemplates:
    @staticmethod
    def templateClustering(path, number_clusters, expected_length_clusters, solver, initial_neighbors, increase_persent, collect_dynamic_flag, ccore_flag):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for _ in range(0, 6, 1):
            sample = read_sample(path);
            network = hsyncnet(sample, number_clusters, initial_type.EQUIPARTITION, initial_neighbors, increase_persent, ccore = ccore_flag);
            
            analyser = network.process(order = 0.997, solution = solver, collect_dynamic = collect_dynamic_flag);
            clusters = analyser.allocate_clusters(0.1);
            
            if (sum([len(cluster) for cluster in clusters]) != sum(expected_length_clusters)):
                continue;
            
            if (sorted([len(cluster) for cluster in clusters]) != expected_length_clusters):
                if (sorted([len(cluster) for cluster in clusters]) != sorted(expected_length_clusters)):
                    continue;
            
            # Unit-test is passed
            result_testing = True;
            break;
        
        assert result_testing;


    @staticmethod
    def templateDynamicLength(path, number_clusters, expected_length, initial_neighbors, increase_persent, collect_dynamic_flag, ccore_flag):
        sample = read_sample(path);
        network = hsyncnet(sample, number_clusters, initial_type.EQUIPARTITION, initial_neighbors, increase_persent, ccore = ccore_flag);
        
        analyser = network.process(order = 0.995, solution = solve_type.FAST, collect_dynamic = collect_dynamic_flag);
        
        assert len(analyser) != 0;
        
        if (collect_dynamic_flag is True):
            assert len(analyser) >= 1;
            if (expected_length is None):
                assert len(analyser) > 1;
            else:
                assert len(analyser) == expected_length;
        
        else:
            assert len(analyser) == 1;


    @staticmethod
    def testCoreInterfaceIntInputData():
        result_testing = False;
        
        for _ in range(10):
            hsyncnet_instance = hsyncnet([ [1], [2], [3], [20], [21], [22] ], 2, initial_type.EQUIPARTITION, ccore = True);
            analyser = hsyncnet_instance.process();
            
            if (len(analyser.allocate_clusters(0.1)) == 2):
                result_testing = True;
                break;
        
        assert result_testing;
