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


#pragma once


#include <limits>
#include <memory>
#include <vector>

#include "container/ensemble_data.hpp"


using namespace ccore::container;


namespace ccore {

namespace nnet {


class spike {
public:
    using ptr = std::shared_ptr<spike>;

private:
    std::size_t    m_begin;
    std::size_t    m_duration;
    std::size_t    m_end;

public:
    spike(void) = default;

    spike(const std::size_t m_begin, const std::size_t p_end);

    spike(const spike & p_other) = default;

    spike(spike && p_other) = default;

public:
    std::size_t get_start(void) const;

    std::size_t get_duration(void) const;

    std::size_t get_stop(void) const;
};


template<class DynamicType, class EnsembleType>
class basic_dynamic_analyser {
private:
    using spike_collection      = std::vector<spike>;

private:
    const static std::size_t  INVALID_ITERATION;
    const static std::size_t  DEFAULT_AMOUNT_SPIKES;
    const static double       DEFAULT_TOLERANCE_PERCENT;

private:
    double                    m_threshold     = -1;
    std::size_t               m_spikes        = DEFAULT_AMOUNT_SPIKES;
    double                    m_tolerance     = DEFAULT_TOLERANCE_PERCENT;

public:
    basic_dynamic_analyser(void) = default;

    basic_dynamic_analyser(const double p_threshold, const double p_tolerance, const std::size_t p_spikes = DEFAULT_AMOUNT_SPIKES);

    void allocate_sync_ensembles(const DynamicType & p_dynamic, EnsembleType & p_ensembles) const;

private:
    void extract_oscillations(const DynamicType & p_dynamic, std::vector<spike_collection> & p_oscillations) const;

    void extract_spikes(const DynamicType & p_dynamic, const std::size_t p_index, spike_collection & p_spikes) const;

    void extract_ensembles(const std::vector<spike_collection> & p_oscillations, EnsembleType & p_ensembles) const;

    std::size_t find_spike_end(const DynamicType & p_dynamic, const std::size_t p_index, const std::size_t p_position) const;
};


template<class DynamicType, class EnsembleType>
const std::size_t basic_dynamic_analyser<DynamicType, EnsembleType>::INVALID_ITERATION = std::numeric_limits<std::size_t>::max();


template<class DynamicType, class EnsembleType>
const std::size_t basic_dynamic_analyser<DynamicType, EnsembleType>::DEFAULT_AMOUNT_SPIKES = 1;


template<class DynamicType, class EnsembleType>
const double basic_dynamic_analyser<DynamicType, EnsembleType>::DEFAULT_TOLERANCE_PERCENT = 0.1;


template<class DynamicType, class EnsembleType>
basic_dynamic_analyser<DynamicType, EnsembleType>::basic_dynamic_analyser(const double p_threshold, const double p_tolerance, const std::size_t p_spikes) :
    m_threshold(p_threshold),
    m_spikes(p_spikes),
    m_tolerance(p_tolerance)
{ }


template<class DynamicType, class EnsembleType>
void basic_dynamic_analyser<DynamicType, EnsembleType>::allocate_sync_ensembles(const DynamicType & p_dynamic, EnsembleType & p_ensembles) const {
    std::vector<spike_collection> oscillations;
    extract_oscillations(p_dynamic, oscillations);
    extract_ensembles(oscillations, p_ensembles);
}


template<class DynamicType, class EnsembleType>
void basic_dynamic_analyser<DynamicType, EnsembleType>::extract_oscillations(const DynamicType & p_dynamic, std::vector<spike_collection> & p_oscillations) const {
    std::size_t amount_oscillators = p_dynamic[0].size();
    p_oscillations = std::vector<spike_collection>(amount_oscillators);

    /* extract marker spikes */
    for (std::size_t index_neuron = 0; index_neuron < amount_oscillators; index_neuron++) {
        extract_spikes(p_dynamic, index_neuron, p_oscillations[index_neuron]);
    }
}


template<class DynamicType, class EnsembleType>
void basic_dynamic_analyser<DynamicType, EnsembleType>::extract_spikes(const DynamicType & p_dynamic, const std::size_t p_index, spike_collection & p_spikes) const {
    spike_collection spikes = { };

    std::size_t position = p_dynamic[p_index].size() - 1;
    for (std::size_t cur_spike = 0; (cur_spike < m_spikes) && (position > 0); cur_spike++) {
        std::size_t stop = find_spike_end(p_dynamic, p_index, position);
        if (stop == INVALID_ITERATION) {
            return;
        }

        for (; (position > 0) && (p_dynamic[position][p_index] > m_threshold); position--) { }
        if (p_dynamic[position][p_index] < m_threshold) {
            spikes.emplace_back(position, stop);
        }
    }

    if (spikes.size() == m_spikes) {
        p_spikes = std::move(spikes);
    }
}


template<class DynamicType, class EnsembleType>
std::size_t basic_dynamic_analyser<DynamicType, EnsembleType>::find_spike_end(const DynamicType & p_dynamic, const std::size_t p_index, const std::size_t p_position) const {
    std::size_t time_stop_simulation = p_position;
    bool spike_fired = false;

    if (p_dynamic[time_stop_simulation][p_index] > m_threshold) {
        spike_fired = true;
    }

    /* if active state is detected, it means we don't have whole oscillatory period for the considered oscillator, should be skipped */
    if (spike_fired) {
        for (; (p_dynamic[time_stop_simulation][p_index] > m_threshold) && (time_stop_simulation > 0); time_stop_simulation--) { }

        if (time_stop_simulation == 0) {
            return INVALID_ITERATION;
        }
    }

    for (; (p_dynamic[time_stop_simulation][p_index] < m_threshold) && (time_stop_simulation > 0); time_stop_simulation--) { }
    return (time_stop_simulation == 0) ? INVALID_ITERATION : time_stop_simulation;
}


template<class DynamicType, class EnsembleType>
void basic_dynamic_analyser<DynamicType, EnsembleType>::extract_ensembles(const std::vector<spike_collection> & p_oscillations, EnsembleType & p_ensembles) const {

}


}

}