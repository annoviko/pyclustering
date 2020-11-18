/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>


/**
 *
 * @brief   Deallocate pyclustering package.
 *
 * @param[in]: package: pointer to clustering results.
 *
 */
extern "C" DECLARATION void free_pyclustering_package(pyclustering_package * package);

