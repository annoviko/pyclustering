#include "pcnn.h"

#include <unordered_set>

pcnn::pcnn(const unsigned int size, const conn_type connection_type, const pcnn_parameters & parameters) :
	m_oscillators(size, pcnn_oscillator()), 
	network(size, connection_type)
{
	m_params = parameters;
}

pcnn::pcnn(const unsigned int size, const conn_type connection_type, const size_t height, const size_t width, const pcnn_parameters & parameters) :
m_oscillators(size, pcnn_oscillator()),
network(size, connection_type, height, width)
{
    m_params = parameters;
}

pcnn::~pcnn() { }

void pcnn::simulate(const unsigned int steps, const pcnn_stimulus & stimulus, pcnn_dynamic & output_dynamic) {
	output_dynamic.resize(steps, size());

	for (unsigned int i = 0; i < steps; i++) {
		calculate_states(stimulus);
		store_dynamic(i, output_dynamic);
	}
}

void pcnn::calculate_states(const pcnn_stimulus & stimulus) {
	std::vector<double> feeding(size(), 0.0);
	std::vector<double> linking(size(), 0.0);
	std::vector<double> outputs(size(), 0.0);

	for (unsigned int index = 0; index < size(); index++) {
		pcnn_oscillator & current_oscillator = m_oscillators[index];
		std::vector<size_t> neighbors;
		get_neighbors(index, neighbors);

		double feeding_influence = 0.0;
		double linking_influence = 0.0;

        for (std::vector<size_t>::const_iterator iter = neighbors.begin(); iter != neighbors.end(); iter++) {
			const double output_neighbor = m_oscillators[(*iter)].output;

			feeding_influence += output_neighbor * m_params.M;
			linking_influence += output_neighbor * m_params.W;
		}

		feeding_influence *= m_params.VF;
		linking_influence *= m_params.VL;

		feeding[index] = m_params.AF * current_oscillator.feeding + stimulus[index] + feeding_influence;
		linking[index] = m_params.AL * current_oscillator.linking + linking_influence;

		/* calculate internal activity */
		double internal_activity = feeding[index] * (1.0 + m_params.B * linking[index]);

		/* calculate output of the oscillator */
		if (internal_activity > current_oscillator.threshold) {
			outputs[index] = OUTPUT_ACTIVE_STATE;
		}
		else {
			outputs[index] = OUTPUT_INACTIVE_STATE;
		}
	}

	/* fast linking */
	if (m_params.FAST_LINKING) {
		fast_linking(feeding, linking, outputs);
	}

	/* update states of oscillators */
	for (unsigned int index = 0; index < size(); index++) {
		pcnn_oscillator & oscillator = m_oscillators[index];

		oscillator.feeding = feeding[index];
		oscillator.linking = linking[index];
		oscillator.output = outputs[index];
		oscillator.threshold = m_params.AT * oscillator.threshold + m_params.VT * outputs[index];
	}
}

void pcnn::fast_linking(const std::vector<double> & feeding, std::vector<double> & linking, std::vector<double> & output) {
	std::vector<double> previous_outputs(output.cbegin(), output.cend());
	
	bool previous_output_change = true;
	bool current_output_change = false;
	
	while (previous_output_change) {
		for (unsigned int index = 0; index < size(); index++) {
			pcnn_oscillator & current_oscillator = m_oscillators[index];

            std::vector<size_t> neighbors;
			get_neighbors(index, neighbors);

			double linking_influence = 0.0;

            for (std::vector<size_t>::const_iterator iter = neighbors.begin(); iter != neighbors.end(); iter++) {
				linking_influence += previous_outputs[(*iter)] * m_params.W;
			}

			linking_influence *= m_params.VL;
			linking[index] = linking_influence;

			double internal_activity = feeding[index] * (1.0 + m_params.B * linking[index]);
			if (internal_activity > current_oscillator.threshold) {
				output[index] = OUTPUT_ACTIVE_STATE;
			}
			else {
				output[index] = OUTPUT_INACTIVE_STATE;
			}

			if (output[index] != previous_outputs[index]) {
				current_output_change = true;
			}
		}

		/* check for changes for avoiding useless operation copy */
		if (current_output_change) {
			std::copy(output.begin(), output.end(), previous_outputs.begin());
		}

		previous_output_change = current_output_change;
		current_output_change = false;
	}
}

void pcnn::store_dynamic(const unsigned int step, pcnn_dynamic & dynamic) {
	pcnn_network_state & current_state = (pcnn_network_state &) dynamic[step];
	current_state.m_output.resize(size());

	current_state.m_time = step;
	for (size_t i = 0; i < m_oscillators.size(); i++) {
		current_state.m_output[i] = m_oscillators[i].output;
	}
}



pcnn_dynamic::pcnn_dynamic() { }

pcnn_dynamic::~pcnn_dynamic() { }

/* TODO: implementation */
pcnn_dynamic::pcnn_dynamic(const unsigned int number_oscillators, const unsigned int simulation_steps) { }

void pcnn_dynamic::allocate_sync_ensembles(ensemble_data<pcnn_ensemble> & ensembles) const {
	std::unordered_set<unsigned int> traverse_oscillators;
	traverse_oscillators.reserve(number_oscillators());

	for (const_reverse_iterator iter_state = crbegin(); iter_state != crend(); iter_state++) {
		pcnn_ensemble ensemble;
		const pcnn_network_state & state_network = (*iter_state);

		for (unsigned int i = 0; i < number_oscillators(); i++) {
			if (state_network.m_output[i] == OUTPUT_ACTIVE_STATE) {
				if (traverse_oscillators.find(i) == traverse_oscillators.end()) {
					ensemble.push_back(i);
					traverse_oscillators.insert(i);
				}
			}
		}

		if (!ensemble.empty()) {
			ensembles.push_back(ensemble);
		}
	}
}

void pcnn_dynamic::allocate_spike_ensembles(ensemble_data<pcnn_ensemble> & ensembles) const {
	for (const_iterator iter_state = cbegin(); iter_state != cend(); iter_state++) {
		pcnn_ensemble ensemble;
		const pcnn_network_state & state_network = (*iter_state);

		for (unsigned int i = 0; i < number_oscillators(); i++) {
			if (state_network.m_output[i] == OUTPUT_ACTIVE_STATE) {
				ensemble.push_back(i);
			}
		}

		if (!ensemble.empty()) {
			ensembles.push_back(ensemble);
		}
	}
}

void pcnn_dynamic::allocate_time_signal(pcnn_time_signal & time_signal) const {
	time_signal.resize(size());

	for (size_t t = 0; t < size(); t++) {
		const pcnn_network_state & state_network = (*this)[t];

		for (unsigned int i = 0; i < number_oscillators(); i++) {
			if (state_network.m_output[i] == OUTPUT_ACTIVE_STATE) {
				time_signal[t]++;
			}
		}
	}
}
