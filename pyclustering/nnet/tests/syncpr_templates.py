"""!

@brief Templates for tests of SyncPR (oscillatory network based on Kuramoto model for pattern recognition).

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


# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet import solve_type;
from pyclustering.nnet.syncpr import syncpr, syncpr_visualizer;


class SyncprTestTemplates:
    @staticmethod
    def templateOutputDynamic(solver, ccore):
        net = syncpr(5, 0.1, 0.1, ccore);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solver, True);
         
        assert len(output_dynamic) == 11; # 10 steps without initial values.


    @staticmethod
    def templateOutputDynamicLengthStaticSimulation(collect_flag, ccore_flag):
        net = syncpr(5, 0.1, 0.1, ccore_flag);
        output_dynamic = net.simulate_static(10, 10, [-1, 1, -1, 1, -1], solution = solve_type.FAST, collect_dynamic = collect_flag);
         
        if (collect_flag is True):
            assert len(output_dynamic) == 11; # 10 steps without initial values.
        else:
            assert len(output_dynamic) == 1;


    @staticmethod
    def templateOutputDynamicLengthDynamicSimulation(collect_flag, ccore_flag):
        net = syncpr(5, 0.1, 0.1, ccore_flag);
        output_dynamic = net.simulate_dynamic([-1, 1, -1, 1, -1], solution = solve_type.FAST, collect_dynamic = collect_flag);
         
        if (collect_flag is True):
            assert len(output_dynamic) > 1;
        else:
            assert len(output_dynamic) == 1;


    @staticmethod
    def templateIncorrectPatternForSimulation(pattern, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore=ccore_flag);
        try: net.simulate(10, 10, pattern);
        except: return;
        assert False;


    @staticmethod
    def templateTrainNetworkAndRecognizePattern(ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
         
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        net.train(patterns);
         
        # recognize it
        for i in range(len(patterns)):
            output_dynamic = net.simulate(10, 10, patterns[i], solve_type.RK4, True);
             
            ensembles = output_dynamic.allocate_sync_ensembles(0.5);
            assert len(ensembles) == 2;
            assert len(ensembles[0]) == len(ensembles[1]);
             
            # sort results
            ensembles[0].sort();
            ensembles[1].sort();
             
            assert (ensembles[0] == [0, 1, 2, 3, 4]) or (ensembles[0] == [5, 6, 7, 8, 9]);
            assert (ensembles[1] == [0, 1, 2, 3, 4]) or (ensembles[1] == [5, 6, 7, 8, 9]);


    @staticmethod
    def templateIncorrectPatternForTraining(patterns, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        try: net.train(patterns);
        except: return;
        assert False;


    @staticmethod
    def templatePatternVisualizer(collect_dynamic, ccore_flag = False):
        net = syncpr(5, 0.1, 0.1, ccore = ccore_flag);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solve_type.RK4, collect_dynamic);
         
        syncpr_visualizer.show_pattern(output_dynamic, 5, 2);
        syncpr_visualizer.animate_pattern_recognition(output_dynamic, 1, 5);


    @staticmethod
    def templateMemoryOrder(ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        net.train(patterns);
        assert net.memory_order(patterns[0]) < 0.8;
        assert net.memory_order(patterns[1]) < 0.8;
        
        for pattern in patterns:
            net.simulate(20, 10, pattern, solve_type.RK4);
            memory_order = net.memory_order(pattern);
            assert (memory_order > 0.95) and (memory_order <= 1.000005);


    @staticmethod
    def templateStaticSimulation(ccore_falg):
        net = syncpr(10, 0.1, 0.1, ccore_falg);
         
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        net.train(patterns);
        net.simulate_static(20, 10, patterns[0], solve_type.RK4);
        memory_order = net.memory_order(patterns[0]);
         
        assert (memory_order > 0.95) and (memory_order <= 1.000005);


    @staticmethod
    def templateDynamicSimulation(ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
         
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        net.train(patterns);
        net.simulate_dynamic(patterns[0], order = 0.998, solution = solve_type.RK4);
        memory_order = net.memory_order(patterns[0]);
         
        assert (memory_order > 0.998) and (memory_order <= 1.0);


    @staticmethod
    def templateGlobalSyncOrder(ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        
        patterns =  [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        global_sync_order = net.sync_order();
        assert (global_sync_order < 1.0) and (global_sync_order > 0.0);
        
        net.train(patterns);
        
        global_sync_order = net.sync_order();
        assert (global_sync_order < 1.0) and (global_sync_order > 0.0);


    @staticmethod
    def templateLocalSyncOrder(ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        
        patterns =  [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        local_sync_order = net.sync_local_order();
        assert (local_sync_order < 1.0) and (local_sync_order > 0.0);
        
        net.train(patterns);
        
        local_sync_order = net.sync_local_order();
        assert (local_sync_order < 1.0) and (local_sync_order > 0.0);


    @staticmethod
    def templateIncorrectPatternValues(ccore_flag):
        patterns =  [];
        patterns += [ [2, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -2, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        SyncprTestTemplates.templateIncorrectPatternForTraining(patterns, ccore_flag);