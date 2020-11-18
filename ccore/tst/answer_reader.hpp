/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
