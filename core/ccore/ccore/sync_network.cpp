#include "sync_network.h"
#include "support.h"

#include <iostream>
#include <cmath>
#include <random>
#include <complex>
#include <stdexcept>
#include <chrono>

/***********************************************************************************************
 *
 * @brief   Contructor of the oscillatory network SYNC based on Kuramoto model.
 *
 * @param   (in) size                - number of oscillators in the network.
 * @param   (in) weight_factor       - coupling strength of the links between oscillators.
 * @param   (in) frequency_factor    - multiplier of internal frequency of the oscillators.
 * @param   (in) qcluster            - number of clusters that should be allocated.
 * @param   (in) connection_type     - type of connection between oscillators in the network.
 * @param   (in) initial_phases      - type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
sync_network::sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int qcluster, const conn_type connection_type, const initial_type initial_phases) :
	network(size, connection_type) 
{
	num_osc = size;
	weight = weight_factor;

	cluster = qcluster;

	std::random_device			device;
	std::default_random_engine		generator(device());
	std::uniform_real_distribution<double>	phase_distribution(0.0, 2.0 * pi());
	std::uniform_real_distribution<double>	frequency_distribution(0.0, 1.0);
	
	oscillators = new std::vector<sync_oscillator>();
	for (unsigned int index = 0; index < size; index++) {
		sync_oscillator oscillator_context;

		switch(initial_phases) {
		case initial_type::RANDOM_GAUSSIAN:
			oscillator_context.phase = phase_distribution(generator);
			break;
		case initial_type::EQUIPARTITION:
			oscillator_context.phase = (2 * pi() / (size - 1) * index);
			break;
		default:
			throw std::runtime_error("Unknown type of initialization");
		}

		oscillator_context.frequency = frequency_distribution(generator) * frequency_factor;
		oscillators->push_back(oscillator_context);
	}

	sync_ensembles = NULL;
}

/***********************************************************************************************
 *
 * @brief   Default destructor.
 *
 ***********************************************************************************************/
sync_network::~sync_network() {
	if (oscillators != NULL) {
		delete oscillators;
		oscillators = NULL;
	}

	free_sync_ensembles();
}

/***********************************************************************************************
 *
 * @brief   Remove allocated clusters. Should be used when dynamic is changed (phases of
 *          oscillators are changed). Required for fast providing results of clustering.
 *
 ***********************************************************************************************/
void sync_network::free_sync_ensembles() {
	if (sync_ensembles != NULL) {
		for (std::vector< std::vector<unsigned int> * >::const_iterator iter = sync_ensembles->begin(); iter != sync_ensembles->end(); iter++) {
			if (*iter != NULL) {
				delete *iter;
			}
		}

		delete sync_ensembles;
		sync_ensembles = NULL;
	}
}

/***********************************************************************************************
 *
 * @brief   Calculates level of global synchorization in the network.
 *
 * @return  Return level of global synchorization in the network.
 *
 ***********************************************************************************************/
double sync_network::sync_order() const {
	double exp_amount = 0;
	double average_phase = 0;

	for (unsigned int index = 0; index < num_osc; index++) {
		exp_amount += std::exp( std::abs( std::complex<double>(0, 1) * (*oscillators)[index].phase ) );
		average_phase += (*oscillators)[index].phase;
	}

	exp_amount /= num_osc;
	average_phase = std::exp( std::abs( std::complex<double>(0, 1) * (average_phase / num_osc) ) );

	return std::abs(average_phase) / std::abs(exp_amount);
}

/***********************************************************************************************
 *
 * @brief   Calculates level of local (partial) synchorization in the network.
 *
 * @return  Return level of local (partial) synchorization in the network.
 *
 ***********************************************************************************************/
double sync_network::sync_local_order() const {
	double			exp_amount = 0.0;
	unsigned int	number_neighbors = 0;

	for (unsigned int i = 0; i < num_osc; i++) {
		for (unsigned int j = 0; j < num_osc; j++) {
			if (get_connection(i, j) > 0) {
				exp_amount += std::exp( -std::abs( (*oscillators)[j].phase - (*oscillators)[i].phase ) );
				number_neighbors++;
			}
		}
	}

	if (number_neighbors == 0) {
		number_neighbors = 1;
	}

	return exp_amount / (double) number_neighbors;
}

