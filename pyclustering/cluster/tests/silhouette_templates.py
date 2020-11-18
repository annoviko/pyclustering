"""!

@brief Test templates for Silhouette clustering module.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import math

from pyclustering.cluster.silhouette import silhouette, silhouette_ksearch

from pyclustering.samples import answer_reader
from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.tests.assertion import assertion

from pyclustering.utils import read_sample, calculate_distance_matrix, distance_metric, type_metric


class silhouette_test_template:
    @staticmethod
    def correct_scores(sample_path, answer_path, ccore_flag, **kwargs):
        data_type = kwargs.get('data_type', 'points')

        sample = read_sample(sample_path)
        if data_type == 'distance_matrix':
            sample = calculate_distance_matrix(sample, distance_metric(type_metric.EUCLIDEAN_SQUARE))

        clusters = answer_reader(answer_path).get_clusters()

        scores = silhouette(sample, clusters, ccore=ccore_flag, data_type=data_type).process().get_score()

        assertion.eq(len(sample), len(scores))
        for score in scores:
            assertion.le(-1.0, score)
            assertion.ge(1.0, score)

        return scores


    @staticmethod
    def correct_processing_data_types(sample_path, answer_path, ccore_flag):
        scores_points = silhouette_test_template.correct_scores(sample_path, answer_path, ccore_flag, data_type='points')
        scores_matrix = silhouette_test_template.correct_scores(sample_path, answer_path, ccore_flag, data_type='distance_matrix')

        assertion.eq(len(scores_points), len(scores_matrix))
        assertion.eq(scores_points, scores_matrix)


    @staticmethod
    def correct_ksearch(sample_path, answer_path, kmin, kmax, algorithm, ccore_flag):
        attempts = 15
        testing_result = False

        sample = read_sample(sample_path)
        clusters = answer_reader(answer_path).get_clusters()

        for _ in range(attempts):
            ksearch_instance = silhouette_ksearch(sample, kmin, kmax, algorithm=algorithm, ccore=ccore_flag).process()
            amount = ksearch_instance.get_amount()
            score = ksearch_instance.get_score()
            scores = ksearch_instance.get_scores()

            assertion.le(-1.0, score)
            assertion.ge(1.0, score)
            assertion.eq(kmax - kmin, len(scores))

            upper_limit = len(clusters) + 1
            lower_limit = len(clusters) - 1
            if lower_limit < 1:
                lower_limit = 1

            if (amount > upper_limit) or (amount < lower_limit):
                continue

            testing_result = True
            break

        assertion.true(testing_result)


    @staticmethod
    def random_state(kmin, kmax, algorithm, random_state, ccore_flag):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

        ksearch_instance_1 = silhouette_ksearch(sample, kmin, kmax, algorithm=algorithm, random_state=random_state,
                                                ccore=ccore_flag).process()

        ksearch_instance_2 = silhouette_ksearch(sample, kmin, kmax, algorithm=algorithm, random_state=random_state,
                                                ccore=ccore_flag).process()

        assertion.eq(ksearch_instance_1.get_amount(), ksearch_instance_2.get_amount())
        assertion.eq(ksearch_instance_1.get_score(), ksearch_instance_2.get_score())
        assertion.eq(len(ksearch_instance_1.get_scores()), len(ksearch_instance_2.get_scores()))

        scores1 = ksearch_instance_1.get_scores()
        scores2 = ksearch_instance_2.get_scores()
        for key in scores1:
            key = int(key)
            if math.isnan(scores1[key]) and math.isnan(scores2[key]):
                continue
            else:
                assertion.eq(scores1[key], scores2[key])
