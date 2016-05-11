#ifndef SRC_CLUSTER_CLUSTER_ALGORITHM_HPP_
#define SRC_CLUSTER_CLUSTER_ALGORITHM_HPP_


#include <vector>

#include "cluster_data.hpp"


namespace cluster {


/***********************************************************************************************
*
* @brief    Clustering algorithm interface
*
***********************************************************************************************/
class cluster_algorithm {
public:
    using point         = std::vector<double>;
    using input_data    = std::vector<point>;

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
    virtual void process(const input_data & p_data, cluster_data & p_result) = 0;
};


}


#endif