/***********************************************************************************************
 *
 * @brief   Adapter for solving differential equation for calculation of oscillator phase.
 *
 * @param   (in) t      - current value of phase.
 * @param   (in) teta   - time (can be ignored). 
 * @param   (in) argv   - pointer to the network 'argv[0]' and index of oscillator whose phase 
 *                        represented by argument teta 'argv[1]'.
 *
 * @return  Return new value of phase of oscillator that is specified in index 'argv[1]'.
 *
 ***********************************************************************************************/
double sync_network::adapter_phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	return ((sync_network *) argv[0])->phase_kuramoto(t, teta, argv);
}

/***********************************************************************************************
 *
 * @brief   Calculation of oscillator phase using Kuramoto model.
 *
 * @param   (in) t      - current value of phase.
 * @param   (in) teta   - time (can be ignored). 
 * @param   (in) argv   - index of oscillator whose phase represented by argument teta.
 *
 * @return  Return new value of phase of oscillator with index 'argv[1]'.
 *
 ***********************************************************************************************/
double sync_network::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	unsigned int index = *(unsigned int *) argv[1];
	double phase = 0;

	for (unsigned int k = 0; k < num_osc; k++) {
		if (get_connection(index, k) > 0) {
			phase += std::sin(cluster * ( (*oscillators)[k].phase - teta ) );
		}
	}

	phase = (*oscillators)[index].frequency + (phase * weight / num_osc);
	return phase;
}

/***********************************************************************************************
 *
 * @brief   Allocate clusters in line with ensembles of synchronous oscillators where each
 *          synchronous ensemble corresponds to only one cluster.
 *
 * @param   (in) tolerance   - maximum error for allocation of synchronous ensemble oscillators.
 *
 * @return  Return vectors synchronous oscillators.
 *
 ***********************************************************************************************/
std::vector< std::vector<unsigned int> * > * sync_network::allocate_sync_ensembles(const double tolerance) {	
	if (sync_ensembles == NULL) {
		sync_ensembles = new std::vector< std::vector<unsigned int> * >();
	}
	else {
		return sync_ensembles;
	}

	sync_ensembles->push_back(new std::vector<unsigned int> ());
	
	if (num_osc > 0) {
		(*sync_ensembles)[0]->push_back(0);
	}

	for (unsigned int i = 1; i < num_osc; i++) {
		bool cluster_allocated = false;

		std::vector< std::vector<unsigned int> * >::iterator last_sync_ensemble_element = sync_ensembles->end();
		for (std::vector< std::vector<unsigned int> * >::const_iterator cluster = sync_ensembles->begin(); cluster != last_sync_ensemble_element; cluster++) {

			std::vector<unsigned int>::iterator last_cluster_element = (*cluster)->end();
			for (std::vector<unsigned int>::const_iterator neuron_index = (*cluster)->begin(); neuron_index != last_cluster_element; neuron_index++) {
				if ( ( (*oscillators)[i].phase < ((*oscillators)[*neuron_index].phase + tolerance) ) && ( (*oscillators)[i].phase > ((*oscillators)[*neuron_index].phase - tolerance) ) ) {
					cluster_allocated = true;
					(*cluster)->push_back(i);

					break;
				}
			}

			if (cluster_allocated == true) {
				break;
			}
		}

		if (cluster_allocated == false) {
			std::vector<unsigned int> * allocated_cluster = new std::vector<unsigned int>();
			allocated_cluster->push_back(i);
			sync_ensembles->push_back(allocated_cluster);
		}
	}

	return sync_ensembles;
}

