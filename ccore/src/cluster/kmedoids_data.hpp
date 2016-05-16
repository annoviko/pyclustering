#ifndef SRC_CLUSTER_KMEDOIDS_DATA_HPP_
#define SRC_CLUSTER_KMEDOIDS_DATA_HPP_


#include <memory>
#include <vector>

#include "cluster/cluster_data.hpp"


namespace cluster_analysis {


using medoid_sequence = std::vector<size_t>;
using medoid_sequence_ptr = std::shared_ptr<medoid_sequence>;


/***********************************************************************************************
*
* @brief    Clustering results of K-Medoids algorithm that consists of information about allocated
*           clusters and medoids that correspond to them.
*
***********************************************************************************************/
class kmedoids_data : public cluster_data {
private:
    medoid_sequence_ptr     m_medoids;

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
    * @brief    Returns shared pointer to medoids that corresponds to allocated clusters.
    *
    ***********************************************************************************************/
    medoid_sequence_ptr medoids(void);
};


}


#endif
