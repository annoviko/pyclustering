#ifndef SRC_INTERFACE_PYCLUSTERING_PACKAGE_HPP_
#define SRC_INTERFACE_PYCLUSTERING_PACKAGE_HPP_


#include <cstddef>
#include <vector>

#include "definitions.hpp"


typedef enum pyclustering_type_data {
    PYCLUSTERING_TYPE_INT               = 0,
    PYCLUSTERING_TYPE_UNSIGNED_INT      = 1,
    PYCLUSTERING_TYPE_FLOAT             = 2,
    PYCLUSTERING_TYPE_DOUBLE            = 3,
    PYCLUSTERING_TYPE_LONG              = 4,
    PYCLUSTERING_TYPE_UNSIGNED_LONG     = 5,
    PYCLUSTERING_TYPE_LIST              = 6,
    PYCLUSTERING_TYPE_SIZE_T            = 7,
    PYCLUSTERING_TYPE_UNDEFINED         = 8,
} pyclustering_type_data;


typedef struct pyclustering_package {
public:
    unsigned int size;
    unsigned int type;      /* pyclustering type data    */
    void * data;            /* pointer to data           */

public:
    pyclustering_package(void);

    pyclustering_package(unsigned int package_type);

    ~pyclustering_package(void);

private:
    void free_package(pyclustering_package * p_package);

} pyclustering_package;


pyclustering_package * create_package(const std::vector<int> * const data);


pyclustering_package * create_package(const std::vector<unsigned int> * const data);


pyclustering_package * create_package(const std::vector<float> * const data);


pyclustering_package * create_package(const std::vector<double> * const data);


pyclustering_package * create_package(const std::vector<long> * const data);


pyclustering_package * create_package(const std::vector<size_t> * const data);


template <class type_object>
void prepare_package(const std::vector<type_object> * const data, pyclustering_package * package) {
    package->size = data->size();
    package->data = (void *) new type_object[package->size];

    for (unsigned int i = 0; i < data->size(); i++) {
        ((type_object *) package->data)[i] = (*data)[i];
    }
}


template <class type_object>
pyclustering_package * create_package(const std::vector< std::vector<type_object> > * const data) {
   pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);

   package->size = data->size();
   package->data = new pyclustering_package * [package->size];

   for (unsigned int i = 0; i < package->size; i++) {
           ((pyclustering_package **) package->data)[i] = create_package(&(*data)[i]);
   }

   return package;
}


template <class type_object>
pyclustering_package * create_package(const std::vector< std::vector<type_object> * > * const data) {
   pyclustering_package * package = new pyclustering_package((unsigned int) pyclustering_type_data::PYCLUSTERING_TYPE_LIST);

   package->size = data->size();
   package->data = new pyclustering_package * [package->size];

   for (unsigned int i = 0; i < package->size; i++) {
           ((pyclustering_package **) package->data)[i] = create_package((*data)[i]);
   }

   return package;
}



#endif
