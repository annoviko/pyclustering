/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/cluster/fcm_data.hpp>


namespace pyclustering {

namespace clst {

/*!

@class      fcm fcm.hpp pyclustering/cluster/fcm.hpp

@brief      Class represents Fuzzy C-means (FCM) clustering algorithm.
@details    Fuzzy clustering is a form of clustering in which each data point can belong to more than one cluster.

Fuzzy C-Means algorithm uses two general formulas for cluster analysis. The first is to updated membership of each
point:
\f[w_{ij}=\frac{1}{\sum_{k=0}^{c}\left ( \frac{\left \| x_{i}-c_{j} \right \|}{\left \| x_{i}-c_{k} \right \|} \right )^{\frac{2}{m-1}}}\f]

The second formula is used to update centers in line with obtained centers:
\f[c_{k}=\frac{\sum_{i=0}^{N}w_{k}\left ( x_{i} \right )^{m}x_{i}}{\sum_{i=0}^{N}w_{k}\left ( x_{i} \right )^{m}}\f]

Fuzzy C-Means clustering results depend on initial centers. Algorithm K-Means++ can used for center initialization to improve
clustering quality.

Here is an example how to perform cluster analysis using Fuzzy C-Means algorithm:
@code
    int main() {
        // Read two-dimensional input data 'OldFaithful'.
        dataset data = read_data("OldFaithful.txt");

        // Prepare initial centers
        const std::size_t amount_clusters = 2;
        const std::size_t candidates = 5;

        dataset initial_centers;
        kmeans_plus_plus(amount_clusters, candidates).initialize(data, initial_centers);

        // Create and run FCM clustering algorithm.
        fcm_data result;
        fcm(initial_centers).process(data, result);

        // Obtain clustering results.
        const cluster_sequence & clusters = result.clusters();
        const dataset & centers = result.centers();
        const membership_sequence & membership = result.membership();

        // Display points which have membership probability less than 90%.
        std::cout << "Points that have membership probability less than 90%: ";
        for (std::size_t i = 0; i < membership.size(); i++) {
            if (membership[i][0] > 0.1 && membership[i][0] < 0.9) {
                std::cout << i << " ";
            }
        }
        std::cout << std::endl;

        return 0;
    }
@endcode

The next example shows how to perform image segmentation using Fuzzy C-Means algorithm:
@code
    // Read image (photo), for example, using OpenCV2 or any other library.
    dataset data = read_image("stpetersburg_admiral.jpg");

    // Prepare initial centers
    const std::size_t amount_segments = 3;
    const std::size_t candidates = kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE;

    dataset initial_centers;
    kmeans_plus_plus(amount_segments, candidates).initialize(data, initial_centers);

    // Create and run FCM clustering algorithm to extract color segments from the image.
    fcm_data result;
    fcm(initial_centers).process(data, result);
@endcode

@image html fcm_segmentation_stpetersburg.png "Image segmentation using Fuzzy C-Means algorithm."

Visualization has been done using Python version of pyclustering library.

*/
class fcm {
public:
    const static double             DEFAULT_TOLERANCE;          /**< Default value of the tolerance stop condition: if maximum value of change of centers of clusters is less than tolerance then algorithm stops processing. */

    const static std::size_t        DEFAULT_ITERMAX;            /**< Default value of the step stop condition - maximum number of iterations that is used for clustering process. */

    const static double             DEFAULT_HYPER_PARAMETER;    /**< Default value of hyper-parameter that controls how fuzzy the cluster will be. */

private:
    double          m_tolerance             = DEFAULT_TOLERANCE;

    std::size_t     m_itermax               = DEFAULT_ITERMAX;

    dataset         m_initial_centers       = { };

    double          m_degree                = 0.0;

    fcm_data        * m_ptr_result          = nullptr;      /* temporary pointer to output result */

    const dataset   * m_ptr_data            = nullptr;      /* used only during processing */

public:
    /*!
    
    @brief  Default constructor of FCM clustering algorithm.
    
    */
    fcm() = default;

    /*!
    
    @brief  Constructor of FCM clustering algorithm with specific parameters.

    @param[in] p_initial_centers: initial centers for clusters.
    @param[in] p_m: hyper-parameter that controls how fuzzy the cluster will be; the higher it is, the fuzzier the cluster will be in the end.
    @param[in] p_tolerance: stop condition value: if maximum value of change of centers of clusters is less 
                than tolerance then algorithm stops processing.
    @param[in] p_itermax: maximum number of iterations that is used for clustering process.
    
    */
    fcm(const dataset & p_initial_centers, 
        const double p_m = DEFAULT_HYPER_PARAMETER,
        const double p_tolerance = DEFAULT_TOLERANCE,
        const std::size_t p_itermax = DEFAULT_ITERMAX);

    /*!

    @brief  Default destructor of FCM clustering algorithm.

    */
    ~fcm() = default;

public:
    /*!

    @brief    Performs cluster analysis of an input data.

    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: FCM clustering result of an input data.

    */
    void process(const dataset & p_data, fcm_data & p_result);

private:
    void verify() const;

    double update_centers();

    double update_center(const std::size_t p_index);

    void update_membership();

    void update_point_membership(const std::size_t p_index);

    void extract_clusters(cluster_sequence & p_clusters);
};


}

}