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


#include <cstddef>


namespace pyclustering {

namespace clst {


/**
 *
 * @brief Object description that used by OPTICS algorithm for cluster analysis.
 *
 */
struct optics_descriptor {
public:
    static const double NONE_DISTANCE;

public:
    std::size_t     m_index = -1;
    double          m_core_distance = 0;
    double          m_reachability_distance = 0;
    bool            m_processed = false;

public:
    /**
     *
     * @brief Default constructor to create optics object descriptor.
     *
     */
    optics_descriptor() = default;

    /**
     *
     * @brief Default copy constructor to create optics object descriptor.
     *
     */
    optics_descriptor(const optics_descriptor & p_other) = default;

    /**
     *
     * @brief Default move constructor to create optics object descriptor.
     *
     */
    optics_descriptor(optics_descriptor && p_other) = default;

    /**
     *
     * @brief Creates optics object descriptor using specified parameters.
     * @details Processing is always false after creating for any created optics descriptor.
     *
     * @param[in] p_index: index of optics object that corresponds to index of real object in dataset.
     * @param[in] p_core_distance: core distance of optics-object.
     * @param[in] p_reachability_distance: reachability distance of optics-object.
     *
     */
    optics_descriptor(const std::size_t p_index, const double p_core_distance, const double p_reachability_distance);

    /**
     *
     * @brief Default destructor to destroy optics object descriptor.
     *
     */
    ~optics_descriptor() = default;

public:
    /**
     *
     * @brief Clears core and reachability distances and processing flag (at the same time index is not reseted).
     *
     */
    void clear();
};



/**
 *
 * @brief Less comparator for object description that used by OPTICS algorithm for cluster analysis.
 *
 */
struct optics_pointer_descriptor_less {
    /**
     *
     * @brief Compare two OPTICS object using following rule: p_object1 < p_object2.
     *
     * @param[in] p_object1: left operand to compare.
     * @param[in] p_object2: right operand to compare.
     *
     * @return 'true' if left operand is less than right operand.
     *
     */
    bool operator()(const optics_descriptor * p_object1, const optics_descriptor * p_object2) const;
};


}

}