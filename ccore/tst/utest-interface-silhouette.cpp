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

#include <pyclustering/interface/silhouette_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>
#include <pyclustering/utils/metric.hpp>

#include "samples.hpp"

#include "answer.hpp"
#include "answer_reader.hpp"
#include "utenv_utils.hpp"

#include <memory>


using namespace pyclustering;


TEST(utest_interface_silhouette, silhouette) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    answer ans = answer_reader::read(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);

    dataset matrix;
    distance_matrix(*data, distance_metric_factory<point>::euclidean_square(), matrix);

    std::shared_ptr<pyclustering_package> data_package = pack(*data);
    std::shared_ptr<pyclustering_package> matrix_package = pack(matrix);
    std::shared_ptr<pyclustering_package> cluster_package = pack(ans.clusters());

    pyclustering_package * result_points = silhouette_algorithm(data_package.get(), cluster_package.get(), nullptr, 0);
    pyclustering_package * result_matrix = silhouette_algorithm(matrix_package.get(), cluster_package.get(), nullptr, 1);

    ASSERT_NE(nullptr, result_points);
    ASSERT_NE(nullptr, result_matrix);

    ASSERT_EQ(result_points->size, result_matrix->size);
    ASSERT_EQ(result_points->type, result_matrix->type);

    delete result_matrix;
    delete result_points;
}


TEST(utest_interface_silhouette, silhouette_ksearch) {
    dataset_ptr data = simple_sample_factory::create_sample(SAMPLE_SIMPLE::SAMPLE_SIMPLE_01);
    std::shared_ptr<pyclustering_package> sample = pack(*data);

    pyclustering_package * result = silhouette_ksearch_algorithm(sample.get(), 2, 5, 0, -1);

    ASSERT_EQ((std::size_t) SILHOUETTE_KSEARCH_PACKAGE_SIZE, result->size);

    delete result;
}
