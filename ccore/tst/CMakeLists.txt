#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


cmake_minimum_required(VERSION 3.10)


# C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# Sources
file(GLOB_RECURSE UT_SOURCES "*.cpp")


# Header folders
include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/external/include)


# Library folders
link_directories(${PROJECT_SOURCE_DIR}/build)


# Build targets
add_executable(utcore ${UT_SOURCES})

# Dependecies
add_dependencies(utcore pyclustering-static)
add_dependencies(utcore gtest)
target_link_libraries(utcore PUBLIC pyclustering-static)
target_link_libraries(utcore PUBLIC gtest)
