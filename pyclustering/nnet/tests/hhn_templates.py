"""!

@brief Templates for tests of Hodgkin-Huxley oscillatory network.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.nnet.hhn import hhn_network;


class HhnTestTemplates:
    @staticmethod
    def templateSyncEnsembleAllocation(stimulus, params, sim_steps, sim_time, expected_clusters, ccore):
        result_testing = False;

        for _ in range(0, 5, 1):
            net = hhn_network(len(stimulus), stimulus, params, ccore=ccore);
            (t, dyn_p, dyn_c) = net.simulate(sim_steps, sim_time);

            assert t is not None;
            assert dyn_p is not None;
            assert dyn_c is not None;

            assert len(t) == sim_steps + 1;
            assert len(dyn_p) == sim_steps + 1;
            assert len(dyn_c) == sim_steps + 1;

            ensembles = net.allocate_sync_ensembles(1.0);
            if (ensembles != expected_clusters):
                continue;

            result_testing = True;
            break;

        assert result_testing;