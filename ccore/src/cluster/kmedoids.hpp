/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#ifndef SRC_CLUSTER_KMEDOIDS_HPP_
#define SRC_CLUSTER_KMEDOIDS_HPP_


#include <memory>

#include "cluster/cluster_algorithm.hpp"
#include "cluster/kmedoids_data.hpp"


namespace cluster_analysis {


/**
*
* @brief    Represents K-Medoids clustering algorithm for cluster analysis.
* @details  The algorithm related to partitional class when input data is divided into groups.
*           K-Medoids algorithm is also known as the PAM (Partitioning Around Medoids).
*
*/
class kmedoids : public cluster_algorithm {
private:
    const dataset                   * m_data_ptr;         /* temporary pointer to input data that is used only during processing */

    kmedoids_data                   * m_result_ptr;       /* temporary pointer to clustering result that is used only during processing */

    medoid_sequence                 m_initial_medoids;

    double                          m_tolerance;

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    kmedoids(void);

    /**
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_initial_medoids: initial medoids that are used for processing.
    * @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
    *             medoids of clusters is less than tolerance than algorithm will stop processing.
    *
    */
    kmedoids(const medoid_sequence & p_initial_medoids, const double p_tolerance = 0.25);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    virtual ~kmedoids(void);

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    virtual void process(const dataset & p_data, cluster_data & p_result);

private:
    /**
    *
    * @brief    Updates clusters in line with current medoids.
    *
    */
    void update_clusters(void);

    /**
    *
    * @brief    Erases clusters that do not have any points.
    *
    * @param[in|out] p_clusters: clusters that should be analyzed and modified.
    *
    */
    void erase_empty_clusters(cluster_sequence & p_clusters);

    /**
    *
    * @brief    Calculates medoids in line with current clusters.
    *
    * @param[out] p_medoids: calculated medoids for current clusters.
    *
    */
    void calculate_medoids(cluster & p_medoids);

    /**
    *
    * @brief    Calculates medoid for specified cluster.
    *
    * @param[in] p_cluster: cluster that is used for medoid calculation.
    *
    * @return   Medoid (index point) of specified cluster.
    *
    */
    size_t calculate_cluster_medoid(const cluster & p_cluster) const;

    /**
    *
    * @brief    Calculates maximum difference in data allocation between previous medoids and specified.
    *
    * @param[in] p_medoids: medoids that should be used for difference calculation.
    *
    * @return   Maximum difference between current medoids and specified.
    *
    */
    double calculate_changes(const medoid_sequence & p_medoids) const;
};


}


#endif
