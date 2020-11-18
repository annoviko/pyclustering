"""!

@brief Unit-tests for basic dynamic visualizer.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');


from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer;


class DynamicVisualizerUnitTest(unittest.TestCase):
    def testVisualizeSignleDynamicNoCrash(self):
        t = [0, 1, 2, 3, 4, 5, 6, 7];
        y = [0, 0, 1, 2, 0, 1, 2, 0];

        visualizer = dynamic_visualizer(1);
        visualizer.append_dynamic(t, y);


    def testVisualizeMultipleDynamicNoCrash(self):
        t = [0, 1, 2, 3, 4, 5, 6, 7];
        y = [ [0, 0], [0, 0], [1, 0], [2, 1], [0, 2], [1, 0], [2, 1], [0, 2] ];

        visualizer = dynamic_visualizer(1);
        visualizer.append_dynamics(t, y);


    def testVisualizeSeparateSequenceNoCrash(self):
        t = [0, 1, 2, 3, 4, 5, 6, 7];
        y = [ [0, 0], [0, 0], [1, 0], [2, 1], [0, 2], [1, 0], [2, 1], [0, 2] ];

        visualizer = dynamic_visualizer(2);
        visualizer.append_dynamics(t, y, canvas=0, separate=True);


    def testVisualizeSeparateListNoCrash(self):
        t = [0, 1, 2, 3, 4, 5, 6, 7];
        y = [ [0, 0], [0, 0], [1, 0], [2, 1], [0, 2], [1, 0], [2, 1], [0, 2] ];

        visualizer = dynamic_visualizer(2);
        visualizer.append_dynamics(t, y, canvas=0, separate=[ [0], [1] ]);


    def testVisualizeSeveralDynamicsOneCanvasNoCrash(self):
        t1 = [0, 1, 2, 3, 4, 5, 6, 7];
        y1 = [0, 0, 1, 2, 0, 1, 2, 0];

        t2 = [0, 1, 2, 3, 4, 5, 6, 7];
        y2 = [ [0, 0], [0, 0], [1, 0], [2, 1], [0, 2], [1, 0], [2, 1], [0, 2] ];

        visualizer = dynamic_visualizer(1);
        visualizer.append_dynamic(t1, y1);
        visualizer.append_dynamics(t2, y2);


    def testVisualizeSeveralDynamicsSeveralCanvasesNoCrash(self):
        t1 = [0, 1, 2, 3, 4, 5, 6, 7];
        y1 = [0, 0, 1, 2, 0, 1, 2, 0];

        t2 = [0, 1, 2, 3, 4, 5, 6, 7];
        y2 = [ [0, 0], [0, 0], [1, 0], [2, 1], [0, 2], [1, 0], [2, 1], [0, 2] ];

        visualizer = dynamic_visualizer(3);
        visualizer.append_dynamic(t1, y1, canvas=0);
        visualizer.append_dynamics(t2, y2, canvas=1, separate=True);


    def testVisualizeDynamicWithColorNoCrash(self):
        t = [0, 1, 2, 3, 4, 5, 6, 7];
        y = [0, 0, 1, 2, 0, 1, 2, 0];

        visualizer = dynamic_visualizer(1);
        visualizer.append_dynamic(t, y, canvas=0, color='red');


    def testVisualizeUnusedCanvasesNoCrash(self):
        t = [0, 1, 2, 3, 4, 5, 6, 7];
        y = [0, 0, 1, 2, 0, 1, 2, 0];

        visualizer = dynamic_visualizer(3);
        visualizer.append_dynamic(t, y, canvas=0, color='red');