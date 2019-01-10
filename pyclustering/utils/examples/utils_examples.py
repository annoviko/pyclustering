"""!

@brief Examples of usage utils.

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
    along with this program. If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import pyclustering.tests as utils;

from pyclustering.cluster.agglomerative import agglomerative;
from pyclustering.samples.definitions import SIMPLE_SAMPLES;

import matplotlib.pyplot as plt;


def cluster_distances(path_sample, amount_clusters):
    distances = ['euclidian', 'manhattan', 'avr-inter', 'avr-intra', 'variance'];
    
    sample = utils.read_sample(path_sample);
    
    agglomerative_instance = agglomerative(sample, amount_clusters);
    agglomerative_instance.process();
    
    obtained_clusters = agglomerative_instance.get_clusters();
    
    print("Measurements for:", path_sample);
    
    for index_cluster in range(len(obtained_clusters)):
        for index_neighbor in range(index_cluster + 1, len(obtained_clusters), 1):
            cluster1 = obtained_clusters[index_cluster];
            cluster2 = obtained_clusters[index_neighbor];
            
            center_cluster1 = utils.centroid(sample, cluster1);
            center_cluster2 = utils.centroid(sample, cluster2);
            
            for index_distance_type in range(len(distances)):
                distance = None;
                distance_type = distances[index_distance_type];
        
                if (distance_type == 'euclidian'):
                    distance = utils.euclidean_distance(center_cluster1, center_cluster2);
                    
                elif (distance_type == 'manhattan'):
                    distance = utils.manhattan_distance(center_cluster1, center_cluster2);
                    
                elif (distance_type == 'avr-inter'):
                    distance = utils.average_inter_cluster_distance(cluster1, cluster2, sample);
                
                elif (distance_type == 'avr-intra'):
                    distance = utils.average_intra_cluster_distance(cluster1, cluster2, sample);
                
                elif (distance_type == 'variance'):
                    distance = utils.variance_increase_distance(cluster1, cluster2, sample);
            
            print("\tDistance", distance_type, "from", index_cluster, "to", index_neighbor, "is:", distance);
        

def display_two_dimensional_cluster_distances(path_sample, amount_clusters):
    distances = ['euclidian', 'manhattan', 'avr-inter', 'avr-intra', 'variance'];
    
    ajacency = [ [0] * amount_clusters for i in range(amount_clusters) ];
    
    sample = utils.read_sample(path_sample);
    
    agglomerative_instance = agglomerative(sample, amount_clusters);
    agglomerative_instance.process();
    
    obtained_clusters = agglomerative_instance.get_clusters();
    stage = utils.draw_clusters(sample, obtained_clusters, display_result = False);
    
    for index_cluster in range(len(ajacency)):
        for index_neighbor_cluster in range(index_cluster + 1, len(ajacency)):
            if ( (index_cluster == index_neighbor_cluster) or (ajacency[index_cluster][index_neighbor_cluster] is True) ):
                continue;
            
            ajacency[index_cluster][index_neighbor_cluster] = True;
            ajacency[index_neighbor_cluster][index_cluster] = True;
            
            cluster1 = obtained_clusters[index_cluster];
            cluster2 = obtained_clusters[index_neighbor_cluster];
            
            center_cluster1 = utils.centroid(sample, cluster1);
            center_cluster2 = utils.centroid(sample, cluster2);
            
            x_maximum, x_minimum, y_maximum, y_minimum = None, None, None, None;
            x_index_maximum, y_index_maximum = 1, 1;
            
            if (center_cluster2[0] > center_cluster1[0]):
                x_maximum = center_cluster2[0];
                x_minimum = center_cluster1[0];
                x_index_maximum = 1;
            else:
                x_maximum = center_cluster1[0];
                x_minimum = center_cluster2[0];
                x_index_maximum = -1;
            
            if (center_cluster2[1] > center_cluster1[1]):
                y_maximum = center_cluster2[1];
                y_minimum = center_cluster1[1];
                y_index_maximum = 1;
            else:
                y_maximum = center_cluster1[1];
                y_minimum = center_cluster2[1];
                y_index_maximum = -1;
            
            print("Cluster 1:", cluster1, ", center:", center_cluster1);
            print("Cluster 2:", cluster2, ", center:", center_cluster2);
            
            stage.annotate(s = '', xy = (center_cluster1[0], center_cluster1[1]), xytext = (center_cluster2[0], center_cluster2[1]), arrowprops = dict(arrowstyle = '<->'));
            
            for index_distance_type in range(len(distances)):
                distance = None;
                distance_type = distances[index_distance_type];
                
                if (distance_type == 'euclidian'):
                    distance = utils.euclidean_distance(center_cluster1, center_cluster2);
                    
                elif (distance_type == 'manhattan'):
                    distance = utils.manhattan_distance(center_cluster1, center_cluster2);
                    
                elif (distance_type == 'avr-inter'):
                    distance = utils.average_inter_cluster_distance(cluster1, cluster2, sample);
                
                elif (distance_type == 'avr-intra'):
                    distance = utils.average_intra_cluster_distance(cluster1, cluster2, sample);
                
                elif (distance_type == 'variance'):
                    distance = utils.variance_increase_distance(cluster1, cluster2, sample);
                
                print("\tCluster distance -", distance_type, ":", distance);
                
                x_multiplier = index_distance_type + 3;
                if (x_index_maximum < 0):
                    x_multiplier = len(distances) - index_distance_type + 3;
                
                y_multiplier = index_distance_type + 3;
                if (y_index_maximum < 0):
                    y_multiplier = len(distances) - index_distance_type + 3;
                
                x_text = x_multiplier * (x_maximum - x_minimum) / (len(distances) + 6) + x_minimum;
                y_text = y_multiplier * (y_maximum - y_minimum) / (len(distances) + 6) + y_minimum;
                
                #print(x_text, y_text, "\n");
                stage.text(x_text, y_text, distance_type + " {:.3f}".format(distance), fontsize = 9, color='blue');
    
    plt.show();


def display_cluster_distances_simple_sample_01():
    display_two_dimensional_cluster_distances(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2);

def display_cluster_distances_simple_sample_02():
    display_two_dimensional_cluster_distances(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3);

def display_cluster_distances_simple_sample_03():
    display_two_dimensional_cluster_distances(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4);


def print_cluster_distances_simple_sample_07():
    cluster_distances(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2);

def print_cluster_distances_simple_sample_08():
    cluster_distances(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 4);


display_cluster_distances_simple_sample_01();
display_cluster_distances_simple_sample_02();
display_cluster_distances_simple_sample_03();

print_cluster_distances_simple_sample_07();
print_cluster_distances_simple_sample_08();

