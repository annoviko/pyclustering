#ifndef SRC_CLUSTER_DBSCAN_DATA_HPP_
#define SRC_CLUSTER_DBSCAN_DATA_HPP_


#include <memory>
#include <vector>

#include "cluster/cluster_data.hpp"


namespace cluster_analysis {


/***********************************************************************************************
*
* @brief    Clustering results of DBSCAM algorithm that consists of information about allocated
*           clusters and noise (points that are not related to any cluster).
*
***********************************************************************************************/
class dbscan_data : public cluster_data {
private:
    noise_ptr       m_noise;

public:
    /***********************************************************************************************
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    ***********************************************************************************************/
    dbscan_data(void);

    /***********************************************************************************************
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    ***********************************************************************************************/
    dbscan_data(const dbscan_data & p_other);

    /***********************************************************************************************
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    ***********************************************************************************************/
    dbscan_data(dbscan_data && p_other);

    /***********************************************************************************************
    *
    * @brief    Default destructor that destroys clustering data.
    *
    ***********************************************************************************************/
    virtual ~dbscan_data(void);

public:
    /***********************************************************************************************
    *
    * @brief    Returns shared pointer to noise.
    *
    ***********************************************************************************************/
    noise_ptr noise(void);
};


}


#endif
