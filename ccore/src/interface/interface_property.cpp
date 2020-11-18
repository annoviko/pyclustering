/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#include <pyclustering/interface/interface_property.h>


const char * INTERFACE_DESCRIPTION  = "pyclustering library is a C/C++ part of python pyclustering library";
const char * INTERFACE_VERSION      = "0.10.1";


void * get_interface_description() {
    return (void *) INTERFACE_DESCRIPTION;
}


void * get_interface_version() {
    return (void *) INTERFACE_VERSION;
}