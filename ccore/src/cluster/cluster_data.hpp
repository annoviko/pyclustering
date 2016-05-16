/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef SRC_CLUSTER_CLUSTER_DATA_HPP_
#define SRC_CLUSTER_CLUSTER_DATA_HPP_


#include <vector>
#include <memory>


namespace cluster_analysis {


using noise = std::vector<size_t>;
using noise_ptr = std::shared_ptr<noise>;

using cluster = std::vector<size_t>;
using cluster_sequence = std::vector<cluster>;
using cluster_sequence_ptr = std::shared_ptr<cluster_sequence>;


/**
*
* @brief    Represents result of cluster analysis.
*
*/
class cluster_data {
protected:
    cluster_sequence_ptr    m_clusters;

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    cluster_data(void);

    /**
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    cluster_data(const cluster_data & p_other);

    /**
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    cluster_data(cluster_data && p_other);

    /**
    *
    * @brief    Default destructor that destroy clustering data.
    *
    */
    virtual ~cluster_data(void);

public:
    /**
    *
    * @brief    Returns direct access to encapsulated clusters.
    *
    */
    cluster_sequence_ptr clusters(void);

    /**
    *
    * @brief    Returns amount of clusters that is stored.
    *
    */
    size_t size(void) const;

public:
    /**
    *
    * @brief    Provides access to specified cluster.
    *
    * @param[in] p_index: index of specified cluster.
    *
    */
    cluster & operator[](const size_t p_index);

    /**
    *
    * @brief    Provides access to specified cluster.
    *
    * @param[in] p_index: index of specified cluster.
    *
    */
    const cluster & operator[](const size_t p_index) const;

    /**
    *
    * @brief    Set clustering data by copy it from another object.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    cluster_data & operator=(const cluster_data & p_other);

    /**
    *
    * @brief    Set clustering data by move it from another object.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    cluster_data & operator=(cluster_data && p_other);

    /**
    *
    * @brief    Compares clustering data.
    *
    * @param[in] p_other: another clustering data that is used for comparison.
    *
    * @return  Returns true if both objects have the same amount of clusters with the same elements.
    *
    */
    bool operator==(const cluster_data & p_other) const;

    /**
    *
    * @brief    Compares clustering data.
    *
    * @param[in] p_other: another clustering data that is used for comparison.
    *
    * @return  Returns true if both objects have are not the same.
    *
    */
    bool operator!=(const cluster_data & p_other) const;
};


}


#endif
