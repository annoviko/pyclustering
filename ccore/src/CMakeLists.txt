#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright GNU Public License
#
# @cond GNU_PUBLIC_LICENSE
#   pyclustering is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyclustering is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
# @endcond
#


cmake_minimum_required(VERSION 3.10)


# C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# Sources
file(GLOB_RECURSE PYCLUSTERING_SOURCES "*.cpp")


# Headers
include_directories(${PROJECT_SOURCE_DIR}/include)


# Executable
if (BUILD_STATIC_LIB)
    add_library(pyclustering STATIC ${PYCLUSTERING_SOURCES})
elseif(BUILD_SHARED_LIB)
    add_compile_definitions(EXPORT_PYCLUSTERING_INTERFACE)
    add_library(pyclustering SHARED ${PYCLUSTERING_SOURCES})
else()
    add_compile_definitions(EXPORT_PYCLUSTERING_INTERFACE)
    add_library(pyclustering SHARED ${PYCLUSTERING_SOURCES})
endif()
