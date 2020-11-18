/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>


template <class ContainerType>
static std::shared_ptr<pyclustering_package> pack(const ContainerType & container) {
    pyclustering_package * package = create_package(&container);

    std::shared_ptr<pyclustering_package> shared_package(package);

    return shared_package;
}