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

#include <thread>

#include "answer.hpp"
#include "answer_reader.hpp"
#include "samples.hpp"

#include <pyclustering/cluster/silhouette_ksearch.hpp>


using namespace pyclustering;
using namespace pyclustering::clst;


static void template_correct_ksearch(
    const dataset_ptr & p_data, 
    const answer & p_answer, 
    const std::size_t p_kmin, 
    const std::size_t p_kmax, 
    const silhouette_ksearch_allocator::ptr & p_allocator = std::make_shared<kmeans_allocator>())
{
    const std::size_t attempts = 5;
    bool testing_result = false;

    for (std::size_t i = 0; i < attempts; i++) {
        silhouette_ksearch_data result;
        silhouette_ksearch(p_kmin, p_kmax, p_allocator).process(*p_data, result);

        ASSERT_LE(-1.0, result.get_score());
        ASSERT_GE(1.0, result.get_score());
        ASSERT_EQ(p_kmax - p_kmin, result.scores().size());

        const std::size_t upper_limit = p_answer.clusters().size() + 1;
        const std::size_t lower_limit = p_answer.clusters().size() > 1 ? p_answer.clusters().size() - 1 : 1;

        if ((result.get_amount() > upper_limit) || (result.get_amount() < lower_limit)) {
            std::this_thread::sleep_for(std::chrono::duration<int, std::milli>(25));
            continue;
        }

        testing_result = true;
        break;
    }

    ASSERT_TRUE(testing_result);
}


TEST(utest_silhouette_ksearch, correct_ksearch_simple01_kmeans) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple01_kmedians) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01),
        2, 10, std::make_shared<kmedians_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple01_kmedoids) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01),
        2, 10, std::make_shared<kmedoids_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple02) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple02_kmedians) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02),
        2, 10, std::make_shared<kmedians_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple02_kmedoids) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02),
        2, 10, std::make_shared<kmedoids_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple03) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple05) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple06) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple07) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple08) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_08),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple10) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_10),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple11) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple12) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12),
        2, 10, std::make_shared<kmeans_allocator>());
}

TEST(utest_silhouette_ksearch, correct_ksearch_simple13) {
    template_correct_ksearch(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13), answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_13),
        2, 10, std::make_shared<kmeans_allocator>());
}


static void template_random_state(
    const std::size_t p_kmin,
    const std::size_t p_kmax,
    const silhouette_ksearch_allocator::ptr & p_allocator = std::make_shared<kmeans_allocator>(),
    const long long p_random_state = RANDOM_STATE_CURRENT_TIME)
{
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);

    silhouette_ksearch_data result_1, result_2;
    silhouette_ksearch(p_kmin, p_kmax, p_allocator, p_random_state).process(*data, result_1);
    silhouette_ksearch(p_kmin, p_kmax, p_allocator, p_random_state).process(*data, result_2);

    ASSERT_EQ(result_1, result_2);
}


TEST(utest_silhouette_ksearch, random_state_1_kmeans) {
    template_random_state(2, 10, std::make_shared<kmeans_allocator>(), 1);
}

TEST(utest_silhouette_ksearch, random_state_2_kmeans) {
    template_random_state(2, 10, std::make_shared<kmeans_allocator>(), 2);
}

TEST(utest_silhouette_ksearch, random_state_500_kmeans) {
    template_random_state(2, 10, std::make_shared<kmeans_allocator>(), 500);
}

TEST(utest_silhouette_ksearch, random_state_10000_kmeans) {
    template_random_state(2, 10, std::make_shared<kmeans_allocator>(), 10000);
}

TEST(utest_silhouette_ksearch, random_state_1_kmedians) {
    template_random_state(2, 10, std::make_shared<kmedians_allocator>(), 1);
}

TEST(utest_silhouette_ksearch, random_state_2_kmedians) {
    template_random_state(2, 10, std::make_shared<kmedians_allocator>(), 2);
}

TEST(utest_silhouette_ksearch, random_state_500_kmedians) {
    template_random_state(2, 10, std::make_shared<kmedians_allocator>(), 500);
}

TEST(utest_silhouette_ksearch, random_state_10000_kmedians) {
    template_random_state(2, 10, std::make_shared<kmedians_allocator>(), 10000);
}

TEST(utest_silhouette_ksearch, random_state_1_kmedoids) {
    template_random_state(2, 10, std::make_shared<kmedoids_allocator>(), 1);
}

TEST(utest_silhouette_ksearch, random_state_2_kmedoids) {
    template_random_state(2, 10, std::make_shared<kmedoids_allocator>(), 2);
}

TEST(utest_silhouette_ksearch, random_state_500_kmedoids) {
    template_random_state(2, 10, std::make_shared<kmedoids_allocator>(), 500);
}

TEST(utest_silhouette_ksearch, random_state_10000_kmedoids) {
    template_random_state(2, 10, std::make_shared<kmedoids_allocator>(), 10000);
}
