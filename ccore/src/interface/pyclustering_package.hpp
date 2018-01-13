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

#pragma once


#include <cstddef>
#include <stdexcept>
#include <sstream>
#include <string>
#include <type_traits>
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


struct pyclustering_package {
public:
    std::size_t     size      = 0;
    unsigned int    type      = (unsigned int) PYCLUSTERING_TYPE_UNDEFINED;
    void            * data    = nullptr;

public:
    pyclustering_package(void) = default;

    pyclustering_package(const pyclustering_type_data package_type);

    ~pyclustering_package(void);

public:
    template <class TypeValue>
    auto & at(const std::size_t index) const {
        if (size <= index) {
            throw std::out_of_range("pyclustering_package::at() [" + std::to_string(__LINE__) + "]: index '" + std::to_string(index) + "' out of range (size: '" + std::to_string(size) + "').");
        }

        return ((TypeValue *) data)[index];
    }

    template <class TypeValue>
    auto & at(const std::size_t index_row, const std::size_t index_column) const {
        if (size <= index_row) {
            throw std::out_of_range("pyclustering_package::at() [" + std::to_string(__LINE__) + "]: index '" + std::to_string(index_row) + "' out of range (size: '" + std::to_string(size) + "').");
        }

        pyclustering_package * package = at<pyclustering_package *>(index_row);
        return ((TypeValue *) package->data)[index_column];
    }


    template <class TypeValue>
    void extract(std::vector<TypeValue> & container) const {
        extract(container, this);
    }


    template <class TypeValue>
    void extract(std::vector<std::vector<TypeValue>> & container) const {
        if (type != PYCLUSTERING_TYPE_LIST) {
            throw std::invalid_argument("pyclustering_package::extract() [" + std::to_string(__LINE__) + "]: argument is not 'PYCLUSTERING_TYPE_LIST').");
        }

        for (std::size_t i = 0; i < size; i++) {
            std::vector<TypeValue> subcontainer = { };
            extract(subcontainer, at<pyclustering_package *>(i));
            container.push_back(subcontainer);
        }
    }

private:
    template <class TypeValue>
    void extract(std::vector<TypeValue> & container, const pyclustering_package * const package) const {
        for (std::size_t i = 0; i < package->size; i++) {
            container.push_back(package->at<TypeValue>(i));
        }
    }
};


template <class TypeContainer>
pyclustering_package * create_package(const TypeContainer * const data) {
    using contaner_data_t = typename TypeContainer::value_type;

    pyclustering_type_data type_package = PYCLUSTERING_TYPE_UNDEFINED;
    if (std::is_same<contaner_data_t, int>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_INT;
    }
    else if (std::is_same<contaner_data_t, unsigned int>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_INT;
    }
    else if (std::is_same<contaner_data_t, float>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_FLOAT;
    }
    else if (std::is_same<contaner_data_t, double>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE;
    }
    else if (std::is_same<contaner_data_t, long>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_LONG;
    }
    else if (std::is_same<contaner_data_t, size_t>::value) {
        type_package = pyclustering_type_data::PYCLUSTERING_TYPE_SIZE_T;
    }
    else {
        return nullptr;
    }

    pyclustering_package * package = new pyclustering_package(type_package);

    package->size = data->size();
    package->data = (void *) new contaner_data_t[package->size];

    std::size_t index = 0;
    for (auto iter = std::begin(*data); iter != std::end(*data); iter++, index++) {
        ( (contaner_data_t *) package->data)[index] = *iter;
    }

    return package;
}


template <class TypeObject>
pyclustering_package * create_package(const std::vector< std::vector<TypeObject> > * const data) {
    pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);

    package->size = data->size();
    package->data = new pyclustering_package * [package->size];

    for (size_t i = 0; i < package->size; i++) {
        ((pyclustering_package **) package->data)[i] = create_package(&(*data)[i]);
    }

    return package;
}


template <class TypeObject>
pyclustering_package * create_package(const std::vector< std::vector<TypeObject> * > * const data) {
   pyclustering_package * package = new pyclustering_package(pyclustering_type_data::PYCLUSTERING_TYPE_LIST);

   package->size = data->size();
   package->data = new pyclustering_package * [package->size];

   for (size_t i = 0; i < package->size; i++) {
       ((pyclustering_package **) package->data)[i] = create_package((*data)[i]);
   }

   return package;
}