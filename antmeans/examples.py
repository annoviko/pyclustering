
import numpy as np
import random as rnd
import matplotlib.pyplot as plt;
import math

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;
from support import read_sample;

import antmeans as ant_clustering


def draw( X, weights, mean_min ):
    fig = plt.figure()
    axes = fig.add_subplot(111);

    colors = ['b', 'r', 'g', 'y', 'm', 'k', 'c']

    for i in range(len(X)):
        for j in range(len(weights)):
            if weights[i][j] == 1:
                break
        axes.plot(X[i][0], X[i][1], colors[j] + 'o');

    #print( mean_min )
    for i in range(len(mean_min)):
        axes.plot(mean_min[i][0], mean_min[i][1], colors[i] + '*', markersize=24);

    plt.grid();
    plt.show();


def example( name_data_set, num_clusters ):
    sample = read_sample( name_data_set );

    X = np.zeros( (len(sample),2) )
    for i in range( len(sample) ):
        for j in range( 2 ):
            X[i,j] = sample[i][j];

    [pheromone, weights, f, mean_min ]= ant_clustering.clustering( X, 1, 1, 0.1, len(X), num_clusters, 2 );

    draw( X, weights, mean_min )


#example( SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2 );
#example( SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2 );

"""
example( "../samples/SampleSimple1.txt", 2 );
example( "../samples/SampleSimple2.txt", 3 );
example( "../samples/SampleSimple3.txt", 4 );
example( "../samples/SampleSimple4.txt", 3 );
example( "../samples/SampleSimple5.txt", 4 );
"""


example( "../samples/SampleTwoDiamonds.txt", 2 );
#example( "../samples/SampleSimple2.txt", 3 );








