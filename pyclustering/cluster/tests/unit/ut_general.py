"""!

@brief Unit-tests for other cluster functionality

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy
import random

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.utils import read_sample

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.dbscan import dbscan
from pyclustering.cluster.cure import cure


class Test(unittest.TestCase):
    def testVisualize1DClustersOneCanvas(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE8)
        clusters = dbscan(sample, 1.0, 3, False).process().get_clusters()
          
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize1DClustersOneCanvasNumpy(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, return_type='numpy')
        clusters = dbscan(sample, 1.0, 3, False).process().get_clusters()

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize1DClustersOneCanvasSampleOnly(self):
        clusters = [[[0.1], [0.2], [0.5]], [[0.1], [0.2], [0.5]]]

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize1DClustersOneCanvasSampleOnlyNumpy(self):
        clusters = numpy.array([[[0.1], [0.2], [0.5]], [[0.1], [0.2], [0.5]]])

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize1DClustersTwoCanvases(self):
        sample_simple7 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE7)
        sample_simple8 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE8)
     
        # Two canvas visualization
        visualizer = cluster_visualizer(2)
        visualizer.append_clusters([sample_simple7], None, 0, markersize=30)
        visualizer.append_clusters([sample_simple8], None, 1, markersize=30)
        figure = visualizer.show()
        visualizer.close(figure)
 
    def testVisualize3DClustersOneCanvas(self):
        sample = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA)
          
        dbscan_instance = dbscan(sample, 0.5, 3, False)
        dbscan_instance.process()
        clusters = dbscan_instance.get_clusters()
          
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, markersize=30)
        figure = visualizer.show()
        visualizer.close(figure)
 
    def testVisualize3DClustersTwoCanvases(self):
        sample_tetra = read_sample(FCPS_SAMPLES.SAMPLE_TETRA)
        sample_hepta = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA)
              
        # Two canvas visualization
        visualizer = cluster_visualizer(2)
        visualizer.append_clusters([sample_tetra], None, 0, markersize=30)
        visualizer.append_clusters([sample_hepta], None, 1, markersize=30)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize3DClustersTwoCanvasesNumpy(self):
        sample_tetra = read_sample(FCPS_SAMPLES.SAMPLE_TETRA, return_type='numpy')
        sample_hepta = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA, return_type='numpy')

        # Two canvas visualization
        visualizer = cluster_visualizer(2)
        visualizer.append_clusters([sample_tetra], None, 0, markersize=30)
        visualizer.append_clusters([sample_hepta], None, 1, markersize=30)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize2DClustersOneCanvas(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
 
        dbscan_instance = dbscan(sample, 0.7, 3, False)
        dbscan_instance.process()
        clusters = dbscan_instance.get_clusters()
          
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize2DClustersOneCanvasNumpy(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, return_type='numpy')
        clusters = dbscan(sample, 0.7, 3, False).process().get_clusters()

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize2DClustersThreeCanvases(self):
        sample_simple1 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        sample_simple2 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        sample_simple3 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
              
        clusters_sample1 = dbscan(sample_simple1, 0.4, 2, False).process().get_clusters()
        clusters_sample2 = dbscan(sample_simple2, 1, 2, False).process().get_clusters()
        clusters_sample3 = dbscan(sample_simple3, 0.7, 3, False).process().get_clusters()
              
        visualizer = cluster_visualizer(3)
        visualizer.append_clusters(clusters_sample1, sample_simple1, 0, markersize=5)
        visualizer.append_clusters(clusters_sample2, sample_simple2, 1, markersize=5)
        visualizer.append_clusters(clusters_sample3, sample_simple3, 2, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize2DClustersThreeCanvasesNumpy(self):
        sample_simple1 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, return_type='numpy')
        sample_simple2 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, return_type='numpy')
        sample_simple3 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, return_type='numpy')

        clusters_sample1 = dbscan(sample_simple1, 0.4, 2, False).process().get_clusters()
        clusters_sample2 = dbscan(sample_simple2, 1, 2, False).process().get_clusters()
        clusters_sample3 = dbscan(sample_simple3, 0.7, 3, False).process().get_clusters()

        visualizer = cluster_visualizer(3)
        visualizer.append_clusters(clusters_sample1, sample_simple1, 0, markersize=5)
        visualizer.append_clusters(clusters_sample2, sample_simple2, 1, markersize=5)
        visualizer.append_clusters(clusters_sample3, sample_simple3, 2, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize2DAnd3DClusters(self):
        sample_2d = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        sample_3d = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA)
          
        visualizer = cluster_visualizer(2, 2)
        visualizer.append_clusters([sample_2d], None, 0, markersize=5)
        visualizer.append_clusters([sample_3d], None, 1, markersize=30)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualize2DAnd3DClustersNumpy(self):
        sample_2d = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, return_type='numpy')
        sample_3d = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA, return_type='numpy')

        visualizer = cluster_visualizer(2, 2)
        visualizer.append_clusters([sample_2d], None, 0, markersize=5)
        visualizer.append_clusters([sample_3d], None, 1, markersize=30)
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualizeRectangeRepresentation2x2(self):
        sample_simple1 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        sample_simple2 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        sample_simple3 = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
           
        visualizer = cluster_visualizer(3, 2)
        visualizer.append_clusters([sample_simple1], None, 0, markersize=5)
        visualizer.append_clusters([sample_simple2], None, 1, markersize=5)
        visualizer.append_clusters([sample_simple3], None, 2, markersize=5)
        figure = visualizer.show()
        visualizer.close(figure)
     
    def testVisualizeRectangeRepresentation3x5(self):
        visualizer = cluster_visualizer(15, 5)
         
        for i in range(15):
            sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
            visualizer.append_clusters([sample], None, i, markersize=5)
         
        figure = visualizer.show()
        visualizer.close(figure)
     
    def testVisualizeByDataOnly(self):
        visualizer = cluster_visualizer()
         
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        visualizer.append_clusters([sample])
         
        figure = visualizer.show()
        visualizer.close(figure)
     
    def testVisualizeHugeAmountClusters(self):
        visualizer = cluster_visualizer()
         
        data_clusters = [[[random.random()]] for _ in range(0, 100)]
        visualizer.append_clusters(data_clusters)

        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualizeOnExistedFigure(self):
        figure = plt.figure()
         
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
         
        visualizer = cluster_visualizer()
        visualizer.append_clusters([sample])
        visualizer.show(figure)
        visualizer.close(figure)

    def testVisualizeOnExistedFigureNumpy(self):
        figure = plt.figure()

        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, return_type='numpy')

        visualizer = cluster_visualizer()
        visualizer.append_clusters(numpy.array([sample]))
        visualizer.show(figure)
        visualizer.close(figure)

    def testVisualizeOnExistedFigureWithContent(self):
        figure = plt.figure()
        axis = figure.add_subplot(121)
        axis.plot(range(0, 10, 1), range(0, 10, 1), marker='o', color='blue', ls='')
         
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
         
        visualizer = cluster_visualizer(size_row=2)
        visualizer.append_clusters([sample])
        visualizer.show(figure)
        visualizer.close(figure)

    def testVisualizeOnExistedFigureWithContentNumpy(self):
        figure = plt.figure()
        axis = figure.add_subplot(121)
        axis.plot(range(0, 10, 1), range(0, 10, 1), marker='o', color='blue', ls='')

        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, return_type='numpy')

        visualizer = cluster_visualizer(size_row=2)
        visualizer.append_clusters(numpy.array([sample]))
        visualizer.show(figure)
        visualizer.close(figure)

    def testVisualizeOnExistedFigureWithContentByDefault(self):
        figure = plt.figure()
        axis = figure.add_subplot(211)
        axis.plot(range(0, 10, 1), range(0, 10, 1), marker='o', color='blue', ls='')
        
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        
        visualizer = cluster_visualizer()
        visualizer.append_clusters([sample])
        visualizer.show(figure)
        visualizer.close(figure)
    
    def testVisualizeClusterWithAttributes(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        cure_instance = cure(sample, 2, 5, 0.5, False)
        cure_instance.process()
        
        clusters = cure_instance.get_clusters()
        representors = cure_instance.get_representors()
        means = cure_instance.get_means()
        
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        
        for cluster_index in range(len(clusters)):
            visualizer.append_cluster_attribute(0, cluster_index, representors[cluster_index], '*', 10)
            visualizer.append_cluster_attribute(0, cluster_index, [means[cluster_index]], 'o')
        
        figure = visualizer.show()
        visualizer.close(figure)

    def testVisualizeClusterWithAttributesNumpy(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, return_type='numpy')
        cure_instance = cure(sample, 2, 5, 0.5, False)
        cure_instance.process()

        clusters = cure_instance.get_clusters()
        representors = cure_instance.get_representors()
        means = cure_instance.get_means()

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)

        for cluster_index in range(len(clusters)):
            visualizer.append_cluster_attribute(0, cluster_index, numpy.array(representors[cluster_index]), '*', 10)
            visualizer.append_cluster_attribute(0, cluster_index, numpy.array([means[cluster_index]]), 'o')

        figure = visualizer.show()
        visualizer.close(figure)
