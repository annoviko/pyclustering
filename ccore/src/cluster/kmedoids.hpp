#ifndef SRC_CLUSTER_KMEDOIDS_HPP_
#define SRC_CLUSTER_KMEDOIDS_HPP_


#include <memory>

#include "cluster/cluster.hpp"


namespace cluster {


/***********************************************************************************************
*
* @brief    Clustering results of K-Medoids algorithm that consists of information about allocated
*           clusters and medoids that correspond to them.
*
***********************************************************************************************/
class kmedoids_data : public cluster_data {
private:
    std::vector<size_t>     m_medoids;

public:
    /***********************************************************************************************
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    ***********************************************************************************************/
    kmedoids_data(void);

    /***********************************************************************************************
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    ***********************************************************************************************/
    kmedoids_data(const kmedoids_data & p_other);

    /***********************************************************************************************
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    ***********************************************************************************************/
    kmedoids_data(kmedoids_data && p_other);

    /***********************************************************************************************
    *
    * @brief    Default destructor that destroys clustering data.
    *
    ***********************************************************************************************/
    virtual ~kmedoids_data(void);

public:
    /***********************************************************************************************
    *
    * @brief    Returns direct access to encapsulated medoids.
    *
    ***********************************************************************************************/
    std::vector<size_t> & medoids(void);
};


/***********************************************************************************************
*
* @brief    Represents K-Medoids clustering algorithm for cluster analysis.
* @details  The algorithm related to partitional class when input data is divided into groups.
*           K-Medoids algorithm is also known as the PAM (Partitioning Around Medoids).
*
***********************************************************************************************/
class kmedoids : public cluster_algorithm {
private:
    const cluster_algorithm::input_data * m_data_ptr;   /* temporary pointer to input data that is used only during processing */

    kmedoids_data                   * m_result_ptr;       /* temporary pointer to clustering result that is used only during processing */

    std::vector<size_t>             m_initial_medoids;

    double                          m_tolerance;

public:
    /***********************************************************************************************
    *
    * @brief    Default constructor of clustering algorithm.
    *
    ***********************************************************************************************/
    kmedoids(void);

    /***********************************************************************************************
    *
    * @brief    Constructor of clustering algorithm where algorithm parameters for processing are
    *           specified.
    *
    * @param[in] p_initial_medoids: initial medoids that are used for processing.
    * @param[in] p_tolerance: stop condition in following way: when maximum value of distance change of
    *             medoids of clusters is less than tolerance than algorithm will stop processing.
    *
    ***********************************************************************************************/
    kmedoids(const std::vector<size_t> & p_initial_medoids, const double p_tolerance = 0.25);

    /***********************************************************************************************
    *
    * @brief    Default destructor of the algorithm.
    *
    ***********************************************************************************************/
    virtual ~kmedoids(void);

public:
    /***********************************************************************************************
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    ***********************************************************************************************/
    virtual void process(const cluster_algorithm::input_data & p_data, kmedoids_data & p_result);

private:
    /***********************************************************************************************
    *
    * @brief    Updates clusters in line with current medoids.
    *
    ***********************************************************************************************/
    void update_clusters(void);

    /***********************************************************************************************
    *
    * @brief    Erases clusters that do not have any points.
    *
    * @param[in|out] p_clusters: clusters that should be analyzed and modified.
    *
    ***********************************************************************************************/
    void erase_empty_clusters(std::vector<cluster_data::cluster> & p_clusters);

    /***********************************************************************************************
    *
    * @brief    Calculates medoids in line with current clusters.
    *
    * @param[out] p_medoids: calculated medoids for current clusters.
    *
    ***********************************************************************************************/
    void calculate_medoids(std::vector<size_t> & p_medoids);

    /***********************************************************************************************
    *
    * @brief    Calculates medoid for specified cluster.
    *
    * @param[in] p_cluster: cluster that is used for medoid calculation.
    *
    * @return   Medoid (index point) of specified cluster.
    *
    ***********************************************************************************************/
    size_t calculate_cluster_medoid(const cluster_data::cluster & p_cluster) const;

    /***********************************************************************************************
    *
    * @brief    Calculates maximum difference in data allocation between previous medoids and specified.
    *
    * @param[in] p_medoids: medoids that should be used for difference calculation.
    *
    * @return   Maximum difference between current medoids and specified.
    *
    ***********************************************************************************************/
    double calculate_changes(const std::vector<size_t> & p_medoids) const;
};


}


#endif
