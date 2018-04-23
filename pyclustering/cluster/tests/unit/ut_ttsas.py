"""!

@brief Unit-tests for TTSAS algorithm.

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

import unittest;
import matplotlib;

matplotlib.use('Agg');

from pyclustering.tests.assertion import assertion;

from pyclustering.cluster.ttsas import ttsas;

from pyclustering.utils import read_sample;
from pyclustering.utils.metric import type_metric, distance_metric;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class ttsas_test:
    @staticmethod
    def clustering(path, threshold1, threshold2, expected, ccore, **kwargs):
        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN));

        sample = read_sample(path);

        ttsas_instance = ttsas(sample, threshold1, threshold2, ccore=ccore, metric=metric);
        ttsas_instance.process();

        clusters = ttsas_instance.get_clusters();
        representatives = ttsas_instance.get_representatives();

        obtained_length = 0;
        obtained_cluster_length = [];
        for cluster in clusters:
            obtained_length += len(cluster);
            obtained_cluster_length.append(len(cluster));

        assertion.eq(len(sample), obtained_length);
        assertion.eq(len(expected), len(clusters));
        assertion.eq(len(expected), len(representatives));
        assertion.ge(len(sample), len(clusters));

        dimension = len(sample[0]);
        for rep in representatives:
            assertion.eq(dimension, len(rep));

        expected.sort();
        obtained_cluster_length.sort();

        assertion.eq(expected, obtained_cluster_length);



class ttsas_unit_tests(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False);

    def testClusteringSampleSimple1Euclidean(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False, metric=distance_metric(type_metric.EUCLIDEAN));

    def testClusteringSampleSimple1EuclideanSquare(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 100.0, 200.0, [10], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));

    def testClusteringSampleSimple1Manhattan(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.MANHATTAN));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False, metric=distance_metric(type_metric.MANHATTAN));

    def testClusteringSampleSimple1Chebyshev(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.CHEBYSHEV));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False, metric=distance_metric(type_metric.CHEBYSHEV));

    def testClusteringSampleSimple2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1.0, 2.0, [5, 8, 10], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10.0, 20.0, [23], False);

    def testClusteringSampleSimple3(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.0, 2.0, [10, 10, 10, 30], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 10.0, 20.0, [60], False);

    def testOneDimentionalPoints1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1.0, 2.0, [10, 10], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 10.0, 20.0, [20], False);

    def testOneDimentionalPoints2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 2.0, [10, 20], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 10.0, 20.0, [30], False);

    def testThreeDimentionalPoints(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1.0, 2.0, [10, 10], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 10.0, 20.0, [20], False);

    def testTheSamePoints1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 1.5, [5, 5, 5], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 0.001, 0.002, [5, 5, 5], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1000, 2000, [15], False);

    def testTheSamePoints2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 2.0, [10, 20], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 10.0, 20.0, [30], False);



if __name__ == "__main__":
    unittest.main();