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


#include "interface/optics_interface.h"

#include "cluster/optics.hpp"


pyclustering_package * optics_algorithm(const pyclustering_package * const p_sample,
                                        const double p_radius,
                                        const size_t p_minumum_neighbors,
                                        const size_t p_amount_clusters,
                                        const size_t p_data_type)
{
    dataset input_dataset;
    p_sample->extract(input_dataset);

    ccore::clst::optics solver(p_radius, p_minumum_neighbors, p_amount_clusters);

    ccore::clst::optics_data output_result;
    solver.process(input_dataset, (ccore::clst::optics_data_t) p_data_type, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);
    package->size = OPTICS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [OPTICS_PACKAGE_SIZE];

    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_NOISE] = create_package(&output_result.noise());
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_ORDERING] = create_package(&output_result.cluster_ordering());

    std::vector<double> radius_storage(1, output_result.get_radius());
    ((pyclustering_package **) package->data)[OPTICS_PACKAGE_INDEX_RADIUS] = create_package(&radius_storage);

    return package;
}