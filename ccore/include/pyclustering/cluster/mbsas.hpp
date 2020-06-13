/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/

#pragma once


#include <pyclustering/cluster/bsas.hpp>
#include <pyclustering/cluster/mbsas_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/*!

@class    mbsas mbsas.hpp pyclustering/cluster/mbsas.hpp

@brief    Class represents MBSAS (Modified Basic Sequential Algorithmic Scheme).
@details  Interface of MBSAS algorithm is the same as for BSAS. This algorithm performs clustering in two steps.
           The first - is determination of amount of clusters. The second - is assignment of points that were not
           marked as a cluster representatives to clusters.

*/
class mbsas : public bsas {
public:
    /*!

    @brief    Default constructor of the clustering algorithm.

    */
    mbsas() = default;

    /*!

    @brief    Creates MBSAS algorithm using specified parameters.

    @param[in] p_amount: amount of clusters that should be allocated.
    @param[in] p_threshold: threshold of dissimilarity (maximum distance) between points.
    @param[in] p_metric: metric for distance calculation between points.

    */
    mbsas(const std::size_t p_amount,
          const double p_threshold,
          const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean());

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: clustering result of an input data.
    
    */
    void process(const dataset & p_data, mbsas_data & p_result);
};


}

}