"""!

@brief Unit-tests for Silhouette algorithms.

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

import unittest

from pyclustering.cluster.silhouette import silhouette, silhouette_ksearch, silhouette_ksearch_type

from pyclustering.samples import answer_reader
from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS

from pyclustering.tests.assertion import assertion

from pyclustering.utils import read_sample


class silhouette_unit_tests(unittest.TestCase):
    def template_correct_scores(self, sample_path, answer_path):
        sample = read_sample(sample_path)
        clusters = answer_reader(answer_path).get_clusters()

        scores = silhouette(sample, clusters).process().get_score()

        assertion.eq(len(sample), len(scores))
        for score in scores:
            assertion.le(-1.0, score)
            assertion.ge(1.0, score)

    def test_correct_score_simple01(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1)

    def test_correct_score_simple02(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2)

    def test_correct_score_simple03(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3)

    def test_correct_score_simple04(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4)

    def test_correct_score_simple05(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5)

    def test_correct_score_simple06(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6)

    def test_correct_score_simple07(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7)

    def test_correct_score_simple08(self):
        self.template_correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8)


    def template_correct_ksearch(self, sample_path, answer_path, kmin, kmax, algorithm):
        attempts = 5
        testing_result = False

        sample = read_sample(sample_path)
        clusters = answer_reader(answer_path).get_clusters()

        for _ in range(attempts):
            ksearch_instance = silhouette_ksearch(sample, kmin, kmax, algorithm=algorithm).process()
            amount = ksearch_instance.get_amount()
            score = ksearch_instance.get_score()
            scores = ksearch_instance.get_scores()

            assertion.le(-1.0, score)
            assertion.ge(1.0, score)
            assertion.eq(kmax - kmin, len(scores))

            if amount != len(clusters): continue
            testing_result = True
            break

        assertion.true(testing_result)

    def test_correct_ksearch_simple01(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple01_kmedoids(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 2, 10,
                                      silhouette_ksearch_type.KMEDOIDS)

    def test_correct_ksearch_simple01_kmedians(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 2, 10,
                                      silhouette_ksearch_type.KMEDIANS)

    def test_correct_ksearch_simple02(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple03(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple04(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple05(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple06(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple07(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple08(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple09(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple10(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple11(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple12(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

    def test_correct_ksearch_simple13(self):
        self.template_correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, 2, 10,
                                      silhouette_ksearch_type.KMEANS)

if __name__ == "__main__":
    unittest.main()
