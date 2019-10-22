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


#include <pyclustering/utils/metric.hpp>

#include <algorithm>


namespace pyclustering {

namespace utils {

namespace metric {


double average_neighbor_distance(const std::vector<std::vector<double> > * points, const std::size_t num_neigh) {
    std::vector<std::vector<double> > dist_matrix( points->size(), std::vector<double>(points->size(), 0.0) );
    for (std::size_t i = 0; i < points->size(); i++) {
        for (std::size_t j = i + 1; j < points->size(); j++) {
            double distance = euclidean_distance( (*points)[i], (*points)[j] );
            dist_matrix[i][j] = distance;
            dist_matrix[j][i] = distance;
        }

        std::sort(dist_matrix[i].begin(), dist_matrix[i].end());
    }

    double total_distance = 0.0;
    for (std::size_t i = 0; i < points->size(); i++) {
        for (std::size_t j = 0; j < num_neigh; j++) {
            total_distance += dist_matrix[i][j + 1];
        }
    }

    return total_distance / ( (double) num_neigh * (double) points->size() );
}


}

}

}
