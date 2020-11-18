/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <cstddef>


namespace pyclustering {

namespace clst {


/*!

@class   optics_descriptor optics_descriptor.hpp pyclustering/cluster/optics_descriptor.hpp

@brief   Object description that used by OPTICS algorithm for cluster analysis.

*/
struct optics_descriptor {
public:
    static const double NONE_DISTANCE;              /**< Denotes if a distance value is not defined. */

public:
    std::size_t     m_index = -1;                   /**< Index of the object in the data set. */
    double          m_core_distance = 0;            /**< Core distance that is minimum distance to specified number of neighbors. */
    double          m_reachability_distance = 0;    /**< Reachability distance to this object. */
    bool            m_processed = false;            /**< Defines the object is processed -`true` if is current object has been already processed. */

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
     * @param[in] p_object1: the left operand to compare.
     * @param[in] p_object2: the right operand to compare.
     *
     * @return `true` if left operand is less than right operand.
     *
     */
    bool operator()(const optics_descriptor * p_object1, const optics_descriptor * p_object2) const;
};


}

}