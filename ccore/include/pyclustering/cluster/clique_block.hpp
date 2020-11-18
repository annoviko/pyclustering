/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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

@class    clique_spatial_block clique_block.hpp pyclustering/cluster/clique_block.hpp

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

@class    clique_block clique_block.hpp pyclustering/cluster/clique_block.hpp

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
    /*!
    
    @brief  CLIQUE block constructor.

    @param[in] p_location: logical location of the block in CLIQUE grid.
    @param[in] p_block: spatial location in data space.

    */
    clique_block(const clique_block_location & p_location, const clique_spatial_block & p_block);

    /*!

    @brief  CLIQUE block constructor that construct object by moving input arguments.

    @param[in] p_location: logical location of the block in CLIQUE grid.
    @param[in] p_block: spatial location in data space.

    */
    clique_block(clique_block_location && p_location, clique_spatial_block && p_block);

public:
    /*!
    
    @return  Returns logical location of the block in CLIQUE grid.
    
    */
    const clique_block_location & get_logical_location() const;

    /*!

    @return  Returns spatial location of the block in data space.

    */
    const clique_spatial_block & get_spatial_block() const;

    /*!

    @return  Returns points that are belong to the block.

    */
    const clique_block::content & get_points() const;

    /*!
    
    @return  Returns `true` if the block has been already visited (processed) by CLIQUE algorithm.
    
    */
    bool is_visited() const;

    /*!
    
    @brief  Mark the block as visited (processed) by CLIQUE algorithm.
    
    */
    void touch();

    /*!

    @brief  Finds points that belong to this block using availability map to reduce computational complexity by
             checking whether the point belongs to the block.

    @details Algorithm complexity of this method is O(n).

    @param[in] p_data: data where points are represented as coordinates.
    @param[in,out] p_availability: contains boolean values that denote whether point is already belong
                    to another CLIQUE block. Points that are captured by the current block in this
                    method are also marked as captured.

    */
    void capture_points(const dataset & p_data, std::vector<bool> & p_availability);

    /*!
    
    @brief  Forms list of logical location of each neighbor for this particular CLIQUE block.

    @param[in] p_edge: amount of intervals in each dimension that is used for clustering process.
    @param[in] p_neighbors: logical location of each neighbor for the CLIQUE block.

    */
    void get_location_neighbors(const std::size_t p_edge, std::vector<clique_block_location> & p_neighbors) const;
};


}

}