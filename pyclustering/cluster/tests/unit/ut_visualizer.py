"""!

@brief Unit-tests for cluster visualizers.
@details This tests should be run manually to without option 'matplotlib.use('Agg')' to check that everything is
          displayed correctly, because these tests check that there is no exceptions and critical failures.

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

from pyclustering.cluster import cluster_visualizer_multidim

from pyclustering.samples import answer_reader
from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS, FAMOUS_SAMPLES, FAMOUS_ANSWERS

from pyclustering.utils import read_sample


class visualizer_unit_tests(unittest.TestCase):
    def template_visualize(self, path_sample, path_answer, filter=None, **kwargs):
        data = read_sample(path_sample)
        clusters = answer_reader(path_answer).get_clusters()

        visualizer = cluster_visualizer_multidim()
        visualizer.append_clusters(clusters, data)
        visualizer.show(filter, **kwargs)


    def template_visualize_adding_step_by_step(self, path_sample, path_answer, filter=None, **kwargs):
        data = read_sample(path_sample)
        clusters = answer_reader(path_answer).get_clusters()

        visualizer = cluster_visualizer_multidim()
        for cluster in clusters:
            visualizer.append_cluster(cluster, data)

        visualizer.show(filter, **kwargs)


    def test_multidim_one_dimension_simple07(self):
        self.template_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7)

    def test_multidim_one_dimension_simple08(self):
        self.template_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8)

    def test_multidim_two_dimension_simple01(self):
        self.template_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1)

    def test_multidim_two_dimension_simple02(self):
        self.template_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2)

    def test_multidim_two_dimension_simple03(self):
        self.template_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3)

    def test_multidim_three_dimension_simple11(self):
        self.template_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11)

    def test_multidim_four_dimension_iris(self):
        self.template_visualize(FAMOUS_SAMPLES.SAMPLE_IRIS, FAMOUS_ANSWERS.ANSWER_IRIS)

    def test_multidim_four_dimension_one_column(self):
        self.template_visualize(FAMOUS_SAMPLES.SAMPLE_IRIS, FAMOUS_ANSWERS.ANSWER_IRIS, max_row_size=1)

    def test_multidim_non_default_settings(self):
        self.template_visualize(FAMOUS_SAMPLES.SAMPLE_IRIS, FAMOUS_ANSWERS.ANSWER_IRIS,
                                max_row_size=2,
                                visible_axis=True,
                                visible_labels=False,
                                visible_grid=False)

    def test_multidim_simple07_by_steps(self):
        self.template_visualize_adding_step_by_step(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7)

    def test_multidim_simple08_by_steps(self):
        self.template_visualize_adding_step_by_step(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8)
