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


#include <pyclustering/definitions.hpp>

#include <list>
#include <vector>


namespace pyclustering {

namespace clst {


/*!

@brief  Defines logical location of CLIQUE block in a data space.

*/
using clique_block_location = std::vector<std::size_t>;


/*!

@brief    Geometrical description of CLIQUE block in a data space.
@details  Provides services related to spatial functionality.

@see bang_block

*/
class clique_spatial_block {
private:
    point   m_max_corner;
    point   m_min_corner;

public:
    /*!

    @brief    Default constructor of the CLIQUE spatial block.

    */
    clique_spatial_block() = default;

    /*!

    @brief    Constructor of the CLIQUE spatial block.

    @param[in] p_max_corner: maximum corner coordinates of the block.
    @param[in] p_min_corner: minimal corner coordinates of the block.

    */
    clique_spatial_block(const point & p_max_corner, const point & p_min_corner);

public:
    /*!

    @brief    Point is considered as contained if it lies in block (belong to it).

    @param[in] p_point: maximum corner coordinates of the block.

    @return   `true` if the point belongs to the block, otherwise `false` is returned.

    */
    bool contains(const point & p_point) const;

    /*!

    @return   Returns maximum corner coordinates of the block.

    */
    const point & get_max_corner() const;

    /*!
    
    @brief    Update maximum corner coordinates of the block.

    @param[in] p_corner: new maximum coordinates of the block.
    
    */
    void move_max_corner(point && p_corner);

    /*!

    @return   Returns minimum corner coordinates of the block.

    */
    const point & get_min_corner() const;

    /*!

    @brief    Update minimum corner coordinates of the block.

    @param[in] p_corner: new minimum coordinates of the block.

    */
    void move_min_corner(point && p_corner);
};


/*!

@brief  Defines CLIQUE block that contains information about its logical location and spatial location in a data space and
         set points that are covered by that block.

*/
class clique_block {
public:
    /*!

    @brief  Sequence container where points that belong to CLIQUE block are stored.

    */
    using content   = std::list<std::size_t>;

private:
    clique_block_location     m_logical_location;
    clique_spatial_block      m_spatial_location;
    content                   m_points;
    bool                      m_visited = false;

public:
    clique_block(const clique_block_location & p_location, const clique_spatial_block & p_block);

    clique_block(clique_block_location && p_location, clique_spatial_block && p_block);

public:
    const clique_block_location & get_logical_location() const;

    const clique_spatial_block & get_spatial_block() const;

    const clique_block::content & get_points() const;

    bool is_visited() const;

    void touch();

    void capture_points(const dataset & p_data, std::vector<bool> & p_availability);

    void get_location_neighbors(const std::size_t p_edge, std::vector<clique_block_location> & p_neighbors) const;
};


}

}