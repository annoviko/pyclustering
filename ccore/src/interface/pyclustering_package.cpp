#include "interface/pyclustering_package.hpp"


pyclustering_package::pyclustering_package(void) :
        size(0),
        type(PYCLUSTERING_TYPE_UNDEFINED),
        data(nullptr)
{ }


pyclustering_package::pyclustering_package(unsigned int package_type) :
    size(0),
    type(package_type),
    data(nullptr)
{ }


pyclustering_package::~pyclustering_package(void) {
    if (type != (unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST) {
        switch(type) {
            case pyclustering_type_data::PYCLUSTERING_TYPE_INT:
                delete [] (int *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_INT:
                delete [] (unsigned int *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_FLOAT:
                delete [] (float *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE:
                delete [] (double *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_LONG:
                delete [] (long *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_UNSIGNED_LONG:
                delete [] (unsigned long *) data;
                break;

            case pyclustering_type_data::PYCLUSTERING_TYPE_SIZE_T:
                delete [] (size_t *) data;
                break;

            default:
                /* Memory Leak */
                break;
        }
    }
    else {
        for (unsigned int i = 0; i < size; i++) {
            pyclustering_package * package = ((pyclustering_package **) data)[i];
            delete package;
        }
    }
}


pyclustering_package * create_package(const std::vector<int> * const data) {
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_INT);
    prepare_package(data, package);

    return package;
}

pyclustering_package * create_package(const std::vector<unsigned int> * const data) {
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_INT);
    prepare_package(data, package);

    return package;
}

pyclustering_package * create_package(const std::vector<float> * const data) {
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_FLOAT);
    prepare_package(data, package);

    return package;
}

pyclustering_package * create_package(const std::vector<double> * const data) {
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_DOUBLE);
    prepare_package(data, package);

    return package;
}

pyclustering_package * create_package(const std::vector<long> * const data) {
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LONG);
    prepare_package(data, package);

    return package;
}

pyclustering_package * create_package(const std::vector<size_t> * const data) {
    pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_SIZE_T);
    prepare_package(data, package);

    return package;
}
