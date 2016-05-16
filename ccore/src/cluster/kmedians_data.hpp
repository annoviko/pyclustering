#ifndef SRC_CLUSTER_KMEDIANS_DATA_HPP_
#define SRC_CLUSTER_KMEDIANS_DATA_HPP_


#include <memory>
#include <vector>

#include "cluster/cluster_data.hpp"

#include "definitions.hpp"


namespace cluster_analysis {


/***********************************************************************************************
*
* @brief    Clustering results of K-Medians algorithm that consists of information about allocated
*           clusters and medians of each cluster.
*
***********************************************************************************************/
class kmedians_data : public cluster_data {
private:
    dataset_ptr       m_medians;

public:
    /***********************************************************************************************
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    ***********************************************************************************************/
    kmedians_data(void);

    /***********************************************************************************************
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    ***********************************************************************************************/
    kmedians_data(const kmedians_data & p_other);

    /***********************************************************************************************
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    ***********************************************************************************************/
    kmedians_data(kmedians_data && p_other);

    /***********************************************************************************************
    *
    * @brief    Default destructor that destroys clustering data.
    *
    ***********************************************************************************************/
    virtual ~kmedians_data(void);

public:
    /***********************************************************************************************
    *
    * @brief    Returns shared pointer to medians that correspond to allocated clusters.
    *
    ***********************************************************************************************/
    dataset_ptr medians(void);
};


}


#endif
