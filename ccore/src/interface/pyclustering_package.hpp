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

#ifndef SRC_INTERFACE_PYCLUSTERING_PACKAGE_HPP_
#define SRC_INTERFACE_PYCLUSTERING_PACKAGE_HPP_


#include <cstddef>
#include <vector>

#include "definitions.hpp"


typedef enum pyclustering_type_data {
    PYCLUSTERING_TYPE_INT               = 0,
    PYCLUSTERING_TYPE_UNSIGNED_INT      = 1,
    PYCLUSTERING_TYPE_FLOAT             = 2,
    PYCLUSTERING_TYPE_DOUBLE            = 3,
    PYCLUSTERING_TYPE_LONG              = 4,
    PYCLUSTERING_TYPE_RESERVED          = 5,
    PYCLUSTERING_TYPE_LIST              = 6,
    PYCLUSTERING_TYPE_SIZE_T            = 7,
    PYCLUSTERING_TYPE_UNDEFINED         = 8,
} pyclustering_type_data;


typedef struct pyclustering_package {
public:
    unsigned int size;
    unsigned int type;      /* pyclustering type data    */
    void * data;            /* pointer to data           */

public:
    pyclustering_package(void);

    pyclustering_package(unsigned int package_type);

    ~pyclustering_package(void);

} pyclustering_package;


template <typename TypeValue>
pyclustering_package * create_package(const std::vector<TypeValue> * const data) {
    pyclustering_type_data type_package = PYCLUSTERING_TYPE_UNDEFINED;
    if (std::is_same<TypeValue, int>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_INT;
    }
    else if (std::is_same<TypeValue, unsigned int>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_INT;
    }
    else if (std::is_same<TypeValue, float>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_FLOAT;
    }
    else if (std::is_same<TypeValue, double>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE;
    }
    else if (std::is_same<TypeValue, long>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_LONG;
    }
    else if (std::is_same<TypeValue, size_t>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_SIZE_T;
    }
    else {
        return nullptr;
    }

    pyclustering_package * package = new pyclustering_package((unsigned int) type_package);

    package->size = data->size();
    package->data = (void *) new TypeValue[package->size];

    for (unsigned int i = 0; i < data->size(); i++) {
        ((TypeValue *) package->data)[i] = (*data)[i];
    }

    return package;
}


template <class TypeObject>
pyclustering_package * create_package(const std::vector< std::vector<TypeObject> > * const data) {
   pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);

   package->size = data->size();
   package->data = new pyclustering_package * [package->size];

   for (unsigned int i = 0; i < package->size; i++) {
           ((pyclustering_package **) package->data)[i] = create_package(&(*data)[i]);
   }

   return package;
}


template <class type_object>
pyclustering_package * create_package(const std::vector< std::vector<type_object> * > * const data) {
   pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);

   package->size = data->size();
   package->data = new pyclustering_package * [package->size];

   for (unsigned int i = 0; i < package->size; i++) {
       ((pyclustering_package **) package->data)[i] = create_package((*data)[i]);
   }

   return package;
}


#endif
