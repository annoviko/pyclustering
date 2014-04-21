import numpy as np
import random as rnd
import matplotlib.pyplot as plt;
import math


ro = 0.0;
coeff = 10;
coeff_each = 0.1;
alfa = 1;
MAX_VAL = 10**10;
unless_perm = 0;
calc_new_mean = 0;

def getProbablyWeights( probably ):
    weights = np.zeros( len(probably) )
    rand_num = rnd.random()
    prob_sum = 0;

    for i in range( len(probably) ):
        prob_sum += probably[i]

        if( rand_num <= prob_sum ):
            weights[i] = 1
            break
    return weights


def change_custer_for_further(    weights
                                , mean_cluster
                                , data_to_clusters
                                , num_of_samples_with_further_distance ):
    data = data_to_clusters[num_of_samples_with_further_distance,:]

    f_min = 10**10;
    num_cluster_shortest_distance = -1

    for i in range( len(mean_cluster[:,0]) ):
        f = 0

        for j in range( len(mean_cluster[i,:]) ):
            f += ( data[j]-mean_cluster[i,j] ) ** 2;

        if f < f_min:
            f_min = f;
            num_cluster_shortest_distance = i

    weights[num_of_samples_with_further_distance,:] = 0
    weights[num_of_samples_with_further_distance,num_cluster_shortest_distance] = 1

    return weights


def clustering(   data_to_clusters
                , num_iterations
                , count_ants
                , init_pheromone
                , num_samples
                , num_clusters
                , dimention           ):
    global ro, coeff, coeff_each, alfa, MAX_VAL, unless_perm, calc_new_mean

    weights_ants = np.zeros( (num_samples, num_clusters, count_ants) )
    mean_cluster_ants = np.zeros( (num_clusters, dimention, count_ants) )

    f_min = MAX_VAL;
    set_min = np.zeros( (num_samples, num_clusters) )
    #pheromone_min = np.zeros( (num_samples, num_clusters) )
    mean_min = np.zeros( (num_clusters, dimention) )

    f = np.zeros( (count_ants) )
    pheromone = np.ones( (num_samples, num_clusters) ) * float(init_pheromone);

    mean_cluster = np.zeros( (num_clusters, dimention) )
    weights = np.zeros( (num_samples, num_clusters) )

    for iteration in range(num_iterations):
        for ant in range(count_ants):

            weights = weights_ants[:,:,ant];

            for i in range(num_samples):
                probably = pheromone[i,:] / sum( pheromone[i, :] )
                weights[i] = getProbablyWeights( probably );

            for i in range(num_clusters):
                for j in range(dimention):
                    mean_cluster[i,j] = 0

                    for k in range(num_samples):
                        mean_cluster[i,j] = mean_cluster[i,j] + weights[k,i]*data_to_clusters[k,j];

                    if( sum(weights[:,i]) > 0 ):
                        mean_cluster[i,j] = mean_cluster[i,j]  / float( sum(weights[:,i] ) )
            f[ant] = 0
            for i in range(num_clusters):
                for j in range(num_samples):
                    for k in range(dimention):
                        f[ant] += weights[j,i] * (data_to_clusters[j,k] - mean_cluster[i,k])**2

            for i in range(num_clusters):
                num_of_samples_with_further_distance = 0

                for ii in range(num_samples):
                    num_of_samples_with_further_distance = -1
                    num_of_samples_with_further_distance = ii

                    weights_old = weights[num_of_samples_with_further_distance,:]
                    weights = change_custer_for_further(  weights
                                                        , mean_cluster
                                                        , data_to_clusters
                                                        , num_of_samples_with_further_distance )

                    if calc_new_mean:
                        f_new = 0
                        for u in range(num_clusters):
                            for j in range(num_samples):
                                for k in range(dimention):
                                    f_new += weights[j,u] * ( data_to_clusters[j,k] - mean_cluster[u,k])**2

                        if f_new < f[ant]:
                            f[ant] = f_new
                            for jj in range(num_clusters):
                                for j in range(dimention):
                                    mean_cluster[jj,j] = 0

                                    for k in range(num_samples):
                                        mean_cluster[jj,j] += weights[k,jj]*data_to_clusters[k,j]

                                    if sum( weights[:,jj] ) > 0:
                                        mean_cluster[jj,j] /= sum( weights[:,jj] )
                        else:
                            weights[num_of_samples_with_further_distance,:] = weights_old
                            unless_perm = unless_perm + 1;
                    else:
                        f_new = 0;
                        for u in range(num_clusters):
                            for j in range(num_samples):
                                for k in range(dimention):
                                    f_new = f_new + weights[j,u] * ( data_to_clusters[j,k] - mean_cluster[u,k] )**2
                        f[ant] = f_new
                        for jj in range(num_clusters):
                            for j in range(dimention):
                                mean_cluster[jj,j] = 0
                                for k in range(num_samples):
                                    mean_cluster[jj,j] += weights[k,jj]*data_to_clusters[k,j]
                                if sum( weights[:,jj] ) > 0:
                                    mean_cluster[jj,j] /= sum( weights[:,jj] )
            weights_ants[:,:,ant] = weights[:,:]
            mean_cluster_ants[:,:,ant] = mean_cluster

            for i in range(num_samples):
                for j in range(num_clusters):
                    if set_min[i,j] == 1:
                        pheromone[i,j] += coeff_each*(1/f[ant])**alfa

        for i in range(count_ants):
            if f_min > f[i]:
                f_min = f[i]
                set_min = weights_ants[:,:,i]
                mean_min = mean_cluster_ants[:,:,i]

        for i in range(num_samples):
            for j in range(num_clusters):
                pheromone[i,j] = (1-ro) * pheromone[i,j]

                if set_min[i,j] == 1:
                    pheromone[i,j] += coeff * 1/f_min


    return pheromone, set_min, f_min, mean_min

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


[pheromone, weights, f, mean_min ]= clustering( X, 1, 1, 0.1, len(X), 4, 2 );

#print( weights )

fig = plt.figure()
axes = fig.add_subplot(111);

colors = ['b', 'r', 'g', 'y', 'm', 'k', 'c']

for i in range(len(X)):
    for j in range(len(weights)):
        if weights[i][j] == 1:
            idx_color = j
            break
    axes.plot(X[i][0], X[i][1], colors[j] + 'o');

#print( mean_min )
for i in range(len(mean_min)):
    axes.plot(mean_min[i][0], mean_min[i][1], colors[i] + '*', markersize=24);

plt.grid();
plt.show();





