/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/


#pragma once


#include <memory>
#include <string>
#include <sstream>
#include <vector>


#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    #define DECLARATION __attribute__ ((__visibility__("default")))
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    #if defined(BUILDING_LIBRARY)
        #define DECLARATION __declspec(dllexport)
    #elif defined(BUILDING_UT_PROJECT)
        #define DECLARATION
    #else
        #define DECLARATION __declspec(dllimport)
    #endif
#else
    #error Unsupported platform
#endif


namespace pyclustering {


constexpr long long RANDOM_STATE_CURRENT_TIME = -1;     /**< Defines value of the random state that means to use current system time as a seed for random functionality. */


/*!

@brief   Defines a patten that consists of features that describe this pattern.

*/
using pattern           = std::vector<double>;

/*!

@brief   Defines shared pointer to pattern container.

*/
using pattern_ptr       = std::shared_ptr<pattern>;

/*!

@brief   Defines point that represents a container with coordinates.

*/
using point             = std::vector<double>;

/*!

@brief   Defines shared pointer to point container.

*/
using point_ptr         = std::shared_ptr<point>;

/*!

@brief   Defines dataset that represents a container with points.

*/
using dataset           = std::vector<point>;

/*!

@brief   Defines shared pointer to dataset container.

*/
using dataset_ptr       = std::shared_ptr<dataset>;


/*!

@brief   Converts an input scalar value to string representation.

@param[in] p_value: scalar value that should be represented by string.

@return  String representation of a scalar value.

*/
template<typename Type, 
    typename std::enable_if<
        std::is_scalar<Type>::value
    >::type* = nullptr
>
std::string to_string(const Type & p_value) {
    return std::to_string(p_value);
}


/*!

@brief   Converts a container to string representation.

@param[in] p_container: container that should be represented by string.

@return  String representation of a container.

*/
template<typename TypeContainer, 
    typename std::enable_if<
        std::is_same<TypeContainer,
            std::vector<typename TypeContainer::value_type, typename TypeContainer::allocator_type>
        >::value
    >::type* = nullptr
>
std::string to_string(const TypeContainer & p_container) {
    std::stringstream stream;
    stream << "[";
    for (std::size_t p_index = 0; p_index < p_container.size(); p_index++) {
        stream << pyclustering::to_string(p_container[p_index]);

        if (p_index != (p_container.size() - 1)) {
            stream << " ";
        }
    }

    stream << "]";
    return stream.str();
}


}
