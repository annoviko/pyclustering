#ifndef _UTEST_SOM_
#define _UTEST_SOM_

#include "ccore/som.h"

#include "gtest/gtest.h"

#include "samples.h"

#include <algorithm>
#include <numeric>

extern dataset SIMPLE_SAMPLE_01;
extern dataset SIMPLE_SAMPLE_02;

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



static void template_award_neurons(dataset & data, 
                                   const unsigned int epouchs, 
                                   const bool autostop, 
                                   const unsigned int rows, 
                                   const unsigned int cols, 
                                   const som_conn_type conn_type, 
                                   const std::vector<unsigned int> & expected_result) {

    som_parameters params;
	som som_map(rows, cols, conn_type, params);
	som_map.train(data, epouchs, autostop);

    std::vector<unsigned int> awards;
    som_map.allocate_awards(awards);

    std::sort(awards.begin(), awards.end());

    ASSERT_EQ(expected_result.size(), awards.size());

    for (size_t i = 0; i < awards.size(); i++) {
        ASSERT_EQ(expected_result[i], awards[i]);
    }

    std::vector<std::vector<unsigned int> > captured_objects;
    som_map.allocate_capture_objects(captured_objects);

    unsigned int total_capture_points = 0;
    for (size_t i = 0; i < captured_objects.size(); i++) {
        total_capture_points += captured_objects[i].size();
    }

    unsigned int expected_capture_points = std::accumulate(expected_result.begin(), expected_result.end(), 0);
    ASSERT_EQ(expected_capture_points, total_capture_points);
}

TEST(utest_som, awards_two_clusters_func_neighbor) {
    std::vector<unsigned int> expected_awards = {5, 5};
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 1, 2, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 2, 1, som_conn_type::SOM_FUNC_NEIGHBOR, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_eight) {
    std::vector<unsigned int> expected_awards = {5, 5};
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 1, 2, som_conn_type::SOM_GRID_EIGHT, expected_awards);
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 2, 1, som_conn_type::SOM_GRID_EIGHT, expected_awards);
}

TEST(utest_som, awards_two_clusters_grid_four) {
    std::vector<unsigned int> expected_awards = {5, 5};
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 1, 2, som_conn_type::SOM_GRID_FOUR, expected_awards);
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 2, 1, som_conn_type::SOM_GRID_FOUR, expected_awards);
}

TEST(utest_som, awards_two_clusters_honeycomb) {
    std::vector<unsigned int> expected_awards = {5, 5};
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 1, 2, som_conn_type::SOM_HONEYCOMB, expected_awards);
    template_award_neurons(SIMPLE_SAMPLE_01, 100, false, 2, 1, som_conn_type::SOM_HONEYCOMB, expected_awards);
}

TEST(utest_som, double_training) {
    som_parameters params;
	som som_map(2, 2, som_conn_type::SOM_GRID_EIGHT, params);

	som_map.train(SIMPLE_SAMPLE_01, 100, false);
    som_map.train(SIMPLE_SAMPLE_01, 100, false);

    std::vector<std::vector<unsigned int> > captured_objects;
    som_map.allocate_capture_objects(captured_objects);

    unsigned int total_capture_points = 0;
    for (size_t i = 0; i < captured_objects.size(); i++) {
        total_capture_points += captured_objects[i].size();
    }

    ASSERT_EQ(SIMPLE_SAMPLE_01.size(), total_capture_points);

    std::vector<unsigned int> awards;
    som_map.allocate_awards(awards);

    unsigned int number_awards = std::accumulate(awards.begin(), awards.end(), 0);

    ASSERT_EQ(SIMPLE_SAMPLE_01.size(), number_awards);
}

#endif
