/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <mutex>
#include <vector>

#include <pyclustering/cluster/gmeans_data.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/*!

@class    gmeans gmeans.hpp pyclustering/cluster/gmeans.hpp

@brief    Represents G-Means clustering algorithm for cluster analysis.
@details  The G-means algorithm starts with a small number of centers, and grows the number of centers.
           Each iteration of the G-Means algorithm splits into two those centers whose data appear not to come from a
           Gaussian distribution. G-means repeatedly makes decisions based on a statistical test for the data
           assigned to each center.

@image html gmeans_example_clustering.png "G-Means clustering results on most common data-sets."

Example #1. In this example, G-Means starts analysis from single cluster.
@code
    int main() {
        // Read two-dimensional input data 'Lsun'.
        dataset data = read_data("Lsun.txt");

        // Create and run G-Means clustering algorithm.
        // By default the algorithm starts search from a single cluster.
        gmeans_data result;
        gmeans().process(data, result);

        // Obtain clustering results.
        const cluster_sequence & clusters = result.clusters();
        const dataset & centers = result.centers();

        // Display results to console.
        for (std::size_t i = 0; i < clusters.size(); i++) {
            std::cout << "Cluster #" << i + 1 << std::endl;
            std::cout << " - Center: ";

            const auto & center = centers[i];
            for (const auto coordinate : center) {
                std::cout << coordinate << " ";
            }

            std::cout << std::endl;
            std::cout << "- Size: " << clusters[i].size() << std::endl << std::endl;
        }

        return 0;
    }
@endcode

Example #2. Sometimes G-Means may found local optimum. 'repeat' value can be used to increase probability to
find global optimum. Argument 'repeat' defines how many times K-Means clustering with K-Means++
initialization should be run to find optimal clusters.
@code
    // Create and run G-Means clustering algorithm.
    const std::size_t initial_k = 1;
    const double tolerance = gmeans::DEFAULT_TOLERANCE;
    const std::size_t repeat = 5;   // Repeat each iteration 5 time to find optimum.

    gmeans_data result;
    gmeans(initial_k, tolerance, repeat).process(data, result);
@endcode

Implementation based on the paper @cite inproceedings::cluster::gmeans::1.

*/
class gmeans {
private:
    using projection = std::vector<double>;

public:
    const static long long          IGNORE_KMAX;                /**< Defines value that means to ignore K maximum value. */

    const static std::size_t        DEFAULT_AMOUNT_CENTERS;     /**< Defaule value of amount of initial K - the value from that the search procedure is started. */

    const static double             DEFAULT_TOLERANCE;          /**< Default value of the tolerance (stop condition): if the maximum value of cluster changes is less than tolerance then the algorithm stops processing. */

    const static std::size_t        DEFAULT_REPEAT;             /**< Default value that defines how many times K-Means should be run to improve parameters. */

    const static std::size_t        DEFAULT_CANDIDATES;         /**< Default value of amount of candidates to consider by K-Means++ to initialize initial centers for K-Means on each iteration. */

private:
    std::size_t             m_amount                = DEFAULT_AMOUNT_CENTERS;

    double                  m_tolerance             = DEFAULT_TOLERANCE;

    std::size_t             m_repeat                = DEFAULT_REPEAT;

    long long               m_kmax                  = IGNORE_KMAX;

    long long               m_random_state          = RANDOM_STATE_CURRENT_TIME;

    gmeans_data             * m_ptr_result          = nullptr;      /* temporary pointer to output result */

    const dataset           * m_ptr_data            = nullptr;      /* used only during processing */

public:
    /*!
    
    @brief    Default constructor of G-Means clustering algorithm.
    
    */
    gmeans() = default;

    /*!
    
    @brief    Constructor of clustering algorithm where algorithm parameters for processing are
               specified.
    
    @param[in] p_k_initial: initial amount of centers.
    @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
                cluster centers is less than tolerance then algorithm stops processing.
    @param[in] p_repeat: how many times K-Means should be run to improve parameters (by default is 3),
                with larger `repeat` values suggesting higher probability of finding global optimum.
    @param[in] p_kmax: maximum amount of clusters that might be allocated. The argument is considered as a stop
                condition. When the maximum amount is reached then algorithm stops processing. By default the maximum
                amount of clusters is not restricted (`k_max` is `IGNORE_KMAX`).
    @param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).
    
    */
    gmeans(const std::size_t p_k_initial, 
           const double p_tolerance = DEFAULT_TOLERANCE,
           const std::size_t p_repeat = DEFAULT_REPEAT,
           const long long p_kmax = IGNORE_KMAX,
           const long long p_random_state = RANDOM_STATE_CURRENT_TIME);

    /*!
    
    @brief    Default destructor of G-Means algorithm.
    
    */
    ~gmeans() = default;

public:
    /*!
    
    @brief    Performs cluster analysis of an input data.
    
    @param[in]     p_data: input data for cluster analysis.
    @param[in,out] p_result: clustering result of an input data, it is also considered as an input argument to
                    where observer parameter can be set to collect changes of clusters and centers on each step of
                    processing.
    
    */
    void process(const dataset & p_data, gmeans_data & p_result);

private:
    bool is_run_condition() const;

    void search_optimal_parameters(const dataset & p_data, const std::size_t p_amount, cluster_sequence & p_clusters, dataset & p_centers) const;

    void statistical_optimization();

    void perform_clustering();

    void split_and_search_optimal(const cluster & p_cluster, dataset & p_centers) const;

    static bool is_null_hypothesis(const dataset & p_data, const point & p_center1, const point & p_center2);

    static std::size_t get_amount_candidates(const dataset & p_data);

    static projection calculate_projection(const dataset & p_data, const point & p_vector);
};


}

}
