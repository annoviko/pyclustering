"""!

@brief Test templates for G-Means algorithm.

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


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.samples import answer_reader
from pyclustering.cluster.gmeans import gmeans
from pyclustering.utils import read_sample


class gmeans_test_template(unittest.TestCase):
    def clustering(self, sample_path, answer_path, amount, ccore):
        attempts = 10

        failures = ""

        for _ in range(attempts):
            data = read_sample(sample_path)

            gmeans_instance = gmeans(data, amount, ccore).process()

            reader = answer_reader(answer_path)
            expected_length_clusters = sorted(reader.get_cluster_lengths())

            clusters = gmeans_instance.get_clusters()
            centers = gmeans_instance.get_centers()
            wce = gmeans_instance.get_total_wce()

            self.assertEqual(len(expected_length_clusters), len(centers))

            if len(clusters) > 1:
                self.assertGreater(wce, 0.0)
            else:
                self.assertGreaterEqual(wce, 0.0)

            unique_indexes = set()
            for cluster in clusters:
                for index_point in cluster:
                    unique_indexes.add(index_point)

            if len(data) != len(unique_indexes):
                failures += "1. %d != %d\n" % (len(data), len(unique_indexes))
                continue

            expected_total_length = sum(expected_length_clusters)
            actual_total_length = sum([len(cluster) for cluster in clusters])
            if expected_total_length != actual_total_length:
                failures += "2. %d != %d\n" % (expected_total_length, actual_total_length)
                continue

            actual_length_clusters = sorted([len(cluster) for cluster in clusters])
            if expected_length_clusters != actual_length_clusters:
                failures += "3. %s != %s\n" % (str(expected_length_clusters), str(actual_length_clusters))
                continue

            return

        self.fail("Expected result is not obtained during %d attempts: %s\n" % (attempts, failures))