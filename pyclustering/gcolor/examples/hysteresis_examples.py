"""!

@brief Examples of usage and demonstration of abilities of algorithm (based on Hysteresis Oscillatory Network) in graph coloring.

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

from pyclustering.gcolor.hysteresis import hysteresisgcolor;

from pyclustering.utils.graph import read_graph, draw_graph;
from pyclustering.utils import draw_dynamics;

from pyclustering.samples.definitions import GRAPH_SIMPLE_SAMPLES;

def template_graph_coloring(filename, alpha, eps, steps, time, title = None, tolerance = 0.1, threshold_steps = 10):
    if (title is None): title = filename;
    
    graph = read_graph(filename);
    network = hysteresisgcolor(graph.data, alpha, eps);
    
    output_dynamic = network.simulate(steps, time);
    draw_dynamics(output_dynamic.time, output_dynamic.output, x_title = "Time", y_title = "State");
    
    clusters = output_dynamic.allocate_clusters(tolerance, threshold_steps);
    for index in range(0, len(clusters)):
        print("Color #", index, ": ", clusters[index]);
    
    coloring_map = output_dynamic.allocate_map_coloring(tolerance, threshold_steps);
    draw_graph(graph, coloring_map);


def graph_simple1():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1, 1.2, 1.8, 2000, 20);
    
def graph_one_line():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE, 1.2, 1.8, 2000, 20);
    
def graph_one_crossroad():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD, 1.2, 1.8, 2000, 20);
    
def graph_two_crossroads():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS, 1.2, 1.8, 2000, 20);
    
def graph_full_interconnected1():
    "Bad result - two vertices colored by the same color"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1, 1.2, 1.8, 2000, 20, tolerance = 0.05);
    
def graph_full_interconnected2():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2, 1.2, 1.8, 2000, 20, tolerance = 0.05);

def graph_one_circle1():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1, 1.1, 1.1, 2000, 20);

def graph_one_circle2():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2, 1.1, 1.1, 2000, 20);

def graph_one_circle3():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3, 1.1, 1.1, 2000, 20);

def graph_five_pointed_frame_star():
    "Good result - not optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR, 1.1, 1.4, 3000, 30);



graph_simple1();
graph_one_line();
graph_one_crossroad();
graph_two_crossroads();
graph_full_interconnected1();
graph_full_interconnected2();
graph_one_circle1();
graph_one_circle2();
graph_one_circle3();
graph_five_pointed_frame_star();