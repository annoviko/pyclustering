#ifndef SRC_CLUSTER_CURE_DATA_HPP_
#define SRC_CLUSTER_CURE_DATA_HPP_


#include <memory>
#include <vector>

#include "cluster/cluster_data.hpp"

#include "definitions.hpp"


namespace cluster_analysis {


using representor_sequence = std::vector<dataset>;
using representor_sequence_ptr = std::shared_ptr<representor_sequence>;


/**
*
* @brief    Clustering results of CURE algorithm that consists of information about allocated
*           clusters and their representative points and mean value.
*
*/
class cure_data : public cluster_data {
private:
    representor_sequence_ptr    m_representative_sequence = std::make_shared<representor_sequence>();

    dataset_ptr                 m_mean_sequence = std::make_shared<dataset>();

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    cure_data(void) = default;

    /**
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    cure_data(const cure_data & p_other) = default;

    /**
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    cure_data(cure_data && p_other) = default;

    /**
    *
    * @brief    Default destructor that destroys clustering data.
    *
    */
    virtual ~cure_data(void) = default;

public:
    /**
    *
    * @brief    Returns shared pointer to representative points of each cluster.
    * @details  Cluster index should be used to navigate in collections of representative points.
    *           An example of representative points of two clusters:
    *           { {{ 1.0, 2.0 }, { 3.4, 4.0 }}, {{ 7.5, 6.3 }, { -1.4, -4.7 }} }
    *           where points { {{ 1.0, 2.0 }, { 3.4, 4.0 }} are related to the first cluster
    *           and {{ 7.5, 6.3 }, { -1.4, -4.7 }} to the second.
    *
    * @return   Shared pointer to representative points of each cluster.
    *
    */
    inline representor_sequence_ptr representors(void) { return m_representative_sequence; }

    /**
    *
    * @brief    Returns shared pointer to mean point of each cluster.
    * @details  Cluster index should be used to navigate in collections of mean points.
    *           An example of mean points of three clusters: { { 1.0, 2.0 }, { 3.4, 4.0 }, { 7.0, 9.1 } }
    *           where { 1.0, 2.0 } is mean of the first cluster, { 3.4, 4.0 } - mean of the second and
    *           { 7.0, 9.1 } of the third.
    *
    * @return   Shared pointer to mean point of each cluster.
    *
    */
    inline dataset_ptr means(void) { return m_mean_sequence; }
};


}


#endif
