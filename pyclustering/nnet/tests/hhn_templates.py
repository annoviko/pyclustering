"""!

@brief Templates for tests of Hodgkin-Huxley oscillatory network.

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