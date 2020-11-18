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

@brief  Sequence container that contains Silhouette's score for each point.

*/
using silhouette_sequence      = std::vector<double>;


/*!

@class  silhouette_data silhouette_data.hpp pyclustering/cluster/silhouette_data.hpp

@brief  Silhouette analysis result that contain information about Silhouette score for each point.

*/
class silhouette_data {
private:
    silhouette_sequence m_scores;

public:
    /*!
    
    @brief  Returns constant reference to the container with Silhouette score for each point
    
    */
    const silhouette_sequence & get_score() const { return m_scores; }

    /*!

    @brief  Returns reference to the container with Silhouette score for each point

    */
    silhouette_sequence & get_score() { return m_scores; }
};


}

}