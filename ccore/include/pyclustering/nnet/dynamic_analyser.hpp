/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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


#pragma once


#include <limits>
#include <memory>
#include <vector>

#include <pyclustering/container/ensemble_data.hpp>


using namespace pyclustering::container;


namespace pyclustering {

namespace nnet {


class spike {
public:
    using ptr = std::shared_ptr<spike>;

private:
    std::size_t    m_begin          = 0;
    std::size_t    m_duration       = 0;
    std::size_t    m_end            = 0;

public:
    spike() = default;

    spike(const std::size_t p_begin, const std::size_t p_end);

    spike(const spike & p_other) = default;

    spike(spike && p_other) = default;

public:
    std::size_t get_start() const;

    std::size_t get_duration() const;

    std::size_t get_stop() const;

    bool compare(const spike & p_other, const double p_tolerance) const;
};


class dynamic_analyser {
private:
    using spike_collection      = std::vector<spike>;

private:
    const static std::size_t  INVALID_ITERATION;
    const static std::size_t  DEFAULT_AMOUNT_SPIKES;
    const static double       DEFAULT_TOLERANCE;

private:
    double                    m_threshold     = -1;
    std::size_t               m_spikes        = DEFAULT_AMOUNT_SPIKES;
    double                    m_tolerance     = DEFAULT_TOLERANCE;

public:
    dynamic_analyser() = default;

    dynamic_analyser(const double p_threshold, const double p_tolerance = DEFAULT_TOLERANCE, const std::size_t p_spikes = DEFAULT_AMOUNT_SPIKES);

    template<class DynamicType, class EnsemblesType>
    void allocate_sync_ensembles(const DynamicType & p_dynamic, EnsemblesType & p_ensembles, typename EnsemblesType::value_type & p_dead) const;

private:
    template<class DynamicType>
    void extract_oscillations(const DynamicType & p_dynamic, std::vector<spike_collection> & p_oscillations) const;

    template<class DynamicType>
    void extract_spikes(const DynamicType & p_dynamic, const std::size_t p_index, spike_collection & p_spikes) const;

    template<class EnsemblesType>
    void extract_ensembles(const std::vector<spike_collection> & p_oscillations, EnsemblesType & p_ensembles, typename EnsemblesType::value_type & p_dead) const;

    template<class DynamicType>
    std::size_t find_spike_end(const DynamicType & p_dynamic, const std::size_t p_index, const std::size_t p_position) const;

    bool is_sync_spikes(const spike_collection & p_spikes1, const spike_collection & p_spikes2) const;
};



template<class DynamicType, class EnsemblesType>
void dynamic_analyser::allocate_sync_ensembles(const DynamicType & p_dynamic, EnsemblesType & p_ensembles, typename EnsemblesType::value_type & p_dead) const {
    std::vector<spike_collection> oscillations;
    extract_oscillations(p_dynamic, oscillations);
    extract_ensembles(oscillations, p_ensembles, p_dead);
}


template<class DynamicType>
void dynamic_analyser::extract_oscillations(const DynamicType & p_dynamic, std::vector<spike_collection> & p_oscillations) const {
    std::size_t amount_oscillators = p_dynamic[0].size();
    p_oscillations = std::vector<spike_collection>(amount_oscillators);

    /* extract marker spikes */
    for (std::size_t index_neuron = 0; index_neuron < amount_oscillators; index_neuron++) {
        extract_spikes(p_dynamic, index_neuron, p_oscillations[index_neuron]);
    }
}


template<class DynamicType>
void dynamic_analyser::extract_spikes(const DynamicType & p_dynamic, const std::size_t p_index, spike_collection & p_spikes) const {
    std::size_t position = p_dynamic.size() - 1;
    for (std::size_t cur_spike = 0; (cur_spike < m_spikes) && (position > 0); cur_spike++) {
        std::size_t stop = find_spike_end(p_dynamic, p_index, position);
        if (stop == INVALID_ITERATION) {
            return;
        }

        for (position = stop; (position > 0) && (p_dynamic[position][p_index] >= m_threshold); position--) { }
        if (p_dynamic[position][p_index] < m_threshold) {
            p_spikes.emplace_back(position, stop);
        }
    }
}


template<class DynamicType>
std::size_t dynamic_analyser::find_spike_end(const DynamicType & p_dynamic, const std::size_t p_index, const std::size_t p_position) const {
    std::size_t time_stop_simulation = p_position;
    bool spike_fired = false;

    if (p_dynamic[time_stop_simulation][p_index] >= m_threshold) {
        spike_fired = true;
    }

    /* if active state is detected, it means we don't have whole oscillatory period for the considered oscillator, should be skipped */
    if (spike_fired) {
        for (; (p_dynamic[time_stop_simulation][p_index] >= m_threshold) && (time_stop_simulation > 0); time_stop_simulation--) { }

        if (time_stop_simulation == 0) {
            return INVALID_ITERATION;
        }
    }

    for (; (p_dynamic[time_stop_simulation][p_index] < m_threshold) && (time_stop_simulation > 0); time_stop_simulation--) { }
    return (time_stop_simulation == 0) ? INVALID_ITERATION : time_stop_simulation;
}


template<class EnsemblesType>
void dynamic_analyser::extract_ensembles(const std::vector<spike_collection> & p_oscillations, EnsemblesType & p_ensembles, typename EnsemblesType::value_type & p_dead) const {
    if (p_oscillations.empty()) {
        return;
    }

    for (std::size_t index_neuron = 0; index_neuron < p_oscillations.size(); index_neuron++) {
        /* if oscillator does not have enough spikes than it's dead neuron */
        if (p_oscillations[index_neuron].size() < m_spikes) {
            p_dead.push_back(index_neuron);
            continue;
        }

        if (p_ensembles.empty()) {
            p_ensembles.push_back({ index_neuron });
            continue;
        }

        const spike_collection & neuron_spikes = p_oscillations[index_neuron];
        bool ensemble_found = false;

        for (auto & ensemble : p_ensembles) {
            const std::size_t anchour_neuron_index = ensemble[0];
            const spike_collection & ensemble_anchor_spikes = p_oscillations[anchour_neuron_index];

            if (is_sync_spikes(neuron_spikes, ensemble_anchor_spikes)) {
                ensemble.push_back(index_neuron);
                ensemble_found = true;

                break;
            }
        }

        if (!ensemble_found) {
            p_ensembles.push_back({ index_neuron });
        }
    }
}


}

}
