"""!

@brief Examples of usage and demonstration of abilities of CLIQUE algorithm in cluster analysis.

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


import os

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.clique import clique, clique_visualizer

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(data_path, intervals, density_threshold, **kwargs):
    print("Sample: '%s'." % os.path.basename(data_path))

    data = read_sample(data_path)

    clique_instance = clique(data, intervals, density_threshold)
    clique_instance.process()

    clusters = clique_instance.get_clusters()
    noise = clique_instance.get_noise()
    cells = clique_instance.get_cells()

    print([len(cluster) for cluster in clusters])

    clique_visualizer.show_grid(cells, data)

    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, data)
    visualizer.append_cluster(noise, data, marker='x')
    visualizer.show()


def cluster_simple_sample():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 15, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 7, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 7, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 7, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 2, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 7, 0)


def cluster_fcps():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 15, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 15, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 15, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 10, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 9, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 10, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 10, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 10, 0)


cluster_simple_sample()
cluster_fcps()
