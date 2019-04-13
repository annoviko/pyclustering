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


#pragma once


#include <memory>
#include <string>
#include <sstream>
#include <vector>


#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    #define DECLARATION __attribute__ ((__visibility__("default")))
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    #define DECLARATION __declspec(dllexport)
#else
    #error Unsupported platform
#endif


using pattern           = std::vector<double>;
using pattern_ptr       = std::shared_ptr<pattern>;

using point             = std::vector<double>;
using point_ptr         = std::shared_ptr<point>;

using dataset           = std::vector<point>;
using dataset_ptr       = std::shared_ptr<dataset>;



namespace std {


template <typename TypeContainer>
std::string to_string(const TypeContainer & p_container) {
    std::stringstream stream;
    stream << "[";
    for (std::size_t p_index = 0; p_index < p_container.size(); p_index++) {
        stream << std::to_string(p_container[p_index]);

        if (p_index != (p_container.size() - 1)) {
            stream << " ";
        }
    }

    stream << "]";
    return stream.str();
}


}
