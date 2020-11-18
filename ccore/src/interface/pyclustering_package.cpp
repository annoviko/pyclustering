/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/interface/pyclustering_package.hpp>

#include <type_traits>


pyclustering_package::pyclustering_package(const pyclustering_data_t package_type) :
        size(0),
        type((unsigned int) package_type),
        data(nullptr)
{ }


pyclustering_package::~pyclustering_package() {
    if (type != (unsigned int) pyclustering_data_t::PYCLUSTERING_TYPE_LIST) {
        switch(type) {
            case pyclustering_data_t::PYCLUSTERING_TYPE_INT:
                delete [] (int *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_UNSIGNED_INT:
                delete [] (unsigned int *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_FLOAT:
                delete [] (float *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_DOUBLE:
                delete [] (double *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_LONG:
                delete [] (long *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_SIZE_T:
                delete [] (size_t *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_CHAR:
                delete[] (char *) data;
                break;

            case pyclustering_data_t::PYCLUSTERING_TYPE_WCHAR_T:
                delete[] (wchar_t *) data;
                break;

            default:
                /* Memory Leak */
                break;
        }
    }
    else {
        for (std::size_t i = 0; i < size; i++) {
            pyclustering_package * package = ((pyclustering_package **) data)[i];
            delete package;
            package = nullptr;
        }

        delete [] (pyclustering_package **) data;
        data = nullptr;
    }
}


pyclustering_package * create_package_container(const std::size_t p_size) {
    pyclustering_package * package = new pyclustering_package(pyclustering_data_t::PYCLUSTERING_TYPE_LIST);
    package->size = p_size;
    package->data = new pyclustering_package * [p_size];

    return package;
}
