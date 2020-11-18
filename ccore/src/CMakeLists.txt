#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright BSD-3-Clause
#


cmake_minimum_required(VERSION 3.10)


# C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Required packages
find_package(Threads REQUIRED)

# Sources
file(GLOB_RECURSE PYCLUSTERING_SOURCES "*.cpp")


# Headers
include_directories(${PROJECT_SOURCE_DIR}/include)


# Build targets
add_library(pyclustering-static STATIC ${PYCLUSTERING_SOURCES})
target_link_libraries(pyclustering-static Threads::Threads)

add_library(pyclustering-shared SHARED ${PYCLUSTERING_SOURCES})
target_compile_definitions(pyclustering-shared PUBLIC EXPORT_PYCLUSTERING_INTERFACE)
target_link_libraries(pyclustering-shared Threads::Threads)
set_target_properties(pyclustering-shared PROPERTIES OUTPUT_NAME "pyclustering")

add_library(pyclustering SHARED ${PYCLUSTERING_SOURCES})
target_compile_definitions(pyclustering PUBLIC EXPORT_PYCLUSTERING_INTERFACE)
target_link_libraries(pyclustering Threads::Threads)

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(PYCLUSTERING_BINARY_DIR "pyclustering/core/64-bit")
elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    set(PYCLUSTERING_BINARY_DIR "pyclustering/core/32-bit")
endif()

if (UNIX)
    string(CONCAT PYCLUSTERING_BINARY_DIR ${PYCLUSTERING_BINARY_DIR} "/linux")
elseif (WIN32)
    string(CONCAT PYCLUSTERING_BINARY_DIR ${PYCLUSTERING_BINARY_DIR} "/win")
elseif (APPLE)
    string(CONCAT PYCLUSTERING_BINARY_DIR ${PYCLUSTERING_BINARY_DIR} "/macos")
endif()

string(CONCAT PYCLUSTERING_BINARY_DIR "${PROJECT_SOURCE_DIR}/../" ${PYCLUSTERING_BINARY_DIR})

add_custom_command(TARGET pyclustering-shared POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:pyclustering-shared> ${PYCLUSTERING_BINARY_DIR}
    COMMENT "Copying pyclustering binary to the package '${PYCLUSTERING_BINARY_DIR}'."
)
