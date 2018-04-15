"""!

@brief Cluster analysis algorithm: BSAS
@details Implementation based on book:
         - Theodoridis, Koutroumbas, Konstantinos. Elsevier Academic Press - Pattern Recognition - 2nd Edition. 2003.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


class bsas:
    def __init__(self, maximum_clusters, threshold, ccore=True):
        self.__maximum_clusters = maximum_clusters;
        self.__threshold = threshold;
        self.__ccore = ccore;

    def process(self):
        pass;

    def get_clusters(self):
        pass;