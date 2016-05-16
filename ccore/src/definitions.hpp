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

#ifndef SRC_DEFINITIONS_HPP_
#define SRC_DEFINITIONS_HPP_


#include <memory>
#include <vector>


#if defined (__GNUC__) && defined(__unix__)
    #define DECLARATION __attribute__ ((__visibility__("default")))
#elif defined (WIN32)
    #define DECLARATION __declspec(dllexport)
#else
    #error Unsupported platform
#endif


using point         = std::vector<double>;
using point_ptr     = std::shared_ptr<point>;

using dataset       = std::vector<point>;
using dataset_ptr   = std::shared_ptr<dataset>;


/* TODO: use pyclustering_package instead of this */
typedef struct data_representation {
public:
    unsigned int            size;
    unsigned int            dimension;
    double                  ** objects;
} data_representation;


#endif
