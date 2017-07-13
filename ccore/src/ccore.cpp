/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#include <string>
#include <fstream>
#include <sstream>

#include "ccore.h"

#include "cluster/agglomerative.hpp"
#include "cluster/hsyncnet.hpp"
#include "cluster/syncnet.hpp"
#include "cluster/xmeans.hpp"

#include "interface/sync_interface.h"

#include "nnet/legion.hpp"

#include "tsp/ant_colony.hpp"

#include "utils.hpp"


using namespace container;


/***********************************************************************************************
*
* @brief syncnet - phase oscillatory network (for cluster analysis) interface implementation.
*
***********************************************************************************************/
void * syncnet_create_network(const data_representation * const sample, const double connectivity_radius, const bool enable_conn_weight, const unsigned int initial_phases) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);	/* belongs to syncnet */
	return (void *) new syncnet(dataset, connectivity_radius, enable_conn_weight, (initial_type) initial_phases);
}

void syncnet_destroy_network(const void * pointer_network) {
	if (pointer_network != NULL) {
		delete (syncnet *) pointer_network;
	}
}

void * syncnet_process(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic) {
	syncnet * network = (syncnet *) pointer_network;
	
	syncnet_analyser * analyser = new syncnet_analyser();
	network->process(order, (solve_type) solver, collect_dynamic, (*analyser));

	ensemble_data<sync_ensemble> ensembles;
	analyser->allocate_sync_ensembles(0.1, ensembles);

	return analyser;
}

void syncnet_analyser_destroy(const void * pointer_analyser) {
	if (pointer_analyser != NULL) {
		delete (syncnet_analyser *) pointer_analyser;
	}
}



void * hsyncnet_create_network(const data_representation * const sample, 
                               const unsigned int number_clusters, 
                               const unsigned int initial_phases,
                               const unsigned int initial_neighbors,
                               const double increase_persent) {

	std::vector<std::vector<double> > * dataset = read_sample(sample);	/* belongs to hsyncnet */
	return (void *) new hsyncnet(dataset, number_clusters, (initial_type) initial_phases, initial_neighbors, increase_persent);
}

void hsyncnet_destroy_network(const void * pointer_network) {
	if (pointer_network != NULL) {
		delete (hsyncnet *) pointer_network;
	}
}

void * hsyncnet_process(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic) {
	hsyncnet * network = (hsyncnet *) pointer_network;

	hsyncnet_analyser * analyser = new hsyncnet_analyser();
	network->process(order, (solve_type) solver, collect_dynamic, *analyser);

	return (void *) analyser;
}

void hsyncnet_analyser_destroy(const void * pointer_analyser) {
	if (pointer_analyser != NULL) {
		delete (hsyncnet_analyser *) pointer_analyser;
	}
}


/////////////////////////////////////////////////////////////////////////////
//                  Ant Colony functions
//
tsp_result * ant_colony_tsp_process_get_result(std::shared_ptr<city_distance::distance_matrix>& dist, const ant::ant_colony_tsp_params * algorithm_params) {
       // Algorithm params
       using AntAPI = ant::ant_colony_TSP_params_initializer;
       auto algo_params = ant::ant_colony_TSP_params::make_param
           (AntAPI::Q_t{ algorithm_params->q }
               , AntAPI::Ro_t{ algorithm_params->ro }
               , AntAPI::Alpha_t{ algorithm_params->alpha }
               , AntAPI::Beta_t{ algorithm_params->beta }
               , AntAPI::Gamma_t{ algorithm_params->gamma }
               , AntAPI::InitialPheramone_t{ algorithm_params->initial_pheramone }
               , AntAPI::Iterations_t{ algorithm_params->iterations }
               , AntAPI::CountAntsInIteration_t{ algorithm_params->count_ants_in_iteration }
       );

       // process()
       ant::ant_colony ant_algo{ dist, algo_params };
       auto algo_res = ant_algo.process();

       // create result for python
       tsp_result * result = new tsp_result();

       // init path length
       result->path_length = algo_res->path_length;

       // create array to stored cities in the path
       result->objects_sequence = new unsigned int[algo_res->shortest_path.size()];
       result->size = algo_res->shortest_path.size();

       // copy cities to result
       for (std::size_t object_number = 0; object_number < algo_res->shortest_path.size(); ++object_number) {
           result->objects_sequence[object_number] = algo_res->shortest_path[object_number];
       }

       return result;
}

