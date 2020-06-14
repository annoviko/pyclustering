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
