"""!

@brief CCORE Wrapper for ant colony based algorithm for travelling salesman problem.

@authors Andrei Novikov, Alexey Kukushkin (pyclustering@yandex.ru)
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

from pyclustering.core.wrapper import *;

import types;


CITIES_DISTANCE_SET_BY_MATRIX = True
CITIES_DISTANCE_SET_BY_LIST_OF_COORDINATES = False


class c_antcolony_tsp_parameters(Structure):
    """
    double                  q;
    double                  ro;
    double                  alpha;
    double                  beta;
    double                  gamma;
    double                  initial_pheramone;
    unsigned int            iterations;
    unsigned int            ants_per_iteration;
    
    """
    _fields_ = [("q"        , c_double),
                ("ro"       , c_double),
                ("alpha"    , c_double),
                ("beta"     , c_double),
                ("gamma"    , c_double),
                ("qinit_pheramone"          , c_double),
                ("iterations"               , c_uint),
                ("ants_per_iteration"       , c_uint)    ];


class c_antcolony_tsp_objects(Structure):
    """
    unsigned int            size;
    unsigned int            dimension;
    double                  *data;
    
    """
    _fields_ = [("size"        , c_uint),
                ("dimension"   , c_uint),
                ("data"        , POINTER(c_double)) ];


class c_antcolony_tsp_matrix(Structure):
    """
    unsigned int            size;
    double                  **data;
    
    """
    _fields_ = [("size"        , c_uint),
                ("data"        , POINTER(POINTER(c_double))) ];
                

class c_antcolony_tsp_result(Structure):
    """
    unsigned int            size;
    double                  path_length;
    unsigned int            *cities_num;
    
    """
    _fields_ = [("size"              , c_uint),
                ("path_length"       , c_double),
                ("object_sequence"   , POINTER(c_uint)) ];



def get_algo_params(params):
    
    algorithm_params = c_antcolony_tsp_parameters();
    algorithm_params.q          = c_double(params.q);
    algorithm_params.ro         = c_double(params.ro);
    algorithm_params.alpha      = c_double(params.alpha);
    algorithm_params.beta       = c_double(params.beta);
    algorithm_params.gamma      = c_double(params.gamma);
    algorithm_params.qinit_pheramone            = c_double(params.qinit_pheramone);
    algorithm_params.iterations                 = c_uint(params.iterations);
    algorithm_params.ants_per_iteration         = c_uint(params.ants_per_iteration);
    
    algorithm_params = pointer(algorithm_params);
    
    return algorithm_params


def antcolony_tsp_prepare_matrix(matrix):
    dist_matrix = c_antcolony_tsp_matrix()
    
    dist_matrix.size = len(matrix)
    
    p_dist = (POINTER(c_double) * dist_matrix.size)();
     
    for i in range(dist_matrix.size):
        tmp_p_dist = (c_double * dist_matrix.size)();
        for j in range(dist_matrix.size):
            tmp_p_dist[j] = matrix[i][j];
            
        p_dist[i] = cast(tmp_p_dist, POINTER(c_double));
    
    dist_matrix.data = cast(p_dist, POINTER(POINTER(c_double)));
    dist_matrix = pointer(dist_matrix)
    
    return dist_matrix
    
    
def antcolony_tsp_prepare_cities_list(cities):
    dimension = len(cities[0]);
    
    cities_coord = c_antcolony_tsp_objects();
    cities_coord.size = c_uint(len(cities) * dimension);
    cities_coord.dimension = c_uint(dimension);
    
    cities_coord.data = (c_double * cities_coord.size)();
    
    for i in range(0, cities_coord.size):
        cities_coord.data[i] = cities[i // dimension][i % dimension];
    
    cities_coord = pointer(cities_coord);
    
    return cities_coord


def antcolony_tsp_process(cities, params, citiesDistRepresent = CITIES_DISTANCE_SET_BY_LIST_OF_COORDINATES):
    algorithm_params = get_algo_params(params)
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
     
    if citiesDistRepresent == CITIES_DISTANCE_SET_BY_MATRIX:
        cities_coord = antcolony_tsp_prepare_matrix(cities)
        result_pointer = ccore.ant_colony_tsp_process_by_matrix(cities_coord, algorithm_params);
    else:
        cities_coord = antcolony_tsp_prepare_cities_list(cities)
        result_pointer = ccore.ant_colony_tsp_process(cities_coord, algorithm_params);
    
    result = cast(result_pointer, POINTER(c_antcolony_tsp_result))[0];
    
    return (result_pointer, result);


def antcolony_tsp_destroy(tsp_result_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.ant_colony_tsp_destroy(tsp_result_pointer);
