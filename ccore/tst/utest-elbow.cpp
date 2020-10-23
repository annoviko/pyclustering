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


#include "utest-elbow.hpp"

#include "samples.hpp"

#include <pyclustering/cluster/random_center_initializer.hpp>


#define IGNORE_CLUSTERS_CHECK       (std::size_t) -1


TEST(utest_elbow, simple_01) {
  elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1, 10);
}

TEST(utest_elbow, simple_01_random_initializer) {
  elbow_template<random_center_initializer>(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), 2, 1, 10);
}

TEST(utest_elbow, simple_01_border_step) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), IGNORE_CLUSTERS_CHECK, 1, 3, 1);
}

TEST(utest_elbow, simple_01_step_2) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), IGNORE_CLUSTERS_CHECK, 1, 10, 2);
}

TEST(utest_elbow, simple_01_step_3) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), IGNORE_CLUSTERS_CHECK, 1, 10, 3);
}

TEST(utest_elbow, simple_01_step_4) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), IGNORE_CLUSTERS_CHECK, 1, 10, 4);
}

TEST(utest_elbow, simple_02) {
  elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 1, 10);
}

TEST(utest_elbow, simple_02_step_2) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 1, 10, 2);
}

TEST(utest_elbow, simple_02_step_3) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), IGNORE_CLUSTERS_CHECK, 1, 10, 3);
}

TEST(utest_elbow, simple_02_step_4) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), IGNORE_CLUSTERS_CHECK, 1, 10, 4);
}

TEST(utest_elbow, simple_02_random_initializer) {
  elbow_template<random_center_initializer>(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), 3, 1, 10);
}

TEST(utest_elbow, simple_03) {
  elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), 4, 1, 10);
}

TEST(utest_elbow, simple_05) {
  elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 4, 1, 10);
}

TEST(utest_elbow, simple_05_step_2) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05), 4, 1, 10, 3);
}

TEST(utest_elbow, simple_06) {
  elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_06), 2, 1, 10);
}

TEST(utest_elbow, one_dimensional_simple_07) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_07), 2, 1, 10);
}

TEST(utest_elbow, simple_09) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), 2, 1, 10);
}

TEST(utest_elbow, three_dimensional_simple_11) {
    elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_11), 2, 1, 10);
}

TEST(utest_elbow, simple_12) {
  elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12), 3, 1, 10);
}

TEST(utest_elbow, exception_kmin_zero) {
    EXPECT_THROW({ 
        elbow<kmeans_plus_plus>(0, 10); 
    }, std::invalid_argument);
}

TEST(utest_elbow, exception_kmax_less_than_kmin) {
    EXPECT_THROW({
        elbow<kmeans_plus_plus>(10, 1);
    }, std::invalid_argument);
}

TEST(utest_elbow, exception_kmax_less_than_3_kmin) {
    EXPECT_THROW({
        elbow<kmeans_plus_plus>(1, 2);
    }, std::invalid_argument);
}

TEST(utest_elbow, exception_kstep_too_big) {
    EXPECT_THROW({
        elbow<kmeans_plus_plus>(1, 10, 5, RANDOM_STATE_CURRENT_TIME);
    }, std::invalid_argument);
}

TEST(utest_elbow, exception_kmax_greater_than_data) {
    EXPECT_THROW({
        elbow_template(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), IGNORE_CLUSTERS_CHECK, 1, 11, 1);
    }, std::invalid_argument);
}