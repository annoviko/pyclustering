"""!

@brief Unit-tests for MBSAS algorithm.

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

from pyclustering.cluster.mbsas import mbsas;

from pyclustering.utils import read_sample;
from pyclustering.utils.metric import type_metric, distance_metric;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class MbsasTestTemplate:
    @staticmethod
    def clustering(path, amount, threshold, expected, ccore, **kwargs):
        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN));

        sample = read_sample(path);

        mbsas_instance = mbsas(sample, amount, threshold, ccore=ccore, metric=metric);
        mbsas_instance.process();

        clusters = mbsas_instance.get_clusters();
        representatives = mbsas_instance.get_representatives();

        obtained_length = 0;
        obtained_cluster_length = [];
        for cluster in clusters:
            obtained_length += len(cluster);
            obtained_cluster_length.append(len(cluster));

        assertion.eq(len(sample), obtained_length);
        assertion.eq(len(expected), len(clusters));
        assertion.eq(len(expected), len(representatives));
        assertion.ge(amount, len(clusters));

        dimension = len(sample[0]);
        for rep in representatives:
            assertion.eq(dimension, len(rep));

        expected.sort();
        obtained_cluster_length.sort();

        assertion.eq(expected, obtained_cluster_length);



class MbsasUnitTest(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 1.0, [5, 5], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 1.0, [10], False);

    def testClusteringSampleSimple1Euclidean(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN));
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], False, metric=distance_metric(type_metric.EUCLIDEAN));

    def testClusteringSampleSimple1EuclideanSquare(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 100.0, [10], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));

    def testClusteringSampleSimple1Manhattan(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], False, metric=distance_metric(type_metric.MANHATTAN));
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], False, metric=distance_metric(type_metric.MANHATTAN));

    def testClusteringSampleSimple1Chebyshev(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], False, metric=distance_metric(type_metric.CHEBYSHEV));
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], False, metric=distance_metric(type_metric.CHEBYSHEV));

    def testClusteringSampleSimple2(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1.0, [5, 8, 10], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 10.0, [23], False);

    def testClusteringSampleSimple3(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 2.0, [10, 10, 10, 30], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 10.0, [60], False);

    def testOneDimentionalPoints1(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 1.0, [10, 10], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 10.0, [20], False);

    def testOneDimentionalPoints2(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 1.0, [10, 20], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 10.0, [30], False);

    def testThreeDimentionalPoints(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 1.0, [10, 10], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 10.0, [20], False);

    def testTheSamePoints1(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 3, 1.0, [5, 5, 5], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 30, 1.0, [5, 5, 5], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 3, 10.0, [15], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 1.0, [15], False);

    def testTheSamePoints2(self):
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3, 1.0, [10, 20], False);
        MbsasTestTemplate.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3, 10.0, [30], False);



if __name__ == "__main__":
    unittest.main();