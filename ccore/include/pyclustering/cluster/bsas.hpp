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


#include <pyclustering/cluster/bsas_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {

/*!

@class    bsas bsas.hpp pyclustering/cluster/bsas.hpp

@brief    Class represents BSAS clustering algorithm - basic sequential algorithmic scheme.
@details  Algorithm has two mandatory parameters: maximum allowable number of clusters and threshold
           of dissimilarity or in other words maximum distance between points. Distance metric also can
           be specified using 'metric' parameters, by default 'Manhattan' distance is used.
           BSAS using following rule for updating cluster representative:

\f[
\vec{m}_{C_{k}}^{new}=\frac{ \left ( n_{C_{k}^{new}} - 1 \right )\vec{m}_{C_{k}}^{old} + \vec{x} }{n_{C_{k}^{new}}}
\f]

Clustering results of this algorithm depends on objects order in input data.

Example of cluster analysis using BSAS algorithm:
@code
    using namespace pyclustering;
    using namespace pyclustering::clst;

    int main() {
        dataset data = read_data("Simple02.txt");

        // Algorithm configuration: amount of clusters to allocate and threshold of dissimilarity.
        const std::size_t amount_clusters = 3;
        const double threshold = 1.0;

        // Create and run BSAS algorithm.
        bsas_data result;
        bsas(amount_clusters, threshold).process(data, result);

        // Extract clustering results: clusters and representative points.
        const cluster_sequence & clusters = result.clusters();
        const representative_sequence & representatives = result.representatives();

        // Display allocated clusters.
        for (const auto group : clusters) {
            for (const auto index : group) { std::cout << index << " "; }
            std::cout << std::endl;
        }

        return 0;
    }
@endcode

There is another one example where distance metric is specified:
@code
    // Create manhattan distance metric.
    auto metric = distance_metric_factory<point>::manhattan();

    // Create BSAS and run clustering algorithm using Manhattan distance.
    bsas_data result;
    bsas(amount_clusters, threshold, metric).process(data, result);
@endcode

Implementation based on paper @cite book::pattern_recognition::2009.

*/
class bsas {
protected:
    /*!

    @brief    Description of the nearest cluster to a point that is described by cluster index and distance from the cluster to the specified point.

    */
    struct nearest_cluster {
        std::size_t   m_index       = (std::size_t) -1;                     /**< Cluster index. */
        double        m_distance    = std::numeric_limits<double>::max();   /**< Distance between the cluster and a specific point. */
    };

protected:
    bsas_data       * m_result_ptr  = nullptr;  /**< Temporary pointer to clustering result that is used only during processing. */

    double          m_threshold     = 0.0;      /**< Threshold of dissimilarity (maximum distance) between points. */

    std::size_t     m_amount        = 0;        /**< Amount of clusters that should be allocated. */

    distance_metric<point>          m_metric;   /**< Metric for distance calculation between points. */

public:
    /*!

    @brief    Default constructor of the clustering algorithm.

    */
    bsas() = default;

    /*!

    @brief    Creates BSAS algorithm using specified parameters.

    @param[in] p_amount: amount of clusters that should be allocated.
    @param[in] p_threshold: threshold of dissimilarity (maximum distance) between points.
    @param[in] p_metric: metric for distance calculation between points.

    */
    bsas(const std::size_t p_amount,
         const double p_threshold,
         const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean());

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: clustering result of an input data.
    
    */
    virtual void process(const dataset & p_data, bsas_data & p_result);

protected:
    /*!

    @brief    Find nearest cluster to the specified point.

    @param[in] p_point: point for which nearest cluster is searched.

    @return   Description of nearest cluster that is defined by cluster index and distance to the point.

    */
    nearest_cluster find_nearest_cluster(const point & p_point) const;

    /*!

    @brief    Update cluster representative in line with new cluster size and added point to it.

    @param[in] p_index: index of cluster whose representative should be updated.
    @param[in] p_point: new point that was added to cluster.

    */
    void update_representative(const std::size_t p_index, const point & p_point);
};


}

}