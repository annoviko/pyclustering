#ifndef _UTEST_SOM_
#define _UTEST_SOM_

#include "ccore/som.h"

#include "gtest/gtest.h"

#include "samples.h"

extern dataset SIMPLE_SAMPLE_1;
extern dataset SIMPLE_SAMPLE_2;

static void template_create_delete(const dataset & data, const unsigned int rows, const unsigned int cols, const som_conn_type conn_type, const som_init_type init_type) {
	som_parameters params;
	params.init_type = init_type;

	som * som_map = new som(rows, cols, conn_type, params);
	ASSERT_EQ(rows * cols, som_map->get_size());

	delete som_map;
}

#if 1

TEST(utest_som, create_delete_conn_func_neighbor) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_grid_eight) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_GRID_EIGHT, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_grid_four) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_GRID_FOUR, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_conn_honeycomb) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_HONEYCOMB, som_init_type::SOM_RANDOM);
}

TEST(utest_som, create_delete_init_centroid) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM_CENTROID);
}

TEST(utest_som, create_delete_init_surface) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_RANDOM_SURFACE);
}

TEST(utest_som, create_delete_init_uniform_grid) {
	template_create_delete(SIMPLE_SAMPLE_1, 10, 10, som_conn_type::SOM_FUNC_NEIGHBOR, som_init_type::SOM_UNIFORM_GRID);
}

#endif

#endif