/***********************************************************************************************
 *
 * @brief   Performs static simulation of oscillatory network.
 *
 * @param   (in) steps             - number steps of simulations during simulation.
 * @param   (in) time              - time of simulation.
 * @param   (in) solver            - type of solver for simulation.
 * @param   (in) collect_dynamic   - if true - returns whole dynamic of oscillatory network, 
 *                                   otherwise returns only last values of dynamics.
 *
 * @return  Returns dynamic of oscillatory network. If argument 'collect_dynamic' = true, than it 
 *          returns dynamic for the whole simulation time, otherwise returns only last values 
 *          (last step of simulation) of dynamic.
 *
 ***********************************************************************************************/
std::vector< std::vector<sync_dynamic> * > * sync_network::simulate_static(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic) {
	free_sync_ensembles();

	std::vector< std::vector<sync_dynamic> * > * dynamic = new std::vector< std::vector<sync_dynamic> * >;

	const double step = time / (double) steps;
	const double int_step = step / 10.0;

	for (double cur_time = 0; cur_time < time; cur_time += step) {
		calculate_phases(solver, cur_time, step, int_step);

		store_dynamic(dynamic, cur_time, collect_dynamic);
	}

	return dynamic;
}

/***********************************************************************************************
 *
 * @brief   Performs dynamic simulation of oscillatory network until stop condition is not 
 *          reached. Stop condition is defined by input argument 'order'.
 *
 * @param   (in) order               - order of process synchronization, destributed 0..1.
 * @param   (in) solver              - type of solver for simulation.
 * @param   (in) collect_dynamic     - if true - returns whole dynamic of oscillatory network, 
 *                                     otherwise returns only last values of dynamics.
 * @param   (in) step                - time step of one iteration of simulation (can be ignored).
 * @param   (in) step_int            - integration step, should be less than step (can be ignored).
 * @param   (in) threshold_changes   - additional stop condition that helps prevent infinite 
 *                                     simulation, defines limit of changes of oscillators between 
 *                                     current and previous steps.
 *
 * @return  Returns dynamic of oscillatory network. If argument 'collect_dynamic' = true, than it 
 *          returns dynamic for the whole simulation time, otherwise returns only last values 
 *          (last step of simulation) of dynamic.
 *
 ***********************************************************************************************/
std::vector< std::vector<sync_dynamic> * > * sync_network::simulate_dynamic(const double order, const solve_type solver, const bool collect_dynamic, const double step, const double step_int, const double threshold_changes) {
	free_sync_ensembles();

	double previous_order = 0.0;
	double current_order = sync_local_order();

	std::vector< std::vector<sync_dynamic> * > * dynamic = new std::vector< std::vector<sync_dynamic> * >();

	for (double time_counter = 0; current_order < order; time_counter += step) {
		calculate_phases(solver, time_counter, step, step_int);

		store_dynamic(dynamic, time_counter, collect_dynamic);

		previous_order = current_order;
		current_order = sync_local_order();

		if (std::abs(current_order - previous_order) < threshold_changes) {
			std::cout << "Warning: sync_network::simulate_dynamic - simulation is aborted due to low level of convergence rate (order = " << current_order << ")." << std::endl;
			break;
		}
	}

	return dynamic;
}

/***********************************************************************************************
 *
 * @brief   Stores dynamic of oscillators. Type of saving depends on argument 'collect_dynamic', 
 *          if it's true - than new values are added to previous, otherwise new values rewrite 
 *          previous.
 *
 * @param   (in) dynamic             - dynamic of oscillators.
 * @param   (in) time                - type of solver for simulation.
 * @param   (in) collect_dynamic     - if true - added new values to previous, otherwise rewrites 
 *                                     previous values by new values of dynamics.
 *
 ***********************************************************************************************/
void sync_network::store_dynamic(std::vector< std::vector<sync_dynamic> * > * dynamic, const double time, const bool collect_dynamic) const {
	std::vector<sync_dynamic> * network_dynamic = new std::vector<sync_dynamic>();

	for (unsigned int index = 0; index < num_osc; index++) {
		sync_dynamic oscillator_dynamic;
		oscillator_dynamic.phase = (*oscillators)[index].phase;
		oscillator_dynamic.time = time;

		network_dynamic->push_back(oscillator_dynamic);
	}
	
	if (collect_dynamic == false) {
		dynamic->clear();
	}

	dynamic->push_back(network_dynamic);
}

