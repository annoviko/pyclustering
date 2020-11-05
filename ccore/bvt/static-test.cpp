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


#include <pyclustering/cluster/gmeans.hpp>


#define SUCCESS                                      0
#define FAILURE_INCORRECT_RESULT                    -1


int main() {
    pyclustering::clst::gmeans_data result;
    pyclustering::clst::gmeans algorithm(2);

    algorithm.process({ { 1.0 }, { 1.2 }, { 1.1 }, { 3.0 }, { 3.2 }, { 3.1 }, { 8.0 }, { 8.2 }, { 8.1 } }, result);

    if (result.clusters().empty()) {
        return FAILURE_INCORRECT_RESULT;
    }

    return SUCCESS;
}
