"""!

@brief Examples of usage and demonstration of abilities of self-organized feature map.

@authors Andrei Novikov (spb.andr@yandex.ru)
@date 2014-2015
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

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.samples.definitions import FCPS_SAMPLES;

from pyclustering.support import read_sample;

import matplotlib.pyplot as plt;
from matplotlib import cm;
from pylab import *;

def template_self_organization(file, rows, cols, time, structure, init_type = type_init.uniform_grid):
    sample = read_sample(file);
    network = som(rows, cols, sample, time, structure, init_type, True);
    network.train();        
    network.show_network(False, dataset = False);
    

def template_matrix_self_organization(file, rows, cols, time, structure, init_type = type_init.uniform_grid):
    sample = read_sample(file);
    network = som(rows, cols, sample, time, structure, init_type, True);
    network.train();        
    network.show_network(False, dataset = False);
    network.show_distance_matrix();
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


def som_distance_matrix():
    template_matrix_self_organization(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 12, 12, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_LSUN, 10, 10, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 16, 16, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_TARGET, 16, 16, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_WING_NUT, 30, 30, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_CHAINLINK, 12, 12, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_TETRA, 12, 12, 100, type_conn.grid_eight);
    template_matrix_self_organization(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 25, 25, 100, type_conn.grid_eight);


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

som_distance_matrix();

som_target_diffence_intialization();
som_two_diamonds_diffence_intialization();