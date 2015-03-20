#include "pcnn.h"

#include <unordered_set>

pcnn::pcnn(const unsigned int size, const conn_type connection_type, const pcnn_parameters & parameters) :
	oscillators(size), 
	network(size, connection_type)
{
	params = parameters;
}

pcnn::~pcnn() { }

pcnn_dynamic * pcnn::simulate_static(const unsigned int steps, const std::vector<double> & stimulus) {
	pcnn_dynamic * dynamic = new pcnn_dynamic(num_osc, steps);

	for (unsigned int i = 0; i < steps; i++) {
		calculate_states(stimulus);
		store_dynamic(dynamic, i);
	}

	return dynamic;
}

void pcnn::calculate_states(const std::vector<double> & stimulus) {
	std::vector<double> feeding(num_osc, 0.0);
	std::vector<double> linking(num_osc, 0.0);
	std::vector<double> outputs(num_osc, 0.0);
	std::vector<double> threshold(num_osc, 0.0);

	bool output_change = false;

	for (unsigned int index = 0; index < num_osc; index++) {
		pcnn_oscillator & current_oscillator = oscillators[index];
		std::vector<unsigned int> * neighbors = get_neighbors(index);

		double feeding_influence = 0.0;
		double linking_influence = 0.0;

		for (std::vector<unsigned int>::const_iterator iter = neighbors->begin(); iter != neighbors->end(); iter++) {
			const double output_neighbor = oscillators[(*iter)].output;

			feeding_influence += output_neighbor * params.M;
			linking_influence += output_neighbor * params.W;
		}

		delete neighbors;

		feeding_influence *= params.VF;
		linking_influence *= params.VL;

		feeding[index] = params.AF * current_oscillator.feeding + stimulus[index] + feeding_influence;
		linking[index] = params.AL * current_oscillator.linking + linking_influence;

		/* calculate internal activity */
		double internal_activity = feeding[index] * (1.0 + params.B * linking[index]);

		/* calculate output of the oscillator */
		if (internal_activity > current_oscillator.threshold) {
			outputs[index] = OUTPUT_ACTIVE_STATE;
		}
		else {
			outputs[index] = OUTPUT_INACTIVE_STATE;
		}

		if (outputs[index] != current_oscillator.output) {
			output_change = true;
		}
	}

	/* fast linking */
	if ( (params.FAST_LINKING) && (output_change) ) {
		fast_linking(feeding, linking, outputs);
	}

	/* update states of oscillators */
	for (unsigned int index = 0; index < size(); index++) {
		pcnn_oscillator & oscillator = oscillators[index];

		oscillator.feeding = feeding[index];
		oscillator.linking = linking[index];
		oscillator.output = outputs[index];
		oscillator.threshold = params.AT * oscillator.threshold + params.VT * outputs[index];
	}
}

void pcnn::fast_linking(const std::vector<double> & feeding, std::vector<double> & linking, std::vector<double> & output) {
	std::vector<double> previous_outputs(output.begin(), output.end());
	
	bool previous_output_change = false;
	bool current_output_change = false;
	
	while (previous_output_change) {
		for (unsigned int index = 0; index < num_osc; index++) {
			pcnn_oscillator & current_oscillator = oscillators[index];
			std::vector<unsigned int> * neighbors = get_neighbors(index);

			double linking_influence = 0.0;

			for (std::vector<unsigned int>::const_iterator iter = neighbors->begin(); iter != neighbors->end(); iter++) {
				linking_influence += previous_outputs[(*iter)] * params.W;
			}

			delete neighbors;

			linking_influence *= params.VL;
			linking[index] = linking_influence;

			double internal_activity = feeding[index] * (1.0 + params.B * linking[index]);
			if (internal_activity > current_oscillator.threshold) {
				output[index] = OUTPUT_ACTIVE_STATE;
			}
			else {
				output[index] = OUTPUT_INACTIVE_STATE;
			}

			if (output[index] != current_oscillator.output) {
				current_output_change = true;
			}
		}

		previous_output_change = current_output_change;
		current_output_change = false;

		/* check for changes for avoiding useless operation copy */
		if (current_output_change) {
			std::copy(output.begin(), output.end(), previous_outputs.begin());
		}
	}
}

void pcnn::store_dynamic(pcnn_dynamic * const dynamic, const unsigned int step) {
	for (unsigned int index = 0; index < num_osc; index++) {
		dynamic->dynamic[step][index] = oscillators[index].output;
	}
}


pcnn_dynamic::pcnn_dynamic() { }

pcnn_dynamic::~pcnn_dynamic() { }

pcnn_dynamic::pcnn_dynamic(const unsigned int number_oscillators, const unsigned int simulation_steps) : 
	dynamic(simulation_steps, std::vector<double>(number_oscillators, 0)) { }

std::vector< std::vector<unsigned int> * > * pcnn_dynamic::allocate_sync_ensembles(void) const {
	std::vector< std::vector<unsigned int> * > * sync_ensembles = new std::vector< std::vector<unsigned int> * >();

	std::unordered_set<unsigned int> traverse_oscillators;
	traverse_oscillators.reserve(dynamic.size());

	const unsigned int number_oscillators = dynamic[0].size();

	for (unsigned int t = (dynamic.size() - 1); t != 0; t--) {
		std::vector<unsigned int> * sync_ensemble = new std::vector<unsigned int>();
		
		for (unsigned int i = 0; i < number_oscillators; i++) {
			if (dynamic[t][i] == OUTPUT_ACTIVE_STATE) {
				if (traverse_oscillators.find(i) != traverse_oscillators.end()) {
					sync_ensemble->push_back(i);
					traverse_oscillators.insert(i);
				}
			}
		}

		if (!sync_ensembles->empty()) {
			sync_ensembles->push_back(sync_ensemble);
		}
		else {
			delete sync_ensemble;
		}
	}

	return sync_ensembles;
}

std::vector< std::vector<unsigned int> * > * pcnn_dynamic::allocate_spike_ensembles(void) const {
	std::vector< std::vector<unsigned int> * > * sync_ensembles = new std::vector< std::vector<unsigned int> * >();

	const unsigned int number_oscillators = dynamic[0].size();

	for (unsigned int t = 0; t < dynamic.size(); t++) {
		std::vector<unsigned int> * sync_ensemble = new std::vector<unsigned int>();

		for (unsigned int i = 0; i < number_oscillators; i++) {
			if (dynamic[t][i] == OUTPUT_ACTIVE_STATE) {
				sync_ensemble->push_back(i);
			}
		}

		if (!sync_ensembles->empty()) {
			sync_ensembles->push_back(sync_ensemble);
		}
		else {
			delete sync_ensemble;
		}
	}

	return sync_ensembles;
}

std::vector<unsigned int> * pcnn_dynamic::allocate_time_signal(void) const {
	const unsigned int number_oscillators = dynamic[0].size();

	std::vector<unsigned int> * signal_vector = new std::vector<unsigned int>(number_oscillators, 0);

	for (unsigned int t = 0; t < dynamic.size(); t++) {
		for (unsigned int i = 0; i < number_oscillators; i++) {
			if (dynamic[t][i] == OUTPUT_ACTIVE_STATE) {
				(*signal_vector)[t]++;
			}
		}
	}

	return signal_vector;
}