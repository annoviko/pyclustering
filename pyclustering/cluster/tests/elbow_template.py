"""!

@brief Test templates for Elbow clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import math

from pyclustering.utils import read_sample

from pyclustering.cluster.elbow import elbow

from pyclustering.tests.assertion import assertion

from pyclustering.samples import answer_reader


class elbow_test_template:
    @staticmethod
    def calculate_elbow(path_to_data, path_to_answer, kmin, kmax, ccore, **kwargs):
        repeat = 15  # Elbow method randomly chooses initial centers therefore we need to repeat test if it fails.
        testing_result = False
        kstep = kwargs.get('kstep', 1)

        sample = read_sample(path_to_data)

        expected_clusters_amount = None
        if path_to_answer is not None:
            if isinstance(path_to_answer, int):
                expected_clusters_amount = path_to_answer
            else:
                expected_clusters_amount = len(answer_reader(path_to_answer).get_clusters())

        additional_info = []

        for _ in range(repeat):
            elbow_instance = elbow(sample, kmin, kmax, ccore=ccore, **kwargs)
            elbow_instance.process()

            actual_elbow = elbow_instance.get_amount()
            actual_wce = elbow_instance.get_wce()

            assertion.gt(actual_elbow, kmin)
            assertion.lt(actual_elbow, kmax)
            assertion.eq(len(actual_wce), math.floor((kmax - kmin) / kstep + 1))
            assertion.lt(actual_wce[-1], actual_wce[0] + 0.0000001)

            if (expected_clusters_amount is not None) and (actual_elbow != expected_clusters_amount):
                additional_info.append(actual_elbow)
                continue

            testing_result = True
            break

        message = None
        if expected_clusters_amount is not None:
            message = str(expected_clusters_amount) + ": " + str(additional_info)

        assertion.true(testing_result, message=message)


    @staticmethod
    def random_state_fixed(path_to_data, kmin, kmax, ccore, **kwargs):
        repeat = kwargs.get('repeat', 1)
        kstep = kwargs.get('kstep', 1)

        for _ in range(repeat):
            sample = read_sample(path_to_data)

            elbow_instance = elbow(sample, kmin, kmax, ccore=ccore, **kwargs).process()
            elbow_1 = elbow_instance.get_amount()
            wce_1 = elbow_instance.get_wce()

            assertion.eq(len(wce_1), (kmax - kmin) / kstep + 1)

            elbow_instance = elbow(sample, kmin, kmax, ccore=ccore, **kwargs).process()
            elbow_2 = elbow_instance.get_amount()
            wce_2 = elbow_instance.get_wce()

            assertion.eq(len(wce_2), (kmax - kmin) / kstep + 1)

            assertion.eq(elbow_1, elbow_2)
            assertion.eq(wce_1, wce_2)
