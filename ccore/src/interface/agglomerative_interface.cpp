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

#include <pyclustering/interface/agglomerative_interface.h>

#include <pyclustering/cluster/agglomerative.hpp>


pyclustering_package * agglomerative_algorithm(const pyclustering_package * const p_sample, const size_t p_number_clusters, const size_t p_link) {
    pyclustering::clst::agglomerative algorithm(p_number_clusters, (pyclustering::clst::type_link) p_link);

    pyclustering::dataset data;
    p_sample->extract(data);

    pyclustering::clst::cluster_data result;
    algorithm.process(data, result);

    pyclustering_package * package = create_package(&result.clusters());

    return package;
}
