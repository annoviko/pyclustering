"""!

@brief Examples of usage and demonstration of abilities of self-organized feature map.

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

from pyclustering.nnet.som import som;
from pyclustering.nnet.som import type_conn;
from pyclustering.nnet.som import type_init;
from pyclustering.nnet.som import som_parameters;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.samples.definitions import FCPS_SAMPLES;

from pyclustering.utils import read_sample;

import matplotlib.pyplot as plt;
from matplotlib import cm;
from pylab import *;


def template_self_organization(file, rows, cols, time, structure, init_type = None, init_radius = None, init_rate = None, umatrix = False, pmatrix = False, awards = False):
    parameters = som_parameters();
    
    if (init_type is not None):
        parameters.init_type = init_type;
    if (init_radius is not None):
        parameters.init_radius = init_radius;
    if (init_rate is not None):
        parameters.init_learn_rate = init_rate;
    
    sample = read_sample(file);
    network = som(rows, cols, structure, parameters, True);
    network.train(sample, time);
    network.show_network(False, dataset = False);
    
    if (umatrix is True):
        network.show_distance_matrix();
        
    if (pmatrix is True): 
        network.show_density_matrix();
    
    if (awards is True):
        network.show_winner_matrix();


def som_sample1():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, type_conn.grid_four);
    
def som_sample2():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, type_conn.grid_four);
    
def som_sample3():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, type_conn.grid_four);
    
def som_sample4():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, type_conn.grid_four);
    
def som_sample5():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, type_conn.grid_four);
    
def som_lsun():
    template_self_organization(FCPS_SAMPLES.SAMPLE_LSUN, 5, 5, 100, type_conn.grid_four);
    
def som_target():
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 5, 5, 100, type_conn.grid_four);
    
def som_tetra():
    template_self_organization(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, type_conn.grid_four);
    
def som_two_diamonds():
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 5, 5, 100, type_conn.grid_four);
    
def som_elongate():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 5, 5, 100, type_conn.grid_four);
    
def som_wing_nut():
    template_self_organization(FCPS_SAMPLES.SAMPLE_WING_NUT, 5, 5, 100, type_conn.grid_four);
    
def som_chainlink():
    template_self_organization(FCPS_SAMPLES.SAMPLE_CHAINLINK, 5, 5, 100, type_conn.grid_four);
    
def som_atom():
    template_self_organization(FCPS_SAMPLES.SAMPLE_ATOM, 5, 5, 100, type_conn.grid_four);
    
def som_golf_ball():
    template_self_organization(FCPS_SAMPLES.SAMPLE_GOLF_BALL, 5, 5, 100, type_conn.grid_four);
    
def som_hepta():
    template_self_organization(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, type_conn.grid_four);
    
def som_engy_time():
    template_self_organization(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 5, 5, 100, type_conn.grid_four);


def som_winner_matrix():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 10, 10, 150, type_conn.func_neighbor, init_radius = 6.0, init_rate = 0.1, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_LSUN, 10, 10, 200, type_conn.func_neighbor, init_radius = 2.5, init_rate = 0.5, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 10, 10, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.5, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 10, 10, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_WING_NUT, 10, 10, 200, type_conn.func_neighbor, init_radius = 6.0, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_CHAINLINK, 10, 10, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TETRA, 10, 10, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, awards = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 10, 10, 100, type_conn.func_neighbor, init_radius = 6.0, awards = True);

def som_distance_matrix():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 32, 32, 150, type_conn.func_neighbor, init_radius = 6.0, init_rate = 0.1, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_LSUN, 32, 32, 1000, type_conn.func_neighbor, init_radius = 2.5, init_rate = 0.5, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 32, 32, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.5, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 32, 32, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_WING_NUT, 32, 32, 200, type_conn.func_neighbor, init_radius = 6.0, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_CHAINLINK, 32, 32, 1000, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TETRA, 32, 32, 1000, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, umatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 32, 32, 100, type_conn.func_neighbor, init_radius = 6.0, umatrix = True);

def som_density_matrix():
    template_self_organization(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 32, 32, 150, type_conn.func_neighbor, init_radius = 6.0, init_rate = 0.1, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_LSUN, 32, 32, 1000, type_conn.func_neighbor, init_radius = 2.5, init_rate = 0.5, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 32, 32, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.5, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 32, 32, 200, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_WING_NUT, 32, 32, 200, type_conn.func_neighbor, init_radius = 6.0, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_CHAINLINK, 32, 32, 1000, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TETRA, 32, 32, 1000, type_conn.func_neighbor, init_radius = 3.0, init_rate = 0.6, pmatrix = True);
    template_self_organization(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 32, 32, 100, type_conn.func_neighbor, init_radius = 6.0, pmatrix = True);   


def som_target_diffence_intialization():
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 9, 9, 150, type_conn.grid_four, type_init.random);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 9, 9, 150, type_conn.grid_four, type_init.random_centroid);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 9, 9, 150, type_conn.grid_four, type_init.random_surface);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 9, 9, 150, type_conn.grid_four, type_init.uniform_grid);
    
def som_two_diamonds_diffence_intialization():
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 9, 9, 150, type_conn.grid_four, type_init.random);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 9, 9, 150, type_conn.grid_four, type_init.random_centroid);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 9, 9, 150, type_conn.grid_four, type_init.random_surface);
    template_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 9, 9, 150, type_conn.grid_four, type_init.uniform_grid);    


som_sample1();
som_sample2();
som_sample3();
som_sample4();
som_sample5();
som_lsun();
som_target();
som_tetra();
som_two_diamonds();
som_elongate();
som_wing_nut();
som_chainlink();
som_atom();
som_golf_ball();
som_hepta();
som_engy_time();
 
som_winner_matrix();
som_distance_matrix();
som_density_matrix();

som_target_diffence_intialization();
som_two_diamonds_diffence_intialization();