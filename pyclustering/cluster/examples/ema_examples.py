"""!

@brief Examples of usage and demonstration of abilities of expectation maximization algorithm.

@authors Andrey Novikov (pyclustering@yandex.ru)
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


from pyclustering.cluster.ema import ema, ema_initializer, ema_observer, ema_visualizer, ema_init_type;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES, FAMOUS_SAMPLES;


def template_clustering(sample_file_path, amount_clusters, initializer, show_animation = False):
    sample = read_sample(sample_file_path);
    
    observer = None;
    if (show_animation is True):
        observer = ema_observer();

    initial_means, initial_covariance = ema_initializer(sample, amount_clusters).initialize(initializer);
    ema_instance = ema(sample, amount_clusters, initial_means, initial_covariance, observer=observer);
    ema_instance.process();
    
    clusters = ema_instance.get_clusters();
    covariances = ema_instance.get_covariances();
    means = ema_instance.get_centers();

    cluster_length = [ len(cluster) for cluster in clusters ];

    print("Data '" + sample_file_path + "'");
    print("Clusters: " + str(len(clusters)) + ", Length:" + str(cluster_length));

    if (observer is True):
        ema_visualizer.show_clusters(observer.get_evolution_clusters()[0], sample, observer.get_evolution_covariances()[0], observer.get_evolution_means()[0]);
    
    ema_visualizer.show_clusters(clusters, sample, covariances, means);
    
    if (show_animation is True):
        ema_visualizer.animate_cluster_allocation(sample, observer);
        #ema_visualizer.animate_cluster_allocation(sample, observer, movie_fps=2, save_movie="ema_target.mp4");


def cluster_sample01_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample01_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, ema_init_type.KMEANS_INITIALIZATION);

def cluster_sample02_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample02_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, ema_init_type.KMEANS_INITIALIZATION);

def cluster_sample03_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample03_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, ema_init_type.KMEANS_INITIALIZATION);

def cluster_sample04_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample04_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, ema_init_type.KMEANS_INITIALIZATION);

def cluster_sample05_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample05_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, ema_init_type.KMEANS_INITIALIZATION);

def cluster_sample08_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 4, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample08_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 4, ema_init_type.KMEANS_INITIALIZATION);

def cluster_sample11_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, ema_init_type.RANDOM_INITIALIZATION);

def cluster_sample11_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, ema_init_type.KMEANS_INITIALIZATION);

def cluster_elongate_init_random():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2, ema_init_type.RANDOM_INITIALIZATION);

def cluster_elongate_init_kmeans():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2, ema_init_type.KMEANS_INITIALIZATION);

def cluster_lsun_init_random():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3, ema_init_type.RANDOM_INITIALIZATION);

def cluster_lsun_init_kmeans():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3, ema_init_type.KMEANS_INITIALIZATION);

def cluster_target_init_random():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 6, ema_init_type.RANDOM_INITIALIZATION);

def cluster_target_init_kmeans():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 6, ema_init_type.KMEANS_INITIALIZATION);

def cluster_two_diamonds_init_random():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2, ema_init_type.RANDOM_INITIALIZATION);

def cluster_two_diamonds_init_kmeans():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2, ema_init_type.KMEANS_INITIALIZATION);

def cluster_wing_nut_init_random():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 2, ema_init_type.RANDOM_INITIALIZATION);

def cluster_wing_nut_init_kmeans():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 2, ema_init_type.KMEANS_INITIALIZATION);

def cluster_engy_time_init_kmeans():
    template_clustering(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 2, ema_init_type.KMEANS_INITIALIZATION, False);

def cluster_engy_time_init_random():
    template_clustering(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 2, ema_init_type.RANDOM_INITIALIZATION, False);


def cluster_old_faithful_init_kmeans():
    template_clustering(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL, 2, ema_init_type.KMEANS_INITIALIZATION, True);

def cluster_old_faithful_init_random():
    template_clustering(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL, 2, ema_init_type.RANDOM_INITIALIZATION, True);


def cluster_lsun_more_gaussians():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 6, ema_init_type.KMEANS_INITIALIZATION);

def cluster_target_more_gaussians():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 12, ema_init_type.KMEANS_INITIALIZATION);



cluster_sample01_init_random();
cluster_sample01_init_kmeans();
cluster_sample02_init_random();
cluster_sample02_init_kmeans();
cluster_sample03_init_random();
cluster_sample03_init_kmeans();
cluster_sample04_init_random();
cluster_sample04_init_kmeans();
cluster_sample05_init_random();
cluster_sample05_init_kmeans();
cluster_sample08_init_random();
cluster_sample08_init_kmeans();
cluster_sample11_init_random();
cluster_sample11_init_kmeans();
cluster_elongate_init_random();
cluster_elongate_init_kmeans();

cluster_lsun_init_random();
cluster_lsun_init_kmeans();
cluster_target_init_random();
cluster_target_init_kmeans();
cluster_two_diamonds_init_random();
cluster_two_diamonds_init_kmeans();
cluster_wing_nut_init_random();
cluster_wing_nut_init_kmeans();

cluster_old_faithful_init_kmeans();
cluster_old_faithful_init_random();

cluster_engy_time_init_kmeans();
cluster_engy_time_init_random();

cluster_lsun_more_gaussians();
cluster_target_more_gaussians();