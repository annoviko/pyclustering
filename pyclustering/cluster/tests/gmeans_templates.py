"""!

@brief Test templates for G-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.samples import answer_reader
from pyclustering.cluster.gmeans import gmeans
from pyclustering.utils import read_sample


class gmeans_test_template(unittest.TestCase):
    def clustering(self, sample_path, answer, amount, ccore, **kwargs):
        attempts = 10

        failures = ""

        k_max = kwargs.get('k_max', -1)
        random_state = kwargs.get('random_state', None)
        data = read_sample(sample_path)

        if isinstance(answer, str):
            reader = answer_reader(answer)
            expected_length_clusters = sorted(reader.get_cluster_lengths())
            amount_clusters = len(expected_length_clusters)

        elif isinstance(answer, int):
            expected_length_clusters = None
            amount_clusters = answer

        else:
            expected_length_clusters = answer
            amount_clusters = len(answer)

        for _ in range(attempts):
            gmeans_instance = gmeans(data, amount, ccore, k_max=k_max, random_state=random_state).process()

            clusters = gmeans_instance.get_clusters()
            centers = gmeans_instance.get_centers()
            wce = gmeans_instance.get_total_wce()

            self.assertEqual(amount_clusters, len(centers))

            if len(clusters) > 1:
                self.assertGreater(wce, 0.0)
            else:
                self.assertGreaterEqual(wce, 0.0)

            if len(clusters) != amount_clusters:
                failures += "1. %d != %d\n" % (len(clusters), amount_clusters)
                continue

            unique_indexes = set()
            for cluster in clusters:
                for index_point in cluster:
                    unique_indexes.add(index_point)

            if len(data) != len(unique_indexes):
                failures += "2. %d != %d\n" % (len(data), len(unique_indexes))
                continue

            if expected_length_clusters is None:
                return

            expected_total_length = sum(expected_length_clusters)
            actual_total_length = sum([len(cluster) for cluster in clusters])
            if expected_total_length != actual_total_length:
                failures += "3. %d != %d\n" % (expected_total_length, actual_total_length)
                continue

            actual_length_clusters = sorted([len(cluster) for cluster in clusters])
            if expected_length_clusters != actual_length_clusters:
                failures += "4. %s != %s\n" % (str(expected_length_clusters), str(actual_length_clusters))
                continue

            return

        self.fail("Expected result is not obtained during %d attempts: %s\n" % (attempts, failures))