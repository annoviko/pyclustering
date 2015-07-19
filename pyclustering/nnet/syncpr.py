from pyclustering.nnet import sync;

import math;

class syncpr(sync):
    _increase_strength1 = 0.0;
    _increase_strength2 = 0.0;
    _coupling = None;
    
    def _phase_kuramoto(self, teta, t, argv):
        index = argv;
        
        phase = 0.0;
        term = 0.0;
        
        for k in range(0, self._num_osc):
            phase_delta = self._phases[k] - teta;
            
            phase += self._coupling[index][k] * math.sin(phase_delta);
            
            term1 = self._increase_strength1 * math.sin(2.0 * phase_delta);
            term2 = self._increase_strength2 * math.sin(3.0 * phase_delta);
            
            term += (term1 - term2);
                
        return ( phase + (1 / len(self)) * term );