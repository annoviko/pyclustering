/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/cluster/gmeans.hpp>


#define SUCCESS                                      0
#define FAILURE_INCORRECT_RESULT                     1


int main() {
    pyclustering::clst::gmeans_data result;
    pyclustering::clst::gmeans algorithm(2);

    algorithm.process({ { 1.0 }, { 1.2 }, { 1.1 }, { 3.0 }, { 3.2 }, { 3.1 }, { 8.0 }, { 8.2 }, { 8.1 } }, result);

    if (result.clusters().empty()) {
        return FAILURE_INCORRECT_RESULT;
    }

    return SUCCESS;
}
