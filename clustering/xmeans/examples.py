from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from clustering.xmeans import xmeans;

from support import draw_clusters, read_sample, timedcall;

def template_clustering(start_centers, path, tolerance = 0.25, ccore = True):
    sample = read_sample(path);
    
    (ticks, clusters) = timedcall(xmeans, sample, start_centers);
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    draw_clusters(sample, clusters);
    

def cluster_sample1():
    start_centers = [[3.7, 5.5], [6.7, 7.5]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    
cluster_sample1();