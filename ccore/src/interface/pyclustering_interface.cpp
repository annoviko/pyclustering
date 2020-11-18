/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/pyclustering_interface.h>


void free_pyclustering_package(pyclustering_package * package) {
    delete package;
}
