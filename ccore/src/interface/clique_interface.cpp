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

#include <pyclustering/interface/clique_interface.h>

#include <pyclustering/cluster/clique.hpp>


pyclustering_package * clique_algorithm(const pyclustering_package * const p_sample, const std::size_t p_intervals, const std::size_t p_threshold) {
    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::clique solver(p_intervals, p_threshold);

    pyclustering::clst::clique_data output_result;

    solver.process(input_dataset, output_result);

    pyclustering_package * package = create_package_container(CLIQUE_PACKAGE_SIZE);

    ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_NOISE] = create_package(&output_result.noise());

    const auto & blocks = output_result.blocks();
    ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_LOGICAL_LOCATION] = create_package_container(blocks.size());
    ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_MAX_CORNER] = create_package_container(blocks.size());
    ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_MIN_CORNER] = create_package_container(blocks.size());
    ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_BLOCK_POINTS] = create_package_container(blocks.size());

    pyclustering_package * logical_location = ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_LOGICAL_LOCATION];
    pyclustering_package * max_corner = ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_MAX_CORNER];
    pyclustering_package * min_corner = ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_MIN_CORNER];
    pyclustering_package * block_points = ((pyclustering_package **) package->data)[CLIQUE_PACKAGE_INDEX_BLOCK_POINTS];

    for (std::size_t i = 0; i < blocks.size(); i++) {
        ((pyclustering_package **) logical_location->data)[i] = create_package(&(blocks[i].get_logical_location()));
        ((pyclustering_package **) max_corner->data)[i] = create_package(&(blocks[i].get_spatial_block().get_max_corner()));
        ((pyclustering_package **) min_corner->data)[i] = create_package(&(blocks[i].get_spatial_block().get_min_corner()));
        ((pyclustering_package **) block_points->data)[i] = create_package(&(blocks[i].get_points()));
    }

    return package;
}