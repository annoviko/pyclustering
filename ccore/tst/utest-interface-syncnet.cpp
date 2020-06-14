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



#include <gtest/gtest.h>

#include <pyclustering/interface/sync_interface.h>
#include <pyclustering/interface/syncnet_interface.h>
#include <pyclustering/interface/pyclustering_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/cluster/syncnet.hpp>

#include "utenv_utils.hpp"


using namespace pyclustering;


static void CHECK_FREE_PACKAGE(pyclustering_package * package) {
    ASSERT_NE(nullptr, package);
    ASSERT_TRUE(package->size > 0);

    free_pyclustering_package(package);
}

TEST(utest_interface_syncnet, syncnet_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    void * network_pointer = syncnet_create_network(sample.get(), 3, false, 0);
    ASSERT_NE(nullptr, network_pointer);

    void * analyser_pointer = syncnet_process(network_pointer, 0.995, (unsigned int) solve_type::FORWARD_EULER, true);
    ASSERT_NE(nullptr, analyser_pointer);

    pyclustering_package * package = sync_dynamic_allocate_sync_ensembles(analyser_pointer, 0.1, sync_dynamic_get_size(analyser_pointer) - 1);
    CHECK_FREE_PACKAGE(package);

    package = sync_dynamic_allocate_correlation_matrix(analyser_pointer, sync_dynamic_get_size(analyser_pointer) - 1);
    CHECK_FREE_PACKAGE(package);

    package = sync_dynamic_get_time(analyser_pointer);
    CHECK_FREE_PACKAGE(package);

    package = sync_dynamic_get_output(analyser_pointer);
    CHECK_FREE_PACKAGE(package);

    syncnet_destroy_network(network_pointer);
    syncnet_analyser_destroy(analyser_pointer);
}