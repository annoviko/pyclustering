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


print_error() {
    echo "[PYCLUSTERING CI] ERROR: $1"
}


print_info() {
    echo "[PYCLUSTERING CI] INFO: $1"
}


check_failure() {
    if [ $? -ne 0 ] ; then
        if [ -z $1 ] ; then
            print_error $1
        else
            print_error "Failure exit code is detected."
        fi
        exit 1
    fi
}


run_pypi_install_job() {
    print_info "PyPi Installer Testing."
    print_info "- Download and install the library using pip3."
    print_info "- Run tests for the library."

    print_info "Install 'setuptools' for pip3."

    sudo apt-get install -qq python3-pip

    print_info "Install 'pyclustering' from PyPi."

    PYPI_SOURCE=$1

    if [[ $PYPI_SOURCE == "testpypi" ]]; then
        pip3 install --extra-index-url https://testpypi.python.org/pypi pyclustering
    else
        pip3 install pyclustering
    fi

    print_info "Navigate to the system root directory to run tests for installed version"

    cd /

    print_info "Run tests for 'pyclustering' package."

    python3 -m pyclustering.tests

    print_info "Navigate to the repository folder."

    cd -
}


run_cmake_pyclustering_build() {
    print_info "C++ pyclustering build using CMake."
    print_info "- Build C++ static and shared pyclustering library using CMake."
    print_info "- Run build verification test for the static library."
    print_info "- Run build verification test for the shared library."
    
    print_info "Create a build folder."

    mkdir ccore/build

    print_info "Navigate to the build folder."

    cd ccore/build

    print_info "Run CMake to generate makefiles to build pyclustering library."

    cmake ..

    print_info "Build C++ pyclustering shared library and build verification test for it."

    make -j8 bvt-shared

    print_info "Build C++ pyclustering static library and build verification test for it."

    make -j8 bvt-static

    print_info "Run build verification test for the C++ pyclustering shared library."
    ./bvt-shared
    check_failure "Build verification test failed for the C++ pyclustering shared library."

    print_info "Run build verification test for the C++ pyclustering static library."
    ./bvt-static
    check_failure "Build verification test failed for the C++ pyclustering static library."

    print_info "Navigate to the repository folder."

    cd -
}


set -e
set -x


case $1 in
    PYPI_INSTALLER)
        run_pypi_install_job ;;

    TESTPYPI_INSTALLER)
        run_pypi_install_job testpypi ;;

    TEST_CMAKE_PYCLUSTERING_BUILD)
        run_cmake_pyclustering_build ;;

    *)
        print_error "Unknown target is specified: '$1'"
        exit 1 ;;
esac
