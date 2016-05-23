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

#include "samples.hpp"

#include <fstream>
#include <sstream>
#include <iostream>


#if defined _WIN32 || defined __CYGWIN__
    #define separator std::string("\\")
#else
    #define separator std::string("/")
#endif


const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_FOLDER = ".." + separator + ".." + separator + "pyclustering" + separator + "samples" + separator + "samples";


const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_01 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple01.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_02 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple02.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_03 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple03.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_04 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple04.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_05 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple05.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_06 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple06.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_07 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple07.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_08 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple08.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_09 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple09.txt";
const std::string simple_sample_factory::PATH_SAMPLE_SIMPLE_10 = PATH_SAMPLE_SIMPLE_FOLDER + separator + "SampleSimple10.txt";


const simple_sample_factory::map_sample simple_sample_factory::m_sample_table = {
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_01, simple_sample_factory::PATH_SAMPLE_SIMPLE_01 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_02, simple_sample_factory::PATH_SAMPLE_SIMPLE_02 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_03, simple_sample_factory::PATH_SAMPLE_SIMPLE_03 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_04, simple_sample_factory::PATH_SAMPLE_SIMPLE_04 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_05, simple_sample_factory::PATH_SAMPLE_SIMPLE_05 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_06, simple_sample_factory::PATH_SAMPLE_SIMPLE_06 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_07, simple_sample_factory::PATH_SAMPLE_SIMPLE_07 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_08, simple_sample_factory::PATH_SAMPLE_SIMPLE_08 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_09, simple_sample_factory::PATH_SAMPLE_SIMPLE_09 },
    { SAMPLE_SIMPLE::SAMPLE_SIMPLE_10, simple_sample_factory::PATH_SAMPLE_SIMPLE_10 },
};


std::shared_ptr<dataset> simple_sample_factory::create_sample(const SAMPLE_SIMPLE sample) {
    std::shared_ptr<dataset> sample_data(new dataset);
    size_t sample_dimension = 0;

    const std::string path_sample = m_sample_table.at(sample);
    
    std::ifstream file_sample(path_sample);
    if (file_sample.is_open()) {
        std::string file_line;

        while(std::getline(file_sample, file_line)) {
            double value = 0.0;
            point sample_point;

            std::istringstream stream_value(file_line);

            while(stream_value >> value) {
                sample_point.push_back(value);
            }

            if (sample_dimension == 0) {
                sample_dimension = sample_point.size();
            }
            else {
                if (sample_dimension != sample_point.size()) {
                    throw std::runtime_error("Points from input data set should have the same dimension.");
                }
            }

            sample_data->push_back(sample_point);
        }
    }

    return sample_data;
}
