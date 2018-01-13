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


#include "gtest/gtest.h"

#include "samples.hpp"

#include "nnet/som.hpp"

#include <algorithm>
#include <numeric>


using namespace ccore::nnet;


static void template_create_delete(const unsigned int rows, const unsigned int cols, const som_conn_type conn_type, const som_init_type init_type) {
    som_parameters params;
    params.init_type = init_type;

    som * som_map = new som(rows, cols, conn_type, params);
    ASSERT_EQ(rows * cols, som_map->get_size());

    delete som_map;
}


TEST(utest_som, create_delete_conn_func_neighbor) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_grid_eight) {
    template_create_delete(10, 10, som_conn_type::SOM_GRID_EIGHT, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_grid_four) {
    template_create_delete(10, 10, som_conn_type::SOM_GRID_FOUR, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_honeycomb) {
  template_create_delete(10, 10, som_conn_type::SOM_HONEYCOMB, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_init_centroid) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM_CENTROID);
}

TEST(utest_som, create_delete_init_surface) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM_SURFACE);
}

TEST(utest_som, create_delete_init_uniform_grid) {
    template_create_delete(10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_UNIFORM_GRID);
}


static void template_award_neurons(const std::shared_ptr<dataset> & data,
                                   const unsigned int epouchs, 
                                   const bool autostop, 
                                   const unsigned int rows, 
                                   const unsigned int cols, 
                                   const som_conn_type conn_type, 
                                   const std::vector<unsigned int> & expected_result) {

    som_parameters params;
    som som_map(rows, cols, conn_type, params);
    som_map.train(*data.get(), epouchs, autostop);

    size_t winners = som_map.get_winner_number();
    ASSERT_EQ(expected_result.size(), winners);

    som_award_sequence awards;
    som_map.allocate_awards(awards);

    std::sort(awards.begin(), awards.end());

    ASSERT_EQ(expected_result.size(), awards.size());

    for (size_t i = 0; i < awards.size(); i++) {
        ASSERT_EQ(expected_result[i], awards[i]);
    }

    som_gain_sequence captured_objects;
    som_map.allocate_capture_objects(captured_objects);

    size_t total_capture_points = 0;
    for (size_t i = 0; i < captured_objects.size(); i++) {
        total_capture_points += captured_objects[i].size();
    }

    size_t expected_capture_points = std::accumulate(expected_result.begin(), expected_result.end(), (std::size_t) 0);
    ASSERT_EQ(expected_capture_points, total_capture_points);
}

TEST(utest_som, awards_two_clusters_func_neighbor) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_two_clusters_func_neighbor_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_eight) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_eight_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_four) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_four_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_two_clusters_honeycomb) {
    std::vector<unsigned int> expected_awards = {5, 5};
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, false, 1, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_01, 100, false, 2, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, awards_two_clusters_honeycomb_autostop) {
    std::vector<unsigned int> expected_awards = { 5, 5 };
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_award_neurons(sample_simple_01, 100, true, 1, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_01, 100, true, 2, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, awards_clusters_func_neighbor_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_clusters_grid_eight_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_clusters_func_grid_four_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_clusters_honeycomb_simple_sample_02) {
    std::vector<unsigned int> expected_awards = { 5, 8, 10 };
    std::shared_ptr<dataset> sample_simple_02 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_award_neurons(sample_simple_02, 100, false, 1, 3, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_02, 100, false, 3, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, awards_clusters_func_neighbor_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_clusters_grid_eight_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_clusters_func_grid_four_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_clusters_honeycomb_simple_sample_03) {
    std::vector<unsigned int> expected_awards = { 10, 10, 10, 30 };
    std::shared_ptr<dataset> sample_simple_03 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_award_neurons(sample_simple_03, 100, false, 1, 4, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(sample_simple_03, 100, false, 2, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, double_training) {
    som_parameters params;
    som som_map(2, 2, som_conn_type::SOM_GRID_EIGHT, params);

    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    som_map.train(*sample_simple_01.get(), 100, false);
    som_map.train(*sample_simple_01.get(), 100, false);

    som_gain_sequence captured_objects;
    som_map.allocate_capture_objects(captured_objects);

    size_t total_capture_points = 0;
    for (size_t i = 0; i < captured_objects.size(); i++) {
        total_capture_points += captured_objects[i].size();
    }

    ASSERT_EQ(sample_simple_01->size(), total_capture_points);

    som_award_sequence awards;
    som_map.allocate_awards(awards);

    size_t number_awards = std::accumulate(awards.begin(), awards.end(), (std::size_t) 0);

    ASSERT_EQ(sample_simple_01->size(), number_awards);
}


static void template_simulate_check_winners(const som_conn_type conn_type, const bool autostop) {
    som_parameters params;
    std::shared_ptr<dataset> sample_simple_01 = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    som som_map(1, 2, conn_type, params);
    som_map.train(*sample_simple_01.get(), 100, autostop);

    std::vector<std::size_t> expected_winners = { 0, 1 };
    for (std::size_t i = 0; i < sample_simple_01->size(); i++) {
        std::size_t index_winner = som_map.simulate(sample_simple_01->at(i));
        if ( (i == 0) && (index_winner != 0) ) {
            expected_winners = { 1, 0 };
        }

        if (i < 5)
            EXPECT_EQ(expected_winners[0], index_winner);
        else
            EXPECT_EQ(expected_winners[1], index_winner);
    }
}


TEST(utest_som, simulate_func_neighbors_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_FUNC_NEIGHBOR, true);
}

TEST(utest_som, simulate_grid_four_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_FOUR, true);
}

TEST(utest_som, simulate_grid_eight_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_EIGHT, true);
}

TEST(utest_som, simulate_honeycomb_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_HONEYCOMB, true);
}

TEST(utest_som, simulate_func_neighbors_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_FUNC_NEIGHBOR, false);
}

TEST(utest_som, simulate_grid_four_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_FOUR, false);
}

TEST(utest_som, simulate_grid_eight_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_GRID_EIGHT, false);
}

TEST(utest_som, simulate_honeycomb_without_autostop) {
    template_simulate_check_winners(som_conn_type::SOM_HONEYCOMB, false);
}