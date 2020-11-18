"""!

@brief Examples devoted to KD-tree.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.container.kdtree import kdtree, kdtree_visualizer

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_build_visualize(sample_path):
    print("KD Tree for sample: '" + sample_path + "'")
    sample = read_sample(sample_path)
    tree_instance = kdtree(sample)

    kdtree_visualizer(tree_instance).visualize()


def kdtree_sample_simple01():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

def kdtree_sample_simple02():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

def kdtree_sample_simple03():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

def kdtree_sample_simple04():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

def kdtree_sample_simple05():
    template_build_visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

def kdtree_fcps_two_diamonds():
    template_build_visualize(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)


kdtree_sample_simple01()
kdtree_sample_simple02()
kdtree_sample_simple03()
kdtree_sample_simple04()
kdtree_sample_simple05()
kdtree_fcps_two_diamonds()
