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

#include <pyclustering/interface/xmeans_interface.h>

#include <pyclustering/cluster/xmeans.hpp>


pyclustering_package * xmeans_algorithm(const pyclustering_package * const p_sample,
                                        const pyclustering_package * const p_centers,
                                        const std::size_t p_kmax,
                                        const double p_tolerance,
                                        const unsigned int p_criterion,
                                        const std::size_t p_repeat)
{
    pyclustering::dataset data, centers;
    p_sample->extract(data);
    p_centers->extract(centers);

    pyclustering::clst::xmeans solver(centers, p_kmax, p_tolerance, (pyclustering::clst::splitting_type) p_criterion, p_repeat);

    pyclustering::clst::xmeans_data output_result;
    solver.process(data, output_result);

    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = xmeans_package_indexer::XMEANS_PACKAGE_SIZE;
    package->data = new pyclustering_package * [package->size];

    ((pyclustering_package **) package->data)[xmeans_package_indexer::XMEANS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[xmeans_package_indexer::XMEANS_PACKAGE_INDEX_CENTERS] = create_package(&output_result.centers());
    ((pyclustering_package **) package->data)[xmeans_package_indexer::XMEANS_PACKAGE_INDEX_WCE] = create_package(1, output_result.wce());

    return package;
}
