/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include <string>
#include <vector>
#include <memory>
#include <map>

#include "definitions.hpp"


class generic_sample_factory {
public:
    /**
    *
    * @brief   Creates sample for cluster analysis.
    *
    * @param[in] sample: sample that should be created.
    *
    * @return  Smart pointer to created dataset.
    *
    */
    static std::shared_ptr<dataset> create_sample(const std::string & path_sample);
};


/**
*
* @brief   Samples from set SIMPLE SAMPLE that is used for easy testing of clustering algorithms.
*
*/
enum class SAMPLE_SIMPLE {
    SAMPLE_SIMPLE_01,
    SAMPLE_SIMPLE_02,
    SAMPLE_SIMPLE_03,
    SAMPLE_SIMPLE_04,
    SAMPLE_SIMPLE_05,
    SAMPLE_SIMPLE_06,
    SAMPLE_SIMPLE_07,
    SAMPLE_SIMPLE_08,
    SAMPLE_SIMPLE_09,
    SAMPLE_SIMPLE_10,
    SAMPLE_SIMPLE_11,
    SAMPLE_SIMPLE_12
};


/**
*
* @brief   Factory of samples from SIMPLE SAMPLE set.
*
*/
class simple_sample_factory {
private:
    typedef std::map<SAMPLE_SIMPLE, std::string>    map_sample;

private:
    const static map_sample  m_sample_table;

private:
    const static std::string PATH_SAMPLE_SIMPLE_FOLDER;
    const static std::string PATH_SAMPLE_SIMPLE_01;
    const static std::string PATH_SAMPLE_SIMPLE_02;
    const static std::string PATH_SAMPLE_SIMPLE_03;
    const static std::string PATH_SAMPLE_SIMPLE_04;
    const static std::string PATH_SAMPLE_SIMPLE_05;
    const static std::string PATH_SAMPLE_SIMPLE_06;
    const static std::string PATH_SAMPLE_SIMPLE_07;
    const static std::string PATH_SAMPLE_SIMPLE_08;
    const static std::string PATH_SAMPLE_SIMPLE_09;
    const static std::string PATH_SAMPLE_SIMPLE_10;
    const static std::string PATH_SAMPLE_SIMPLE_11;
    const static std::string PATH_SAMPLE_SIMPLE_12;

public:
    /**
    *
    * @brief   Creates sample for cluster analysis.
    *
    * @param[in] sample: sample that should be created.
    *
    * @return  Smart pointer to created dataset.
    *
    */
    static std::shared_ptr<dataset> create_sample(const SAMPLE_SIMPLE sample);

    /**
    *
    * @brief   Creates random (uniform distribution) sample for cluster analysis.
    *
    * @param[in] p_cluster_size: size of each cluster in dataset.
    * @param[in] p_clusters: amount of clusters in dataset.
    *
    * @return  Smart pointer to created dataset.
    *
    */
    static std::shared_ptr<dataset> create_random_sample(const std::size_t p_cluster_size, const std::size_t p_clusters);
};


/**
*
* @brief   Samples from set FCPS that is used for functional testing of clustering algorithms.
*
*/
enum class FCPS_SAMPLE {
    ATOM,
    CHAINLINK,
    ENGY_TIME,
    GOLF_BALL,
    HEPTA,
    LSUN,
    TARGET,
    TETRA,
    TWO_DIAMONDS,
    WING_NUT
};


/**
*
* @brief   Factory of samples from SIMPLE SAMPLE set.
*
*/
class fcps_sample_factory {
private:
    typedef std::map<FCPS_SAMPLE, std::string>    map_sample;

private:
    const static map_sample  m_sample_table;

private:
    const static std::string PATH_FCPS_SAMPLE_FOLDER;
    const static std::string PATH_SAMPLE_ATOM;
    const static std::string PATH_SAMPLE_CHAINLINK;
    const static std::string PATH_SAMPLE_ENGY_TIME;
    const static std::string PATH_SAMPLE_GOLF_BALL;
    const static std::string PATH_SAMPLE_HEPTA;
    const static std::string PATH_SAMPLE_LSUN;
    const static std::string PATH_SAMPLE_TARGET;
    const static std::string PATH_SAMPLE_TETRA;
    const static std::string PATH_SAMPLE_TWO_DIAMONDS;
    const static std::string PATH_SAMPLE_WING_NUT;

public:
    /**
    *
    * @brief   Creates sample for cluster analysis.
    *
    * @param[in] sample: sample that should be created.
    *
    * @return  Smart pointer to created dataset.
    *
    */
    static std::shared_ptr<dataset> create_sample(const FCPS_SAMPLE sample);
};
