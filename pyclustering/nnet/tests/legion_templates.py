"""!

@brief Templates for tests of Local Excitatory Global Inhibitory Oscillatory Network (LEGION).

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


from pyclustering.nnet.legion import legion_network;
from pyclustering.nnet import conn_type;

from pyclustering.utils import extract_number_oscillations;


class LegionTestTemplates:
    @staticmethod
    def templateOscillationsWithStructures(type_conn, ccore_flag):
        net = legion_network(4, type_conn = conn_type.LIST_BIDIR, ccore = ccore_flag);
        dynamic = net.simulate(500, 1000, [1, 1, 1, 1]);
          
        for i in range(len(net)):
            assert extract_number_oscillations(dynamic.output, i) > 1;


    @staticmethod
    def templateSyncEnsembleAllocation(stimulus, params, type_conn, sim_steps, sim_time, expected_clusters, ccore_flag):
        result_testing = False;
         
        for _ in range(0, 5, 1):
            net = legion_network(len(stimulus), params, type_conn, ccore = ccore_flag);
            dynamic = net.simulate(sim_steps, sim_time, stimulus);
             
            ensembles = dynamic.allocate_sync_ensembles(0.1);
            if (ensembles != expected_clusters):
                continue;
             
            result_testing = True;
            break;
         
        assert result_testing;


    @staticmethod
    def templateOutputDynamicInformation(stimulus, params, type_conn, sim_steps, sim_time, ccore_flag):
        legion_instance = legion_network(len(stimulus), params, type_conn, ccore = ccore_flag);
        dynamic = legion_instance.simulate(sim_steps, sim_time, stimulus);
         
        assert len(dynamic.output) > 0;
        assert len(dynamic.inhibitor) > 0;
        assert len(dynamic.time) > 0;