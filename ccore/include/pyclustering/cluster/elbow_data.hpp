/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>


namespace pyclustering {

namespace clst {


/*!

@brief  Sequence container to store within cluster errors (WCE) for each K-value.

*/
using wce_sequence      = std::vector<double>;


/*!

@class  elbow_data elbow_data.hpp pyclustering/cluster/elbow_data.hpp

@brief  Elbow analysis result that contain information about optimal amount of clusters and
         total within cluster errors (WCE) for each K-value.

*/
class elbow_data {
private:
    std::size_t           m_amount  = 0;
    wce_sequence          m_wce     = { };

public:
    /*!
    
    @brief  Default constructor of the Elbow result.
    
    */
    elbow_data() = default;

    /*!

    @brief  Default desctructor of the Elbow result.

    */
    ~elbow_data() = default;

public:
    /*!
    
    @brief  Returns constant reference to total within cluster errors (WCE) for each K-value.

    @return Constant reference to total within cluster errors (WCE) for each K-value.
    
    */
    const wce_sequence & get_wce() const { return m_wce; }

    /*!

    @brief  Returns reference to total within cluster errors (WCE) for each K-value.

    @return Reference to total within cluster errors (WCE) for each K-value.

    */
    wce_sequence & get_wce() { return m_wce; }

    /*!

    @brief   Set optimal amount of clusters.
    @details The method is used by Elbow method to set the final analysis result.

    */
    void set_amount(const std::size_t p_amount) { m_amount = p_amount; }

    /*!

    @brief   Returns optimal amount of clusters.

    @return  Optimal amount of clusters.

    */
    std::size_t get_amount() const { return m_amount; }
};


}

}