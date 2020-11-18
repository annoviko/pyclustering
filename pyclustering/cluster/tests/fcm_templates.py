"""!

@brief Test templates for Fuzzy C-Means (FCM) clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.tests.assertion import assertion

from pyclustering.cluster.fcm import fcm

from pyclustering.utils import read_sample


class fcm_test_template:
    @staticmethod
    def cluster_allocation(path, initial_centers, m, expected_cluster_length, ccore, **kwargs):
        itermax = kwargs.get('itermax', 100)
        tolerance = kwargs.get('tolerance', 0.001)

        sample = read_sample(path)

        fcm_instance = fcm(sample, initial_centers, m=m, ccore=ccore, tolerance=tolerance, itermax=itermax)
        fcm_instance.process()

        clusters = fcm_instance.get_clusters()
        centers = fcm_instance.get_centers()
        membership = fcm_instance.get_membership()

        if itermax == 0:
            assertion.eq([], clusters)
            assertion.eq(initial_centers, centers)
            assertion.eq([], membership)
            return

        for probabilities in membership:
            total_probability = 0.0
            for p in probabilities:
                total_probability += p

            assertion.eq_float(1.0, total_probability, 0.0000001)

        obtained_cluster_sizes = [len(cluster) for cluster in clusters]
        assertion.eq(len(sample), sum(obtained_cluster_sizes))

        assertion.eq(len(clusters), len(centers))
        for center in centers:
            assertion.eq(len(sample[0]), len(center))

        if expected_cluster_length is not None:
            obtained_cluster_sizes.sort()
            expected_cluster_length.sort()
            assertion.eq(obtained_cluster_sizes, expected_cluster_length)
