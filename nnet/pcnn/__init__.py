from nnet import *;

class pcnn_network(network, network_interface):
    "Model of oscillatory network that is based on the Eckhorn model."
    
    # Protected members:
    _name = "Pulse Coupled Neural Network";
    _stimulus = None;           # stimulus of each oscillator.
    _outputs = None;            # list of outputs of oscillors.
    
    _feeding = None;            # feeding compartment of each oscillator.
    _buffer_feeding = None;     # previous feeding compartment of each oscillator.
    
    _linking = None;            # linking compartment of each oscillator.
    _buffer_linking = None;     # previous linking compartment of each oscillator.
    
    _threshold = None;          # threshold of each oscillator.
    
    _linking_strength = 1;      # linking strength in the network.
    
    def __init__(self, num_osc, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX):
        super().__init__(num_osc, type_conn, conn_represent);
        
        self._outputs = [0] * self._num_osc;
        
        self._feeding = [0] * self._num_osc;
        self._buffer_feeding = [0] * self._num_osc;
        
        self._linking = [0] * self._num_osc;
        self._buffer_linking = [0] * self._num_osc;
        
        self._threshold = [0] * self._num_osc;
    
    
    def simulate_static(self, steps, time, solution = solve_type.ODEINT, collect_dynamic = False):
        for step in range(0, steps, 1):
            self._buffer_feeding = self._feeding[:];
            self._buffer_linking = self._linking[:];
            
            
        
    def _calculate_states(self, solution, t, step, int_step):
        feeding = [0] * self._num_osc;
        linking = [0] * self._num_osc;
        outputs = [0] * self._num_osc;
        threshold = [0] * self._num_osc;
        
        for index in range(0, self._num_osc, 1):
            feeding[index] = self._feeding[index] + self._stimulus[index];
            linking[index] = self._linking[index];
            
            # calculate internal activity
            internal_activity = self._feeding[index] * (1 + self._linking_strength * linking[index]);
            
            # calculate output of the oscillator
            if (internal_activity > self._threshold[index]):
                outputs[index] = 1;
            else:
                outputs[index] = 0;
                
            threshold[index] = self._threshold[index] + outputs[index];
        