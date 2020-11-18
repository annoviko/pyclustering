/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>

#include <pyclustering/cluster/cluster_data.hpp>
#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace clst {


/*!

@brief  A storage where Agglometative clustering results are stored.

*/
using agglomerative_data = cluster_data;


/*!

@class    agglomerative agglomerative.hpp pyclustering/cluster/agglomerative.hpp

@brief    Agglomerative algorithm implementation that is used bottom up approach for clustering.
@details  Agglomerative algorithm considers each data point (object) as a separate cluster at the beginning and
          step by step finds the best pair of clusters for merge until required amount of clusters is obtained.

Example of agglomerative algorithm where centroid link 'CENTROID_LINK' is used for clustering sample 'Simple01':
@code
    using namespace pyclustering;
    using namespace pyclustering::clst;

    int main() {
        // Read an input data 'Simple01' from text file.
        dataset data = read_data("Simple01.txt");

        // Create storage where the result is going to be stored.
        agglomerative_data result;

        // Create the algorithm and process the input data using centroid link.
        agglomerative(2, agglomerative::type_link::CENTROID_LINK).process(data, result);

        // Display allocated clusters.
        for (auto group : result.clusters()) {
            std::cout << "[ ";
            for (auto index : group) { std::cout << index << " "; }
            std::cout << "]";
        }

        return 0;
    }
@endcode

Example of 'Lsun' clustering by the algorithm where single link method is more suitable due to elongated clusters:
@code
    dataset data = read_data("Lsun.txt");

    agglomerative_data result;
    agglomerative(2, agglomerative::type_link::SINGLE_LINK).process(data, result);
@endcode

There is an illustration how various methods affect the clustering result:
@image html agglomerative_lsun_clustering_single_link.png

Implementation based on paper @cite book::algorithms_for_clustering_data.

*/
class agglomerative {
public:
    /*!

    @brief  Defines methods (how to define closest clusters) for Agglomerative clustering.

    */
    enum class type_link {
        SINGLE_LINK   = 0,  /**< Distance between the two nearest objects in clusters is considered as a link, so-called SLINK method (the single-link clustering method). */
        COMPLETE_LINK = 1,  /**< Distance between the farthest objects in clusters is considered as a link, so-called CLINK method (the complete-link clustering method). */
        AVERAGE_LINK  = 2,  /**< Average distance between objects in clusters is considered as a link. */
        CENTROID_LINK = 3   /**< Distance between centers of clusters is considered as a link. */
    };

private:
    size_t                  m_number_clusters;

    type_link               m_similarity;

    dataset                 m_centers;

    cluster_sequence        * m_ptr_clusters;

    const dataset           * m_ptr_data;

public:
    /*!
    
    @brief    Default constructor of the clustering algorithm.
    
    */
    agglomerative();

    /*!
    
    @brief    Constructor of clustering algorithm where algorithm parameters for processing are
              specified.
    
    @param[in] number_clusters: amount of clusters that should be allocated.
    @param[in] link: type of the linking method for clustering.
    
    */
    agglomerative(const size_t number_clusters, const type_link link);

    /*!
    
    @brief    Default destructor of the algorithm.
    
    */
    ~agglomerative() = default;

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]  p_data: an input data that should be clusted.
    @param[out] p_result: agglomerative clustering result of an input data.
    
    */
     void process(const dataset & p_data, agglomerative_data & p_result);

private:
    /*!
    
    @brief    Merges the most similar clusters in line with link type.
    
    */
    void merge_similar_clusters();

    /*!
    
    @brief    Merges the most similar clusters in line with average link type.
    
    */
    void merge_by_average_link();

    /*!
    
    @brief    Merges the most similar clusters in line with centroid link type.
    
    */
    void merge_by_centroid_link();

    /*!
    
    @brief    Merges the most similar clusters in line with complete link type.
    
    */
    void merge_by_complete_link();

    /*!
    
    @brief    Merges the most similar clusters in line with single link type.
    
    */
    void merge_by_signle_link();

    /*!
    
    @brief    Calculates new center.
    
    @param[in] cluster: cluster whose center should be calculated.
    @param[out] center: coordinates of the cluster center.
    
    */
    void calculate_center(const cluster & cluster, point & center) const;
};


}

}