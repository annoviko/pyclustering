#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


cmake_minimum_required(VERSION 3.10)


project(pyclustering VERSION 0.10.1 LANGUAGES CXX)


file(MAKE_DIRECTORY build)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build)

add_subdirectory(bvt)
add_subdirectory(external)
add_subdirectory(src)
add_subdirectory(tst)
