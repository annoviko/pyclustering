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

#include <pyclustering/interface/kmedoids_interface.h>

#include <pyclustering/cluster/kmedoids.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


pyclustering_package * kmedoids_algorithm(const pyclustering_package * const p_sample,
                                          const pyclustering_package * const p_medoids,
                                          const double p_tolerance,
                                          const std::size_t p_itermax,
                                          const void * const p_metric,
                                          const std::size_t p_type)
{
    pyclustering::clst::medoid_sequence medoids;
    p_medoids->extract(medoids);

    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::kmedoids algorithm(medoids, p_tolerance, p_itermax, *metric);

    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::kmedoids_data output_result;
    algorithm.process(input_dataset, (pyclustering::clst::kmedoids_data_t) p_type, output_result);

    pyclustering_package * package = create_package_container(KMEDOIDS_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[KMEDOIDS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[KMEDOIDS_PACKAGE_INDEX_MEDOIDS] = create_package(&output_result.medoids());

    return package;
}

