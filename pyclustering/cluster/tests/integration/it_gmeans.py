"""!

@brief Integration-tests for G-Means algorithm.

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

from pyclustering.cluster.tests.gmeans_templates import gmeans_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS


class gmeans_integration_test(unittest.TestCase):
    def test_clustering_sample_01(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, True)

    def test_clustering_sample_02(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, True)

    def test_clustering_sample_03(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, True)

    def test_clustering_sample_05(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 1, True)

    def test_clustering_sample_06(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 1, True)

    def test_clustering_sample_07(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 1, True)

    def test_clustering_sample_08(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, 1, True)

    def test_clustering_sample_09(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 1, True)

    def test_clustering_sample_10(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 1, True)

    def test_clustering_sample_11(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 1, True)

    def test_clustering_sample_12(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 1, True)

    def test_clustering_sample_13(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, 1, True)
