/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef _UTEST_SYNCPR_
#define _UTEST_SYNCPR_


#include "gtest/gtest.h"

#include "nnet/syncpr.hpp"

#include <algorithm>


static void template_syncpr_create_delete(const unsigned int size) {
    syncpr * network = new syncpr(size, 0.5, 0.5);
    ASSERT_EQ(size, network->size());

    delete network;
}

TEST(utest_syncpr, create_delete_10_oscillators) {
    template_syncpr_create_delete(10);
}

TEST(utest_syncpr, create_delete_50_oscillators) {
    template_syncpr_create_delete(50);
}

TEST(utest_syncpr, create_delete_100_oscillators) {
    template_syncpr_create_delete(100);
}

static void template_simulation_static(const unsigned int steps,
                                           const solve_type solver,
                                           const bool collect_flag) {
    syncpr network(5, 0.3, 0.3);
    syncpr_dynamic output_dynamic;
    syncpr_pattern pattern = { 1, 1, 1, -1, -1 };

    network.simulate_static(steps, 10, pattern, solver, collect_flag, output_dynamic);

    if (collect_flag) {
        ASSERT_TRUE(output_dynamic.size() > steps);
    }
    else {
        ASSERT_EQ(1, output_dynamic.size());
    }
}

TEST(utest_syncpr, static_simulation_10_FAST) {
    template_simulation_static(10, solve_type::FAST, true);
}

TEST(utest_syncpr, static_simulation_100_FAST) {
    template_simulation_static(100, solve_type::FAST, true);
}

TEST(utest_syncpr, static_simulation_5_RK4) {
    template_simulation_static(5, solve_type::RK4, true);
}

TEST(utest_syncpr, static_simulation_6_RKF45) {
    template_simulation_static(6, solve_type::RKF45, true);
}

TEST(utest_syncpr, static_simulation_FAST_no_collecting) {
    template_simulation_static(5, solve_type::FAST, false);
}

TEST(utest_syncpr, static_simulation_RK4_no_collecting) {
    template_simulation_static(5, solve_type::RK4, false);
}

TEST(utest_syncpr, static_simulation_RKF45_no_collecting) {
    template_simulation_static(5, solve_type::RKF45, false);
}


static void template_simulation_dynamic(const solve_type solver,
                                        const bool collect_flag) {
    syncpr network(5, 0.3, 0.3);
    syncpr_dynamic output_dynamic;
    syncpr_pattern pattern = { 1, 1, 1, -1, -1 };

    network.simulate_dynamic(pattern, 0.95, 1, solver, collect_flag, output_dynamic);

    if (collect_flag) {
        ASSERT_TRUE(output_dynamic.size() > 1);
    }
    else {
        ASSERT_EQ(1, output_dynamic.size());
    }
}

TEST(utest_syncpr, dynamic_simulation_FAST) {
    template_simulation_dynamic(solve_type::FAST, true);
}

TEST(utest_syncpr, dynamic_simulation_RK4) {
    template_simulation_dynamic(solve_type::RK4, true);
}

TEST(utest_syncpr, dynamic_simulation_RKF45) {
    template_simulation_dynamic(solve_type::RKF45, true);
}

TEST(utest_syncpr, dynamic_simulation_FAST_no_collecting) {
    template_simulation_dynamic(solve_type::FAST, false);
}

TEST(utest_syncpr, dynamic_simulation_RK4_no_collecting) {
    template_simulation_dynamic(solve_type::RK4, false);
}

TEST(utest_syncpr, dynamic_simulation_RKF45_no_collecting) {
    template_simulation_dynamic(solve_type::RKF45, false);
}

TEST(utest_syncpr, train_and_recognize_pattern) {
    syncpr network(10, 0.1, 0.1);
    syncpr_dynamic output_dynamic;

    std::vector<syncpr_pattern> patterns = {
        {  1,  1,  1,  1,  1, -1, -1, -1, -1, -1 },
        { -1, -1, -1, -1, -1,  1,  1,  1,  1,  1 }
    };

    double memory_order1 = network.memory_order(patterns[0]);
    double memory_order2 = network.memory_order(patterns[1]);

    ASSERT_TRUE(memory_order1 < 0.9);
    ASSERT_TRUE(memory_order2 < 0.9);

    network.train(patterns);

    /* recognize it */
    for (size_t i = 0; i < patterns.size(); i++) {
        syncpr_dynamic output_dynamic;
        network.simulate_static(20, 10, patterns[i], solve_type::RK4, true, output_dynamic);

        double memory_order = network.memory_order(patterns[i]);
        ASSERT_TRUE(memory_order > 0.995);

        ensemble_data<sync_ensemble> sync_ensembles;
        output_dynamic.allocate_sync_ensembles(0.1, sync_ensembles);

        ASSERT_EQ(2, sync_ensembles.size());

        for (sync_ensemble & ensemble : sync_ensembles) {
            std::sort(ensemble.begin(), ensemble.end());
        }

        sync_ensemble expected_ensemble1 = { 0, 1, 2, 3, 4 };
        sync_ensemble expected_ensemble2 = { 5, 6, 7, 8, 9 };

        ASSERT_TRUE( (expected_ensemble1 == sync_ensembles[0]) || (expected_ensemble2 == sync_ensembles[0]) );
        ASSERT_TRUE( (expected_ensemble1 == sync_ensembles[1]) || (expected_ensemble2 == sync_ensembles[1]));
    }
}

TEST(utest_syncpr, sync_local_order) {
    syncpr network(10, 0.1, 0.1);

    double local_order = network.sync_local_order();
    ASSERT_TRUE((local_order > 0.0) && (local_order < 1.0));

    std::vector<syncpr_pattern> patterns = {
        { 1, 1, 1, 1, 1, -1, -1, -1, -1, -1 },
        { -1, -1, -1, -1, -1, 1, 1, 1, 1, 1 }
    };

    network.train(patterns);

    local_order = network.sync_local_order();
    ASSERT_TRUE((local_order > 0.0) && (local_order < 1.0));
}

TEST(utest_syncpr, sync_global_order) {
    syncpr network(10, 0.1, 0.1);

    double global_order = network.sync_order();
    ASSERT_TRUE((global_order > 0.0) && (global_order < 1.0));

    std::vector<syncpr_pattern> patterns = {
        { 1, 1, 1, 1, 1, -1, -1, -1, -1, -1 },
        { -1, -1, -1, -1, -1, 1, 1, 1, 1, 1 }
    };

    network.train(patterns);

    global_order = network.sync_order();
    ASSERT_TRUE((global_order > 0.0) && (global_order < 1.0));
}

#endif
