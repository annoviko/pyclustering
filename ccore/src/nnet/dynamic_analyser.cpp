/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/nnet/dynamic_analyser.hpp>

#include <sstream>
#include <stdexcept>

#include <pyclustering/utils/math.hpp>


using namespace pyclustering::utils::math;


namespace pyclustering {

namespace nnet {


spike::spike(const std::size_t p_begin, const std::size_t p_end) {
    if (p_end < p_begin) {
        std::stringstream stream;
        stream << __FUNCTION__ << ": End time '" << p_end << "' of the spike cannot be less or equal to begin time '" << p_begin << "'.";

        throw std::invalid_argument(stream.str());
    }

    m_begin = p_begin;
    m_duration = p_end - p_begin;
    m_end = p_end;
}


std::size_t spike::get_start() const {
    return m_begin;
}


std::size_t spike::get_duration() const {
    return m_duration;
}


std::size_t spike::get_stop() const {
    return m_end;
}


bool spike::compare(const spike & p_other, const double p_tolerance) const {
    const double delta = m_duration * p_tolerance;

    if (absolute_difference(p_other.get_duration(), get_duration()) > delta) {
        return false;
    }

    const double difference = (double) absolute_difference(p_other.get_start(), get_start()) + absolute_difference(p_other.get_stop(), get_stop());
    if (difference > delta) {
        return false;
    }

    return true;
}



const std::size_t dynamic_analyser::INVALID_ITERATION = std::numeric_limits<std::size_t>::max();

const std::size_t dynamic_analyser::DEFAULT_AMOUNT_SPIKES = 1;

const double dynamic_analyser::DEFAULT_TOLERANCE = 0.1;


dynamic_analyser::dynamic_analyser(const double p_threshold, const double p_tolerance, const std::size_t p_spikes) :
    m_threshold(p_threshold),
    m_spikes(p_spikes),
    m_tolerance(p_tolerance)
{ }


bool dynamic_analyser::is_sync_spikes(const spike_collection & p_spikes1, const spike_collection & p_spikes2) const {
    if (p_spikes1.size() != p_spikes2.size()) {
        return false;
    }

    for (std::size_t index_spike = 0; index_spike < p_spikes1.size(); index_spike++) {
        auto & spike1 = p_spikes1[index_spike];
        auto & spike2 = p_spikes2[index_spike];

        if (!spike1.compare(spike2, m_tolerance)) {
            return false;
        }
    }

    return true;
}


}

}