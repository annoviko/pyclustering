/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
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

#include <pyclustering/cluster/kmeans.hpp>
#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include "utenv_check.hpp"


using namespace pyclustering;
using namespace pyclustering::clst;


void template_kmeans_plus_plus_initialization(const dataset_ptr & p_data, const std::size_t p_amount, const std::size_t p_candidates)
{
    kmeans_plus_plus initializer(p_amount, p_candidates);

    dataset centers;
    initializer.initialize(*p_data, centers);

    ASSERT_EQ(p_amount, centers.size());
    for (auto & center : centers) {
        auto object = std::find(p_data->begin(), p_data->end(), center);
        ASSERT_NE(p_data->cend(), object);
    }

    dataset copy_data = *p_data;
    std::unique(copy_data.begin(), copy_data.end());

    if (copy_data.size() == p_data->size()) {
        std::unique(centers.begin(), centers.end());
        ASSERT_EQ(p_amount, centers.size());
    }
}


TEST(utest_kmeans_plus_plus, no_center_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 0, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, no_center_sample_simple_01_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 0, 1);
}

TEST(utest_kmeans_plus_plus, no_center_sample_simple_01_two_candidates) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 0, 2);
}

TEST(utest_kmeans_plus_plus, one_center_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, one_center_sample_simple_01_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 1, 1);
}

TEST(utest_kmeans_plus_plus, one_center_sample_simple_01_two_candidates) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 1, 2);
}

TEST(utest_kmeans_plus_plus, two_centers_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, three_center_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 3, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, three_center_sample_simple_01_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 3, 1);
}

TEST(utest_kmeans_plus_plus, three_center_sample_simple_01_three_candidates) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, 3, 3);
}

TEST(utest_kmeans_plus_plus, max_centers_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, data->size(), kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, max_centers_sample_simple_01_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, data->size(), 1);
}

TEST(utest_kmeans_plus_plus, max_centers_sample_simple_01_two_candidates) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, data->size(), 2);
}

TEST(utest_kmeans_plus_plus, max_centers_sample_simple_01_max_candidates) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization(data, data->size(), data->size());
}

TEST(utest_kmeans_plus_plus, one_center_identical_data_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, one_center_identical_data_01_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, 1, 1);
}

