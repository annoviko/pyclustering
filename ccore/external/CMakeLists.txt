#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


cmake_minimum_required(VERSION 3.10)

# C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Source for google test framework
file(GLOB_RECURSE GTEST_SOURCES src/gtest "*.cpp")

# Headers
include_directories(include)

# Build targets
add_library(gtest STATIC ${GTEST_SOURCES})
