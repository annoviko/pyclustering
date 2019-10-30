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

#include <pyclustering/cluster/bsas.hpp>
#include <pyclustering/cluster/ttsas_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


class ttsas : public bsas {
private:
    const dataset * m_data_ptr = nullptr;   /* temporary pointer to data - exists only during processing */

    double          m_threshold2 = 0.0;

    std::vector<bool>   m_skipped_objects = { };
    std::size_t         m_start;

public:
    ttsas() = default;

    ttsas(const double p_threshold1,
          const double p_threshold2,
          const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean());

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
    void process_objects(const std::size_t p_changes);

    void process_skipped_object(const std::size_t p_index_point);

    void append_to_cluster(const std::size_t p_index_cluster, const std::size_t p_index_point, const point & p_point);

    void allocate_cluster(const std::size_t p_index_point, const point & p_point);
};


}

}