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

#include <pyclustering/interface/gmeans_interface.h>

#include <pyclustering/cluster/gmeans.hpp>


pyclustering_package * gmeans_algorithm(const pyclustering_package * const p_sample, 
                                        const std::size_t p_amount, 
                                        const double p_tolerance,
                                        const std::size_t p_repeat)
{
    pyclustering::dataset data;
    p_sample->extract(data);

    pyclustering::clst::gmeans algorithm(p_amount, p_tolerance, p_repeat);

    pyclustering::clst::gmeans_data output_result;
    algorithm.process(data, output_result);

    std::vector<double> wce_storage(1, output_result.wce());

    pyclustering_package * package = create_package_container(GMEANS_PACKAGE_SIZE);
    ((pyclustering_package **) package->data)[GMEANS_PACKAGE_INDEX_CLUSTERS] = create_package(&output_result.clusters());
    ((pyclustering_package **) package->data)[GMEANS_PACKAGE_INDEX_CENTERS] = create_package(&output_result.centers());
    ((pyclustering_package **) package->data)[GMEANS_PACKAGE_INDEX_WCE] = create_package(&wce_storage);

    return package;
}
