#ifndef SRC_DEFINITIONS_HPP_
#define SRC_DEFINITIONS_HPP_


#include <memory>
#include <vector>


#if defined (__GNUC__) && defined(__unix__)
    #define DECLARATION __attribute__ ((__visibility__("default")))
#elif defined (WIN32)
    #define DECLARATION __declspec(dllexport)
#else
    #error Unsupported platform
#endif


using point         = std::vector<double>;
using point_ptr     = std::shared_ptr<point>;

using dataset       = std::vector<point>;
using dataset_ptr   = std::shared_ptr<dataset>;


/* TODO: use pyclustering_package instead of this */
typedef struct data_representation {
public:
    unsigned int            size;
    unsigned int            dimension;
    double                  ** objects;
} data_representation;


#endif
