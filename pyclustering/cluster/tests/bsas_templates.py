"""!

@brief Test templates for BSAS algorithm.

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


# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.tests.assertion import assertion;

from pyclustering.cluster.bsas import bsas, bsas_visualizer;

from pyclustering.utils import read_sample;

from pyclustering.utils.metric import type_metric, distance_metric;


class bsas_test_template:
    @staticmethod
    def clustering(path, amount, threshold, expected, ccore, **kwargs):
        metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN));

        sample = read_sample(path);

        bsas_instance = bsas(sample, amount, threshold, ccore=ccore, metric=metric);
        bsas_instance.process();

        clusters = bsas_instance.get_clusters();
        representatives = bsas_instance.get_representatives();

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


    @staticmethod
    def visualizing(path, amount, threshold, ccore):
        sample = read_sample(path);
        bsas_instance = bsas(sample, amount, threshold, ccore=ccore);
        bsas_instance.process();

        bsas_visualizer.show_clusters(sample, bsas_instance.get_clusters(), bsas_instance.get_representatives());