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