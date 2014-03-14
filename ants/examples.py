
from support import read_sample
from ants.clustering import clustering

def templateClustering( file, num_ants, size_lattice, count_iteration ):
    sample = read_sample(file);
    return clustering( num_ants, size_lattice, count_iteration, sample, len(sample) )


def testClusteringSampleSimple1():
    print( templateClustering( '../Samples/SampleSimpleForAntsClustering1.txt', 10, 11, 10000 ) )


testClusteringSampleSimple1()