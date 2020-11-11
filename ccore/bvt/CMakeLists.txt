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
