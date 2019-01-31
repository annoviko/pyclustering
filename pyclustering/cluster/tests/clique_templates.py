"""!

@brief Test templates for CLIQUE algorithm.

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

from pyclustering.cluster.clique import clique, clique_visualizer

from pyclustering.utils import read_sample


class clique_test_template:
    @staticmethod
    def clustering(path, intervals, density_threshold, expected_clusters, expected_noise, ccore_enabled, **kwargs):
        sample = read_sample(path)
        dimension = len(sample[0])

        clique_instance = clique(sample, intervals, density_threshold, ccore=ccore_enabled)
        clique_instance.process()

        clusters = clique_instance.get_clusters()
        noise = clique_instance.get_noise()
        cells = clique_instance.get_cells()

        assertion.eq(len(cells), pow(intervals, dimension))

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

        covered_points = set()
        for cell in cells:
            points = cell.points
            for index_point in points:
                covered_points.add(index_point)

        assertion.eq(len(sample), len(covered_points))
        return clique_instance


    @staticmethod
    def visualize(path, levels, threshold, ccore_enabled, **kwargs):
        sample = read_sample(path)

        clique_instance = clique(sample, levels, threshold, ccore=ccore_enabled)
        clique_instance.process()

        cells = clique_instance.get_cells()

        clique_visualizer.show_grid(cells, sample)


    @staticmethod
    def exception(type, sample_storage, levels, threshold, ccore_enabled):
        try:
            sample = sample_storage
            if isinstance(sample_storage, str):
                sample = read_sample(sample_storage)

            bang_instance = clique(sample, levels, threshold, ccore=ccore_enabled)
            bang_instance.process()

        except type:
            return

        except Exception as ex:
            raise AssertionError("Expected: '%s', Actual: '%s'" % (type, type(ex).__name__))

        raise AssertionError("Expected: '%s', Actual: 'None'" % type)