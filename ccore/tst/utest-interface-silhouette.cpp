/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
