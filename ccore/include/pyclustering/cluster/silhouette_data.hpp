/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

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