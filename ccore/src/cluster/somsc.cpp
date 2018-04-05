/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#include "cluster/somsc.hpp"


using namespace ccore::nnet;


namespace ccore {

namespace clst {


somsc::somsc(const std::size_t p_amount_clusters, const std::size_t p_epoch) :
        m_amount_clusters(p_amount_clusters),
        m_epoch(p_epoch)
{ }


void somsc::process(const dataset & data, cluster_data & output_result) {
    output_result = somsc_data();

    som_parameters params;
    som som_map(1, m_amount_clusters, som_conn_type::SOM_GRID_FOUR, params);
    som_map.train(data, m_epoch, true);

    som_map.allocate_capture_objects((som_gain_sequence &) output_result.clusters());
}


}

}