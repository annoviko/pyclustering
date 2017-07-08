#include "gtest/gtest.h"

#include "interface/xmeans_interface.h"
#include "interface/pyclustering_interface.h"

#include <memory>


extern "C" DECLARATION pyclustering_package * xmeans_algorithm(const pyclustering_package * const p_sample,
        const pyclustering_package * const p_centers,
        const std::size_t p_kmax,
        const double p_tolerance,
        const unsigned int p_criterion);


template <class ContainerType>
static std::shared_ptr<pyclustering_package> pack(const ContainerType & container) {
    pyclustering_package * package = create_package(&container);

    std::shared_ptr<pyclustering_package> shared_package(package, [](pyclustering_package * ptr) { free_pyclustering_package(ptr); });

    return shared_package;
}


TEST(utest_interface_xmeans, xmeans_algorithm) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));
    std::shared_ptr<pyclustering_package> centers = pack(dataset({ { 1 }, { 2 } }));

    pyclustering_package * result = xmeans_algorithm(sample.get(), centers.get(), 5, 0.01, 0);
    free_pyclustering_package(result);
}
