/**************************************************************************************************************

Interface of the CCORE library that is used by pyclustering.

Based on article description:
 - S.Guha, R.Rastogi, K.Shim. CURE: An Efficient Clustering Algorithm for Large Databases. 1998.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

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

#include "dbscan.h"
#include "cure.h"
#include "hierarchical.h"
#include "hsyncnet.h"
#include "kmeans.h"
#include "rock.h"
#include "syncnet.h"
#include "xmeans.h"

#include "som.h"
#include "sync_network.h"

#include "support.h"
#include "interface_ccore.h"

/***********************************************************************************************
 *
 * @brief   Free clustering results that have been provided by CCORE to client.
 *
 * @param   (in) pointer            - pointer to clustering results.
 *
 ***********************************************************************************************/
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

/***********************************************************************************************
 *
 * @brief   Free dynamic that have been provided by CCORE to client.
 *
 * @param   (in) pointer            - pointer to dynamic.
 *
 ***********************************************************************************************/
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

/***********************************************************************************************
 *
 * @brief   Clustering algorithm DBSCAN returns allocated clusters and noise that are consisted
 *          from input data.
 *
 * @param   (in) sample				- input data for clustering.
 *          (in) radius				- connectivity radius between points, points may be connected
 *                                    if distance between them less then the radius.
 *          (in) minumum_neighbors	- minimum number of shared neighbors that is required for
 *                                    establish links between points.
 *
 * @return	Returns result of clustering - array of allocated clusters. The last cluster in the
 * 			array is noise.
 *
 ***********************************************************************************************/
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

/***********************************************************************************************
 *
 * @brief   Clustering algorithm CURE returns allocated clusters.
 *
 * @param   (in) sample				- input data for clustering.
 *          (in) number_clusters	- number of clusters that should be allocated.
 *          (in) number_repr_points	- number of representation points for each cluster.
 *          (in) compression        - coefficient defines level of shrinking of representation 
 *                                    points toward the mean of the new created cluster after 
 *                                    merging on each step.
 *
 * @return	Returns result of clustering - array of allocated clusters.
 *
 ***********************************************************************************************/
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

/***********************************************************************************************
 *
 * @brief   Clustering hierarchical algorithm returns allocated clusters.
 *
 * @param   (in) sample				- input data for clustering.
 *          (in) number_clusters	- number of cluster that should be allocated.
 *
 * @return	Returns result of clustering - array of allocated clusters.
 *
 ***********************************************************************************************/
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

/***********************************************************************************************
 *
 * @brief   Clustering algorithm K-Means returns allocated clusters.
 *
 * @param   (in) sample				- input data for clustering.
 *          (in) initial_centers	- initial coordinates of centers of clusters.
 *          (in) tolerance			- stop condition: if maximum value of change of centers of
 *                                    clusters is less than tolerance than algorithm will stop
 *                                    processing.
 *
 * @return	Returns result of clustering - array of allocated clusters.
 *
 ***********************************************************************************************/
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

/***********************************************************************************************
 *
 * @brief   Clustering algorithm ROCK returns allocated clusters.
 *
 * @param   (in) sample				- input data for clustering.
 *          (in) radius				- connectivity radius (similarity threshold).
 *          (in) number_clusters	- defines number of clusters that should be allocated from
 *          						  the input data set.
 *          (in) threshold			- value that defines degree of normalization that influences
 *                                    on choice of clusters for merging during processing.
 *
 * @return	Returns result of clustering - array of allocated clusters.
 *
 ***********************************************************************************************/
clustering_result * rock_algorithm(const data_representation * const sample, const double radius, const unsigned int number_clusters, const double threshold) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);

	rock * solver = new rock(dataset, radius, number_clusters, threshold);
	solver->process();

	clustering_result * result = create_clustering_result(solver->get_clusters());

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
}

/***********************************************************************************************
 *
 * @brief   Clustering algorithm X-Means returns allocated clusters.
 *
 * @param   (in) sample				- input data for clustering.
 *          (in) initial_centers	- initial coordinates of centers of clusters.
 *          (in) kmax               - maximum number of clusters that can be allocated.
 *          (in) tolerance			- stop condition for local parameter improvement.
 *
 * @return	Returns result of clustering - array of allocated clusters.
 *
 ***********************************************************************************************/
