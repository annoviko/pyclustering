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

#include "interface/xmeans_interface.h"

#include "cluster/xmeans.hpp"


pyclustering_package * xmeans_algorithm(const pyclustering_package * const p_sample, const pyclustering_package * const p_centers, const std::size_t p_kmax, const double p_tolerance, const unsigned int p_criterion) {
    dataset data, centers;
    p_sample->extract(data);
    p_centers->extract(centers);

    ccore::clst::xmeans solver(centers, p_kmax, p_tolerance, (ccore::clst::splitting_type) p_criterion);

    ccore::clst::xmeans_data output_result;
    solver.process(data, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = 2;   /* cluster package + center package */
    package->data = new pyclustering_package * [2];

    ((pyclustering_package **) package->data)[0] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[1] = create_package(&output_result.centers());

    return package;
}
