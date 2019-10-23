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


#include <pyclustering/interface/optics_interface.h>

#include <pyclustering/cluster/optics.hpp>


pyclustering_package * optics_algorithm(const pyclustering_package * const p_sample,
                                        const double p_radius,
                                        const size_t p_minumum_neighbors,
                                        const size_t p_amount_clusters,
                                        const size_t p_data_type)
{
    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::optics solver(p_radius, p_minumum_neighbors, p_amount_clusters);

    pyclustering::clst::optics_data output_result;
    solver.process(input_dataset, (pyclustering::clst::optics_data_t) p_data_type, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = OPTICS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [OPTICS_PACKAGE_SIZE];

    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_NOISE] = create_package(&output_result.noise());
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_ORDERING] = create_package(&output_result.cluster_ordering());

    std::vector<double> radius_storage(1, output_result.get_radius());
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_RADIUS] = create_package(&radius_storage);

    /* Pack OPTICS objects to pyclustering packages */
    const auto & objects = output_result.optics_objects();

    std::size_t package_size = objects.size();
    pyclustering_package * package_object_indexes = create_package<std::size_t>(package_size);
    pyclustering_package * package_core_distance = create_package<double>(package_size);
    pyclustering_package * package_reachability_distance = create_package<double>(package_size);

    for (std::size_t i = 0; i < objects.size(); i++) {
        ((std::size_t *) package_object_indexes->data)[i] = objects[i].m_index;
        ((double *) package_core_distance->data)[i] = objects[i].m_core_distance;
        ((double *) package_reachability_distance->data)[i] = objects[i].m_reachability_distance;
    }

    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_INDEX] = package_object_indexes;
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_CORE_DISTANCE] = package_core_distance;
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_REACHABILITY_DISTANCE] = package_reachability_distance;

    return package;
}