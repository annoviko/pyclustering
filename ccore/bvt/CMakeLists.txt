#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


cmake_minimum_required(VERSION 3.10)

# C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Headers
include_directories(${PROJECT_SOURCE_DIR}/include)

# Build target - build verify test for static library
add_executable(bvt-static static-test.cpp)
add_dependencies(bvt-static pyclustering-static)
target_link_libraries(bvt-static PUBLIC pyclustering-static)

# Build target - build verify test for shared library
add_executable(bvt-shared shared-test.cpp)
add_dependencies(bvt-shared pyclustering-shared)

if(CMAKE_DL_LIBS)
    target_link_libraries(bvt-shared ${CMAKE_DL_LIBS})
endif()
