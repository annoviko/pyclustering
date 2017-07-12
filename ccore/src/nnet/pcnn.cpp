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

#include "nnet/pcnn.hpp"

#include <stdexcept>
#include <unordered_set>

#include "container/adjacency_bit_matrix.hpp"
#include "container/adjacency_connector.hpp"
#include "container/adjacency_matrix.hpp"


const size_t pcnn::MAXIMUM_MATRIX_REPRESENTATION_SIZE = 4096;


pcnn::pcnn(void) : m_oscillators(0), m_connection(), m_params() { }


pcnn::pcnn(const size_t p_size, const connection_t p_structure, const pcnn_parameters & p_parameters) {
    initilize(p_size, p_structure, 0, 0, p_parameters);
}


pcnn::pcnn(const size_t p_size, const connection_t p_structure, const size_t p_height, const size_t p_width, const pcnn_parameters & p_parameters) {
    initilize(p_size, p_structure, p_height, p_width, p_parameters);
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

    if (stimulus.size() != size()) {
        throw std::out_of_range("pcnn::calculate_states: length of stimulus should be equal to amount of oscillators in the network.");
    }

    for (unsigned int index = 0; index < size(); index++) {
        pcnn_oscillator & current_oscillator = m_oscillators[index];
        std::vector<size_t> neighbors;
        m_connection->get_neighbors(index, neighbors);

        double feeding_influence = 0.0;
        double linking_influence = 0.0;

        for (auto & index : neighbors) {
            const double output_neighbor = m_oscillators[index].output;

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
          m_connection->get_neighbors(index, neighbors);

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


void pcnn::initilize(const size_t p_size, const connection_t p_structure, const size_t p_height, const size_t p_width, const pcnn_parameters & p_parameters) {
    m_oscillators = std::vector<pcnn_oscillator>(p_size, pcnn_oscillator());
    
    if (p_size > MAXIMUM_MATRIX_REPRESENTATION_SIZE) {
        m_connection = std::shared_ptr<adjacency_collection>(new adjacency_bit_matrix(p_size));
    }
    else {
        m_connection = std::shared_ptr<adjacency_matrix>(new adjacency_matrix(p_size));
    }

    adjacency_connector<adjacency_collection> connector;

    if ((p_height != 0) && (p_width != 0)) {
        connector.create_grid_structure(p_structure, p_width, p_height, *m_connection);
    }
    else {
        connector.create_structure(p_structure, *m_connection);
    }

    m_params = p_parameters;
}



pcnn_dynamic::pcnn_dynamic() { }


pcnn_dynamic::~pcnn_dynamic() { }


/* TODO: implementation */
pcnn_dynamic::pcnn_dynamic(const unsigned int number_oscillators, const unsigned int simulation_steps) { }


void pcnn_dynamic::allocate_sync_ensembles(ensemble_data<pcnn_ensemble> & ensembles) const {
    std::unordered_set<unsigned int> traverse_oscillators;
    traverse_oscillators.reserve(oscillators());

    for (const_reverse_iterator iter_state = crbegin(); iter_state != crend(); iter_state++) {
        pcnn_ensemble ensemble;
        const pcnn_network_state & state_network = (*iter_state);

        for (unsigned int i = 0; i < oscillators(); i++) {
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

        for (unsigned int i = 0; i < oscillators(); i++) {
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

        for (unsigned int i = 0; i < oscillators(); i++) {
            if (state_network.m_output[i] == OUTPUT_ACTIVE_STATE) {
                time_signal[t]++;
            }
        }
    }
}
