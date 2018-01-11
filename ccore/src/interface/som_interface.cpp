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

#include "interface/som_interface.h"


using namespace ccore::nnet;


void * som_create(const size_t num_rows, const size_t num_cols, const size_t type_conn, const void * parameters) {
    return (void *) new som(num_rows, num_cols, (som_conn_type) type_conn,  *((som_parameters *) parameters));
}


void som_destroy(const void * pointer) {
    delete (som *) pointer;
}


size_t som_train(const void * pointer, const pyclustering_package * const sample, const size_t epochs, const bool autostop) {
    dataset input_dataset;
    sample->extract(input_dataset);

    size_t result = ((som *) pointer)->train(input_dataset, epochs, autostop);

    return result;
}


size_t som_simulate(const void * pointer, const pyclustering_package * const p_pattern) {
    pattern input_pattern;
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
    dataset weights;
    ((som *) pointer)->allocate_weights(weights);

    pyclustering_package * package = create_package(&weights);

    return package;
}


pyclustering_package * som_get_capture_objects(const void * pointer) {
    som_gain_sequence capture_objects;
    ((som *) pointer)->allocate_capture_objects(capture_objects);

    pyclustering_package * package = create_package(&capture_objects);

    return package;
}


pyclustering_package * som_get_awards(const void * pointer) {
    som_award_sequence awards;
    ((som *) pointer)->allocate_awards(awards);
    pyclustering_package * package = create_package(&awards);

    return package;
}


pyclustering_package * som_get_neighbors(const void * pointer) {
    pyclustering_package * package = nullptr;

    std::vector<std::vector<size_t> > neighbors;
    ((som *) pointer)->allocate_neighbors(neighbors);
    if (!neighbors.empty()) {
        package = create_package(&neighbors);
    }

    return package;
}
