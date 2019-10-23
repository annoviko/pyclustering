/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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

#include <pyclustering/interface/dbscan_interface.h>

#include <pyclustering/cluster/dbscan.hpp>


pyclustering_package * dbscan_algorithm(const pyclustering_package * const p_sample, 
                                        const double p_radius,
                                        const size_t p_minumum_neighbors,
                                        const size_t p_data_type)
{
    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::dbscan solver(p_radius, p_minumum_neighbors);

    pyclustering::clst::dbscan_data output_result;

    solver.process(input_dataset, (pyclustering::clst::dbscan_data_t) p_data_type, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size() + 1;   /* the last for noise */
    package->data = new pyclustering_package * [package->size + 1];

    for (std::size_t i = 0; i < package->size - 1; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&output_result[i]);
    }

    ((pyclustering_package **) package->data)[package->size - 1] = create_package(&output_result.noise());

    return package;
}