TEST(utest_kmeans_plus_plus, three_centers_identical_data_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, 3, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, max_centers_identical_data_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09);
    template_kmeans_plus_plus_initialization(data, data->size(), kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, one_center_identical_data_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    template_kmeans_plus_plus_initialization(data, 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, three_centers_identical_data_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    template_kmeans_plus_plus_initialization(data, 3, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, max_centers_identical_data_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_12);
    template_kmeans_plus_plus_initialization(data, data->size(), kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, two_centers_two_identical_points) {
    dataset_ptr data = dataset_ptr( new dataset( { { 0.0 }, { 0.0 } } ) );
    template_kmeans_plus_plus_initialization(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, two_centers_two_identical_points_two_candidates) {
    dataset_ptr data = dataset_ptr( new dataset( { { 0.0 }, { 0.0 } } ) );
    template_kmeans_plus_plus_initialization(data, 2, 2);
}

TEST(utest_kmeans_plus_plus, one_center_totally_identical_data) {
    dataset_ptr data = dataset_ptr( new dataset( { { 1.4 }, { 1.4 }, { 1.4 }, { 1.4 } } ) );
    template_kmeans_plus_plus_initialization(data, 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, two_centers_totally_identical_data) {
    dataset_ptr data = dataset_ptr( new dataset( { { 1.4 }, { 1.4 }, { 1.4 }, { 1.4 } } ) );
    template_kmeans_plus_plus_initialization(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, max_centers_totally_identical_data) {
    dataset_ptr data = dataset_ptr( new dataset( { { 1.4 }, { 1.4 }, { 1.4 }, { 1.4 } } ) );
    template_kmeans_plus_plus_initialization(data, data->size(), kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, points_less_than_centers) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    ASSERT_THROW(template_kmeans_plus_plus_initialization(data, data->size() + 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE), std::invalid_argument);
}

TEST(utest_kmeans_plus_plus, empty_data) {
    dataset_ptr data = dataset_ptr( new dataset() );
    ASSERT_THROW(template_kmeans_plus_plus_initialization(data, data->size() + 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE), std::invalid_argument);
}


void template_kmeans_plus_plus_medoid_initialization(const dataset_ptr & p_data, const std::size_t p_amount, const std::size_t p_candidates)
{
    kmeans_plus_plus initializer(p_amount, p_candidates);

    std::vector<std::size_t> medoids;
    initializer.initialize(*p_data, medoids);

    ASSERT_EQ(p_amount, medoids.size());
    for (const auto medoid : medoids) {
        ASSERT_LT(medoid, p_data->size());
        ASSERT_EQ(1, std::count(medoids.begin(), medoids.end(), medoid));
    }
}

TEST(utest_kmeans_plus_plus, medoids_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_medoid_initialization(data, 1, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, medoids_simple_01_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_medoid_initialization(data, 1, 1);
}

TEST(utest_kmeans_plus_plus, medoids_simple_01_two_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_medoid_initialization(data, 1, 2);
}

TEST(utest_kmeans_plus_plus, medoids_simple_01_all_range) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    for (std::size_t i = 1; i < data->size(); i++) {
        template_kmeans_plus_plus_medoid_initialization(data, i, 1);
    }
}

TEST(utest_kmeans_plus_plus, medoids_simple_01_all_range_farthest) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    for (std::size_t i = 1; i < data->size(); i++) {
        template_kmeans_plus_plus_medoid_initialization(data, i, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
    }
}

TEST(utest_kmeans_plus_plus, medoids_simple_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_kmeans_plus_plus_medoid_initialization(data, 0, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, medoids_simple_02_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_kmeans_plus_plus_medoid_initialization(data, 0, 1);
}

TEST(utest_kmeans_plus_plus, medoids_simple_02_all_range) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    for (std::size_t i = 1; i < data->size(); i++) {
        template_kmeans_plus_plus_medoid_initialization(data, i, 1);
    }
}

TEST(utest_kmeans_plus_plus, medoids_simple_03) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_kmeans_plus_plus_medoid_initialization(data, 0, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, medoids_simple_03_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_kmeans_plus_plus_medoid_initialization(data, 0, 1);
}

TEST(utest_kmeans_plus_plus, medoids_simple_04) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    template_kmeans_plus_plus_medoid_initialization(data, 0, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, medoids_simple_04_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    template_kmeans_plus_plus_medoid_initialization(data, 0, 1);
}

TEST(utest_kmeans_plus_plus, medoids_simple_05) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05);
    template_kmeans_plus_plus_medoid_initialization(data, 0, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, medoids_simple_05_one_candidate) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_05);
    template_kmeans_plus_plus_medoid_initialization(data, 0, 1);
}


void template_initialize_kmeans(const dataset_ptr & p_data,
                                const std::size_t p_amount,
                                const std::size_t p_candidate,
                                const std::vector<std::size_t> & p_expected_cluster_length)
{
    kmeans_plus_plus initializer(p_amount, p_candidate);

    dataset centers;
    initializer.initialize(*p_data, centers);

    kmeans instance(centers, 0.0001);
    kmeans_data output_result;

    instance.process(*p_data, output_result);

    const dataset & data = *p_data;
    const cluster_sequence & actual_clusters = output_result.clusters();

    ASSERT_CLUSTER_SIZES(data, actual_clusters, p_expected_cluster_length);
}


TEST(utest_kmeans_plus_plus, allocation_sample_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_initialize_kmeans(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, { 5, 5 });
}

TEST(utest_kmeans_plus_plus, allocation_sample_simple_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_initialize_kmeans(data, 3, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, { 10, 5, 8 });
}

TEST(utest_kmeans_plus_plus, allocation_sample_simple_03) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_initialize_kmeans(data, 4, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, { 10, 10, 10, 30 });
}

TEST(utest_kmeans_plus_plus, allocation_sample_simple_04) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04);
    template_initialize_kmeans(data, 5, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, { 15, 15, 15, 15, 15 });
}


void template_kmeans_plus_plus_metric(const dataset_ptr & p_data,
                                      const std::size_t p_amount,
                                      const std::size_t p_candidate,
                                      const kmeans_plus_plus::metric & solver)
{
    kmeans_plus_plus initializer(p_amount, p_candidate, solver);

    dataset centers;
    initializer.initialize(*p_data, centers);

    ASSERT_EQ(p_amount, centers.size());
    for (auto & center : centers) {
        auto object = std::find(p_data->begin(), p_data->end(), center);
        ASSERT_NE(p_data->cend(), object);
    }

    dataset copy_data = *p_data;
    std::unique(copy_data.begin(), copy_data.end());

    if (copy_data.size() == p_data->size()) {
        std::unique(centers.begin(), centers.end());
        ASSERT_EQ(p_amount, centers.size());
    }
}

