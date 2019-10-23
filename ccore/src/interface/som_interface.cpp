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

#include <pyclustering/interface/som_interface.h>


using namespace pyclustering::nnet;


void * som_create(const size_t num_rows, const size_t num_cols, const size_t type_conn, const void * parameters) {
    return new som(num_rows, num_cols, (som_conn_type) type_conn,  *((som_parameters *) parameters));
}


void som_destroy(const void * pointer) {
    delete (som *) pointer;
}


void som_load(const void * p_pointer, const pyclustering_package * p_weights, const pyclustering_package * p_awards, const pyclustering_package * p_captured_objects) {
    pyclustering::dataset weights;
    p_weights->extract(weights);

    som_award_sequence awards = { };
    if (p_awards) {
        p_awards->extract(awards);
    }

    som_gain_sequence captured_objects = { };
    if (p_captured_objects) {
        p_captured_objects->extract(captured_objects);
    }

    ((som *) p_pointer)->load(weights, awards, captured_objects);
}


size_t som_train(const void * pointer, const pyclustering_package * const sample, const size_t epochs, const bool autostop) {
    pyclustering::dataset input_dataset;
    sample->extract(input_dataset);

    size_t result = ((som *) pointer)->train(input_dataset, epochs, autostop);

    return result;
}


size_t som_simulate(const void * pointer, const pyclustering_package * const p_pattern) {
    pyclustering::pattern input_pattern;
    p_pattern->extract(input_pattern);

    return ((som *) pointer)->simulate(input_pattern);
}


size_t som_get_winner_number(const void * pointer) {
    return ((som *) pointer)->get_winner_number();
}


size_t som_get_size(const void * pointer) {
    return ((som *) pointer)->get_size();
}


pyclustering_package * som_get_weights(const void * pointer) {
    const pyclustering::dataset & weights = ((som *) pointer)->get_weights();
    pyclustering_package * package = create_package(&weights);

    return package;
}


pyclustering_package * som_get_capture_objects(const void * pointer) {
    const som_gain_sequence & capture_objects = ((som *) pointer)->get_capture_objects();
    pyclustering_package * package = create_package(&capture_objects);

    return package;
}


pyclustering_package * som_get_awards(const void * pointer) {
    const som_award_sequence & awards = ((som *) pointer)->get_awards();
    pyclustering_package * package = create_package(&awards);

    return package;
}


pyclustering_package * som_get_neighbors(const void * pointer) {
    pyclustering_package * package = nullptr;

    const som_neighbor_sequence & neighbors = ((som *) pointer)->get_neighbors();
    if (!neighbors.empty()) {
        package = create_package(&neighbors);
    }

    return package;
}
