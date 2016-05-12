#ifndef SRC_CLUSTER_CLUSTER_ALGORITHM_HPP_
#define SRC_CLUSTER_CLUSTER_ALGORITHM_HPP_


#include <vector>

#include "cluster/cluster_data.hpp"

#include "definitions.hpp"


namespace cluster_analysis {


/***********************************************************************************************
*
* @brief    Clustering algorithm interface
*
***********************************************************************************************/
class cluster_algorithm {
public:
    /***********************************************************************************************
    *
    * @brief    Default destructor that destroy object.
    *
    ***********************************************************************************************/
    virtual ~cluster_algorithm(void);

public:
    /***********************************************************************************************
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    ***********************************************************************************************/
    virtual void process(const dataset & p_data, cluster_data & p_result) = 0;
};


}


#endif
