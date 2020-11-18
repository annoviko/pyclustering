/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   Returns text description of the library
 *
 * @returns Returns const char pointer to text library description.
 *
 */
extern "C" DECLARATION void * get_interface_description();


/**
 *
 * @brief   Returns version of the library interface
 *
 * @returns Returns const char pointer to version of the library interface.
 *
 */
extern "C" DECLARATION void * get_interface_version();