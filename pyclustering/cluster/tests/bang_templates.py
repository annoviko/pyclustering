"""!

@brief Test templates for BANG algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
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

from pyclustering.cluster.bang import bang, bang_visualizer, bang_animator

from pyclustering.utils import read_sample


class bang_test_template:
    @staticmethod
    def clustering(path, levels, density_threshold, expected_clusters, expected_noise, ccore, **kwargs):
        sample = read_sample(path)

        amount_threshold = kwargs.get('amount_threshold', 0)

        bang_instance = bang(sample, levels, ccore,
                             density_threshold=density_threshold,
                             amount_threshold=amount_threshold)

        bang_instance.process()

        clusters = bang_instance.get_clusters()
        noise = bang_instance.get_noise()
        directory = bang_instance.get_directory()
        dendrogram = bang_instance.get_dendrogram()

        assertion.eq(len(clusters), len(dendrogram))

        obtained_length = len(noise)
        obtained_cluster_length = []
        for cluster in clusters:
            obtained_length += len(cluster)
            obtained_cluster_length.append(len(cluster))

        obtained_cluster_length.sort()

        assertion.eq(len(sample), obtained_length)
        assertion.eq(expected_noise, len(noise))

        if expected_clusters is not None:
            assertion.eq(len(expected_clusters), len(clusters))
            assertion.eq(expected_clusters, obtained_cluster_length)

        leafs = directory.get_leafs()
        covered_points = set()
        for leaf in leafs:
            points = leaf.get_points()
            for index_point in points:
                covered_points.add(index_point)

        assertion.eq(len(sample), len(covered_points))
        return bang_instance


    @staticmethod
    def visualize(path, levels, threshold, ccore, **kwargs):
        sample = read_sample(path)

        bang_instance = bang(sample, levels, ccore, density_threshold=threshold)
        bang_instance.process()

        directory = bang_instance.get_directory()
        dendrogram = bang_instance.get_dendrogram()

        bang_visualizer.show_blocks(directory)
        bang_visualizer.show_dendrogram(dendrogram)


    @staticmethod
    def animate(path, levels, threshold, ccore, **kwargs):
        sample = read_sample(path)

        bang_instance = bang(sample, levels, ccore, density_threshold=threshold)
        bang_instance.process()

        directory = bang_instance.get_directory()
        clusters = bang_instance.get_clusters()
        noise = bang_instance.get_noise()

        animator = bang_animator(directory, clusters)
        animator.animate()


    @staticmethod
    def exception(type, sample_storage, levels, threshold, ccore):
        try:
            sample = sample_storage
            if isinstance(sample_storage, str):
                sample = read_sample(sample_storage)

            bang_instance = bang(sample, levels, ccore, density_threshold=threshold)
            bang_instance.process()

        except type:
            return

        except Exception as ex:
            raise AssertionError("Expected: '%s', Actual: '%s'" % (type, type(ex).__name__))

        raise AssertionError("Expected: '%s', Actual: 'None'" % type)