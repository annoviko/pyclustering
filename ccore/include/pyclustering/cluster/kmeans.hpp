/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <mutex>
#include <vector>

#include <pyclustering/cluster/kmeans_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {

/*!

@class    kmeans kmeans.hpp pyclustering/cluster/kmeans.hpp

@brief    Represents K-Means clustering algorithm for cluster analysis.
@details  The algorithm related to partitional class when input data is divided into groups.

*/
class kmeans {
public:
    const static double             DEFAULT_TOLERANCE;  /**< Default value of the tolerance stop condition: if maximum value of change of centers of clusters is less than tolerance then algorithm stops processing. */

    const static std::size_t        DEFAULT_ITERMAX;    /**< Default value of the step stop condition - maximum number of iterations that is used for clustering process. */

private:
    double                  m_tolerance             = DEFAULT_TOLERANCE;

    std::size_t             m_itermax               = DEFAULT_ITERMAX;

    dataset                 m_initial_centers       = { };

    kmeans_data             * m_ptr_result          = nullptr;      /* temporary pointer to output result */

    const dataset           * m_ptr_data            = nullptr;      /* used only during processing */

    const index_sequence    * m_ptr_indexes         = nullptr;      /* temporary pointer to indexes */

    distance_metric<point>  m_metric;

public:
    /*!
    
    @brief    Default constructor of clustering algorithm.
    
    */
    kmeans() = default;

    /*!
    
    @brief    Constructor of clustering algorithm where algorithm parameters for processing are
               specified.
    
    @param[in] p_initial_centers: initial centers that are used for processing.
    @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
                cluster centers is less than tolerance than algorithm will stop processing.
    @param[in] p_itermax: maximum number of iterations (by default kmeans::DEFAULT_ITERMAX).
    @param[in] p_metric: distance metric calculator for two points.
    
    */
    kmeans(const dataset & p_initial_centers, 
           const double p_tolerance = DEFAULT_TOLERANCE,
           const std::size_t p_itermax = DEFAULT_ITERMAX,
           const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean_square());

    /*!
    
    @brief    Default destructor of the algorithm.
    
    */
    ~kmeans() = default;

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]     p_data: input data for cluster analysis.
    @param[in,out] p_result: clustering result of an input data, it is also considered as an input argument to
                    where observer parameter can be set to collect changes of clusters and centers on each step of
                    processing.
    
    */
    void process(const dataset & p_data, kmeans_data & p_result);

    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]     p_data: input data for cluster analysis.
    @param[in]     p_indexes: specify indexes of objects in 'p_data' that should be used during clustering process.
    @param[in,out] p_result: clustering result of an input data, it is also considered as an input argument to
                    where observer parameter can be set to collect changes of clusters and centers on each step of
                    processing.
    
    */
    void process(const dataset & p_data, const index_sequence & p_indexes, kmeans_data & p_result);

private:
    void update_clusters(const dataset & p_centers, cluster_sequence & p_clusters);

    double update_centers(const cluster_sequence & clusters, dataset & centers);

    void assign_point_to_cluster(const std::size_t p_index_point, const dataset & p_centers, index_sequence & p_clusters);

    /*!
    
    @brief    Calculate new center for specified cluster.
    
    @param[in] p_cluster: cluster whose center should be calculated.
    @param[in,out] p_center: cluster's center that should calculated.
    
    @return Difference between old and new cluster's center.
    
    */
    double update_center(const cluster & p_cluster, point & p_center);

    /*!
    
    @brief    Calculates total within-cluster errors that is based on distance metric.
    
    */
    void calculate_total_wce();

    /*!
    
    @brief    Erases clusters that do not have any points.
    
    @param[in,out] p_clusters: clusters that should be analyzed and modified.
    
    */
    static void erase_empty_clusters(cluster_sequence & p_clusters);
};


}

}
