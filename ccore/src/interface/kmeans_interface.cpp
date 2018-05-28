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

#include "interface/kmeans_interface.h"

#include "cluster/kmeans.hpp"

#include "utils/metric.hpp"


using namespace ccore::utils::metric;


pyclustering_package * kmeans_algorithm(const pyclustering_package * const p_sample, 
                                        const pyclustering_package * const p_initial_centers, 
                                        const double p_tolerance, 
                                        const bool p_observe,
                                        const void * const p_metric)
{
    dataset data, centers;

    p_sample->extract(data);
    p_initial_centers->extract(centers);

    distance_metric<point> * metric = ((distance_metric<point> *) p_metric);
    distance_metric<point> default_metric = distance_metric_factory<point>::euclidean_square();

    if (!metric)
        metric = &default_metric;

    ccore::clst::kmeans algorithm(centers, p_tolerance, *metric);

    ccore::clst::kmeans_data output_result(p_observe);
    algorithm.process(data, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = KMEANS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [KMEANS_PACKAGE_SIZE];

    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_CENTERS] = create_package(&output_result.centers());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_EVOLUTION_CLUSTERS] = create_package(&output_result.evolution_clusters());
    ((pyclustering_package **) package->data)[KMEANS_PACKAGE_INDEX_EVOLUTION_CENTERS] = create_package(&output_result.evolution_centers());

    return package;
}
