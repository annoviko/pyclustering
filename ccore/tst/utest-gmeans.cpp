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
    const answer & p_answer,
    const long long p_kmax = gmeans::IGNORE_KMAX)
{
    const std::size_t attempts = 10;
    for (std::size_t i = 0; i < attempts; i++) {
        gmeans_data output_result;
        gmeans(1, gmeans::DEFAULT_TOLERANCE, 3, p_kmax).process(*p_data, output_result);

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


static void
template_gmeans_clustering(
    const dataset_ptr & p_data,
    const std::size_t p_k_init,
    const std::vector<std::size_t> & p_expected_cluster_lengths,
    const long long p_kmax = gmeans::IGNORE_KMAX)
{
    const std::size_t attempts = 10;
    for (std::size_t i = 0; i < attempts; i++) {
        gmeans_data output_result;
        gmeans(1, gmeans::DEFAULT_TOLERANCE, 3, p_kmax).process(*p_data, output_result);

        auto clusters = output_result.clusters();
        auto centers = output_result.centers();
        std::vector<std::size_t> actual_cluster_lengths;
        std::set<std::size_t> unique;

        for (const auto & item : clusters) {
            actual_cluster_lengths.push_back(item.size());
            unique.insert(item.begin(), item.end());
        }

        std::sort(actual_cluster_lengths.begin(), actual_cluster_lengths.end());

        if (p_expected_cluster_lengths.size() != clusters.size()) { continue; }
        if (p_expected_cluster_lengths.size() != centers.size()) { continue; }
        if (p_data->size() != unique.size()) { continue; }
        if (p_expected_cluster_lengths != actual_cluster_lengths) { continue; }

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


static void
template_gmeans_clustering(
    const dataset_ptr & p_data,
    const std::size_t p_k_init,
    const std::size_t & p_expected_amount_clusters,
    const long long p_kmax = gmeans::IGNORE_KMAX,
    const long long p_random_state = RANDOM_STATE_CURRENT_TIME)
{
    const std::size_t attempts = 10;
    for (std::size_t i = 0; i < attempts; i++) {
        gmeans_data output_result;
        gmeans(1, gmeans::DEFAULT_TOLERANCE, 3, p_kmax, p_random_state).process(*p_data, output_result);

        auto clusters = output_result.clusters();
        auto centers = output_result.centers();
        std::set<std::size_t> unique;

        for (const auto & item : clusters) {
            unique.insert(item.begin(), item.end());
        }

        if (p_expected_amount_clusters != clusters.size()) { continue; }
        if (p_expected_amount_clusters != centers.size()) { continue; }
        if (p_data->size() != unique.size()) { continue; }

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

TEST(utest_gmeans, simple01_kmax_1) {
    std::vector<std::size_t> expected_length = { 10 };
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1,
        expected_length, 1);
}

TEST(utest_gmeans, simple01_kmax_2) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1,
        answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2);
}

TEST(utest_gmeans, simple01_kmax_10) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 1,
        answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 10);
}

TEST(utest_gmeans, simple02) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1, 
        answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02));
}

TEST(utest_gmeans, simple02_kmax_1) {
    std::vector<std::size_t> expected_length = { 23 };
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1,
        expected_length, 1);
}

TEST(utest_gmeans, simple02_kmax_2) {
    std::vector<std::size_t> expected_length = { 8, 15 };
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1,
        expected_length, 2);
}

TEST(utest_gmeans, simple02_kmax_3) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1,
        answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3);
}

TEST(utest_gmeans, simple02_kmax_4) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1,
        answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 4);
}

TEST(utest_gmeans, simple02_kmax_10) {
    template_gmeans_clustering(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 1,
        answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 10);
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

TEST(utest_gmeans, hepta_kmax_01) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 1, 1, 1);
}

TEST(utest_gmeans, hepta_kmax_02) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 2, 2, 1);
}

TEST(utest_gmeans, hepta_kmax_03) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 3, 3, 1);
}

TEST(utest_gmeans, hepta_kmax_04) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 4, 4, 1);
}

TEST(utest_gmeans, hepta_kmax_05) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 5, 5, 1);
}

TEST(utest_gmeans, hepta_kmax_06) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 6, 6, 1);
}

TEST(utest_gmeans, hepta_kmax_07) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 7, 7, 1);
}

TEST(utest_gmeans, hepta_kmax_08) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 7, 8, 1);
}

TEST(utest_gmeans, hepta_kmax_09) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 7, 9, 1);
}

TEST(utest_gmeans, hepta_kmax_10) {
    template_gmeans_clustering(fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA), 1, 7, 10, 1);
}
