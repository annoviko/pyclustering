/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

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
#include <string>


#define SUCCESS                                      0
#define FAILURE_IMPOSSIBLE_TO_LOAD_LIBRARY           1
#define FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION          2
#define FAILURE_IMPOSSIBLE_TO_CHECK_VERSION          3
#define FAILURE_IMPOSSIBLE_TO_CHECK_DESCRIPTION      4
#define FAILURE_INCORRECT_VERSION                    5
#define FAILURE_INCORRECT_DESCRIPTION                6


void * load_pyclustering(void) {
#if (defined (__GNUC__) && defined(__unix__)) || defined(__APPLE__)
    return dlopen("libpyclustering.so", RTLD_LAZY);
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
    return (interface_desc_func_t *) dlsym(library, "get_interface_version");
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
        return FAILURE_IMPOSSIBLE_TO_LOAD_LIBRARY;
    }

    interface_vers_func_t * get_version = get_interface_vers_func(library);
    if (!get_version) {
        return FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION;
    }

    interface_desc_func_t * get_description = get_interface_desc_func(library);
    if (!get_description) {
        return FAILURE_IMPOSSIBLE_TO_LOAD_FUNCTION;
    }

    const char * version = (const char *)get_version();
    if (!version) {
        return FAILURE_IMPOSSIBLE_TO_CHECK_VERSION;
    }

    if (strlen(version) == 0) {
        return FAILURE_INCORRECT_VERSION;
    }

    const char * description = (const char *)get_description();
    if (!description) {
        return FAILURE_IMPOSSIBLE_TO_CHECK_DESCRIPTION;
    }

    std::string description_as_string(description);
    if (description_as_string.find("pyclustering") == std::string::npos) {
        return FAILURE_INCORRECT_DESCRIPTION;
    }

    close_pyclustering(library);

    return SUCCESS;
}
