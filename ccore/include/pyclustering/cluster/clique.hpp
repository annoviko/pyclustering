/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once

#include <pyclustering/cluster/clique_data.hpp>

#include <list>
#include <unordered_map>


namespace pyclustering {

namespace clst {


/*!

@class      coordinate_iterator clique.hpp pyclustering/cluster/clique.hpp

@brief      Coordinate iterator is used to generate logical location description for each CLIQUE block.
@details    This class is used by CLIQUE algorithm for clustering process.

*/
class coordinate_iterator {
private:
    std::size_t m_dimension = 0;
    std::size_t m_edge      = 0;
    clique_block_location m_coordinate;

public:
    /*!
    
    @brief Constructs coordinate iterator for CLIQUE algorithm.

    @param[in] p_dimension: amount of dimensions in input data space.
    @param[in] p_edge: amount of intervals in each dimension.

    */
    coordinate_iterator(const std::size_t p_dimension, const std::size_t p_edge);

public:
    /*!
    
    @brief Returns constant reference to current block coordinate.
    
    */
    const clique_block_location & get_coordinate() const noexcept;

    /*!

    @brief Returns reference to current block coordinate.

    */
    clique_block_location & get_coordinate() noexcept;

public:
    /*!

    @brief Forms logical location for next block.
    @details Method `get_coordinate` should be used to get new coordinates.

    */
    coordinate_iterator & operator++();
};


/*!

@class      clique clique.hpp pyclustering/cluster/clique.hpp

@brief      Class implements CLIQUE grid based clustering algorithm.
@details    CLIQUE automatically finds subspaces with high-density clusters. It produces identical results
             irrespective of the order in which the input records are presented and it does not presume any canonical
             distribution for input data @cite article::clique::1.

Here is an example where data in two-dimensional space is clustered using CLIQUE algorithm:
@code
    using namespace pyclustering;
    using namespace pyclustering::clst;

    int main() {
        // Read two-dimensional input data 'Target'.
        dataset data = read_data("Target.txt");

        // Prepare algorithm's parameters.
        const std::size_t intervals = 10;   // defines amount of cells in grid in each dimension
        const std::size_t threshold = 0;    // no outliers

        // Create CLIQUE algorithm for processing.
        clique clique_instance = clique(intervals, threshold);

        // Run clustering process.
        clique_data result;
        clique_instance.process(data, result);

        // Obtain results.
        cluster_sequence & clusters = result.clusters();
        clique_block_sequence & blocks = result.blocks();
        noise & outliers = result.noise();  // in this case it is empty because threshold is 0.

        // Display information about extracted clusters:
        std::cout << "Amount of clusters: " << clusters.size() << std::endl;
        std::cout << "Amount of outliers: " << outliers.size() << std::endl;

        return 0;
    }
@endcode

Here is one of the example how to implement read function to get input data:
@code
    dataset read_data(const std::string & filename) {
        dataset data;

        std::ifstream file(filename);
        std::string line;

        while (std::getline(file, line)) {
            std::stringstream stream(line);

            point coordinates;
            double value = 0.0;
            while (stream >> value) {
                coordinates.push_back(value);
            }

            data.push_back(coordinates);
        }

        file.close();
        return data;
    }
@endcode

In example above, 6 clusters are allocated including four small cluster where each such small cluster consists of
three points. There are visualized clustering results - grid that has been formed by CLIQUE algorithm with
density and clusters itself (see Python version of pyclustering library for visualization):
@image html clique_clustering_target.png "Fig. 1. CLIQUE clustering results (grid and clusters itself)."

Sometimes such small clusters should be considered as outliers taking into account fact that two clusters in the
central are relatively huge. To treat them as a noise threshold value should be increased:
@code
    // Prepare algorithm's parameters.
    const std::size_t intervals = 10;   // defines amount of cells in grid in each dimension
    const std::size_t threshold = 3;    // block that contains 3 or less points is considered as a outlier as well as its points
@endcode

After execution following output is obtained:
@code
    Amount of clusters: 2
    Amount of outliers: 25
@endcode

Two clusters are allocated, but in this case some points in cluster-"circle" are also considered as outliers,
because CLIQUE operates with blocks, not with points:
@image html clique_clustering_with_noise.png "Fig. 2. Noise allocation by CLIQUE."

*/
class clique {
private:
    struct data_info {
        point m_min_corner;
        point m_max_corner;
        std::vector<double> m_sizes;
    };

private:
    using block_map = std::unordered_map<std::string, clique_block *>;

private:
    std::size_t     m_intervals         = 0;
    std::size_t     m_density_threshold = 0;

    const dataset * m_data_ptr      = nullptr;
    clique_data *   m_result_ptr    = nullptr;

    block_map       m_cells_map;

public:
    /*!

    @brief Create CLIQUE clustering algorithm.

    @param[in] p_intervals: amount of intervals in each dimension that defines amount of CLIQUE blocks as \f[N_{ blocks } = intervals^{ dimensions }\f].
    @param[in] p_threshold: minimum number of points that should be contained by CLIQUE block to consider its points as non-outliers.

    */
    clique(const std::size_t p_intervals, const std::size_t p_threshold);

public:
    /*!

    @brief    Performs cluster analysis of an input data.

    @param[in]  p_data: input data for cluster analysis.
    @param[out] p_result: clustering result of an input data.

    */
    void process(const dataset & p_data, clique_data & p_result);

private:
    void create_grid();

    void expand_cluster(clique_block & p_block);

    void get_neighbors(const clique_block & p_block, std::list<clique_block *> & p_neighbors) const;

    void get_spatial_location(const clique_block_location & p_location, const clique::data_info & p_info, clique_spatial_block & p_block) const;

    void get_data_info(clique::data_info & p_info) const;

    static std::string location_to_key(const clique_block_location & p_location);
};

}

}