clustering_result * xmeans_algorithm(const data_representation * const sample, const data_representation * const initial_centers, const unsigned int kmax, const double tolerance) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);
	std::vector<std::vector<double> > * centers = read_sample(initial_centers);

	xmeans * solver = new xmeans(dataset, centers, kmax, tolerance);
	solver->process();

	clustering_result * result = create_clustering_result(solver->get_clusters());

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;
	delete centers; centers = NULL;

	return result;	
}

/***********************************************************************************************
 *
 * @brief   Create oscillatory network Sync that is based on Kuramoto model.
 *
 * @param   (in) size				- number of oscillators in the network.
 *          (in) weight_factor		- coupling strength of the links between oscillators.
 *          (in) frequency_factor	- multiplier of internal frequency of the oscillators.
 *          (in) connection_type	- type of connection between oscillators in the network.
 *          (in) initial_phases		- type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
void * create_sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int connection_type, const unsigned int initial_phases) {
	return (void *) new sync_network(size, weight_factor, frequency_factor, (conn_type) connection_type, (initial_type) initial_phases);
}

/***********************************************************************************************
 *
 * @brief   Destroy Sync network (calls destructor).
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *
 ***********************************************************************************************/
void destroy_sync_network(const void * pointer_network) {
	if (pointer_network != NULL) {
		delete (sync_network *) pointer_network;
	}
}

/***********************************************************************************************
 *
 * @brief   Simulate dynamic of the oscillatory Sync network.
 *
 * @param   (in) pointer_network        - pointer to the Sync network.
 *          (in) steps                  - number steps of simulations during simulation.
 *          (in) time                   - time of simulation.
 *          (in) solver	                - type of solution (solving).
 *          (in) collect_dynamic        - true - returns whole dynamic of oscillatory network, 
 *                                        otherwise returns only last values of dynamics.
 *
 * @return  Returns dynamic of simulation of the network.
 *
 ***********************************************************************************************/
dynamic_result * simulate_sync_network(const void * pointer_network, unsigned int steps, const double time, const unsigned int solver, const bool collect_dynamic) {
	sync_network * network = (sync_network *) pointer_network;

	std::vector< std::vector<sync_dynamic> * > * dynamic = network->simulate_static(steps, time, (solve_type) solver, collect_dynamic);
	dynamic_result * result = sync_network::convert_dynamic_representation(dynamic);

	for (std::vector< std::vector<sync_dynamic> * >::const_iterator iter = dynamic->begin(); iter != dynamic->end(); iter++) {
		delete (*iter);
	}

	delete dynamic;
	dynamic = NULL;

	return result;
}

/***********************************************************************************************
 *
 * @brief   Simulate dynamic of the oscillatory Sync network until stop condition is not reached.
 *
 * @param   (in) pointer_network        - pointer to the Sync network.
 *          (in) order                  - order of process synchronization, destributed 0..1.
 *          (in) solver                 - type of solution (solving).
 *          (in) collect_dynamic        - if true - returns whole dynamic of oscillatory network, 
 *                                        otherwise returns only last values of dynamics.
 *          (in) step                   - time step of one iteration of simulation.
 *          (in) step_int               - integration step, should be less than step.
 *          (in) threshold_changes      - additional stop condition that helps prevent infinite 
 *                                        simulation, defines limit of changes of oscillators between 
 *                                        current and previous steps.
 *
 * @return  Returns dynamic of simulation of the network.
 *
 ***********************************************************************************************/
dynamic_result * simulate_dynamic_sync_network(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic, const double step, const double step_int, const double threshold_changes) {
	sync_network * network = (sync_network *) pointer_network;
	
	std::vector< std::vector<sync_dynamic> * > * dynamic = network->simulate_dynamic(order, (solve_type) solver, collect_dynamic, step, step_int, threshold_changes);
	dynamic_result * result = sync_network::convert_dynamic_representation(dynamic);

	for (std::vector< std::vector<sync_dynamic> * >::const_iterator iter = dynamic->begin(); iter != dynamic->end(); iter++) {
		delete (*iter);
	}

	delete dynamic;
	dynamic = NULL;

	return result;
}

/***********************************************************************************************
 *
 * @brief   Allocate clusters of ensembles of synchronous oscillators where each
 *          synchronous ensemble corresponds to only one cluster for Sync network.
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *          (in) tolerance			- maximum error for allocation of synchronous ensemble 
 *                                    oscillators.
 *
 * @return	Returns ensembles of synchronous oscillators as clustering result.
 *
 ***********************************************************************************************/
