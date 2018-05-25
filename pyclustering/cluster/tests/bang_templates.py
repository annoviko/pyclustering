"""!

@brief Test templates for BANG algorithm.

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


# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.assertion import assertion

from pyclustering.cluster.bang import bang, bang_visualizer

from pyclustering.utils import read_sample


class bang_test_template:
    @staticmethod
    def clustering(path, levels, threshold, expected_clusters, expected_noise, ccore, **kwargs):
        sample = read_sample(path)

        bang_instance = bang(sample, levels, threshold, ccore)
        bang_instance.process()

        clusters = bang_instance.get_clusters()
        noise = bang_instance.get_noise()
        directory = bang_instance.get_directory()
        dendrogram = bang_instance.get_dendrogram()

        assertion.eq(len(expected_clusters), len(clusters))
        assertion.eq(len(clusters), len(dendrogram))

        obtained_length = 0
        obtained_cluster_length = []
        for cluster in clusters:
            obtained_length += len(cluster)
            obtained_cluster_length.append(len(cluster))

        assertion.eq(len(sample), obtained_length)
        assertion.eq(len(expected_noise), len(noise))
        assertion.eq(expected_clusters, obtained_cluster_length)

        leafs = directory.get_leafs()
        covered_points = set()
        for leaf in leafs:
            covered_points.add(set(leaf.get_points()))

        assertion.eq(len(sample), len(covered_points))