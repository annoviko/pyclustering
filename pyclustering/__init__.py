"""!

@brief PyClustering module that consists of general modules related to clustering, graph coloring, containers,
        oscillatory networks.

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

@mainpage PyClustering library

@section intro_sec Introduction
PyClustering is an open source data mining library written in Python and C++ that provides a wide range of clustering
algorithms and methods, including bio-inspired oscillatory networks. PyClustering is mostly focused on cluster analysis
to make it more accessible and understandable for users. The library is distributed under GNU Public License and
provides a comprehensive interface that makes it easy to use in every project.

By default, the C++ part of the library is used for processing in order to achieve maximum performance. This is
especially relevant for algorithms that are based on oscillatory networks, whose dynamics are governed by a system of
differential equations. If support for a C++ compiler is not detected, PyClustering falls back to pure Python
implementations of all kernels.

PyClustering consists of five general modules.

Cluster analysis algorithms and methods (module pyclustering.cluster):
- Agglomerative (pyclustering.cluster.agglomerative);
- BANG (pyclustering.cluster.bang);
- BIRCH (pyclustering.cluster.birch);
- BSAS (pyclustering.cluster.bsas);
- CLARANS (pyclustering.cluster.clarans);
- CLIQUE (pyclustering.cluster.clique);
- CURE (pyclustering.cluster.cure);
- DBSCAN (pyclustering.cluster.dbscan);
- Elbow (pyclustering.cluster.elbow);
- EMA (pyclustering.cluster.ema);
- Fuzzy C-Means (pyclustering.cluster.fcm);
- GA (genetic algorithm pyclustering.cluster.ga);
- G-Means (pyclustering.cluster.gmeans);
- HSyncNet (bio-inspired algorithm pyclustering.cluster.hsyncnet);
- K-Means (pyclustering.cluster.kmeans);
- K-Means++ (pyclustering.cluster.center_initializer);
- K-Medians (pyclustering.cluster.kmedians);
- K-Medoids (pyclustering.cluster.kmedoids);
- MBSAS (pyclustering.cluster.mbsas);
- OPTICS (pyclustering.cluster.optics);
- ROCK (pyclustering.cluster.rock);
- Silhouette (pyclustering.cluster.silhouette);
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


Utils (pyclustering.utils) that can be used for analysis, visualization, etc.


@section install_sec Installation
The simplest way to install pyclustering library is to use pip:
@code{.sh}
    pip3 install pyclustering
@endcode

The library can be compiled and manually installed on Linux or MacOS machine wherever you want:
@code{.sh}
    # extract content of the pyclustering library...
    # compile CCORE library (core of the pyclustering library).
    cd pyclustering/ccore
    make ccore_64bit # if platform is 64-bit
    # make ccore_32bit # if platform is 32-bit
    
    # return to parent folder of the pyclustering library
    cd ../
    
    # add current folder to python path
    PYTHONPATH=`pwd`
    export PYTHONPATH=${PYTHONPATH}
@endcode


@section cite_sec Cite the Library

If you are using pyclustering library in a scientific paper, please, cite the library:

Novikov, A., 2019. PyClustering: Data Mining Library. Journal of Open Source Software, 4(36), p.1230. Available at: http://dx.doi.org/10.21105/joss.01230.

BibTeX entry:

@code
    @article{Novikov2019,
        doi         = {10.21105/joss.01230},
        url         = {https://doi.org/10.21105/joss.01230},
        year        = 2019,
        month       = {apr},
        publisher   = {The Open Journal},
        volume      = {4},
        number      = {36},
        pages       = {1230},
        author      = {Andrei Novikov},
        title       = {{PyClustering}: Data Mining Library},
        journal     = {Journal of Open Source Software}
    }
@endcode


@section example_sec Examples

The library provides intuitive and friendly interface. Here is an example how to perform cluster analysis using BIRCH
algorithm:
@code{.py}
    from pyclustering.cluster import cluster_visualizer
    from pyclustering.cluster.birch import birch
    from pyclustering.samples.definitions import FCPS_SAMPLES
    from pyclustering.utils import read_sample

    # Load data for cluster analysis - 'Lsun' sample.
    sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

    # Create BIRCH algorithm to allocate three clusters.
    birch_instance = birch(sample, 3)

    # Run cluster analysis.
    birch_instance.process()

    # Get allocated clusters.
    clusters = birch_instance.get_clusters()

    # Visualize obtained clusters.
    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, sample)
    visualizer.show()
@endcode

Here is an how to perform cluster analysis using well-known K-Means algorithm:
@code{.py}
    from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
    from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
    from pyclustering.samples.definitions import FCPS_SAMPLES
    from pyclustering.utils import read_sample

    # Load list of points for cluster analysis.
    sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

    # Prepare initial centers using K-Means++ method.
    initial_centers = kmeans_plusplus_initializer(sample, 2).initialize()

    # Create instance of K-Means algorithm with prepared centers.
    kmeans_instance = kmeans(sample, initial_centers)

    # Run cluster analysis and obtain results.
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()
    final_centers = kmeans_instance.get_centers()

    # Visualize obtained results
    kmeans_visualizer.show_clusters(sample, clusters, final_centers)
@endcode

An example cluster analysis (that is performed by DBSCAN algorithm) for FCPS samples and visualization of results:
@image html fcps_cluster_analysis.png

An example of Hodgkin-Huxley oscillatory network simulation with 6 oscillators. The first two oscillators
have the same stimulus, as well as the third and fourth oscillators and the last two. Thus three synchronous
ensembles are expected after simulation.
@code{.py}
    from pyclustering.nnet.hhn import hhn_network, hhn_parameters
    from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer

    # Change period of time when high strength value of synaptic connection exists from CN2 to PN.
    params = hhn_parameters()
    params.deltah = 400

    # Create Hodgkin-Huxley oscillatory network with stimulus.
    net = hhn_network(6, [0, 0, 25, 25, 47, 47], params)

    # Simulate network.
    (t, dyn_peripheral, dyn_central) = net.simulate(2400, 600)

    # Visualize network's output (membrane potential of peripheral and central neurons).
    amount_canvases = 6 + 2  # 6 peripheral oscillator + 2 central elements
    visualizer = dynamic_visualizer(amount_canvases, x_title="Time", y_title="V", y_labels=False)
    visualizer.append_dynamics(t, dyn_peripheral, 0, True)
    visualizer.append_dynamics(t, dyn_central, amount_canvases - 2, True)
    visualizer.show()
@endcode

"""