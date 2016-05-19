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

#include "interface/cure_interface.h"

#include "cluster/cure.hpp"


void * cure_algorithm(const data_representation * const sample, const size_t number_clusters, const size_t number_repr_points, const double compression) {
    std::unique_ptr<dataset> input_dataset(read_sample(sample));

    cluster_analysis::cure solver(number_clusters, number_repr_points, compression);

    cluster_analysis::cure_data * output_result = new cluster_analysis::cure_data();
    solver.process(*input_dataset, *output_result);

    return output_result;
}


void cure_data_destroy(void * pointer_cure_data) {
    delete (cluster_analysis::cure *) pointer_cure_data;
}


pyclustering_package * cure_get_clusters(void * pointer_cure_data) {
    cluster_analysis::cure_data & output_result = (cluster_analysis::cure_data &) *((cluster_analysis::cure_data *)pointer_cure_data);

    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&output_result[i]);
    }

    return package;
}


pyclustering_package * cure_get_representors(void * pointer_cure_data) {
    cluster_analysis::cure_data & output_result = (cluster_analysis::cure_data &) *((cluster_analysis::cure_data *)pointer_cure_data);
    cluster_analysis::representor_sequence & representors = *output_result.representors();

    /* TODO: forming packages for clustering is always the same - move to function */
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&representors[i]);
    }

    return package;
}


pyclustering_package * cure_get_means(void * pointer_cure_data) {
    cluster_analysis::cure_data & output_result = (cluster_analysis::cure_data &) *((cluster_analysis::cure_data *)pointer_cure_data);
    dataset & means = *output_result.means();

    /* TODO: forming packages for clustering is always the same - move to function */
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = output_result.size();
    package->data = new pyclustering_package * [package->size];

    for (unsigned int i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&means[i]);
    }

    return package;
}
