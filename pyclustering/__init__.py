"""!

@brief PyClustering module that consists of general modules related to clustering, graph coloring, containers, neural networks, oscillatory networks.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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

@mainpage PyClustering library

@section intro_sec Introduction
PyClustering library is a collection of cluster analysis, graph coloring, travelling salesman problem algorithms, oscillatory and neural network models, containers, 
tools for visualization and result analysis, etc. High performance is ensured by CCORE library that is a part of the pyclustering library where almost the same algorithms,
models, tools are implemented. There is ability to use python code implementation only or CCORE (C/C++) implementation using special flag. CCORE library does not
use python.h interface to communicate with python code due to requirement to save ability to use CCORE library or C/C++ code part of CCORE in other projects.

PyClustering consists of six general modules where the algorithms, models, tools are placed:

Cluster analysis algorithms and methods (module pyclustering.cluster):
- Agglomerative (pyclustering.cluster.agglomerative);
- BANG (pyclustering.cluster.bang);
- BIRCH (pyclustering.cluster.birch);
- BSAS (pyclustering.cluster.bsas);
- CLARANS (pyclustering.cluster.clarans);
- CURE (pyclustering.cluster.cure);
- DBSCAN (pyclustering.cluster.dbscan);
- EMA (pyclustering.cluster.ema);
- GA (genetic algorithm pyclustering.cluster.ga);
- HSyncNet (bio-inspired algorithm pyclustering.cluster.hsyncnet);
- K-Means (pyclustering.cluster.kmeans);
- K-Means++ (pyclustering.cluster.center_initializer);
- K-Medians (pyclustering.cluster.kmedians);
- K-Medoids (pyclustering.cluster.kmedoids);
- MBSAS (pyclustering.cluster.mbsas);
- OPTICS (pyclustering.cluster.optics);
- ROCK (pyclustering.cluster.rock);
- SOM-SC (pyclustering.cluster.somsc);
- SyncNet (bio-inspired algorithm pyclustering.cluster.syncnet);
- SyncSOM (bio-inspired algorithm pyclustering.cluster.syncsom);
- TTSAS (pyclustering.cluster.ttsas);
- X-Means (pyclustering.cluster.xmeans);

Oscillatory and neural network models (module pyclustering.nnet):
- Oscillatory network based on Hodgkin-Huxley model (pyclustering.nnet.hhn);
- fSync: Oscillatory Network based on Landau-Stuart equation and Kuramoto model (pyclustering.nnet.fsync);
- Hysteresis Oscillatory Network (pyclustering.nnet.hysteresis);
- LEGION: Local Excitatory Global Inhibitory Oscillatory Network (pyclustering.nnet.legion);
- PCNN: Pulse-Coupled Neural Network (pyclustering.nnet.pcnn);
- SOM: Self-Organized Map (pyclustering.nnet.som);
- Sync: Oscillatory Network based on Kuramoto model (pyclustering.nnet.sync);
- SyncPR: Oscillatory Network based on Kuramoto model for pattern recognition (pyclustering.nnet.syncpr);
- SyncSegm: Oscillatory Network based on Kuramoto model for image segmentation (pyclustering.nnet.syncsegm);

Graph coloring algorithms (module pyclustering.gcolor):
- DSATUR (pyclustering.gcolor.dsatur);
- Hysteresis Oscillatory Network for graph coloring (pyclustering.gcolor.hysteresis);
- Sync: Oscillatory Network based on Kuramoto model for graph coloring (pyclustering.gcolor.sync);

Containers (module pyclustering.container):
- CF-Tree (pyclustering.container.cftree);
- KD-Tree (pyclustering.container.kdtree);


Utils that can be used for analysis, visualization, etc are placed in module pyclustering.utils.


@section install_sec Installation
The simplest way to install pyclustering library is to use pip:
@code{.sh}
    pip install pyclustering
@endcode

The library can be compiled and manually installed on linux machine wherever you want:
@code{.sh}
    # extract content of the pyclustering library...
    # compile CCORE library (core of the pyclustering library).
    cd pyclustering/ccore
    make ccore
    
    # return to parent folder of the pyclustering library
    cd ../
    
    # add current folder to python path
    PYTHONPATH=`pwd`
    export PYTHONPATH=${PYTHONPATH}
@endcode

The library CCORE for 64-bit windows is distributed with pyclustering library so there is no need to re-built it. If you want to re-built 
CCORE library you can open CCORE Microsoft Visual Studio project that is located in ccore/ folder and compile it.


@section example_sec Examples

The library provides intuitive and friendly interface, cluster analysis can be easily performed:
@code{.py}
    # an example of clustering by BIRCH algorithm.
    from pyclustering.cluster.birch import birch;
    
    from pyclustering.utils import read_sample;
    
    # load data from the FCPS set that is provided by the library.
    sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN);
    
    # create BIRCH algorithm for allocation three objects.
    birch_instance = birch(sample, 3);
    
    # start processing - cluster analysis of the input data.
    birch_instance.process();
    
    # allocate clusters.
    clusters = birch_instance.get_clusters();
    
    # visualize obtained clusters.
    visualizer = cluster_visualizer();
    visualizer.append_clusters(clusters, sample);
    visualizer.show();
@endcode

Clustering algorithms can be used for image processing:
@code{.py}
    # an example of image color segmentation.
    from pyclustering.utils import draw_image_mask_segments, read_image;

    from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;

    from pyclustering.cluster.kmeans import kmeans;
    
    # load image from the pyclustering collection.
    data = read_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH);
    
    # set initial centers for K-Means algorithm.
    start_centers = [ [153, 217, 234, 128], [0, 162, 232, 128], [34, 177, 76, 128], [255, 242, 0, 128] ];
    
    # create K-Means algorithm instance.
    kmeans_instance = kmeans(data, start_centers);
    
    # start processing.
    kmeans_instance.process();
    
    # obtain clusters that are considered as segments.
    segments = kmeans_instance.get_clusters();
    
    # show image segmentation results.
    draw_image_mask_segments(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, segments);
@endcode

An example cluster analysis (that is performed by DBSCAN algorithm) for FCPS samples and visualization of results:
@image html fcps_cluster_analysis.png

Simulation of oscillatory network based on Hodgkin-Huxley neuron model where six synchronous ensembles of oscillators are formed. It means that
three features from input data are allocated where each feature is encoded by only one ensemble.
@code
    # an example of simulation of oscillatory network based on Hodgkin-Huxley model
    from pyclustering.utils import draw_dynamics;

    from pyclustering.nnet.hhn import hhn_network, hhn_parameters;

    # set period of 400 time units when high strength value of synaptic connection exists from CN2 to PN.
    params = hhn_parameters();
    params.deltah = 400;
    
    # prepare external stimulus that encode three different features.
    stimulus = [0, 0, 25, 25, 47, 47];
    
    # create oscillatory network that has six oscillators.
    net = hhn_network(len(stimulus), stimulus, params);
    
    # perform simulation during 1200 steps in 600 time units.
    (t, dyn) = net.simulate(1200, 600);
    
    # visualize results of simulation (output dynamic of the network).
    draw_dynamics(t, dyn, x_title = "Time", y_title = "V", separate = True);
@endcode

"""