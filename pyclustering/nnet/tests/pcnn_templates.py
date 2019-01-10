"""!

@brief Templates for tests of Pulse Coupling Neural Network (PCNN).

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


from pyclustering.nnet.pcnn import pcnn_network, pcnn_parameters, pcnn_visualizer;
from pyclustering.nnet import conn_represent;


class PcnnTestTemplates:
    @staticmethod
    def templateDynamicLength(num_osc, steps, type_conn, repr_type, stimulus, ccore, **kwargs):
        params = kwargs.get('params', None);

        net = pcnn_network(num_osc, params, type_conn, repr_type, None, None, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        assert num_osc == len(dynamic.output[0]);
        assert steps == len(dynamic.allocate_time_signal());

        return net;


    @staticmethod
    def templateDynamicLengthFastLinking(num_osc, steps, type_conn, repr_type, stimulus, ccore):
        params = pcnn_parameters();
        params.FAST_LINKING = True;
        return PcnnTestTemplates.templateDynamicLength(num_osc, steps, type_conn, repr_type, stimulus, ccore, params=params);


    @staticmethod
    def templateGridRectangleDynamicLength(num_osc, steps, type_conn, repr_type, height, width, stimulus, ccore):
        net = pcnn_network(num_osc, None, type_conn, repr_type, height, width, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        assert num_osc == len(dynamic.output[0]);
        assert steps == len(dynamic.allocate_time_signal());


    @staticmethod
    def templateSyncEnsemblesAllocation(num_osc, type_conn, steps, stimulus, ccore, ensembles):
        net = pcnn_network(num_osc, None, type_conn, conn_represent.MATRIX, None, None, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        
        sync_ensembles = dynamic.allocate_sync_ensembles();
        
        if (ensembles is not None):
            assert len(ensembles) == len(sync_ensembles);
            
            for expected_ensemble in ensembles:
                ensemble_correct = False;
                
                for index_ensemble in range(len(sync_ensembles)):
                    sorted_expected_ensemble = expected_ensemble.sort();
                    sorted_ensemble = sync_ensembles[index_ensemble].sort();
                    
                    if (sorted_expected_ensemble == sorted_ensemble):
                        ensemble_correct = True;
                        break;
                
                assert (True == ensemble_correct);
                
        unique_indexes = set();
        
        time_signal = dynamic.allocate_time_signal();
        spike_ensembles = dynamic.allocate_spike_ensembles();
        sync_ensembles = dynamic.allocate_sync_ensembles();
        
        for ensemble in spike_ensembles:
            assert len(ensemble) in time_signal;
        
        for ensemble in sync_ensembles:
            spike_ensembles_exist = False;
            for index in range(len(spike_ensembles)): 
                if ensemble == spike_ensembles[index]:
                    spike_ensembles_exist = True;
                    break;
            
            assert (True == spike_ensembles_exist);
            
            for index_oscillator in ensemble:
                assert index_oscillator not in unique_indexes;
                unique_indexes.add(index_oscillator);


    @staticmethod
    def templateAllocationInRectangleStructure(num_osc, height, width, steps, type_conn, repr_type, stimulus, ccore):
        net = pcnn_network(num_osc, None, type_conn, repr_type, height, width, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        assert num_osc == len(dynamic.output[0]);
        assert steps == len(dynamic.allocate_time_signal());


    @staticmethod
    def visualize(num_osc, steps, type_conn, repr_type, stimulus, height, width, ccore):
        net = pcnn_network(num_osc, None, type_conn, repr_type, None, None, ccore);
        dynamic = net.simulate(steps, stimulus);

        pcnn_visualizer.show_time_signal(dynamic);
        pcnn_visualizer.show_output_dynamic(dynamic);
        pcnn_visualizer.animate_spike_ensembles(dynamic, (height, width));