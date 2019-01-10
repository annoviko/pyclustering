"""!

@brief Examples of usage and demonstration of abilities of Silhouette algorithm.

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

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.silhouette import silhouette_ksearch_type, silhouette_ksearch

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.utils import read_sample


def find_optimal_amout_clusters(sample_path, kmin, kmax, algorithm):
    sample = read_sample(sample_path)
    search_instance = silhouette_ksearch(sample, kmin, kmax, algorithm=algorithm).process()

    amount = search_instance.get_amount()
    scores = search_instance.get_scores()

    print("Sample: '%s', Scores: '%s'" % (sample_path, str(scores)))

    initial_centers = kmeans_plusplus_initializer(sample, amount).initialize()
    kmeans_instance = kmeans(sample, initial_centers).process()

    clusters = kmeans_instance.get_clusters()

    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, sample)
    visualizer.show()


def sample_simple01():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple02():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple03():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple04():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple05():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple06():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple07():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple08():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple09():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple10():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple11():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple12():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple13():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_simple14():
    find_optimal_amout_clusters(SIMPLE_SAMPLES.SAMPLE_SIMPLE14, 2, 10, silhouette_ksearch_type.KMEANS)

def sample_hepta():
    find_optimal_amout_clusters(FCPS_SAMPLES.SAMPLE_HEPTA, 2, 10, silhouette_ksearch_type.KMEANS)


sample_simple01()
sample_simple02()
sample_simple03()
sample_simple04()
sample_simple05()
sample_simple06()
sample_simple07()
sample_simple08()
sample_simple09()
sample_simple10()
sample_simple11()
sample_simple12()
sample_simple13()
sample_simple14()
sample_hepta()