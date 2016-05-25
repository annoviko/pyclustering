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

#include "interface/pyclustering_package.hpp"

#include <type_traits>


pyclustering_package::pyclustering_package(void) :
        size(0),
        type(PYCLUSTERING_TYPE_UNDEFINED),
        data(nullptr)
{ }


pyclustering_package::pyclustering_package(unsigned int package_type) :
    size(0),
    type(package_type),
    data(nullptr)
{ }


pyclustering_package::~pyclustering_package(void) {
    if (type != (unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST) {
        switch(type) {
            case pyclustering_type_data::PYCLUSTERING_TYPE_INT:
                delete [] (int *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_INT:
                delete [] (unsigned int *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_FLOAT:
                delete [] (float *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE:
                delete [] (double *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_LONG:
                delete [] (long *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_SIZE_T:
                delete [] (size_t *) data;
                break;

            default:
                /* Memory Leak */
                break;
        }
    }
    else {
        for (unsigned int i = 0; i < size; i++) {
            pyclustering_package * package = ((pyclustering_package **) data)[i];
            delete package;
        }
    }
}
