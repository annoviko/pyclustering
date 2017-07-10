/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "interface/dbscan_interface.h"

#include "cluster/dbscan.hpp"


pyclustering_package * dbscan_algorithm(const pyclustering_package * const sample, const double radius, const size_t minumum_neighbors) {
    dataset input_dataset;
    sample->extract(input_dataset);

    cluster_analysis::dbscan solver(radius, minumum_neighbors);

    cluster_analysis::dbscan_data output_result;

    solver.process(input_dataset, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size() + 1;   /* the last for noise */
    package->data = new pyclustering_package * [package->size + 1];

    for (unsigned int i = 0; i < package->size - 1; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&output_result[i]);
    }

    ((pyclustering_package **) package->data)[package->size - 1] = create_package(output_result.noise().get());

    return package;
}
