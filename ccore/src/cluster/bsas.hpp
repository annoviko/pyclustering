/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include "cluster/cluster_algorithm.hpp"
#include "cluster/bsas_data.hpp"

#include "utils/metric.hpp"


using namespace ccore::utils::metric;


namespace ccore {

namespace clst {


class bsas : public cluster_algorithm {
private:
    struct nearest_cluster {
        std::size_t   m_index       = (std::size_t) -1;
        double        m_distance    = std::numeric_limits<double>::max();
    };

private:
    bsas_data       * m_result_ptr  = nullptr; /* temporary pointer to clustering result that is used only during processing */

    double          m_threshold     = 0.0;

    std::size_t     m_amount        = 0;

    distance_metric<point>          m_metric;

public:
    bsas(void) = default;

    bsas(const std::size_t p_amount,
         const double p_threshold,
         const distance_metric<point> & p_metric = distance_metric_factory<point>::manhattan());

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result) override;

private:
    nearest_cluster find_nearest_cluster(const point & p_point) const;

    void update_representative(const std::size_t p_index, const point & p_point);
};


}

}