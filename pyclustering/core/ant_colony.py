

import ctypes as ct

from pyclustering.core.definitions import PATH_DLL_CCORE_WIN64

from pyclustering.core.definitions import ant_colony_TSP_cities
from pyclustering.core.definitions import ant_colony_TSP_params
from pyclustering.core.definitions import ant_colony_TSP_result

import collections

def ant_colony_TSP_run(cities, params):
    
    dimension = len(cities[0])
    
    cities_coord = ant_colony_TSP_cities()
    cities_coord.size = ct.c_uint(len(cities) * dimension)
    cities_coord.dimension = ct.c_uint(dimension)
    
    cities_coord.data = (ct.c_double * cities_coord.size)();
    for i in range(0, cities_coord.size):
        cities_coord.data[i] =cities[i // dimension][i % dimension]
    
    cities_coord = ct.pointer(cities_coord);


    algorithm_params = ant_colony_TSP_params()
    algorithm_params.q          = ct.c_double(params.q)
    algorithm_params.ro         = ct.c_double(params.ro)
    algorithm_params.alpha      = ct.c_double(params.alpha)
    algorithm_params.beta       = ct.c_double(params.beta)
    algorithm_params.gamma      = ct.c_double(params.gamma)
    algorithm_params.qinitial_pheramone         = ct.c_double(params.qinitial_pheramone)
    algorithm_params.iterations                 = ct.c_uint(params.iterations)
    algorithm_params.count_ants_in_iteration    = ct.c_uint(params.count_ants_in_iteration)
    
    algorithm_params = ct.pointer(algorithm_params)
    
    
    ccore = ct.cdll.LoadLibrary(PATH_DLL_CCORE_WIN64)
    result = ccore.ant_colony_TSP(cities_coord, algorithm_params)
    
    result = ct.cast(result, ct.POINTER(ant_colony_TSP_result))[0]
    #result = result[0]    
    
    return result
    


cities = [[0.0, 0.0], [0.0, 1.0], [0.0, 2.0], [1.0, 0.0], [1.0, 1.0], [1.0, 2.0]]

params = collections.namedtuple('Params', 'q ro alpha beta gamma qinitial_pheramone iterations count_ants_in_iteration')
params.q        = 1.5;
params.ro       = 0.7
params.alpha    = 1.0
params.beta     = 1.0
params.gamma    = 2.0
params.qinitial_pheramone       = 0.1
params.iterations               = 50
params.count_ants_in_iteration  = 10

res = ant_colony_TSP_run(cities, params)

print ("Result :")
print (res.size)
print (res.path_length)
for i in range(res.size):
    print (res.cities_num[i])

