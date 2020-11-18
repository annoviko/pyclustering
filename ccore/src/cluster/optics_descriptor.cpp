/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/optics_descriptor.hpp>

#include <limits>


namespace pyclustering {

namespace clst {


const double optics_descriptor::NONE_DISTANCE = -1.0;


optics_descriptor::optics_descriptor(const std::size_t p_index, const double p_core_distance, const double p_reachability_distance) :
    m_index(p_index),
    m_core_distance(p_core_distance),
    m_reachability_distance(p_reachability_distance),
    m_processed(false) 
{ }


void optics_descriptor::clear() {
    m_core_distance = optics_descriptor::NONE_DISTANCE;
    m_reachability_distance = optics_descriptor::NONE_DISTANCE;
    m_processed = false;
}


bool optics_pointer_descriptor_less::operator()(const optics_descriptor * p_object1, const optics_descriptor * p_object2) const {
    return p_object1->m_reachability_distance < p_object2->m_reachability_distance;
}


}

}