clustering_result * allocate_sync_ensembles_sync_network(const void * pointer_network, const double tolerance) {
	sync_network * network = (sync_network *) pointer_network;	

	const std::vector<std::vector<unsigned int> *> * const clusters = network->allocate_sync_ensembles(tolerance);
	clustering_result * result = create_clustering_result(clusters);

	return result;
}

/***********************************************************************************************
 *
 * @brief   Returns level of global synchorization in the network.
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *
 * @return	Returns level of global synchorization in the network.
 *
 ***********************************************************************************************/
double sync_order(const void * pointer_network) {
	return ((sync_network *) pointer_network)->sync_order();
}

/***********************************************************************************************
 *
 * @brief   Returns level of local (partial) synchronization in the network.
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *
 * @return	Returns level of global synchorization in the network.
 *
 ***********************************************************************************************/
double sync_local_order(const void * pointer_network) {
	return ((sync_network *) pointer_network)->sync_local_order();
}

/***********************************************************************************************
 *
 * @brief   Create oscillatory network SyncNet for cluster analysis.
 *
 * @param   (in) sample                - input data for clustering.
 * @param   (in) connectivity_radius   - connectivity radius between points.
 * @param   (in) enable_conn_weight    - if True - enable mode when strength between oscillators 
 *                                       depends on distance between two oscillators. Otherwise
 *                                       all connection between oscillators have the same strength.
 * @param   (in) initial_phases        - type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
void * create_syncnet_network(const data_representation * const sample, const double connectivity_radius, const bool enable_conn_weight, const unsigned int initial_phases) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);	/* belongs to syncnet */
	return (void *) new syncnet(dataset, connectivity_radius, enable_conn_weight, (initial_type) initial_phases);
}

/***********************************************************************************************
 *
 * @brief   Destroy SyncNet (calls destructor).
 *
 * @param   (in) pointer_network      - pointer to SyncNet oscillatory network.
 *
 ***********************************************************************************************/
void destroy_syncnet_network(const void * pointer_network) {
	if (pointer_network != NULL) {
		delete (syncnet *) pointer_network;
	}
}

/***********************************************************************************************
 *
 * @brief   Simulate oscillatory network SYNC until clustering problem is not resolved.
 *
 * @param   (in) order             - order of synchronization that is used as indication for 
 *                                   stopping processing.
 * @param   (in) solver            - specified type of solving diff. equation. 
 * @param   (in) collect_dynamic   - specified requirement to collect whole dynamic of the network.
 *
 * @return  Return last values of simulation time and phases of oscillators as a tuple if 
 *          collect_dynamic is False, and whole dynamic if collect_dynamic is True.
 *
 ***********************************************************************************************/
dynamic_result * process_syncnet(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic) {
	syncnet * network = (syncnet *) pointer_network;
	
	std::vector< std::vector<sync_dynamic> * > * dynamic = network->process(order, (solve_type) solver, collect_dynamic);

	dynamic_result * result = sync_network::convert_dynamic_representation(dynamic);

	for (std::vector< std::vector<sync_dynamic> * >::const_iterator iter = dynamic->begin(); iter != dynamic->end(); iter++) {
		delete (*iter);
	}

	delete dynamic;
	dynamic = NULL;

	return result;
}

/***********************************************************************************************
 *
 * @brief   Allocate clusters of ensembles of synchronous oscillators where each
 *          synchronous ensemble corresponds to only one cluster for SYNC network.
 *
 * @param   (in) pointer_network	- pointer to the Sync network.
 *          (in) tolerance			- maximum error for allocation of synchronous ensemble 
 *                                    oscillators.
 *
 * @return	Returns ensembles of synchronous oscillators as clustering result.
 *
 ***********************************************************************************************/
clustering_result * get_clusters_syncnet(const void * pointer_network, const double tolerance) {
	syncnet * network = (syncnet *) pointer_network;	

	const std::vector<std::vector<unsigned int> *> * const clusters = network->allocate_sync_ensembles(tolerance);
	clustering_result * result = create_clustering_result(clusters);

	return result;
}

