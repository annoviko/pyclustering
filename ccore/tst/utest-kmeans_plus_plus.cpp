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

#include "cluster/kmeans.hpp"
#include "cluster/kmeans_plus_plus.hpp"
#include "utenv_check.hpp"


using namespace ccore::clst;


static void
template_kmeans_plus_plus_initialization(const dataset_ptr & p_data, const std::size_t p_amount)
{
    kmeans_plus_plus initializer(p_amount);

    dataset centers;
    initializer.initialize(*p_data, centers);

    ASSERT_EQ(p_amount, centers.size());
    for (auto & center : centers) {
        auto object = std::find(p_data->begin(), p_data->end(), center);
        ASSERT_NE(p_data->cend(), object);
    }
}


TEST(utest_kmeans_plus_plus, no_center_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 0);
}

TEST(utest_kmeans_plus_plus, one_center_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 1);
}

TEST(utest_kmeans_plus_plus, two_centers_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 2);
}

TEST(utest_kmeans_plus_plus, three_center_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 3);
}

TEST(utest_kmeans_plus_plus, max_centers_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, data->size());
}

TEST(utest_kmeans_plus_plus, one_center_identical_data_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, 1);
}

TEST(utest_kmeans_plus_plus, three_centers_identical_data_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, 3);
}

TEST(utest_kmeans_plus_plus, max_centers_identical_data_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, data->size());
}

TEST(utest_kmeans_plus_plus, one_center_identical_data_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    template_kmeans_plus_plus_initialization(data, 1);
}

TEST(utest_kmeans_plus_plus, three_centers_identical_data_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    template_kmeans_plus_plus_initialization(data, 3);
}

TEST(utest_kmeans_plus_plus, max_centers_identical_data_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    template_kmeans_plus_plus_initialization(data, data->size());
}

TEST(utest_kmeans_plus_plus, one_center_totally_identical_data) {
    dataset_ptr data = dataset_ptr( new dataset( { { 1.4 }, { 1.4 }, { 1.4 }, { 1.4 } } ) );
    template_kmeans_plus_plus_initialization(data, 1);
}

TEST(utest_kmeans_plus_plus, two_centers_totally_identical_data) {
    dataset_ptr data = dataset_ptr( new dataset( { { 1.4 }, { 1.4 }, { 1.4 }, { 1.4 } } ) );
    template_kmeans_plus_plus_initialization(data, 2);
}

TEST(utest_kmeans_plus_plus, max_centers_totally_identical_data) {
    dataset_ptr data = dataset_ptr( new dataset( { { 1.4 }, { 1.4 }, { 1.4 }, { 1.4 } } ) );
    template_kmeans_plus_plus_initialization(data, data->size());
}

TEST(utest_kmeans_plus_plus, points_less_than_centers) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    ASSERT_THROW(template_kmeans_plus_plus_initialization(data, data->size() + 1), std::invalid_argument);
}

TEST(utest_kmeans_plus_plus, empty_data) {
    dataset_ptr data = dataset_ptr( new dataset() );
    ASSERT_THROW(template_kmeans_plus_plus_initialization(data, data->size() + 1), std::invalid_argument);
}


static void
template_initialize_kmeans(const dataset_ptr & p_data,
                           const std::size_t p_amount,
                           const std::vector<std::size_t> & p_expected_cluster_length)
{
    kmeans_plus_plus initializer(p_amount);

    dataset centers;
    initializer.initialize(*p_data, centers);

    kmeans instance(centers, 0.0001);
    kmeans_data output_result;

    instance.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = *(output_result.clusters());

    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_kmeans_plus_plus, allocation_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_initialize_kmeans(data, 2, { 5, 5 });
}

TEST(utest_kmeans_plus_plus, allocation_sample_simple_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_initialize_kmeans(data, 3, { 10, 5, 8 });
}

TEST(utest_kmeans_plus_plus, allocation_sample_simple_03) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_initialize_kmeans(data, 4, { 10, 10, 10, 30 });
}

TEST(utest_kmeans_plus_plus, allocation_sample_simple_04) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    template_initialize_kmeans(data, 5, { 15, 15, 15, 15, 15 });
}


static void
template_kmeans_plus_plus_metric(const dataset_ptr & p_data,
                                 const std::size_t p_amount,
                                 const kmeans_plus_plus::metric & solver)
{
    kmeans_plus_plus initializer(p_amount, solver);

    dataset centers;
    initializer.initialize(*p_data, centers);

    ASSERT_EQ(p_amount, centers.size());
    for (auto & center : centers) {
        auto object = std::find(p_data->begin(), p_data->end(), center);
        ASSERT_NE(p_data->cend(), object);
    }
}

TEST(utest_kmeans_plus_plus, metric_manhattan) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    kmeans_plus_plus::metric metric = [](const point & p1, const point & p2) {
        return ccore::utils::metric::manhattan_distance(p1, p2);
    };

    template_kmeans_plus_plus_metric(data, 2, metric);
}

TEST(utest_kmeans_plus_plus, metric_euclidean) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    kmeans_plus_plus::metric metric = [](const point & p1, const point & p2) {
        return ccore::utils::metric::euclidean_distance(p1, p2);
    };

    template_kmeans_plus_plus_metric(data, 2, metric);
}
