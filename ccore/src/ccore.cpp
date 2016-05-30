/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include "nnet/legion.hpp"
#include "nnet/som.hpp"
#include "nnet/sync.hpp"
#include "nnet/syncpr.hpp"

#include "tsp/ant_colony.hpp"

#include "utils.hpp"


using namespace container;


void free_clustering_result(clustering_result * pointer) {
	if (pointer != NULL) {
		if (pointer->clusters != NULL) {
		    for (size_t i = 0; i < pointer->size; i++) {
		        delete [] pointer->clusters[i].objects;
		    }

			delete [] pointer->clusters;
			pointer->clusters = NULL;
		}

		delete pointer;
		pointer = NULL;
	}
}

void free_dynamic_result(dynamic_result * pointer) {
	if (pointer != NULL) {
		if (pointer->times != NULL) {
			delete [] pointer->times;
			pointer->times = NULL;
		}

		if (pointer->dynamic != NULL) {
			for (unsigned int index_object = 0; index_object < pointer->size_dynamic; index_object++) {
				if (pointer->dynamic[index_object] != NULL) {
					delete [] pointer->dynamic[index_object];
					pointer->dynamic[index_object] = NULL;
				}
			}

			delete [] pointer->dynamic;
			pointer->dynamic = NULL;
		}

		delete pointer;
		pointer = NULL;
	}
}

void free_pyclustering_package(pyclustering_package * package) {
    delete package;
}


clustering_result * xmeans_algorithm(const data_representation * const sample, const data_representation * const initial_centers, const unsigned int kmax, const double tolerance) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);
	std::vector<std::vector<double> > * centers = read_sample(initial_centers);

	xmeans solver(*dataset, *centers, kmax, tolerance);
	solver.process();

	std::vector<std::vector<unsigned int> > output_clusters;
	solver.get_clusters(output_clusters);

	clustering_result * result = create_clustering_result(output_clusters);

	delete dataset; dataset = NULL;
	delete centers; centers = NULL;

	return result;	
}

void * sync_create_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int connection_type, const unsigned int initial_phases) {
	return (void *) new sync_network(size, weight_factor, frequency_factor, (connection_t) connection_type, (initial_type) initial_phases);
}

void sync_destroy_network(const void * pointer_network) {
	if (pointer_network != NULL) {
		delete (sync_network *) pointer_network;
	}
}

void * sync_simulate_static(const void * pointer_network, unsigned int steps, const double time, const unsigned int solver, const bool collect_dynamic) {
	sync_network * network = (sync_network *) pointer_network;

	sync_dynamic * dynamic = new sync_dynamic();
	network->simulate_static(steps, time, (solve_type) solver, collect_dynamic, (*dynamic));

	return (void *) dynamic;
}

void * sync_simulate_dynamic(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic, const double step, const double step_int, const double threshold_changes) {
	sync_network * network = (sync_network *) pointer_network;
	
	sync_dynamic * dynamic = new sync_dynamic();
	network->simulate_dynamic(order, step, (solve_type) solver, collect_dynamic, (*dynamic));

	return (void *) dynamic;
}

double sync_order(const void * pointer_network) {
	return ((sync_network *) pointer_network)->sync_order();
}

double sync_local_order(const void * pointer_network) {
	return ((sync_network *) pointer_network)->sync_local_order();
}

unsigned int sync_dynamic_get_size(const void * pointer_network) {
	return ((sync_dynamic *) pointer_network)->size();
}

void sync_dynamic_destroy(const void * pointer) {
	delete (sync_dynamic *) pointer;
}


pyclustering_package * sync_dynamic_allocate_sync_ensembles(const void * pointer, const double tolerance, const size_t iteration) {
	ensemble_data<sync_ensemble> ensembles;

	((sync_dynamic *) pointer)->allocate_sync_ensembles(tolerance, iteration, ensembles);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = ensembles.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&ensembles[i]);
	}

	return package;
}


pyclustering_package * sync_dynamic_allocate_correlation_matrix(const void * pointer_dynamic, const unsigned int iteration) {
    sync_corr_matrix matrix;
    ((sync_dynamic *) pointer_dynamic)->allocate_correlation_matrix(iteration, matrix);

    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = matrix.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&matrix[i]);
    }

    return package;
}


