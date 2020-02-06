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


#include <pyclustering/cluster/clique_block.hpp>
#include <pyclustering/cluster/cluster_data.hpp>


namespace pyclustering {

namespace clst {


/*!

@brief  Sequence container where CLIQUE blocks are stored.

*/
using clique_block_sequence = std::vector<clique_block>;


/*!

@class  clique_data clique_data.hpp pyclustering/cluster/clique_data.hpp

@brief  A storage where CLIQUE clustering results are stored.

*/
class clique_data : public cluster_data {
private:
    clique_block_sequence   m_blocks;
    clst::noise             m_noise;

public:
    /*!

    @brief  Returns constant reference to CLIQUE blocks that are formed during clustering process.

    */
    const clique_block_sequence & blocks() const { return m_blocks; }

    /*!

    @brief  Returns reference to CLIQUE blocks that are formed during clustering process.

    */
    clique_block_sequence & blocks() { return m_blocks; }

    /*!

    @brief  Returns constant reference to outliers that are allocated during clustering process.

    */
    const clst::noise & noise() const { return m_noise; }

    /*!

    @brief  Returns reference to outliers that are allocated during clustering process.

    */
    clst::noise & noise() { return m_noise; }
};


}

}