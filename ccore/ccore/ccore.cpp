/**************************************************************************************************************

Interface of the CCORE library that is used by pyclustering.

Based on article description:
 - S.Guha, R.Rastogi, K.Shim. CURE: An Efficient Clustering Algorithm for Large Databases. 1998.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************************************************/

#include <string>
#include <fstream>
#include <sstream>

#include "agglomerative.h"
#include "dbscan.h"
#include "cure.h"
#include "hierarchical.h"
#include "hsyncnet.h"
#include "kmeans.h"
#include "kmedians.h"
#include "rock.h"
#include "syncnet.h"
#include "xmeans.h"

#include "legion.h"
#include "pcnn.h"
#include "som.h"
#include "sync.h"
#include "syncpr.h"

#include "support.h"
#include "ccore.h"


void free_clustering_result(clustering_result * pointer) {
	if (pointer != NULL) {
		if (pointer->clusters != NULL) {
			delete pointer->clusters;
			pointer->clusters = NULL;
		}

		delete pointer;
		pointer = NULL;
	}
}

void free_dynamic_result(dynamic_result * pointer) {
	if (pointer != NULL) {
		if (pointer->times != NULL) {
			delete pointer->times;
			pointer->times = NULL;
		}

		if (pointer->dynamic != NULL) {
			for (unsigned int index_object = 0; index_object < pointer->size_dynamic; index_object++) {
				if (pointer->dynamic[index_object] != NULL) {
					delete pointer->dynamic[index_object];
					pointer->dynamic[index_object] = NULL;
				}
			}

			delete pointer->dynamic;
			pointer->dynamic = NULL;
		}

		delete pointer;
		pointer = NULL;
	}
}

void free_pyclustering_package(pyclustering_package * package) {
	if (package->type != (unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST) {
		switch(package->type) {
			case pyclustering_type_data::PYCLUSTERING_TYPE_INT:
				delete (int *) package->data;
				break;

			case pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_INT:
				delete (unsigned int *) package->data;
				break;

			case pyclustering_type_data::PYCLUSTERING_TYPE_FLOAT:
				delete (float *) package->data;
				break;

			case pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE:
				delete (double *) package->data;
				break;

			case pyclustering_type_data::PYCLUSTERING_TYPE_LONG:
				delete (long *) package->data;
				break;

			case pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_LONG:
				delete (unsigned long *) package->data;
				break;

			default:
				/* Memory Leak */
				break;
		}

		delete package;
		package = NULL;
	}
	else {
		for (unsigned int i = 0; i < package->size; i++) {
			free_pyclustering_package( ( (pyclustering_package **) package->data)[i] );
		}

		delete package;
		package = NULL;
	}
}

pyclustering_package * agglomerative_algorithm(const data_representation * const sample, const unsigned int number_clusters, const unsigned int link) {
    agglomerative algorithm(number_clusters, (type_link) link);

    std::vector<std::vector<double> > * dataset = read_sample(sample);

    std::vector<cluster> clusters;
    algorithm.process(*dataset);
    algorithm.get_clusters(clusters);

    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = clusters.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&clusters[i]);
    }

    delete dataset;

    return package;
}

clustering_result * dbscan_algorithm(const data_representation * const sample, const double radius, const unsigned int minumum_neighbors) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);

	dbscan * solver = new dbscan(dataset, radius, minumum_neighbors);
	solver->process();

	const std::vector<std::vector<unsigned int> *> * const clusters = solver->get_clusters();

	std::vector<std::vector<unsigned int> *> * clusters_with_noise = new std::vector<std::vector<unsigned int> *>();
	for (std::vector<std::vector<unsigned int> *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
		clusters_with_noise->push_back(*iter);
	}
	clusters_with_noise->push_back((std::vector<unsigned int> *) solver->get_noise());

	clustering_result * result = create_clustering_result(clusters_with_noise);

	delete clusters_with_noise; clusters_with_noise = NULL;
	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
}

clustering_result * cure_algorithm(const data_representation * const sample, const unsigned int number_clusters, const unsigned int number_repr_points, const double compression) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);

	cure * solver = new cure(dataset, number_clusters, number_repr_points, compression);
	solver->process();

	const std::vector<std::vector<unsigned int> *> * const clusters = solver->get_clusters();
	clustering_result * result = create_clustering_result(clusters);

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
}

clustering_result * hierarchical_algorithm(const data_representation * const sample, const unsigned int number_clusters) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);

	hierarchical * solver = new hierarchical(dataset, number_clusters);
	solver->process();

	const std::vector<std::vector<unsigned int> *> * const clusters = solver->get_clusters();
	clustering_result * result = create_clustering_result(clusters);

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
}

clustering_result * kmeans_algorithm(const data_representation * const sample, const data_representation * const initial_centers, const double tolerance) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);
	std::vector<std::vector<double> > * centers = read_sample(initial_centers);

	kmeans * solver = new kmeans(dataset, centers, tolerance);
	solver->process();

	clustering_result * result = create_clustering_result(solver->get_clusters());

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;
	delete centers; centers = NULL;

	return result;
}

