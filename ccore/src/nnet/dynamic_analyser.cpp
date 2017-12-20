/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "dynamic_analyser.hpp"

#include <sstream>
#include <stdexcept>


namespace ccore {

namespace nnet {


spike::spike(const std::size_t p_begin, const std::size_t p_end) {
    if (p_end < p_begin) {
        std::stringstream stream;
        stream << __FUNCTION__ << ": End time '" << p_end << "' of the spike cannot be less or equal to begin time '" << p_begin << "'.";

        throw std::invalid_argument(stream.str());
    }

    m_begin = p_begin;
    m_duration = p_end - p_begin;
    m_end = p_end;
}


std::size_t spike::get_start(void) const {
    return m_begin;
}


std::size_t spike::get_duration(void) const {
    return m_duration;
}


std::size_t spike::get_stop(void) const {
    return m_end;
}


}

}