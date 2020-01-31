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


#include "answer_reader.hpp"

#include <fstream>
#include <sstream>


#if defined _WIN32 || defined __CYGWIN__
    #define separator std::string("\\")
#else
    #define separator std::string("/")
#endif


const std::string answer_reader::PATH_SIMPLE_ANSWER_FOLDER =
    ".." + separator +
    ".." + separator +
    "pyclustering" + separator +
    "samples" + separator +
    "samples" + separator +
    "simple" + separator;


const std::map<SAMPLE_SIMPLE, std::string> answer_reader::SIMPLE_ANSWER_MAP = {
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_01, PATH_SIMPLE_ANSWER_FOLDER + "Simple01.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_02, PATH_SIMPLE_ANSWER_FOLDER + "Simple02.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_03, PATH_SIMPLE_ANSWER_FOLDER + "Simple03.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_04, PATH_SIMPLE_ANSWER_FOLDER + "Simple04.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_05, PATH_SIMPLE_ANSWER_FOLDER + "Simple05.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_06, PATH_SIMPLE_ANSWER_FOLDER + "Simple06.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_07, PATH_SIMPLE_ANSWER_FOLDER + "Simple07.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_08, PATH_SIMPLE_ANSWER_FOLDER + "Simple08.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_09, PATH_SIMPLE_ANSWER_FOLDER + "Simple09.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_10, PATH_SIMPLE_ANSWER_FOLDER + "Simple10.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_11, PATH_SIMPLE_ANSWER_FOLDER + "Simple11.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_12, PATH_SIMPLE_ANSWER_FOLDER + "Simple12.answer" },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_13, PATH_SIMPLE_ANSWER_FOLDER + "Simple13.answer" }
};

answer answer_reader::read(const std::string & p_path) {
    answer result;

    std::ifstream file_stream(p_path);

    std::string line;
    std::size_t index_point = 0;

    while(std::getline(file_stream, line)) {
        if (line[0] == 'n') {
            result.noise().push_back(index_point);
            index_point++;

            continue;
        }

        std::size_t index_cluster = std::stoul(line);
        if (index_cluster >= result.clusters().size()) {
            result.clusters().push_back({ index_point });
        }
        else {
            result.clusters().at(index_cluster).push_back(index_point);
        }

        index_point++;
    }

    file_stream.close();

    for (auto & current_cluster : result.clusters()) {
        result.cluster_lengths().push_back(current_cluster.size());
    }

    return result;
}


answer answer_reader::read(const SAMPLE_SIMPLE p_sample) {
    return read(SIMPLE_ANSWER_MAP.at(p_sample));
}
