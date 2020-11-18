/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/cluster/elbow_data.hpp>
#include <pyclustering/cluster/kmeans.hpp>
#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include <pyclustering/parallel/parallel.hpp>

#include <pyclustering/utils/metric.hpp>

#include <pyclustering/definitions.hpp>


using namespace pyclustering::parallel;
using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


/*!

@class    elbow elbow.hpp pyclustering/cluster/elbow.hpp

@brief    The elbow is a heuristic method to find the appropriate number of clusters in a dataset.
@details  The elbow is a heuristic method of interpretation and validation of consistency within cluster analysis designed to help find the appropriate 
           number of clusters in a dataset. Elbow method performs clustering using K-Means algorithm for each K and estimate clustering results using
           sum of square erros. By default K-Means++ algorithm is used to calculate initial centers that are used by K-Means algorithm.

The Elbow is determined by max distance from each point (x, y) to segment from kmin-point (x0, y0) to kmax-point (x1, y1),
where 'x' is K (amount of clusters), and 'y' is within-cluster error. Following expression is used to calculate Elbow
length:
\f[Elbow_{k} = \frac{\left ( y_{0} - y_{1} \right )x_{k} + \left ( x_{1} - x_{0} \right )y_{k} + \left ( x_{0}y_{1} - x_{1}y_{0} \right )}{\sqrt{\left ( x_{1} - x_{0} \right )^{2} + \left ( y_{1} - y_{0} \right )^{2}}}\f]

Usage example of Elbow method for cluster analysis:
@code
    #include <pyclustering/cluster/elbow.hpp>
    #include <pyclustering/cluster/kmeans.hpp>
    #include <pyclustering/cluster/kmeans_plus_plus.hpp>

    #include <fstream>
    #include <iostream>

    using namespace pyclustering;
    using namespace pyclustering::clst;

    int main() {
        // Read two-dimensional input data 'Simple03'.
        dataset data = read_data("Simple03.txt");   // See an example of the implementation below.

        // Prepare methods's parameters.
        const std::size_t kmin = 1;   // minimum amount of clusters that should be considered
        const std::size_t kmax = 10;  // maximum amount of clusters

        // Create Elbow method for processing.
        elbow<> elbow_instance = elbow<>(kmin, kmax);

        // Run Elbow method to get optimal amount of clusters.
        elbow_data result;
        elbow_instance.process(data, result);

        // Obtain results.
        const std::size_t amount_clusters = result.get_amount();
        const wce_sequence & wce = result.get_wce();    // total within-cluster errors for each K.

        // Perform cluster analysis using K-Means algorithm.
        // Prepare initial centers before running K-Means algorithm.
        dataset initial_centers;
        kmeans_plus_plus(amount_clusters, 5).initialize(data, initial_centers);

        // Create K-Means algorithm and run it.
        kmeans_data clustering_result;
        kmeans(initial_centers).process(data, clustering_result);

        // Obtain clustering results.
        const cluster_sequence & clusters = clustering_result.clusters();
        const dataset & centers = clustering_result.centers();

        // Print results to console.
        for (std::size_t i = 0; i < clusters.size(); i++) {
            std::cout << "Cluster #" << i + 1 << " with center at ( ";

            const point & center = centers[i];
            for (const auto coordinate : center) {
                std::cout << coordinate << " ";
            }

            std::cout << " ): ";

            const cluster & group = clusters[i];
            for (const auto index : group) {
                std::cout << index << " ";
            }

            std::cout << std::endl;
        }

        return 0;
    }
@endcode

Here is an example how to read input data from simple text file:
@code
    dataset read_data(const std::string & filename) {
        dataset data;
        std::ifstream file(filename);
        std::string line;

        while (std::getline(file, line)) {
            std::stringstream stream(line);
            point coordinates;
            double value = 0.0;

            while (stream >> value) { coordinates.push_back(value); }
            data.push_back(coordinates);
        }

        file.close();
        return data;
    }
@endcode

By default Elbow uses K-Means++ initializer to calculate initial centers for K-Means algorithm, it can be changed
using argument 'initializer':
@code
    // Prepare methods's parameters.
    const std::size_t kmin = 1;   // minimum amount of clusters that should be considered
    const std::size_t kmax = 10;  // maximum amount of clusters

    // Create and run Elbow method to get optimal amount of clusters using random center initializer.
    elbow_data result;
    elbow<random_center_initializer>(kmin, kmax).process(data, result);
@endcode

@image html elbow_example_simple_03.png "Elbows analysis with further K-Means clustering."

Implementation based on paper @cite article::cluster::elbow::1.

*/
template <class TypeInitializer = kmeans_plus_plus>
class elbow {
private:
    std::size_t   m_kmin         = 0;
    std::size_t   m_kmax         = 0;
    std::size_t   m_kstep        = 0;
    std::size_t   m_kamount      = 0;
    long long     m_random_state = RANDOM_STATE_CURRENT_TIME;

    std::vector<double> m_elbow  = { };

    const dataset * m_data       = nullptr;
    elbow_data    * m_result     = nullptr;      /* temporary pointer to output result   */

public:
    /*!
    
    @brief  Default constructor of Elbow method.
    
    */
    elbow() = default;

    /*!
    
    @brief  Elbow method constructor with parameters of the method.
    
    @param[in] p_kmin: minimum amount of clusters that should be considered.
    @param[in] p_kmax: maximum amount of clusters that should be considered.

    */
    elbow(const std::size_t p_kmin, const std::size_t p_kmax) :
        elbow(p_kmin, p_kmax, 1, RANDOM_STATE_CURRENT_TIME)
    { }

