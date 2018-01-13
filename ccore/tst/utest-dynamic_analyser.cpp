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

#include "utenv_check.hpp"

#include "nnet/dynamic_analyser.hpp"


using namespace ccore::nnet;


using network_dynamic = std::vector<std::vector<double>>;
using ensemble_collection = std::vector<std::vector<std::size_t>>;


template <class DynamicType, class EnsemblesType>
static void template_sync_ensembles(const double p_amplitude,
                                    const double p_tolerance,
                                    const std::size_t p_spikes,
                                    const DynamicType & p_dynamic,
                                    EnsemblesType & p_expected_ensembles,
                                    typename EnsemblesType::value_type & p_expected_dead)
{
    EnsemblesType ensembles;
    typename EnsemblesType::value_type dead;
    dynamic_analyser(p_amplitude, p_tolerance, p_spikes).allocate_sync_ensembles(p_dynamic, ensembles, dead);

    ASSERT_SYNC_ENSEMBLES(ensembles, p_expected_ensembles, dead, p_expected_dead);
}



TEST(utest_dynamic_analyser, two_absolutely_sync) {
    network_dynamic     dynamic = { { 0.0, 0.0 }, { 0.0, 0.0 }, { 2.0, 2.0 }, { 3.0, 3.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, three_absolutely_sync) {
    network_dynamic     dynamic = { { 0.0, 0.0, 0.0 }, { 0.0, 0.0, 0.0 }, { 2.0, 2.0, 2.0 }, { 3.0, 3.0, 3.0 }, { 0.0, 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1, 2 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, absolutely_sync_two_spikes_but_one) {
    network_dynamic     dynamic = { { 0.0, 0.0 }, { 0.0, 0.0 }, { 2.0, 2.0 }, { 3.0, 3.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, absolutely_sync_two_spikes) {
    network_dynamic     dynamic = { { 0.0, 0.0 }, { 2.0, 2.0 }, { 3.0, 3.0 }, { 0.0, 0.0 }, { 2.0, 2.0 }, { 3.0, 3.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, async_absolutely_sync) {
  network_dynamic     dynamic = { { 0.0, 0.0 }, { 0.0, 2.0 }, { 0.0, 3.0 }, { 2.0, 0.0 }, { 3.0, 0.0 }, { 0.0, 2.0 } };
    ensemble_collection             expected_ensembles = { { 0 }, { 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_at_end_one_spike) {
    network_dynamic     dynamic = { { 0.0, 0.0 }, { 1.0, 0.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_at_end_two_spikes) {
    network_dynamic     dynamic = { { 0.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 0.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0 }, { 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, no_oscillations) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, activity_under_threshold_01) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 1.9, 1.9 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(2.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, activity_under_threshold_02) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 2.0, 2.0 }, { 0.0, 0.0 }, { 2.9, 2.9 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(3.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, permanent_aplitude_over_threshold) {
    network_dynamic dynamic = { { 2.0, 3.0 }, { 2.0, 3.0 }, { 2.0, 3.0 }, { 2.0, 3.0 }, { 2.0, 3.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, oscillations_over_threshold) {
    network_dynamic dynamic = { { 2.0, 2.0 }, { 4.0, 8.0 }, { 2.0, 2.0 }, { 4.0, 8.0 }, { 2.0, 2.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, oscillations_under_threshold) {
    network_dynamic dynamic = { { 2.0, 2.0 }, { 4.0, 8.0 }, { 2.0, 2.0 }, { 4.0, 8.0 }, { 2.0, 2.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(10.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_but_one_under_threshold) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 3.0, 1.0 }, { 0.0, 0.0 }, { 3.0, 1.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0 } };
    ensemble_collection::value_type expected_dead = { 1 };

    template_sync_ensembles(2.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, two_sync_ensembles) {
    network_dynamic dynamic = { { 0.0, 0.0, 1.0, 1.0 },
                                { 1.0, 1.0, 0.0, 0.0 },
                                { 0.0, 0.0, 1.0, 1.0 },
                                { 1.0, 1.0, 0.0, 0.0 },
                                { 0.0, 0.0, 1.0, 1.0 },
                                { 1.0, 1.0, 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 }, { 2, 3 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, three_sync_ensembles) {
    network_dynamic dynamic = { { 0.0, 0.0, 1.0, 1.0, 0.0, 0.0 },
                                { 1.0, 1.0, 0.0, 0.0, 1.0, 1.0 },
                                { 0.0, 0.0, 1.0, 1.0, 0.0, 0.0 },
                                { 1.0, 1.0, 0.0, 0.0, 0.0, 0.0 },
                                { 0.0, 0.0, 1.0, 1.0, 1.0, 1.0 },
                                { 1.0, 1.0, 0.0, 0.0, 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 }, { 2, 3 }, { 4, 5 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, incomplete_spike_at_end) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 1.0, 1.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, incomplete_spike_at_begin) {
    network_dynamic dynamic = { { 1.0, 1.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, incomplete_spike_at_begin_and_end) {
    network_dynamic dynamic = { { 1.0, 1.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 0.0, 0.0 }, { 1.0, 1.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0, 1 };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, two_sync_with_incomplete) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 1.0, 1.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, two_sync_with_async_incomplete) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 1.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_after_time_one_spike) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 1.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 0.0 }, { 1.0, 1.0 },
                                { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_after_time_two_spikes) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 1.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 0.0 }, { 1.0, 1.0 },
                                { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_after_time_three_spikes) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 1.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 0.0 }, { 1.0, 1.0 },
                                { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 1.0, 1.0 }, { 0.0, 0.0 } };
    ensemble_collection             expected_ensembles = { { 0 }, { 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.0, 3, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_with_tolerance_01) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 1.0 }, { 1.0, 1.0 }, { 1.0, 1.0 },
                                { 1.0, 1.0 }, { 1.0, 1.0 }, { 1.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 } };

    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.5, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, sync_with_tolerance_02) {
    network_dynamic dynamic = { { 0.0, 0.0 }, { 0.0, 1.0 }, { 1.0, 1.0 }, { 1.0, 1.0 }, { 1.0, 1.0 },
                                { 1.0, 1.0 }, { 1.0, 1.0 }, { 0.0, 0.0 }, { 0.0, 0.0 }, { 0.0, 0.0 } };

    ensemble_collection             expected_ensembles = { { 0, 1 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.25, 1, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, one_neuron_oscillation) {
    network_dynamic dynamic = { { 0.0 }, { 1.0 }, { 0.0 }, { 1.0 }, { 0.0 } };
    ensemble_collection             expected_ensembles = { { 0 } };
    ensemble_collection::value_type expected_dead = { };

    template_sync_ensembles(1.0, 0.25, 2, dynamic, expected_ensembles, expected_dead);
}

TEST(utest_dynamic_analyser, one_neuron_no_oscillation_01) {
    network_dynamic dynamic = { { 0.0 }, { 0.0 }, { 0.0 }, { 0.0 }, { 0.0 } };
    ensemble_collection             expected_ensembles = { };
    ensemble_collection::value_type expected_dead = { 0 };

    template_sync_ensembles(1.0, 0.25, 2, dynamic, expected_ensembles, expected_dead);
}