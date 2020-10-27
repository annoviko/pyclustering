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


run_pypi_install_job() {
    print_info "Install (installer testing)."
    print_info "- Install pyclustering library from pypi."
    print_info "- Run tests for the library."

    PYPI_SOURCE=$1

    if [[ $PYPI_SOURCE == "testpypi" ]]; then
        pip3 install --extra-index-url https://testpypi.python.org/pypi pyclustering
    else
        pip3 install pyclustering
    fi

    python3 -m pyclustering.tests
}


set -e
set -x


case $1 in
    PYPI_INSTALLER)
        run_pypi_install_job ;;

    TEST_PYPI_INSTALLER)
        run_pypi_install_job testpypi ;;

    *)
        print_error "Unknown target is specified: '$1'"
        exit 1 ;;
esac