/***********************************************************************************************
 *
 * @brief   Calculates new phases for oscillators in the network in line with current step.
 *
 * @param   (in) solver             - type solver of the differential equation.
 * @param   (in) t                  - time of simulation.
 * @param   (in) step               - step of solution at the end of which states of oscillators 
 *                                    should be calculated.
 * @param   (in) int_step           - step differentiation that is used for solving differential 
 *                                    equation (can be ignored in case of solvers when integration
 *                                    step is defined by solver itself).
 *
 ***********************************************************************************************/
void sync_network::calculate_phases(const solve_type solver, const double t, const double step, const double int_step) {
	std::vector<double> * next_phases = new std::vector<double> (num_osc, 0);
	std::vector<void *> argv(2, NULL);

	argv[0] = (void *) this;

	unsigned int number_int_steps = (unsigned int) (step / int_step);

	for (unsigned int index = 0; index < num_osc; index++) {
		argv[1] = (void *) &index;

		switch(solver) {
			case solve_type::FAST: {
				double result = (*oscillators)[index].phase + phase_kuramoto(t, (*oscillators)[index].phase, argv);
				(*next_phases)[index] = phase_normalization(result);
				break;
			}
			case solve_type::RK4: {
				std::vector<differential_result> * result = rk4(&sync_network::adapter_phase_kuramoto, (*oscillators)[index].phase, t, t + step, number_int_steps, false, argv);
				(*next_phases)[index] = phase_normalization( (*result)[0].value );

				delete result;
				break;
			}
			case solve_type::RKF45: {
				std::vector<differential_result> * result = rkf45(&sync_network::adapter_phase_kuramoto, (*oscillators)[index].phase, t, t + step, 0.00001, false, argv);
				(*next_phases)[index] = phase_normalization( (*result)[0].value );

				delete result;
				break;
			}
			default: {
				throw std::runtime_error("Unknown type of solver");
			}
		}
	}

	/* store result */
	for (unsigned int index = 0; index < num_osc; index++) {
		(*oscillators)[index].phase = (*next_phases)[index];
	}

	delete next_phases;
}

/***********************************************************************************************
 *
 * @brief   Normalization of phase of oscillator that should be placed between [0; 2 * pi].
 *
 * @param   (in) teta    - phase of oscillator.
 *
 * @return  Returns normalized phase.
 *
 ***********************************************************************************************/
double sync_network::phase_normalization(const double teta) {
	double norm_teta = teta;

	while ( (norm_teta > 2.0 * pi()) || (norm_teta < 0.0) ) {
		if (norm_teta > 2.0 * pi()) {
			norm_teta -= 2.0 * pi();
		}
		else {
			norm_teta += 2.0 * pi();
		}
	}

	return norm_teta;
}

/***********************************************************************************************
 *
 * @brief   Convert dynamic of the network to CCORE interface representation of dynamic. It
 *          creates new data block and it should deleted by user.
 *
 * @param   (in) dynamic    - dynamic of the network.
 *
 * @return  Returns dynamic in line with CCORE interface representation.
 *
 ***********************************************************************************************/
dynamic_result * sync_network::convert_dynamic_representation(std::vector< std::vector<sync_dynamic> * > * dynamic) {
	dynamic_result * result = new dynamic_result();

	result->size_dynamic = dynamic->size();
	result->size_network = ((*dynamic)[0])->size();
	result->times = new double[result->size_dynamic];
	result->dynamic = new double * [result->size_dynamic];

	for (unsigned int index_dynamic = 0; index_dynamic < result->size_dynamic; index_dynamic++) {
		result->times[index_dynamic] = (*(*dynamic)[index_dynamic])[0].time;
		result->dynamic[index_dynamic] = new double[result->size_network];
		for (unsigned int index_neuron = 0; index_neuron < result->size_network; index_neuron++) {
			result->dynamic[index_dynamic][index_neuron] = (*(*dynamic)[index_dynamic])[index_neuron].phase;
		}

	}

	return result;
}
