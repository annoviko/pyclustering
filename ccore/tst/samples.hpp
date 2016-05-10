#ifndef _SAMPLES_H_
#define _SAMPLES_H_

#include <string>
#include <vector>
#include <memory>
#include <map>


typedef std::vector<double>                     point_t;
typedef std::vector<point_t>                    dataset_t;


/***********************************************************************************************
*
* @brief   Sample from set SIMPLE SAMPLE that is used for easy testing of clustering algorithms.
*
***********************************************************************************************/
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
};


/***********************************************************************************************
*
* @brief   Factory of samples from SIMPLE SAMPLE set.
*
***********************************************************************************************/
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

public:
    /***********************************************************************************************
    *
    * @brief   Creates sample for cluster analysis.
    *
    * @param[in] sample: sample that should be created.
    *
    * @return  Smart pointer to created dataset.
    *
    ***********************************************************************************************/
    static std::shared_ptr<dataset_t> create_sample(const SAMPLE_SIMPLE sample);
};


#endif