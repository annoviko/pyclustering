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

#include "interface/kmedoids_interface.h"

#include "cluster/kmedoids.hpp"

#include "utils/metric.hpp"


using namespace ccore::utils::metric;


pyclustering_package * kmedoids_algorithm(const pyclustering_package * const p_sample,
                                          const pyclustering_package * const p_package_medoids,
                                          const double p_tolerance,
                                          const void * const p_metric,
                                          const std::size_t p_type)
{
    ccore::clst::medoid_sequence medoids;
    p_package_medoids->extract(medoids);

    distance_metric<point> * metric = ((distance_metric<point> *) p_metric);
    distance_metric<point> default_metric = distance_metric_factory<point>::euclidean_square();

    if (!metric)
        metric = &default_metric;

    ccore::clst::kmedoids algorithm(medoids, p_tolerance, *metric);

    dataset input_dataset;
    p_sample->extract(input_dataset);

    ccore::clst::kmedoids_data output_result;
    algorithm.process(input_dataset, (ccore::clst::kmedoids_data_t) p_type, output_result);

    pyclustering_package * package = create_package(&output_result.clusters());
    return package;
}

