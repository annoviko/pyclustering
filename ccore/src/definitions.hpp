#ifndef SRC_DEFINITIONS_HPP_
#define SRC_DEFINITIONS_HPP_


#include <vector>


#if defined (__GNUC__) && defined(__unix__)
    #define DECLARATION __attribute__ ((__visibility__("default")))
#elif defined (WIN32)
    #define DECLARATION __declspec(dllexport)
#else
    #error Unsupported platform
#endif


using point     = std::vector<double>;

using dataset   = std::vector<point>;


#endif