pyclustering_package * kmedians_algorithm(const data_representation * const sample, const data_representation * const initial_medians, const double tolerance) {
    std::vector<std::vector<double> > * dataset = read_sample(sample);
    std::vector<std::vector<double> > * medians = read_sample(initial_medians);

    kmedians algorithm(*medians, tolerance);

    std::vector<cluster> clusters;
    algorithm.process(*dataset);
    algorithm.get_clusters(clusters);

    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = clusters.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&clusters[i]);
    }

    delete dataset;
    delete medians;

    return package;
}

clustering_result * rock_algorithm(const data_representation * const sample, const double radius, const unsigned int number_clusters, const double threshold) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);

	rock * solver = new rock(dataset, radius, number_clusters, threshold);
	solver->process();

	clustering_result * result = create_clustering_result(solver->get_clusters());

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
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
	return (void *) new sync_network(size, weight_factor, frequency_factor, (conn_type) connection_type, (initial_type) initial_phases);
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

pyclustering_package * sync_dynamic_allocate_sync_ensembles(const void * pointer, const double tolerance) {
	ensemble_data<sync_ensemble> ensembles;

	((sync_dynamic *) pointer)->allocate_sync_ensembles(tolerance, ensembles);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = ensembles.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&ensembles[i]);
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
    return sync_dynamic_allocate_sync_ensembles(pointer, tolerance);
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



void * hsyncnet_create_network(const data_representation * const sample, const unsigned int number_clusters, const unsigned int initial_phases) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);	/* belongs to hsyncnet */
	return (void *) new hsyncnet(dataset, number_clusters, (initial_type) initial_phases);
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


void * pcnn_create(const unsigned int size, const unsigned int connection_type, const unsigned int height, const unsigned width, const void * const parameters) {
    pcnn * pcnn_network = new pcnn(size, (conn_type) connection_type, height, width, *((pcnn_parameters *) parameters));
	return (void *) pcnn_network;
}

void pcnn_destroy(const void * pointer) {
	delete (pcnn *) pointer;
}


void * pcnn_simulate(const void * pointer, const unsigned int steps, const void * const stimulus) {
	const pyclustering_package * const package_stimulus = (const pyclustering_package * const) stimulus;
	pcnn_stimulus stimulus_vector((double *) package_stimulus->data, ((double *) package_stimulus->data) + package_stimulus->size);

	pcnn_dynamic * dynamic = new pcnn_dynamic();
	((pcnn *) pointer)->simulate(steps, stimulus_vector, (*dynamic));

	return dynamic;
}

unsigned int pcnn_get_size(const void * pointer) {
	return ((pcnn *) pointer)->size();
}


void pcnn_dynamic_destroy(const void * pointer) {
	delete (pcnn_dynamic *) pointer;
}


pyclustering_package * pcnn_dynamic_allocate_sync_ensembles(const void * pointer) {
	ensemble_data<pcnn_ensemble> sync_ensembles;
	((pcnn_dynamic *) pointer)->allocate_sync_ensembles(sync_ensembles);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = sync_ensembles.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&sync_ensembles[i]);
	}

	return package;
}

pyclustering_package * pcnn_dynamic_allocate_spike_ensembles(const void * pointer) {
	ensemble_data<pcnn_ensemble> spike_ensembles;
	((pcnn_dynamic *) pointer)->allocate_spike_ensembles(spike_ensembles);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = spike_ensembles.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&spike_ensembles[i]);
	}

	return package;
}

pyclustering_package * pcnn_dynamic_allocate_time_signal(const void * pointer) {
	pcnn_time_signal time_signal;
	((pcnn_dynamic *) pointer)->allocate_time_signal(time_signal);

	pyclustering_package * package = create_package(&time_signal);

	return package;
}

pyclustering_package * pcnn_dynamic_get_output(const void * pointer) {
	pcnn_dynamic & dynamic = *((pcnn_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
	package->size = dynamic.size();
	package->data = new pyclustering_package * [package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((pyclustering_package **) package->data)[i] = create_package(&dynamic[i].m_output);
	}

	return package;
}

pyclustering_package * pcnn_dynamic_get_time(const void * pointer) {
	pcnn_dynamic & dynamic = *((pcnn_dynamic *) pointer);

	pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
	package->size = dynamic.size();
	package->data = new double[package->size];

	for (unsigned int i = 0; i < package->size; i++) {
		((double *) package->data)[i]  = dynamic[i].m_time;
	}

	return package;
}

unsigned int pcnn_dynamic_get_size(const void * pointer) {
	return ((pcnn_dynamic *) pointer)->size();
}



void * legion_create(const unsigned int size, const unsigned int connection_type, const void * const parameters) {
	legion_network * pcnn_network = new legion_network(size, (conn_type) connection_type, *((legion_parameters *) parameters));
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
