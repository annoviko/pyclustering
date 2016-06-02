/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef SRC_INTERFACE_SOM_INTERFACE_H_
#define SRC_INTERFACE_SOM_INTERFACE_H_


#include "nnet/som.hpp"

#include "interface/pyclustering_package.hpp"

#include "definitions.hpp"
#include "utils.hpp"


extern "C" DECLARATION void * som_create(const size_t num_rows, const size_t num_cols, const size_t type_conn, const void * parameters);

extern "C" DECLARATION void som_destroy(const void * pointer);

extern "C" DECLARATION size_t som_train(const void * pointer, const data_representation * const sample, const size_t num_epochs, const bool autostop);

extern "C" DECLARATION size_t som_simulate(const void * pointer, const data_representation * const pattern);

extern "C" DECLARATION size_t som_get_winner_number(const void * pointer);

extern "C" DECLARATION size_t som_get_size(const void * pointer);

extern "C" DECLARATION pyclustering_package * som_get_weights(const void * pointer);

extern "C" DECLARATION pyclustering_package * som_get_capture_objects(const void * pointer);

extern "C" DECLARATION pyclustering_package * som_get_awards(const void * pointer);

extern "C" DECLARATION pyclustering_package * som_get_neighbors(const void * pointer);


#endif
