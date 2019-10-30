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

#include <pyclustering/interface/kmeans_interface.h>

#include <pyclustering/cluster/kmeans.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


pyclustering_package * kmeans_algorithm(const pyclustering_package * const p_sample, 
                                        const pyclustering_package * const p_initial_centers,
                                        const double p_tolerance, 
                                        const std::size_t p_itermax,
                                        const bool p_observe,
                                        const void * const p_metric)
{
    pyclustering::dataset data, centers;

    p_sample->extract(data);
    p_initial_centers->extract(centers);

    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::kmeans algorithm(centers, p_tolerance, p_itermax, *metric);

    pyclustering::clst::kmeans_data output_result(p_observe);
    algorithm.process(data, output_result);

    pyclustering_package * package = create_package_container(KMEANS_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_CENTERS] = create_package(&output_result.centers());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_EVOLUTION_CLUSTERS] = create_package(&output_result.evolution_clusters());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_EVOLUTION_CENTERS] = create_package(&output_result.evolution_centers());

    std::vector<double> wce_storage(1, output_result.wce());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_WCE] = create_package(&wce_storage);

    return package;
}
