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

#include "interface/cure_interface.h"

#include "cluster/cure.hpp"


void * cure_algorithm(const pyclustering_package * const sample, const size_t number_clusters, const size_t number_repr_points, const double compression) {
    dataset input_dataset;
    sample->extract(input_dataset);

    cluster_analysis::cure solver(number_clusters, number_repr_points, compression);

    cluster_analysis::cure_data * output_result = new cluster_analysis::cure_data();
    solver.process(input_dataset, *output_result);

    return output_result;
}


void cure_data_destroy(void * pointer_cure_data) {
    delete (cluster_analysis::cure *) pointer_cure_data;
}


pyclustering_package * cure_get_clusters(void * pointer_cure_data) {
    cluster_analysis::cure_data & output_result = (cluster_analysis::cure_data &) *((cluster_analysis::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(output_result.clusters().get());
    return package;
}


pyclustering_package * cure_get_representors(void * pointer_cure_data) {
    cluster_analysis::cure_data & output_result = (cluster_analysis::cure_data &) *((cluster_analysis::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(output_result.representors().get());
    return package;
}


pyclustering_package * cure_get_means(void * pointer_cure_data) {
    cluster_analysis::cure_data & output_result = (cluster_analysis::cure_data &) *((cluster_analysis::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(output_result.means().get());
    return package;
}
