/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <gtest/gtest.h>

#include "samples.hpp"

#include <pyclustering/cluster/syncnet.hpp>


using namespace pyclustering::clst;


static void template_create_delete(const unsigned int size) {
    std::vector<std::vector<double> > sample;
    for (unsigned int i = 0; i < size; i++) {
        sample.push_back( { 0.0 + (double) i } );
    }

    syncnet * network = new syncnet(&sample, 2.0, false, initial_type::EQUIPARTITION);

    ASSERT_EQ(size, network->size());

    delete network;
}

TEST(utest_syncnet, create_delete_network_1) {
    template_create_delete(1);
}

TEST(utest_syncnet, create_delete_network_10) {
    template_create_delete(10);
}

TEST(utest_syncnet, create_delete_network_100) {
    template_create_delete(100);
}

TEST(utest_syncnet, one_cluster) {
    bool result_testing = false;

    for (std::size_t attempt = 0; attempt < 3; attempt++) {
        std::vector<std::vector<double> > sample;

        sample.push_back( { 0.1, 0.1 } );
        sample.push_back( { 0.2, 0.1 } );
        sample.push_back( { 0.0, 0.0 } );

        syncnet network(&sample, 0.5, false, initial_type::EQUIPARTITION);

        syncnet_analyser analyser;
        network.process(0.998, solve_type::FORWARD_EULER, true, analyser);

        syncnet_cluster_data clusters;
        analyser.allocate_clusters(0.1, clusters);

        if (1 != clusters.size()) {
            continue;
        }

        result_testing = true;
    }

    ASSERT_TRUE(result_testing);
}

static void template_two_cluster_allocation(const solve_type solver, const bool collect_dynamic, const bool ena_conn_weight) {
    bool result_testing = false;

    for (std::size_t attempt = 0; attempt < 3; attempt++) {
        std::vector<std::vector<double> > sample;

        sample.push_back( { 0.1, 0.1 } );
        sample.push_back( { 0.2, 0.1 } );
        sample.push_back( { 0.0, 0.0 } );

        sample.push_back( { 2.2, 2.1 } );
        sample.push_back( { 2.3, 2.0 } );
        sample.push_back( { 2.1, 2.4 } );

        syncnet network(&sample, 0.5, ena_conn_weight, initial_type::EQUIPARTITION);

        syncnet_analyser analyser;
        network.process(0.995, solver, true, analyser);

        ensemble_data<syncnet_cluster> ensembles;
        analyser.allocate_clusters(0.1, ensembles);

        if (2 != ensembles.size()) {
            continue;
        }

        result_testing = true;
    }

    ASSERT_TRUE(result_testing);
}

TEST(utest_syncnet, two_clusters_fast_solver_with_collection) {
    template_two_cluster_allocation(solve_type::FORWARD_EULER, true, false);
}

TEST(utest_syncnet, two_clusters_rk4_solver_with_collection) {
    template_two_cluster_allocation(solve_type::RUNGE_KUTTA_4, true, false);
}

TEST(utest_syncnet, two_clusters_rkf45_solver_with_collection) {
    template_two_cluster_allocation(solve_type::RUNGE_KUTTA_FEHLBERG_45, true, false);
}

TEST(utest_syncnet, two_clusters_fast_solver_without_collection) {
    template_two_cluster_allocation(solve_type::FORWARD_EULER, false, false);
}

TEST(utest_syncnet, two_clusters_rk4_solver_without_collection) {
    template_two_cluster_allocation(solve_type::RUNGE_KUTTA_4, false, false);
}

#ifndef VALGRIND_ANALYSIS_SHOCK

TEST(utest_syncnet, two_clusters_rkf45_solver_without_collection) {
    template_two_cluster_allocation(solve_type::RUNGE_KUTTA_FEHLBERG_45, false, false);
}

TEST(utest_syncnet, two_clusters_fast_solver_conn_weight) {
    template_two_cluster_allocation(solve_type::FORWARD_EULER, false, true);
}

#endif
