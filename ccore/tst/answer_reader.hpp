/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
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


#include "answer.hpp"

#include "samples.hpp"

#include <map>


class answer_reader {
private:
    const static std::string PATH_SIMPLE_ANSWER_FOLDER;

    const static std::map<SAMPLE_SIMPLE, std::string> SIMPLE_ANSWER_MAP;

public:
    static answer read(const std::string & p_path);

    static answer read(const SAMPLE_SIMPLE p_sample);
};
