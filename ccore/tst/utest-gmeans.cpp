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


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/cluster/gmeans.hpp>

#include "answer.hpp"
#include "answer_reader.hpp"


using namespace pyclustering::clst;
using namespace pyclustering::utils::metric;


static void
template_gmeans_clustering(
    const dataset_ptr & p_data,
    const std::size_t p_k_init,
    const answer & p_answer)
{
    const std::size_t attempts = 10;
    for (std::size_t i = 0; i < attempts; i++) {
        gmeans_data output_result;
        gmeans(1, gmeans::DEFAULT_TOLERANCE, 3).process(*p_data, output_result);

        auto expected_cluster_lengths = p_answer.cluster_lengths();
        auto expected_clusters = p_answer.clusters();
        std::sort(expected_cluster_lengths.begin(), expected_cluster_lengths.end());

        auto clusters = output_result.clusters();
        auto centers = output_result.centers();
        std::vector<std::size_t> actual_cluster_lengths;
        std::set<std::size_t> unique;

        for (const auto & item : clusters) {
            actual_cluster_lengths.push_back(item.size());
            unique.insert(item.begin(), item.end());
        }

        std::sort(actual_cluster_lengths.begin(), actual_cluster_lengths.end());

        if (expected_clusters.size() != clusters.size()) { continue; }
        if (expected_clusters.size() != centers.size()) { continue; }
        if (p_data->size() != unique.size()) { continue; }
        if (expected_cluster_lengths != actual_cluster_lengths) { continue; }

        if (clusters.size() > 1) {
            if (output_result.wce() <= 0.0) { continue; }
        }
        else {
            if (output_result.wce() < 0.0) { continue; }
        }

        return;
    }

    FAIL();
}


TEST(utest_gmeans, simple01) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01));
}

TEST(utest_gmeans, simple02) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02));
}

TEST(utest_gmeans, simple03) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03));
}

TEST(utest_gmeans, simple05) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05));
}

TEST(utest_gmeans, simple06) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06));
}

TEST(utest_gmeans, simple07) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07));
}

TEST(utest_gmeans, simple08) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08));
}

TEST(utest_gmeans, simple09) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09));
}

TEST(utest_gmeans, simple10) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10));
}

TEST(utest_gmeans, simple11) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11));
}

TEST(utest_gmeans, simple12) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12));
}

TEST(utest_gmeans, simple13) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13), 1, 
                               answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13));
}
