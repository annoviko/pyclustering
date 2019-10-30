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


#include <unordered_set>

#include <pyclustering/definitions.hpp>

#include <pyclustering/cluster/center_initializer.hpp>
#include <pyclustering/cluster/cluster_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


class random_center_initializer : public center_initializer {
private:
    /**
     *
     * @brief Storage where indexes are stored.
     *
     */
    using index_storage = std::unordered_set<std::size_t>;

private:
    std::size_t             m_amount            = 0;

    mutable index_storage   m_available_indexes = { };

public:
    /**
     *
     * @brief Default constructor to create random center initializer.
     *
     */
    random_center_initializer() = default;

    /**
     *
     * @brief    Constructor of center initializer algorithm K-Means++.
     *
     * @param[in] p_amount: amount of centers that should initialized.
     *
     */
    explicit random_center_initializer(const std::size_t p_amount);

    /**
     *
     * @brief Default copy constructor to create random center initializer.
     *
     */
    random_center_initializer(const random_center_initializer & p_other) = default;

    /**
     *
     * @brief Default move constructor to create random center initializer.
     *
     */
    random_center_initializer(random_center_initializer && p_other) = default;

    /**
     *
     * @brief Default destructor to destroy random center initializer.
     *
     */
    ~random_center_initializer() = default;

public:
    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[out] p_centers: initialized centers for the specified data.
    *
    */
    void initialize(const dataset & p_data, dataset & p_centers) const override;

    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration for
    *           specific range of points.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[in]  p_indexes: point indexes from data that are defines which points should be considered
    *              during calculation process. If empty then all data points are considered.
    * @param[out] p_centers: initialized centers for the specified data.
    *
    */
    void initialize(const dataset & p_data, const index_sequence & p_indexes, dataset & p_centers) const override;

private:
    /**
    *
    * @brief    Creates random center and place it to specified storage.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[out] p_centers: storage where new center should be placed.
    *
    */
    void create_center(const dataset & p_data, dataset & p_centers) const;
};


}

}