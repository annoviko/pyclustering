"""!

@brief Cluster analysis algorithm: MBSAS (Modified Basic Sequential Algorithmic Scheme).
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


from pyclustering.cluster.bsas import bsas;


class mbsas(bsas):
    def __init__(self, data, maximum_clusters, threshold, ccore=True, **kwargs):
        super().__init__(data, maximum_clusters, threshold, ccore, **kwargs);

    def process(self):
        self._clusters.append([0]);
        self._representatives.append(self._data[0]);

        skipped_objects = [];

        for i in range(1, len(self._data)):
            point = self._data[i];
            index_cluster, distance = self._find_nearest_cluster(point);

            if (distance > self._threshold) and (len(self._clusters) < self._amount):
                self._representatives.append(point);
                self._clusters.append([i]);
            else:
                skipped_objects.append(i);

        for i in skipped_objects:
            point = self._data[i];
            index_cluster, _ = self._find_nearest_cluster(point);

            self._clusters[index_cluster].append(i);
            self._update_representative(index_cluster, point);

