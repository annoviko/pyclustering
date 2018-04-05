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

#include "cluster/xmeans.hpp"

#include <algorithm>


using namespace ccore::clst;


static void
template_length_process_data(const std::shared_ptr<dataset> & data,
                             const dataset & start_centers,
                             const unsigned int kmax,
                             const std::vector<unsigned int> & expected_cluster_length,
                             const splitting_type criterion,
                             const std::size_t parallel_processing_trigger = xmeans::DEFAULT_DATA_SIZE_PARALLEL_PROCESSING) {
    xmeans solver(start_centers, kmax, 0.0001, criterion);
    solver.set_parallel_processing_trigger(parallel_processing_trigger);

    xmeans_data output_result;
    solver.process(*data.get(), output_result);

    cluster_sequence & results = output_result.clusters();

    /* Check number of clusters */
    if (!expected_cluster_length.empty()) {
        ASSERT_EQ(expected_cluster_length.size(), results.size());
    }

    /* Check cluster sizes */
    std::vector<size_t> obtained_cluster_length;
    std::size_t total_size = 0;
    for (size_t i = 0; i < results.size(); i++) {
        obtained_cluster_length.push_back(results[i].size());
        total_size += results[i].size();
    }

    ASSERT_EQ(data->size(), total_size);
    ASSERT_EQ(output_result.centers().size(), output_result.clusters().size());
    ASSERT_GE(kmax, output_result.centers().size());

    if (!expected_cluster_length.empty()) {
        std::sort(obtained_cluster_length.begin(), obtained_cluster_length.end());

        std::vector<unsigned int> sorted_expected_cluster_length(expected_cluster_length);
        std::sort(sorted_expected_cluster_length.begin(), sorted_expected_cluster_length.end());

        for (size_t i = 0; i < obtained_cluster_length.size(); i++) {
            ASSERT_EQ(obtained_cluster_length[i], sorted_expected_cluster_length[i]);
        }
    }
}


TEST(utest_xmeans, allocation_bic_sample_simple_01) {
    dataset start_centers = { {3.7, 5.5}, {6.7, 7.5} };
    std::vector<unsigned int> expected_clusters_length = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_mndl_sample_simple_01) {
    dataset start_centers = { {3.7, 5.5}, {6.7, 7.5} };
    std::vector<unsigned int> expected_clusters_length = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 20, expected_clusters_length, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
}


TEST(utest_xmeans, allocation_bic_sample_simple_02) {
    dataset start_centers = { {3.5, 4.8}, {6.9, 7.0}, {7.5, 0.5} };
    std::vector<unsigned int> expected_clusters_length = {10, 5, 8};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_mndl_sample_simple_02) {
    dataset start_centers = { {3.5, 4.8}, {6.9, 7.0}, {7.5, 0.5} };
    std::vector<unsigned int> expected_clusters_length = {10, 5, 8};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 20, expected_clusters_length, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
}


TEST(utest_xmeans, allocation_wrong_initial_bic_sample_simple_02) {
    dataset start_centers = { {3.5, 4.8}, {6.9, 7.0} };
    std::vector<unsigned int> expected_clusters_length = {10, 5, 8};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_bic_sample_simple_03) {
    dataset start_centers = { {0.2, 0.1}, {4.0, 1.0}, {2.0, 2.0}, {2.3, 3.9} };
    std::vector<unsigned int> expected_clusters_length = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_wrong_initial_bic_sample_simple_03) {
    dataset start_centers = { {4.0, 1.0}, {2.0, 2.0}, {2.3, 3.9} };
    std::vector<unsigned int> expected_clusters_length = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_kmax_less_real_bic_sample_simple_03) {
    dataset start_centers = { {4.0, 1.0}, {2.0, 2.0}, {2.3, 3.9} };
    std::vector<unsigned int> expected_clusters_length = { };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 3, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_one_cluster_bic_sample_simple_03) {
    dataset start_centers = { {2.0, 2.0} };
    std::vector<unsigned int> expected_clusters_length = { 60 };
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 1, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_mndl_sample_simple_03) {
    dataset start_centers = { {0.2, 0.1}, {4.0, 1.0}, {2.0, 2.0}, {2.3, 3.9} };
    std::vector<unsigned int> expected_clusters_length = {10, 10, 10, 30};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_03), start_centers, 20, expected_clusters_length, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
}