tsp_result * ant_colony_tsp_process_by_matrix(const tsp_matrix * objects_coord, const void * ant_colony_parameters) {
    std::vector<std::vector<double>> matrix;

    matrix.resize(objects_coord->size);

    for (std::size_t i = 0; i < matrix.size(); ++i) {
        matrix[i].resize(objects_coord->size);

        for (std::size_t j = 0; j < matrix[i].size(); ++j) {
            matrix[i][j] = objects_coord->data[i][j];
        }
    }

    auto dist = city_distance::distance_matrix::make_city_distance_matrix (matrix);
    return ant_colony_tsp_process_get_result(dist, static_cast<const ant::ant_colony_tsp_params *>(ant_colony_parameters) );
}


tsp_result * ant_colony_tsp_process(const tsp_objects * objects_coord, const void * ant_colony_parameters) {
    const ant::ant_colony_tsp_params * algorithm_params = (const ant::ant_colony_tsp_params *) ant_colony_parameters;
    std::vector<city_distance::object_coordinate> cities;

    for (std::size_t city_num = 0; city_num < objects_coord->size / objects_coord->dimention; ++city_num) {
        std::vector<double> v(objects_coord->dimention);

        for (std::size_t dim = 0; dim < objects_coord->dimention; ++dim) {
            v[dim] = objects_coord->data[city_num*objects_coord->dimention + dim];
        }

        cities.push_back(std::move(v));
    }

    auto dist = city_distance::distance_matrix::make_city_distance_matrix (cities);
    return ant_colony_tsp_process_get_result(dist, algorithm_params);
}


void ant_colony_tsp_destroy(const void * result) {
    if (result != nullptr) {
        delete [] ((tsp_result *) result)->objects_sequence;
        delete (tsp_result *) result;
    }
}
//
//                  End Ant colony functions
/////////////////////////////////////////////////////////////////////////////


void * legion_create(const unsigned int size, const unsigned int connection_type, const void * const parameters) {
	legion_network * pcnn_network = new legion_network(size, (connection_t) connection_type, *((legion_parameters *) parameters));
	return (void *) pcnn_network;
}

void legion_destroy(const void * pointer) {
	delete (legion_network *) pointer;
}

void * legion_simulate(const void * pointer, 
                       const unsigned int steps, 
					   const double time, 
					   const unsigned int solver, 
					   const bool collect_dynamic, 
					   const void * const stimulus) {

	const pyclustering_package * const package_stimulus = (const pyclustering_package * const) stimulus;
	legion_stimulus stimulus_vector((double *) package_stimulus->data, ((double *) package_stimulus->data) + package_stimulus->size);

	legion_dynamic * dynamic = new legion_dynamic();
	((legion_network *) pointer)->simulate(steps, time, (solve_type) solver, collect_dynamic, stimulus_vector, (*dynamic));

	return dynamic;
}

unsigned int legion_get_size(const void * pointer) {
	return ((legion_network *) pointer)->size();
}

void legion_dynamic_destroy(const void * pointer) {
	delete (legion_dynamic *) pointer;
}

pyclustering_package * legion_dynamic_get_output(const void * pointer) {
	legion_dynamic & dynamic = *((legion_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = dynamic.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_output);
	}

	return package;
}

pyclustering_package * legion_dynamic_get_inhibitory_output(const void * pointer) {
	legion_dynamic & dynamic = *((legion_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
	package->size = dynamic.size();
	package->data = new double[package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((double *) package->data)[i] = dynamic[i].m_inhibitor;
	}

	return package;
}

pyclustering_package * legion_dynamic_get_time(const void * pointer) {
	legion_dynamic & dynamic = *((legion_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
	package->size = dynamic.size();
	package->data = new double[package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((double *) package->data)[i] = dynamic[i].m_time;
	}

	return package;
}

unsigned int legion_dynamic_get_size(const void * pointer) {
	return ((legion_dynamic *) pointer)->size();
}
