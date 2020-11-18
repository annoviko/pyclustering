/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


/*

@brief This is a build verification test (smoke test) that checks possibility to use the library as a shared library by calling one of the functions.

@return     `0` if the build verification test passed, otherwise negative values that define errors that might occur.

*/


#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    #include <dlfcn.h>
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    #include <windows.h>
#else
    #error Unsupported platform
#endif

#include <algorithm>
#include <cstring>
#include <iostream>
#include <string>
#include <unordered_map>


#define SUCCESS                                      0
#define FAILURE_IMPOSSIBLE_TO_LOAD_LIBRARY           1
#define FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION          2
#define FAILURE_IMPOSSIBLE_TO_CHECK_VERSION          3
#define FAILURE_IMPOSSIBLE_TO_CHECK_DESCRIPTION      4
#define FAILURE_INCORRECT_VERSION                    5
#define FAILURE_INCORRECT_DESCRIPTION                6


const std::unordered_map<int, std::string> EXIT_CODE_DESCRIPTION = {
    { SUCCESS, "Build verification test for C++ pyclustering shared library is successfully passed." },
    { FAILURE_IMPOSSIBLE_TO_LOAD_LIBRARY, "Error: Impossible to load C++ pyclustering shared library." },
    { FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION, "Error: Impossible to load function from C++ pyclustering shared library." },
    { FAILURE_IMPOSSIBLE_TO_CHECK_VERSION, "Error: Impossible to check version of C++ pyclustering shared library." },
    { FAILURE_IMPOSSIBLE_TO_CHECK_DESCRIPTION, "Error: Impossible to check description of C++ pyclustering shared library." },
    { FAILURE_INCORRECT_VERSION, "Error: C++ pyclustering library contains wrong version." },
    { FAILURE_INCORRECT_DESCRIPTION, "Error: C++ pyclustering library contains wrong description." }
};


void exit_with_code(const int p_code) {
    const auto iter = EXIT_CODE_DESCRIPTION.find(p_code);
    if (iter != EXIT_CODE_DESCRIPTION.cend()) {
        if (p_code != SUCCESS) {
            std::cerr << iter->second << std::endl;
        }
        else {
            std::cout << iter->second << std::endl;
        }
    }

    std::exit(p_code);
}


void * load_pyclustering(void) {
#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    return dlopen("./libpyclustering.so", RTLD_LAZY);
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    return LoadLibrary("pyclustering.dll");
#else
    #error Unsupported platform
#endif
}


void close_pyclustering(void * library) {
#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    dlclose(library);
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    FreeLibrary((HMODULE) library);
#endif
}


using interface_desc_func_t = void * (void);
using interface_vers_func_t = void * (void);


interface_desc_func_t * get_interface_desc_func(void * library) {
#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    return (interface_desc_func_t *) dlsym(library, "get_interface_description");
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    return (interface_desc_func_t *) GetProcAddress((HMODULE) library, "get_interface_description");
#endif
}


interface_vers_func_t * get_interface_vers_func(void * library) {
#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    return (interface_vers_func_t *) dlsym(library, "get_interface_version");
#elif defined (WIN32) || (_WIN32) || (_WIN64)
    return (interface_vers_func_t *) GetProcAddress((HMODULE) library, "get_interface_version");
#endif
}


int main() {
    void * library = load_pyclustering();
    if (!library) {
        exit_with_code(FAILURE_IMPOSSIBLE_TO_LOAD_LIBRARY);
    }

    interface_vers_func_t * get_version = get_interface_vers_func(library);
    if (!get_version) {
        exit_with_code(FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION);
    }

    interface_desc_func_t * get_description = get_interface_desc_func(library);
    if (!get_description) {
        exit_with_code(FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION);
    }

    const char * version = (const char *)get_version();
    if (!version) {
        exit_with_code(FAILURE_IMPOSSIBLE_TO_CHECK_VERSION);
    }

    if (strlen(version) == 0) {
        exit_with_code(FAILURE_INCORRECT_VERSION);
    }

    const char * description = (const char *)get_description();
    if (!description) {
        exit_with_code(FAILURE_IMPOSSIBLE_TO_CHECK_DESCRIPTION);
    }

    std::string description_as_string(description);
    if (description_as_string.find("pyclustering") == std::string::npos) {
        exit_with_code(FAILURE_INCORRECT_DESCRIPTION);
    }

    close_pyclustering(library);

    exit_with_code(SUCCESS);
}
