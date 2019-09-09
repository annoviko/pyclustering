"""!

@brief Test templates for Silhouette clustering module.

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


from pyclustering.cluster.silhouette import silhouette, silhouette_ksearch

from pyclustering.samples import answer_reader

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
