
import numpy as np
import random as rnd
import matplotlib.pyplot as plt;
import math
import time

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

    t0 = time.clock();
    [pheromone, weights, f, mean_min ]= ant_clustering.clustering( X, 5, 1, 0.1, len(X), num_clusters, 2 );
    t1 = time.clock();
    print( name_data_set,"=", t1 - t0 )
    draw( X, weights, mean_min )

def example_data( X, num_clusters ):
    sample = X

    X = np.zeros( (len(sample),2) )
    for i in range( len(sample) ):
        for j in range( 2 ):
            X[i,j] = sample[i][j];

    t0 = time.clock();
    [pheromone, weights, f, mean_min ]= ant_clustering.clustering( X, 5, 1, 0.1, len(X), num_clusters, 2 );
    t1 = time.clock();
    print( "X","=", t1 - t0 )
    draw( X, weights, mean_min )



example( "../samples/SampleSimple1.txt", 2 );

example( "../samples/SampleSimple2.txt", 3 );
example( "../samples/SampleSimple3.txt", 4 );
example( "../samples/SampleSimple4.txt", 3 );
example( "../samples/SampleSimple5.txt", 4 );

example( "../Samples/SampleWingNut.txt", 2 );


example( "../samples/SampleTwoDiamonds.txt", 2 );


s = 100;
delta = 25;

X = np.zeros( (s,2) )
for i in range(delta): X[i,0] = rnd.random()+1
for i in range(delta): X[i,1] = rnd.random()+1

for i in range(delta): X[i+delta,0] = rnd.random()-1
for i in range(delta): X[i+delta,1] = rnd.random()+1

for i in range(delta): X[i+delta*2,0] = rnd.random()-1
for i in range(delta): X[i+delta*2,1] = rnd.random()-1

for i in range(delta): X[i+delta*3,0] = rnd.random()+1
for i in range(delta): X[i+delta*3,1] = rnd.random()-1

example_data( X, 4 )

'''
example( "../samples/SampleElongate.txt", 2 );

example( "../samples/SampleEngyTime.txt", 2 );


example( "../samples/SampleTarget.txt", 6 );


example( "../samples/SampleLsun.txt", 3 );

'''
