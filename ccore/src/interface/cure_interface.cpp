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

#include <pyclustering/interface/cure_interface.h>

#include <pyclustering/cluster/cure.hpp>


void * cure_algorithm(const pyclustering_package * const sample, const size_t number_clusters, const size_t number_repr_points, const double compression) {
    pyclustering::dataset input_dataset;
    sample->extract(input_dataset);

    pyclustering::clst::cure solver(number_clusters, number_repr_points, compression);

    pyclustering::clst::cure_data * output_result = new pyclustering::clst::cure_data();
    solver.process(input_dataset, *output_result);

    return output_result;
}


void cure_data_destroy(void * pointer_cure_data) {
    delete (pyclustering::clst::cure *) pointer_cure_data;
}


pyclustering_package * cure_get_clusters(void * pointer_cure_data) {
    pyclustering::clst::cure_data & output_result = (pyclustering::clst::cure_data &) *((pyclustering::clst::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(&output_result.clusters());
    return package;
}


pyclustering_package * cure_get_representors(void * pointer_cure_data) {
    pyclustering::clst::cure_data & output_result = (pyclustering::clst::cure_data &) *((pyclustering::clst::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(&output_result.representors());
    return package;
}


pyclustering_package * cure_get_means(void * pointer_cure_data) {
    pyclustering::clst::cure_data & output_result = (pyclustering::clst::cure_data &) *((pyclustering::clst::cure_data *)pointer_cure_data);

    pyclustering_package * package = create_package(&output_result.means());
    return package;
}
