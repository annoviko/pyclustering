"""!

@brief Unit-tests for basic dynamic visualizer.

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