"""!

@brief Examples of usage and demonstration of abilities of oscillatory network
       based on Hodgkin-Huxley model of neuron.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from pyclustering.nnet.cnn import cnn_network, cnn_visualizer;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.utils import read_sample;


def template_dynamic_hhn(num_osc, steps, stimulus):
    network_instance = cnn_network(num_osc);
    
    output_dynamic = network_instance.simulate(steps, stimulus);
    
    cnn_visualizer.show_output_dynamic(output_dynamic);
    cnn_visualizer.show_observation_matrix(output_dynamic);


def chaotic_clustering_sample_simple_01():
    sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    template_dynamic_hhn(len(sample), 100, sample);


chaotic_clustering_sample_simple_01();