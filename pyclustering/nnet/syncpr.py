"""!

@brief Phase oscillatory network for patten recognition based on modified Kuramoto model.
@details Based on article description:
         - R.Follmann, E.E.N.Macau, E.Rosa, Jr., J.R.C.Piqueira. Phase Oscillatory Network and Visual Pattern Recognition. 2014.
         
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2015
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

from pyclustering.nnet import sync;

from pyclustering.nnet import conn_type;

import math;

class syncpr(sync):
    _increase_strength1 = 0.0;
    _increase_strength2 = 0.0;
    _coupling = None;
    
    def __init__(self, num_osc, increase_strength1, increase_strength2):
        self._increase_strength1 = increase_strength1;
        self._increase_strength2 = increase_strength2;
        self._coupling = [ [0 for i in range(num_osc)] for j in range(num_osc) ];
    
        super().__init__(num_osc, type_conn = conn_type.NONE);
        
    def train(self, samples):
        for i in range(0, len(self), 1):
            for j in range(i + 1, len(self), 1):
                
                # go through via all patterns
                for p in range(len(samples)):
                    value1 = 1;
                    if (samples[p][i] > 0.5):
                        value1 = -1;
                    
                    value2 = 1;
                    if (samples[p][j] > 0.5):
                        value2 = -1;
                    
                    self._coupling[i][j] += value1 * value2;
                
                self._coupling[i][j] /= len(self);
                self._coupling[j][i] = self._coupling[i][j];
    
    
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