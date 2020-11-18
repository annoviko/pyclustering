/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/cluster/random_center_initializer.hpp>


using namespace pyclustering::clst;


static void template_random_seed(
    const std::size_t p_random_seed, 
    const std::size_t p_amount,
    const dataset_ptr p_data,
    const std::size_t p_repeat = 1)
{
    for (std::size_t i = 0; i < p_repeat; i++) {
        dataset centers1, centers2;

        random_center_initializer(p_amount, p_random_seed).initialize(*p_data, centers1);
        random_center_initializer(p_amount, p_random_seed).initialize(*p_data, centers2);

        ASSERT_EQ(centers1, centers2);
    }
}


TEST(utest_random_center_initializer, random_seed_n_1) {
    template_random_seed(1, 1, simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01));
}

TEST(utest_random_center_initializer, random_seed_n_2) {
    template_random_seed(1, 2, simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01));
}

TEST(utest_random_center_initializer, random_seed_n_3) {
    template_random_seed(1, 3, simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01));
}

TEST(utest_random_center_initializer, random_seed_n_4) {
    template_random_seed(1, 4, simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01));
}

TEST(utest_random_center_initializer, random_seed_n_5) {
    template_random_seed(1, 5, simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01));
}

TEST(utest_random_center_initializer, random_seed_n_2_continuous) {
    template_random_seed(1, 2, simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 20);
}
