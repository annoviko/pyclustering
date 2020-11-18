"""!

@brief Test templates for SyncNet clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.cluster.syncnet import syncnet;

from pyclustering.utils import read_sample;
from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.nnet import conn_represent;


class SyncnetTestTemplates:
    @staticmethod
    def templateClustering(file, radius, order, solver, initial, storage_flag, conn_weigh_flag, tolerance, connection, expected_cluster_length, ccore_flag):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for _ in range(0, 20, 1):
            sample = read_sample(file);
            network = syncnet(sample, radius, connection, initial, conn_weigh_flag, ccore_flag);
            analyser = network.process(order, solver, storage_flag);
            
            clusters = analyser.allocate_clusters(tolerance);
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters];
    
            if (len(obtained_cluster_sizes) != len(expected_cluster_length)):
                continue;
            
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            
            if (obtained_cluster_sizes != expected_cluster_length):
                continue;
            
            # Unit-test is passed
            result_testing = True;
            break;
        
        assert result_testing;


    @staticmethod
    def templateShowNetwork(file, radius, ccore_flag, connection_storage_type = conn_represent.MATRIX):
        sample = read_sample(file);
        network = syncnet(sample, radius, conn_repr = connection_storage_type, ccore = ccore_flag);

        network.show_network();


    @staticmethod
    def templateConnectionApi(connection_storage_type, ccore_flag):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        network = syncnet(sample, 15, conn_repr = connection_storage_type, ccore = ccore_flag);
        
        for i in range(len(network)):
            neighbors = network.get_neighbors(i);
            
            assert len(sample) == len(network);
            assert len(neighbors) == len(network) - 1;
            assert i not in neighbors;
            
            for j in range(len(network)):
                if (i != j):
                    assert network.has_connection(i, j) == True;
                else:
                    assert network.has_connection(i, j) == False;
