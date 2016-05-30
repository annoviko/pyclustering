/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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


pyclustering_package * kmedoids_algorithm(const data_representation * const sample, const pyclustering_package * const package_medoids, const double tolerance) {
    cluster_analysis::medoid_sequence medoids((size_t *) package_medoids->data, ((size_t *) package_medoids->data) + package_medoids->size);

    cluster_analysis::kmedoids algorithm(medoids, tolerance);

    std::unique_ptr<dataset> input_dataset(read_sample(sample));

    cluster_analysis::kmedoids_data output_result;
    algorithm.process(*input_dataset, output_result);

    pyclustering_package * package = create_package(output_result.clusters().get());
    return package;
}