TEST(utest_kmeans_plus_plus, metric_manhattan) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    kmeans_plus_plus::metric metric = [](const point & p1, const point & p2) {
        return pyclustering::utils::metric::manhattan_distance(p1, p2);
    };

    template_kmeans_plus_plus_metric(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, metric);
}

TEST(utest_kmeans_plus_plus, metric_euclidean) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    kmeans_plus_plus::metric metric = [](const point & p1, const point & p2) {
        return pyclustering::utils::metric::euclidean_distance(p1, p2);
    };

    template_kmeans_plus_plus_metric(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, metric);
}



void template_kmeans_plus_plus_initialization_range(const dataset_ptr & p_data,
                                                    const std::size_t p_amount,
                                                    const std::size_t p_candidate,
                                                    const index_sequence & p_indexes)
{
    kmeans_plus_plus initializer(p_amount, p_candidate);

    dataset centers;
    initializer.initialize(*p_data, p_indexes, centers);

    ASSERT_EQ(p_amount, centers.size());
    for (auto & center : centers) {
        auto iter_object = std::find(p_data->begin(), p_data->end(), center);
        ASSERT_NE(p_data->cend(), iter_object);

        std::size_t index = std::distance(p_data->begin(), iter_object);
        auto iter_index = std::find(p_indexes.begin(), p_indexes.end(), index);
        ASSERT_NE(p_indexes.cend(), iter_index);
    }

    dataset copy_data = *p_data;
    std::unique(copy_data.begin(), copy_data.end());

    if (copy_data.size() == p_data->size()) {
        std::unique(centers.begin(), centers.end());
        ASSERT_EQ(p_amount, centers.size());
    }
}

TEST(utest_kmeans_plus_plus, range_sample_simple_01) {
    index_sequence range = { 0, 1, 2, 5, 6, 7 };
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_initialization_range(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, range);
}

TEST(utest_kmeans_plus_plus, range_sample_simple_02) {
    index_sequence range = { 0, 1, 2, 5, 6, 7, 10, 11, 12 };
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_kmeans_plus_plus_initialization_range(data, 3, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, range);
}

TEST(utest_kmeans_plus_plus, indexes_less_than_centers) {
    index_sequence range = { 0 };
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    ASSERT_THROW(template_kmeans_plus_plus_initialization_range(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE, range), std::invalid_argument);
}


void template_kmeans_plus_plus_several_runs(const dataset_ptr & p_data, const std::size_t p_amount, const std::size_t p_candidates)
{
    const std::size_t attempts = 10;
    for (std::size_t i = 0; i < attempts; i++) {
        index_sequence all_centers;
        index_sequence centers;

        kmeans_plus_plus(p_amount, p_candidates).initialize(*p_data, centers);
        all_centers.insert(std::end(all_centers), std::begin(centers), std::end(centers));

        kmeans_plus_plus(p_amount, p_candidates).initialize(*p_data, centers);
        all_centers.insert(std::end(all_centers), std::begin(centers), std::end(centers));

        kmeans_plus_plus(p_amount, p_candidates).initialize(*p_data, centers);
        all_centers.insert(std::end(all_centers), std::begin(centers), std::end(centers));

        index_sequence unique_centers = all_centers;
        std::unique(unique_centers.begin(), unique_centers.end());

        if (unique_centers.size() != all_centers.size()) {
            continue;
        }

        return;
    }

    FAIL();
}

TEST(utest_kmeans_plus_plus, several_runs_simple_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_several_runs(data, 2, 1);
    template_kmeans_plus_plus_several_runs(data, 10, 1);
}

TEST(utest_kmeans_plus_plus, several_runs_simple_more_candidates_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_several_runs(data, 2, 5);
    template_kmeans_plus_plus_several_runs(data, 9, 10);
}

TEST(utest_kmeans_plus_plus, several_runs_simple_farthest_candidates_01) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    template_kmeans_plus_plus_several_runs(data, 2, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
    template_kmeans_plus_plus_several_runs(data, 10, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE);
}

TEST(utest_kmeans_plus_plus, several_runs_simple_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_kmeans_plus_plus_several_runs(data, 3, 1);
    template_kmeans_plus_plus_several_runs(data, 23, 1);
}

TEST(utest_kmeans_plus_plus, several_runs_simple_more_candidates_02) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02);
    template_kmeans_plus_plus_several_runs(data, 3, 3);
    template_kmeans_plus_plus_several_runs(data, 23, 12);
}

TEST(utest_kmeans_plus_plus, several_runs_simple_03) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03);
    template_kmeans_plus_plus_several_runs(data, 4, 1);
    template_kmeans_plus_plus_several_runs(data, 8, 1);
}