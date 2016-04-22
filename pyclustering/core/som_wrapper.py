"""!

@brief CCORE Wrapper for Self-Organized Feature Map

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from ctypes import cdll, Structure, c_uint, c_double, pointer;

from pyclustering.core.wrapper import PATH_DLL_CCORE_64, create_pointer_data, extract_pyclustering_package;

class c_som_parameters(Structure):
    "Description of SOM parameters in memory"
    " - unsigned int init_type"
    " - double init_radius"
    " - double init_learn_rate"
    " - double adaptation_threshold"
    
    _fields_ = [("init_type", c_uint),
                ("init_radius", c_double),
                ("init_learn_rate", c_double),
                ("adaptation_threshold", c_double)];


def som_create(rows, cols, conn_type, parameters):
    """!
    @brief Create of self-organized map using CCORE pyclustering library.
    
    @param[in] rows (uint): Number of neurons in the column (number of rows).
    @param[in] cols (uint): Number of neurons in the row (number of columns).
    @param[in] conn_type (type_conn): Type of connection between oscillators in the network (grid four, grid eight, honeycomb, function neighbour).
    @param[in] parameters (som_parameters): Other specific parameters.
    
    @return (POINTER) C-pointer to object of self-organized feature in memory.
    
    """  

    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    
    c_params = c_som_parameters();
    
    c_params.init_type = parameters.init_type;
    c_params.init_radius = parameters.init_radius;
    c_params.init_learn_rate = parameters.init_learn_rate;
    c_params.adaptation_threshold = parameters.adaptation_threshold;
    
    som_pointer = ccore.som_create(c_uint(rows), c_uint(cols), c_uint(conn_type), pointer(c_params));
    
    return som_pointer;


def som_destroy(som_pointer):
    """!
    @brief Destroys self-organized map.
    
    @param[in] som_pointer (POINTER): pointer to object of self-organized map.
    
    """
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.som_destroy(som_pointer);
    
    
def som_train(som_pointer, data, epochs, autostop):
    """!
    @brief Trains self-organized feature map (SOM) using CCORE pyclustering library.

    @param[in] data (list): Input data - list of points where each point is represented by list of features, for example coordinates.
    @param[in] epochs (uint): Number of epochs for training.        
    @param[in] autostop (bool): Automatic termination of learining process when adaptation is not occurred.
    
    @return (uint) Number of learining iterations.
    
    """ 
    
    pointer_data = create_pointer_data(data);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.som_train(som_pointer, pointer_data, c_uint(epochs), autostop);

def som_simulate(som_pointer, pattern):
    "Processes input pattern (no learining) and returns index of neuron-winner."
    "Using index of neuron winner catched object can be obtained using property capture_objects."
    
    "(in) som_pointer      - pointer to object of self-organized map."
    "(in) input_pattern    - input pattern."
        
    "Returns index of neuron-winner."
            
    pointer_data = create_pointer_data(pattern);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.som_simulate(som_pointer, pointer_data);

def som_get_winner_number(som_pointer):
    "Returns of number of winner at the last step of learning process."
    
    "(in) som_pointer    - pointer to object of self-organized map."
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.som_get_winner_number(som_pointer);

def som_get_size(som_pointer):
    "Returns size of self-organized map (number of neurons)."
    
    "(in) som_pointer    - pointer to object of self-organized map."
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.som_get_size(som_pointer);

def som_get_capture_objects(som_pointer):
    "Returns list of indexes of captured objects by each neuron."
    
    "(in) som_pointer    - pointer to object of self-organized map."
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.som_get_capture_objects(som_pointer);
    
    result = extract_pyclustering_package(package);
    return result;

def som_get_weights(som_pointer):
    "Returns list of weights of each neuron."
    
    "(in) som_pointer    - pointer to object of self-organized map."
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.som_get_weights(som_pointer);
    
    result = extract_pyclustering_package(package);
    return result;   

def som_get_awards(som_pointer):
    "Returns list of numbers of captured objects by each neuron."
    
    "(in) som_pointer    - pointer to object of self-organized map."
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.som_get_awards(som_pointer);
    
    result = extract_pyclustering_package(package);
    return result;  

def som_get_neighbors(som_pointer):
    "Returns list of indexes of neighbors of each neuron."
    
    "(in) som_pointer    - pointer to object of self-organized map."
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.som_get_neighbors(som_pointer);
    
    result = extract_pyclustering_package(package);
    return result;  