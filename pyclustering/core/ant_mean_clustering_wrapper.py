'''
Created on Jul 1, 2016

@author: alex
'''


from pyclustering.core.wrapper import *;

import types;


class c_antcolony_clustering_parameters(Structure):
    """
    double                  ro;
    double                  pheramone_init;
    unsigned int            iterations;
    unsigned int            count_ants;
    
    """
    _fields_ = [("ro"       , c_double),
                ("pheramone_init"          , c_double),
                ("iterations"               , c_uint),
                ("count_ants"               , c_uint)    ];
    


def ant_mean_clustering_process(params, count_clusters, samples):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    
    algorithm_params = c_antcolony_clustering_parameters();
    algorithm_params.ro                         = c_double(params.ro);
    algorithm_params.pheramone_init             = c_double(params.pheramone_init);
    algorithm_params.iterations                 = c_uint(params.iterations);
    algorithm_params.count_ants                 = c_uint(params.count_ants);
    
    algorithm_params = pointer(algorithm_params);
    
    p_samples = create_pointer_data(samples)
    
    """
        Run algorithm
    """
    res = ccore.ant_mean_clustering(p_samples, algorithm_params, count_clusters)
    res = cast(res, POINTER(clustering_result));
    
    """
        Cast result to python view
    """
    pointer_data = cast(res[0].pointer_clusters, POINTER(cluster_representation))
    num_clusters = res[0].number_clusters
    
    pyResult = [[] for i in range(num_clusters)]
    
    for i in range(num_clusters):
        for j in range(pointer_data[i].number_objects):
            pyResult[i].append(pointer_data[i].pointer_objects[j])

    return pyResult
    
    
#res = ant_mean_clustering_process(ant_mean_clustering(), 2, [[ 0,0 ],[ 1,1 ],[ 10,10 ],[ 11,11 ],[ -2, -2 ],[ 0.55, -1.26 ],[ 13.25, 12.12 ]])
#print(res)
    
    
    
    
    
    
    
    
    
    
    
    