    /*!

    @brief  Elbow method constructor with parameters of the method.

    @param[in] p_kmin: minimum amount of clusters that should be considered.
    @param[in] p_kmax: maximum amount of clusters that should be considered.
    @param[in] p_kstep: search step in the interval [kmin, kmax].

    */
    elbow(const std::size_t p_kmin, const std::size_t p_kmax, const std::size_t p_kstep) :
        elbow(p_kmin, p_kmax, p_kstep, RANDOM_STATE_CURRENT_TIME)
    { }

    /*!

    @brief  Elbow method constructor with parameters of the method.

    @param[in] p_kmin: minimum amount of clusters that should be considered.
    @param[in] p_kmax: maximum amount of clusters that should be considered.
    @param[in] p_kstep: search step in the interval [kmin, kmax].
    @param[in] p_random_state: seed for random state.

    */
    elbow(const std::size_t p_kmin, const std::size_t p_kmax, const std::size_t p_kstep, const long long p_random_state) :
        m_kmin(p_kmin),
        m_kmax(p_kmax),
        m_kstep(p_kstep),
        m_kamount((m_kmax - m_kmin) / m_kstep + 1),
        m_random_state(p_random_state)
    {
        verify();
    }

    /*!

    @brief  Copy constructor of Elbow method.

    */
    elbow(const elbow & p_other) = default;

    /*!

    @brief  Move constructor of Elbow method.

    */
    elbow(elbow && p_other) = default;

    /*!

    @brief  Destructor of Elbow method.

    */
    ~elbow() = default;

public:
    /*!

    @brief    Performs cluster analysis of an input data.

    @param[in]  p_data: an input data that should be clusted.
    @param[out] p_result: elbow input data processing result.

    */
    void process(const dataset & p_data, elbow_data & p_result) {
        if (p_data.size() < m_kmax) {
            throw std::invalid_argument("K max value '" + std::to_string(m_kmax) 
              + "' is greater than amount of data points '" + std::to_string(p_data.size()) + "'.");
        }

        m_data   = &p_data;
        m_result = &p_result;

        m_result->get_wce().resize(m_kamount);

        parallel_for(m_kmin, m_kmax + 1, m_kstep, [this](const std::size_t p_index){
            calculate_wce(p_index);
        });

        calculate_elbows();
        m_result->set_amount(find_optimal_kvalue());
    }

private:
    template<class CenterInitializer = TypeInitializer>
    typename std::enable_if<std::is_same<CenterInitializer, kmeans_plus_plus>::value, void>::type
    static prepare_centers(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, dataset & p_initial_centers) {
        kmeans_plus_plus(p_amount, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, p_random_state).initialize(p_data, p_initial_centers);
    }

    template<class CenterInitializer = TypeInitializer>
    typename std::enable_if<!std::is_same<CenterInitializer, kmeans_plus_plus>::value, void>::type
    static prepare_centers(const std::size_t p_amount, const dataset & p_data, const long long p_random_state, dataset & p_initial_centers) {
        TypeInitializer(p_amount, p_random_state).initialize(p_data, p_initial_centers);
    }

    void calculate_wce(const std::size_t p_kvalue) {
        dataset initial_centers;
        prepare_centers(p_kvalue, *m_data, m_random_state, initial_centers);

        kmeans_data result;
        kmeans instance(initial_centers, kmeans::DEFAULT_TOLERANCE);
        instance.process(*m_data, result);

        m_result->get_wce().at((p_kvalue - m_kmin) / m_kstep) = result.wce();
    }

    void verify() {
        if (m_kmin < 1) {
            throw std::invalid_argument("K min value '" + std::to_string(m_kmin) + "' should be greater than 0.");
        }

        if (m_kmax <= m_kmin) {
            throw std::invalid_argument("K max value '" + std::to_string(m_kmax) + "' should be greater than K min value '" + std::to_string(m_kmin) + "'.");
        }

        if (m_kmax + 1 < 3 + m_kmin) {
            throw std::invalid_argument("Amount of K '" + std::to_string(m_kmax - m_kmin) + "' is too small for analysis.");
        }

        if (m_kamount < 3) {
            throw std::invalid_argument("The search step is too high '" + std::to_string(m_kstep) + "' for analysis (amount of K for analysis is '" + std::to_string(m_kamount) + "').");
        }
    }

    void calculate_elbows() {
        const wce_sequence & wce = m_result->get_wce();

        const double x0 = 0.0;
        const double y0 = wce.front();

        const double x1 = static_cast<double>(wce.size());
        const double y1 = wce.back();

        const double norm = euclidean_distance(point({ x0, y0 }), point({ x1, y1 }));

        m_elbow.resize(wce.size() - 2, 0.0);

        for (std::size_t index_elbow = 1; index_elbow < m_result->get_wce().size() - 1; index_elbow++) {
            const double x = static_cast<double>(index_elbow);
            const double y = wce.at(index_elbow);

            const double segment = std::abs((y0 - y1) * x + (x1 - x0) * y + (x0 * y1 - x1 * y0));
            
            m_elbow[index_elbow - 1] = segment / norm;
        }
    }

    std::size_t find_optimal_kvalue() {
        auto optimal_elbow_iter = std::max_element(m_elbow.cbegin(), m_elbow.cend());
        return (std::distance(m_elbow.cbegin(), optimal_elbow_iter) + 1) * m_kstep + m_kmin;
    }
};


}

}