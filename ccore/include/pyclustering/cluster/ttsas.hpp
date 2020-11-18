/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <unordered_set>

#include <pyclustering/cluster/bsas.hpp>
#include <pyclustering/cluster/ttsas_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/*!

@class    ttsas ttsas.hpp pyclustering/cluster/ttsas.hpp

@brief    Class represents TTSAS (Two-Threshold Sequential Algorithmic Scheme).
@details  Clustering results of BSAS and MBSAS are strongly dependent on the order in which the points in data.
           TTSAS helps to overcome this shortcoming by using two threshold parameters. The first - if the distance
           to the nearest cluster is less than the first threshold then point is assigned to the cluster. The
           second - if distance to the nearest cluster is greater than the second threshold then new cluster is
           allocated.

Code example of TTSAS usage:
@code
    #include <pyclustering/cluster/ttsas.hpp>

    #include <iostream>

    // ... `read_data` implementation to read sample ...

    int main() {
        // Read two-dimensional input data 'Simple03'.
        dataset data = read_data("Simple03.txt");

        // Prepare parameters for TTSAS algorithm.
        const double threshold1 = 1.0;
        const double threshold2 = 2.0;

        // Create TTSAS algorithm and perform cluster analysis.
        ttsas ttsas_instance = ttsas(threshold1, threshold2);
        ttsas_data clustering_result;
        ttsas_instance.process(data, clustering_result);

        // Obtain allocated clusters.
        const auto & clusters = clustering_result.clusters();

        // Print result.
        std::cout << "Amount of allocated clusters: " << clusters.size() << std::endl;

        return 0;
    }
@endcode

Implementation based on paper @cite book::pattern_recognition::2009.

*/
class ttsas : public bsas {
private:
    const dataset * m_data_ptr = nullptr;   /* temporary pointer to data - exists only during processing */

    double          m_threshold2 = 0.0;

    std::vector<bool>   m_skipped_objects = { };
    std::size_t         m_start;

public:
    /*!
    
    @brief  Default TTSAS constructor.
    
    */
    ttsas() = default;

    /*!

    @brief  TTSAS constructor with specific parameters.

    @param[in] p_threshold1: dissimilarity level (distance) between point and its closest cluster, if the distance is
                less than `threshold1` value then point is assigned to the cluster.
    @param[in] p_threshold2: dissimilarity level (distance) between point and its closest cluster, if the distance is
                greater than `threshold2` value then point is considered as a new cluster.
    @param[in] p_metric: metric that is used for distance calculation between two points.

    */
    ttsas(const double p_threshold1,
          const double p_threshold2,
          const distance_metric<point> & p_metric = distance_metric_factory<point>::euclidean());

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: TTSAS clustering result of an input data.
    
    */
    virtual void process(const dataset & p_data, ttsas_data & p_result) override;

private:
    void process_objects(const std::size_t p_changes);

    void process_skipped_object(const std::size_t p_index_point);

    void append_to_cluster(const std::size_t p_index_cluster, const std::size_t p_index_point, const point & p_point);

    void allocate_cluster(const std::size_t p_index_point, const point & p_point);
};


}

}