/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/cluster/cluster_data.hpp>
#include <pyclustering/cluster/data_type.hpp>
#include <pyclustering/cluster/silhouette_data.hpp>

#include <pyclustering/definitions.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/*!

@class  silhouette silhouette.hpp pyclustering/cluster/silhouette.hpp

@brief      Represents Silhouette method that is used interpretation and validation of consistency.
@details    The silhouette value is a measure of how similar an object is to its own cluster compared to other clusters.
             Be aware that silhouette method is applicable for K algorithm family, such as K-Means, K-Medians,
             K-Medoids, X-Means, etc., not not applicable for DBSCAN, OPTICS, CURE, etc. The Silhouette value is
             calculated using following formula:

            \f[s\left ( i \right )=\frac{ b\left ( i \right ) - a\left ( i \right ) }{ max\left \{ a\left ( i \right ), b\left ( i \right ) \right \}}\f]

            where \f$a\left ( i \right )\f$ - is average distance from object i to objects in its own cluster,
            \f$b\left ( i \right )\f$ - is average distance from object i to objects in the nearest cluster (the appropriate among other clusters).

Here is an example where Silhouette score is calculated for K-Means's clustering result:
@code
    #include <pyclustering/cluster/kmeans_plus_plus.hpp>
    #include <pyclustering/cluster/kmeans.hpp>
    #include <pyclustering/cluster/silhouette.hpp>

    #include <iostream>
    
    // ... `read_data` implementation to read sample ...

    int main() {
        // Read two-dimensional input data 'Simple03'.
        dataset data = read_data("Simple03.txt");

        // Prepare initial centers for K-Means algorithm.
        dataset initial_centers;

        const std::size_t amount_clusters = 4;
        const std::size_t candidates_to_consider = 5;
        kmeans_plus_plus(amount_clusters, candidates_to_consider).initialize(data, initial_centers);

        // Perform cluster analysis.
        auto kmeans_instance = kmeans(initial_centers);

        kmeans_data clustering_result;
        kmeans_instance.process(data, clustering_result);

        // Obtain allocated clusters.
        const auto & clusters = clustering_result.clusters();

        // Calculate Silhouette score.
        silhouette_data estimation_result;
        silhouette().process(data, clusters, estimation_result);

        // Print Silhouette score for each point.
        for (const auto score : estimation_result.get_score()) {
            std::cout << score << std::endl;
        }

        return 0;
    }
@endcode

Here is an illustration where clustering has been performed using various `K` values (2, 4, 6 and 8) for 
the same sample as before. `K = 4` is the optimal amount of clusters in line with Silhouette method because 
the score for each point is close to `1.0` and the average score for `K = 4` is biggest value among others `K`.

@image html silhouette_score_for_various_K.png "Fig. 1. Silhouette scores for various K."

Implementation based on paper @cite article::cluster::silhouette::1.

@see kmeans, kmedoids, kmedians, xmeans, elbow

*/
class silhouette {
private:
    const dataset *           m_data      = nullptr;  /* temporary object, exists during processing */
    const cluster_sequence *  m_clusters  = nullptr;  /* temporary object, exists during processing */
    silhouette_data *         m_result    = nullptr;  /* temporary object, exists during processing */

    data_t                    m_type      = data_t::POINTS;

    distance_metric<point>    m_metric    = distance_metric_factory<point>::euclidean_square();

public:
    /*!
    
    @brief  Default constructor for Silhouette method.
    
    */
    silhouette() = default;

    /*!

    @brief  Constructor for Silhouette method with specific parameters.

    @param[in] p_metric: metric that was used for cluster analysis and should be used for Silhouette
                score calculation (by default Square Euclidean distance).

    */
    explicit silhouette(const distance_metric<point> & p_metric);

    /*!

    @brief  Default copy constructor for Silhouette method.

    */
    silhouette(const silhouette & p_other) = default;

    /*!

    @brief  Default move constructor for Silhouette method.

    */
    silhouette(silhouette && p_other) = default;

    /*!

    @brief  Default destructor for Silhouette method.

    */
    ~silhouette() = default;

public:
    /*!

    @brief    Performs analysis of an input data in order to calculate score for each point where input data is represented by points.

    @param[in]  p_data: input data (points) for analysis.
    @param[in]  p_clusters: clusters that have been obtained after cluster analysis.
    @param[out] p_result: silhouette input data processing result.

    */
    void process(const dataset & p_data, const cluster_sequence & p_clusters, silhouette_data & p_result);

    /*!

    @brief    Performs analysis of an input data in order to calculate score for each point.

    @param[in]  p_data: input data for analysis.
    @param[in]  p_clusters: clusters that have been obtained after cluster analysis.
    @param[in]  p_type: data type of input sample `p_data` that is processed by the method (`POINTS`, `DISTANCE_MATRIX`).
    @param[out] p_result: silhouette input data processing result.

    */
    void process(const dataset & p_data, const cluster_sequence & p_clusters, const data_t & p_type, silhouette_data & p_result);

private:
    double calculate_score(const std::size_t p_index_point, const std::size_t p_index_cluster) const;

    void calculate_dataset_difference(const std::size_t p_index_point, std::vector<double> & p_dataset_difference) const;

    double calculate_cluster_difference(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;

    double calculate_within_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;

    double calculate_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;

    double caclulate_optimal_neighbor_cluster_score(const std::size_t p_index_cluster, const std::vector<double> & p_dataset_difference) const;
};


}

}