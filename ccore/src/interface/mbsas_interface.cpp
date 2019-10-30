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


#include <pyclustering/interface/bsas_interface.h>
#include <pyclustering/interface/mbsas_interface.h>

#include <pyclustering/cluster/mbsas.hpp>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;


pyclustering_package * mbsas_algorithm(const pyclustering_package * const p_sample,
                                       const std::size_t p_amount,
                                       const double p_threshold,
                                       const void * const p_metric)
{
    distance_metric<pyclustering::point> * metric = ((distance_metric<pyclustering::point> *) p_metric);
    distance_metric<pyclustering::point> default_metric = distance_metric_factory<pyclustering::point>::euclidean_square();

    if (!metric) {
        metric = &default_metric;
    }

    pyclustering::clst::mbsas algorithm(p_amount, p_threshold, *metric);

    pyclustering::dataset input_dataset;
    p_sample->extract(input_dataset);

    pyclustering::clst::mbsas_data output_result;
    algorithm.process(input_dataset, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = BSAS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [BSAS_PACKAGE_SIZE];

    ((pyclustering_package **) package->data)[BSAS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[BSAS_PACKAGE_INDEX_REPRESENTATIVES] = create_package(&output_result.representatives());

    return package;
}