/***********************************************************************************************
 *
 * @brief   Create oscillatory network hierarchical SYNC for cluster analysis.
 *
 * @param   (in) sample                - input data for clustering.
 * @param   (in) number_clusters       - number of clusters that should be allocated.
 * @param   (in) initial_phases        - type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
void * create_hsyncnet(const data_representation * const sample, const unsigned int number_clusters, const unsigned int initial_phases) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);	/* belongs to hsyncnet */
	return (void *) new hsyncnet(dataset, number_clusters, (initial_type) initial_phases);
}

/***********************************************************************************************
 *
 * @brief   Destroy oscillatory network HSyncNet (calls destructor).
 *
 * @param   (in) pointer_network      - pointer to HSyncNet oscillatory network.
 *
 ***********************************************************************************************/
void destroy_hsyncnet_network(const void * pointer_network) {
	if (pointer_network != NULL) {
		delete (hsyncnet *) pointer_network;
	}
}

/***********************************************************************************************
 *
 * @brief   Simulate oscillatory network hierarchical SYNC until clustering problem is not resolved.
 *
 * @param   (in) order             - order of synchronization that is used as indication for 
 *                                   stopping processing.
 * @param   (in) solver            - specified type of solving diff. equation. 
 * @param   (in) collect_dynamic   - specified requirement to collect whole dynamic of the network.
 *
 * @return  Return last values of simulation time and phases of oscillators as a tuple if 
 *          collect_dynamic is False, and whole dynamic if collect_dynamic is True.
 *
 ***********************************************************************************************/
dynamic_result * process_hsyncnet(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic) {
	hsyncnet * network = (hsyncnet *) pointer_network;

	std::vector< std::vector<sync_dynamic> * > * dynamic = network->process(order, (solve_type) solver, collect_dynamic);

	dynamic_result * result = sync_network::convert_dynamic_representation(dynamic);

	for (std::vector< std::vector<sync_dynamic> * >::const_iterator iter = dynamic->begin(); iter != dynamic->end(); iter++) {
		delete (*iter);
	}

	delete dynamic;
	dynamic = NULL;

	return result;
}

void * som_create(const data_representation * const sample, const unsigned int num_rows, const unsigned int num_cols, const unsigned int num_epochs, const unsigned int type_conn, const unsigned int type_init) {
	std::vector<std::vector<double> > * dataset = read_sample(sample);
	return (void *) new som(dataset, num_rows, num_cols, num_epochs, (som_conn_type) type_conn, (som_init_type) type_init);
}

void som_destroy(const void * pointer) {
	if (pointer != NULL) {
		delete (som *) pointer;
	}
}

unsigned int som_train(const void * pointer, const bool autostop) {
	return ((som *) pointer)->train(autostop);
}

unsigned int som_simulate(const void * pointer, const data_representation * const pattern) {
	std::vector<std::vector<double> > * input_pattern = read_sample(pattern);
	return ((som *) pointer)->simulate( &(*input_pattern)[0] );
}

unsigned int som_get_winner_number(const void * pointer) {
	return ((som *) pointer)->get_winner_number();
}

unsigned int som_get_size(const void * pointer) {
	return ((som *) pointer)->get_size();
}


pyclustering_package * som_get_weights(const void * pointer) {
	std::vector<std::vector<double> * > * wieghts = (std::vector<std::vector<double> * > *) ((som *) pointer)->get_weights();
	pyclustering_package * package = create_package(wieghts);

	return package;
}

pyclustering_package * som_get_capture_objects(const void * pointer) {
	std::vector<std::vector<unsigned int> * > * capture_objects = (std::vector<std::vector<unsigned int> * > *) ((som *) pointer)->get_capture_objects();
	pyclustering_package * package = create_package(capture_objects);

	return package;
}

pyclustering_package * som_get_awards(const void * pointer) {
	std::vector<unsigned int> * awards = (std::vector<unsigned int> *) ((som *) pointer)->get_awards();
	pyclustering_package * package = create_package(awards);

	return package;
}

pyclustering_package * som_get_neighbors(const void * pointer) {
	pyclustering_package * package = NULL;

	std::vector<std::vector<unsigned int> * > * neighbors = (std::vector<std::vector<unsigned int> * > *) ((som *) pointer)->get_neighbors();
	if (neighbors != NULL) {
		package = create_package(neighbors);
	}

	return package;
}