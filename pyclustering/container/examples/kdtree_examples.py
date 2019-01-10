"""!

@brief Examples devoted to KD-tree.

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


from pyclustering.container.kdtree import kdtree, kdtree_text_visualizer;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


def template_build_visualize(sample_path):
    print("KD Tree for sample: '" + sample_path + "'");
    sample = read_sample(sample_path);
    tree_instance = kdtree(sample);
    
    kdtree_text_visualizer(tree_instance).visualize(True);


def kdtree_sample_simple01():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);

def kdtree_sample_simple02():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);

def kdtree_sample_simple03():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);

def kdtree_sample_simple04():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);

def kdtree_sample_simple05():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);


kdtree_sample_simple01();
kdtree_sample_simple02();
kdtree_sample_simple03();
kdtree_sample_simple04();
kdtree_sample_simple05();