TEST(utest_xmeans, allocation_bic_sample_simple_04) {
    dataset start_centers = { {1.5, 0.0}, {1.5, 2.0}, {1.5, 4.0}, {1.5, 6.0}, {1.5, 8.0} };
    std::vector<unsigned int> expected_clusters_length = {15, 15, 15, 15, 15};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_mndl_sample_simple_04) {
    dataset start_centers = { {1.5, 0.0}, {1.5, 2.0}, {1.5, 4.0}, {1.5, 6.0}, {1.5, 8.0} };
    std::vector<unsigned int> expected_clusters_length = {15, 15, 15, 15, 15};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_04), start_centers, 20, expected_clusters_length, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
}


TEST(utest_xmeans, same_size_data_and_centers_bic) {
    dataset_ptr data = dataset_ptr( new dataset({ {1.0}, {2.0}, {3.0}, {4.0} }) );
    dataset start_centers = { {1.0}, {2.0}, {3.0}, {4.0} };

    template_length_process_data(data, start_centers, 20, { 1, 1, 1, 1 }, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, same_size_data_and_centers_mndl) {
    dataset_ptr data = dataset_ptr( new dataset({ {1.0}, {2.0}, {3.0}, {4.0} }) );
    dataset start_centers = { {1.0}, {2.0}, {3.0}, {4.0} };

    template_length_process_data(data, start_centers, 20, { 1, 1, 1, 1 }, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
}


TEST(utest_xmeans, parallel_processing_bic) {
    dataset start_centers = { {0.25, 0.25}, {0.75, 0.65}, {0.95, 0.5} };
    std::size_t parallel_processing_trigger = 100;

    std::shared_ptr<dataset> trigger_parallel_data = simple_sample_factory::create_random_sample(parallel_processing_trigger, 5);

    template_length_process_data(trigger_parallel_data, start_centers, 20, { }, splitting_type::BAYESIAN_INFORMATION_CRITERION, parallel_processing_trigger);
}


TEST(utest_xmeans, parallel_processing_mndl) {
    dataset start_centers = { {0.25, 0.25}, {0.75, 0.65}, {0.95, 0.5} };
    std::size_t parallel_processing_trigger = 100;

    std::shared_ptr<dataset> trigger_parallel_data = simple_sample_factory::create_random_sample(parallel_processing_trigger, 5);

    template_length_process_data(trigger_parallel_data, start_centers, 20, { }, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH, parallel_processing_trigger);
}


TEST(utest_xmeans, parallel_processing_sample_simple_01) {
    dataset start_centers = { {3.7, 5.5}, {6.7, 7.5} };
    std::vector<unsigned int> expected_clusters_length = {5, 5};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION, 0);
}


TEST(utest_xmeans, parallel_processing_sample_simple_02) {
    dataset start_centers = { {3.5, 4.8}, {6.9, 7.0}, {7.5, 0.5} };
    std::vector<unsigned int> expected_clusters_length = {10, 5, 8};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_02), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION, 0);
}


TEST(utest_xmeans, allocation_bic_identical_data_01) {
    dataset start_centers = { {3.0}, {6.0} };
    std::vector<unsigned int> expected_clusters_length = {10, 20};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), start_centers, 20, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}


TEST(utest_xmeans, allocation_mndl_identical_data_01) {
    dataset start_centers = { {3.0}, {6.0} };
    std::vector<unsigned int> expected_clusters_length = {10, 20};
    template_length_process_data(simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_09), start_centers, 20, expected_clusters_length, splitting_type::MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
}


TEST(utest_xmeans, custom_allocation_bic_01) {
    dataset_ptr data = dataset_ptr(new dataset({{0.0, 0.0}, {0.1363766466758196, 1.1783713695419944}, {3.214688621356828, 1.476853479793315}, {2.138463480518565, 4.081574609797002}, {0.7396242774728039, 2.87928051726698}, {4.392971847058702, 9.373294690055928}, {0.9201540078170818, 1.58388176369988}, {4.314084965826241, 1.2011928104209428}, {11.734694885255871, 7.357322102302481}, {3.536693195144401, 7.985381380225232}}));
    dataset start_centers = {{0.5370863032832184, 0.11587434446400902}, {0.88032361344512, 0.1499414823211892}, {0.32937175324286194, 0.1591103849511586}};

    std::vector<unsigned int> expected_clusters_length = { };

    template_length_process_data(data, start_centers, 5, expected_clusters_length, splitting_type::BAYESIAN_INFORMATION_CRITERION);
}