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


#include <pyclustering/cluster/ordering_analyser.hpp>


#include <algorithm>
#include <limits>


namespace pyclustering {

namespace clst {


double ordering_analyser::calculate_connvectivity_radius(const ordering & p_ordering, const std::size_t p_amount_clusters, const std::size_t p_maximum_iterations) {
    const double maximum_distance = *std::max_element(p_ordering.cbegin(), p_ordering.cend());

    double upper_distance = maximum_distance;
    double lower_distance = 0.0;

    double result = -1.0;

    if (extract_cluster_amount(p_ordering, maximum_distance) > p_amount_clusters) {
        return result;
    }

    for(std::size_t i = 0; i < p_maximum_iterations; i++) {
        double radius = (lower_distance + upper_distance) / 2.0;

        std::size_t amount = extract_cluster_amount(p_ordering, radius);
        if (amount == p_amount_clusters) {
            result = radius;
            break;
        }
        else if (amount == 0) {
            break;
        }
        else if (amount > p_amount_clusters) {
            lower_distance = radius;
        }
        else if (amount < p_amount_clusters) {
            upper_distance = radius;
        }
    }

    return result;
}


std::size_t ordering_analyser::extract_cluster_amount(const ordering & p_ordering, const double p_radius) {
    std::size_t amount_clusters = 1;

    bool cluster_start = false;
    bool cluster_pick = false;
    bool total_similariry = true;

    double previous_cluster_distance = 0.0;
    double previous_distance = -1.0;

    for (auto & distance : p_ordering) {
        if (distance >= p_radius) {
            if (!cluster_start) {
                cluster_start = true;
                amount_clusters++;
            }
            else {
                if ( (distance < previous_cluster_distance) && (!cluster_pick) ) {
                    cluster_pick = true;
                }
                else if ( (distance > previous_cluster_distance) && (cluster_pick) ) {
                    cluster_pick = false;
                    amount_clusters += 1;
                }
            }

            previous_cluster_distance = distance;
        }
        else {
            cluster_start = false;
            cluster_pick = false;
        }

        if ( (previous_distance >= 0) && (previous_distance != distance) ) {
            total_similariry = false;
        }

        previous_distance = distance;
    }

    if ( (total_similariry) && (previous_distance > p_radius) ) {
        amount_clusters = 0;
    }

    return amount_clusters;
}


}

}