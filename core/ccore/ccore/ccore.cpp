#include <string>
#include <fstream>
#include <sstream>

#include "dbscan.h"
#include "hierarchical.h"
#include "kmeans.h"
#include "rock.h"

#include "sync_network.h"

#include "support.h"
#include "interface_ccore.h"

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

clustering_result * rock_algorithm(const data_representation * const sample, const double radius, const unsigned int number_clusters, const double threshold) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);

	rock * solver = new rock(dataset, radius, number_clusters, threshold);
	solver->process();

	clustering_result * result = create_clustering_result(solver->get_clusters());

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
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

void destroy_object(void * object) {
	if (object != NULL) {
		delete object;
		object = NULL;
	}
}




/***********************************************************************************************
 *
 * @brief   Create oscillatory network Sync that is based on Kuramoto model.
 *
 * @param   (in) size				- number of oscillators in the network.
 *          (in) weight_factor		- coupling strength of the links between oscillators.
 *          (in) frequency_factor	- multiplier of internal frequency of the oscillators.
 *          (in) qcluster			- number of artificial clustering during synchronization.
 *          (in) connection_type	- type of connection between oscillators in the network.
 *          (in) initial_phases		- type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
void * create_sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int qcluster, const unsigned int connection_type, const unsigned int initial_phases) {
	return (void *) new sync_network(size, weight_factor, frequency_factor, qcluster, (conn_type) connection_type, (initial_type) initial_phases);
}


/***********************************************************************************************
 *
 * @brief   Simulate dynamic of the oscillatory Sync network.
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *          (in) steps				- number steps of simulations during simulation.
 *          (in) time				- time of simulation.
 *          (in) solver				- type of solution (solving).
 *          (in) collect_dynamic	- true - returns whole dynamic of oscillatory network, 
 *                                    otherwise returns only last values of dynamics.
 *
 * @return	Returns dynamic of simulation of the network.
 *
 ***********************************************************************************************/
dynamic_result * simulate_sync_network(const void * pointer_network, unsigned int steps, const double time, const unsigned int solver, const bool collect_dynamic) {
	sync_network * network = (sync_network *) pointer_network;

	std::vector< std::vector<sync_dynamic> * > * dynamic = network->simulate_static(steps, time, (solve_type) solver, collect_dynamic);

	dynamic_result * result = new dynamic_result();
	result->size_dynamic = dynamic->size();
	result->size_network = network->size();
	result->times = new double[result->size_dynamic];
	result->dynamic = new double * [result->size_dynamic];

	for (unsigned int index_dynamic = 0; index_dynamic < result->size_dynamic; index_dynamic++) {
		result->times[index_dynamic] = (*(*dynamic)[index_dynamic])[0].time;
		result->dynamic[index_dynamic] = new double[result->size_network];
		for (unsigned int index_neuron = 0; index_neuron < result->size_network; index_neuron++) {
			result->dynamic[index_dynamic][index_neuron] = (*(*dynamic)[index_dynamic])[index_neuron].phase;
		}

		delete (*dynamic)[index_dynamic];
		(*dynamic)[index_dynamic] = NULL;
	}
	
	delete dynamic;
	dynamic = NULL;

	return result;
}


/***********************************************************************************************
 *
 * @brief   Allocate clusters in line with ensembles of synchronous oscillators where each
 *          synchronous ensemble corresponds to only one cluster.
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *          (in) tolerance			- maximum error for allocation of synchronous ensemble 
 *                                    oscillators.
 *
 * @return	Returns ensembles of synchronous oscillators as clustering result.
 *
 ***********************************************************************************************/
clustering_result * allocate_sync_ensembles(const void * pointer_network, const double tolerance) {
	sync_network * network = (sync_network *) pointer_network;	

	const std::vector<std::vector<unsigned int> *> * const clusters = network->allocate_sync_ensembles(tolerance);
	clustering_result * result = create_clustering_result(clusters);

	return result;
}