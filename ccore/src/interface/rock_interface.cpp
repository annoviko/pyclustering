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

#include "interface/rock_interface.h"

#include "cluster/rock.hpp"


pyclustering_package * rock_algorithm(const pyclustering_package * const p_sample, const double p_radius, const size_t p_number_clusters, const double p_threshold) {
    dataset input_dataset;
    p_sample->extract(input_dataset);

    cluster_analysis::rock solver(p_radius, p_number_clusters, p_threshold);

    cluster_analysis::rock_data output_result;
    solver.process(input_dataset, output_result);

    pyclustering_package * package = create_package(output_result.clusters().get());
    return package;
}