pyclustering_package * sync_dynamic_get_time(const void * pointer) {
	sync_dynamic & dynamic = *((sync_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
	package->size = dynamic.size();
	package->data = new double[package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((double *) package->data)[i]  = dynamic[i].m_time;
	}

	return package;
}

pyclustering_package * sync_dynamic_get_output(const void * pointer) {
	sync_dynamic & dynamic = *((sync_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = dynamic.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_phase);
	}

	return package;
}



/***********************************************************************************************
*
* @brief syncpr - phase oscillatory network (for pattern recognition) interface implementation.
*
***********************************************************************************************/
void * syncpr_create(const unsigned int num_osc,
                     const double increase_strength1,
                     const double increase_strength2)
{
    return (void *) new syncpr(num_osc, increase_strength1, increase_strength2);
}

void syncpr_destroy(const void * pointer_network) {
    delete (syncpr *)pointer_network;
}

unsigned int syncpr_get_size(const void * pointer_network) {
    return ((syncpr *)pointer_network)->size();
}

void syncpr_train(const void * pointer_network, const void * const patterns) {
    syncpr * network = (syncpr *)pointer_network;

    const pyclustering_package * const package_patterns = (const pyclustering_package * const)patterns;
    std::vector<syncpr_pattern> external_patterns(package_patterns->size, syncpr_pattern(network->size(), 0));

    for (size_t i = 0; i < package_patterns->size; i++) {
        const pyclustering_package * const package_pattern = ((pyclustering_package **)package_patterns->data)[i];
        std::copy((int *)package_pattern->data, ((int *)package_pattern->data) + package_pattern->size, external_patterns[i].begin());
    }

    network->train(external_patterns);
}

void * syncpr_simulate_static(const void * pointer_network,
                              unsigned int steps,
                              const double time,
                              const void * const pattern,
                              const unsigned int solver,
                              const bool collect_dynamic) 
{
    syncpr * network = (syncpr *)pointer_network;

    const pyclustering_package * const package_pattern = (const pyclustering_package * const)pattern;
    syncpr_pattern external_pattern((int *)package_pattern->data, ((int *)package_pattern->data) + package_pattern->size);

    syncpr_dynamic * dynamic = new syncpr_dynamic();
    network->simulate_static(steps, time, external_pattern, (solve_type)solver, collect_dynamic, (*dynamic));

    return (void *)dynamic;
}

void * syncpr_simulate_dynamic(const void * pointer_network,
                               const void * const pattern,
                               const double order,
                               const unsigned int solver,
                               const bool collect_dynamic,
                               const double step)
{
    syncpr * network = (syncpr *)pointer_network;

    const pyclustering_package * const package_pattern = (const pyclustering_package * const)pattern;
    syncpr_pattern external_pattern((int *)package_pattern->data, ((int *)package_pattern->data) + package_pattern->size);

    syncpr_dynamic * dynamic = new syncpr_dynamic();
    network->simulate_dynamic(external_pattern, order, step, (solve_type)solver, collect_dynamic, (*dynamic));

    return (void *)dynamic;
}

double syncpr_memory_order(const void * pointer_network, const void * const pattern) {
    const pyclustering_package * const package_pattern = (const pyclustering_package * const)pattern;
    syncpr_pattern external_pattern((int *)package_pattern->data, ((int *)package_pattern->data) + package_pattern->size);

    return ((syncpr *)pointer_network)->memory_order(external_pattern);
}

unsigned int syncpr_dynamic_get_size(const void * pointer_network) {
    return ((syncpr_dynamic *)pointer_network)->size();
}

void syncpr_dynamic_destroy(const void * pointer) {
    delete (syncpr_dynamic *)pointer;
}

pyclustering_package * syncpr_dynamic_allocate_sync_ensembles(const void * pointer, const double tolerance) {
    return sync_dynamic_allocate_sync_ensembles(pointer, tolerance, syncpr_dynamic_get_size(pointer) - 1);
}

pyclustering_package * syncpr_dynamic_get_time(const void * pointer) {
    return sync_dynamic_get_time(pointer);
}

pyclustering_package * syncpr_dynamic_get_output(const void * pointer) {
    return sync_dynamic_get_output(pointer);
}



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
tsp_result * ant_colony_tsp_process_get_result(std::shared_ptr<city_distance::distance_matrix>& dist, const ant::ant_colony_tsp_params * algorithm_params)
{
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

tsp_result * ant_colony_tsp_process_by_matrix(const tsp_matrix * objects_coord, const void * ant_colony_parameters)
{
    std::vector<std::vector<double>> matrix;

    matrix.resize(objects_coord->size);

    for (std::size_t i = 0; i < matrix.size(); ++i)
    {
        matrix[i].resize(objects_coord->size);

        for (std::size_t j = 0; j < matrix[i].size(); ++j)
        {
            matrix[i][j] = objects_coord->data[i][j];
        }
    }
    auto dist = city_distance::distance_matrix::make_city_distance_matrix (matrix);

    return ant_colony_tsp_process_get_result(dist, static_cast<const ant::ant_colony_tsp_params *>(ant_colony_parameters) );
}


tsp_result * ant_colony_tsp_process(const tsp_objects * objects_coord, const void * ant_colony_parameters)
{
	const ant::ant_colony_tsp_params * algorithm_params = (const ant::ant_colony_tsp_params *) ant_colony_parameters;
    std::vector<city_distance::object_coordinate> cities;

    for (std::size_t city_num = 0; city_num < objects_coord->size / objects_coord->dimention; ++city_num)
    {
        std::vector<double> v(objects_coord->dimention);

        for (std::size_t dim = 0; dim < objects_coord->dimention; ++dim)
        {
            v[dim] = objects_coord->data[city_num*objects_coord->dimention + dim];
        }

        cities.push_back(std::move(v));
    }

    auto dist = city_distance::distance_matrix::make_city_distance_matrix (cities);

    return ant_colony_tsp_process_get_result(dist, static_cast<const ant::ant_colony_tsp_params *>(ant_colony_parameters) );
}

void ant_colony_tsp_destroy(const void * result) {
	if (result != NULL) {
		delete [] ((tsp_result *) result)->objects_sequence;
		delete (tsp_result *) result;
	}
}
//
//                  End Ant colony functions
/////////////////////////////////////////////////////////////////////////////


void * som_create(const unsigned int num_rows, const unsigned int num_cols, const unsigned int type_conn, const void * parameters) {
	return (void *) new som(num_rows, num_cols, (som_conn_type) type_conn,  *((som_parameters *) parameters));
}

void som_destroy(const void * pointer) {
	if (pointer != NULL) {
		delete (som *) pointer;
	}
}

unsigned int som_train(const void * pointer, const data_representation * const sample, const unsigned int epochs, const bool autostop) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);
	unsigned int result = ((som *) pointer)->train(*dataset, epochs, autostop);
	delete dataset;

	return result;
}

unsigned int som_simulate(const void * pointer, const data_representation * const pattern) {
	std::vector<std::vector<double> > * input_pattern = read_sample(pattern);
	return ((som *) pointer)->simulate( (*input_pattern)[0] );
}

unsigned int som_get_winner_number(const void * pointer) {
	return ((som *) pointer)->get_winner_number();
}

unsigned int som_get_size(const void * pointer) {
	return ((som *) pointer)->get_size();
}


pyclustering_package * som_get_weights(const void * pointer) {
	std::vector<std::vector<double> > weights;
	((som *) pointer)->allocate_weights(weights);

	pyclustering_package * package = create_package(&weights);

	return package;
}

pyclustering_package * som_get_capture_objects(const void * pointer) {
	std::vector<std::vector<unsigned int> > capture_objects;
	((som *) pointer)->allocate_capture_objects(capture_objects);

	pyclustering_package * package = create_package(&capture_objects);

	return package;
}

pyclustering_package * som_get_awards(const void * pointer) {
	std::vector<unsigned int> awards;
	((som *) pointer)->allocate_awards(awards);
	pyclustering_package * package = create_package(&awards);

	return package;
}

pyclustering_package * som_get_neighbors(const void * pointer) {
	pyclustering_package * package = NULL;

	std::vector<std::vector<unsigned int> > neighbors;
	((som *) pointer)->allocate_neighbors(neighbors);
	if (!neighbors.empty()) {
		package = create_package(&neighbors);
	}

	return package;
}


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

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = dynamic.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_output);
	}

	return package;
}

pyclustering_package * legion_dynamic_get_inhibitory_output(const void * pointer) {
	legion_dynamic & dynamic = *((legion_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
	package->size = dynamic.size();
	package->data = new double[package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((double *) package->data)[i] = dynamic[i].m_inhibitor;
	}

	return package;
}

pyclustering_package * legion_dynamic_get_time(const void * pointer) {
	legion_dynamic & dynamic = *((legion_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
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
