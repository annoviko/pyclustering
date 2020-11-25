"""!

@brief PyClustering module that consists of general modules related to clustering, graph coloring, containers,
        oscillatory networks.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause



@mainpage PyClustering library

@section intro_sec Introduction
PyClustering is an open source data mining library written in Python and C++ that provides a wide range of clustering
algorithms and methods, including bio-inspired oscillatory networks. PyClustering is mostly focused on cluster analysis
to make it more accessible and understandable for users. The library is distributed under the 3-Clause BSD License and
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
- K-Medoids (PAM) (pyclustering.cluster.kmedoids);
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


@section section_install Installation
The simplest way to install pyclustering library is to use `pip`:
@code{.sh}
    pip3 install pyclustering
@endcode

The library can be built and installed manually. pyclustering's python code delegates computations to pyclustering C++
code that is represented by C++ pyclustering library: `pyclustering.dll` in case of Windows and `libpyclustering.so` in
case of Linux and MacOS. There are three general ways to build C++ pyclustering:
1. @ref subsection_build_makefile
2. @ref subsection_build_cmake
3. @ref subsection_build_msvc

@subsection subsection_build_makefile Build PyClustering Using Makefile

1. Clone pyclustering library from the official repository:
@code{.sh}
    mkdir pyclustering
    cd pyclustering
    git clone https://github.com/annoviko/pyclustering.git .
@endcode

2. The Makefile is located in `ccore` folder. Navigate to that folder:
@code{.sh}
    cd ccore
@endcode

3. The Makefile uses GCC to build pyclustering library. Make sure that your GCC compiler supports C++14. Build pyclustering
 library for corresponding platform:
@code{.sh}
    make ccore_64bit    # build the library for 64-bit operating system.
    # make ccore_32bit    # build the library for 32-bit operating system.
@endcode

4. Install pyclustering library:
@code{.sh}
    cd ../  # Return back to pyclustering's root folder when setup.py is located.
    python3 setup.py install
@endcode

@subsection subsection_build_cmake Build PyClustering Using CMake

1. Clone pyclustering library from the official repository:
@code{.sh}
    mkdir pyclustering
    cd pyclustering
    git clone https://github.com/annoviko/pyclustering.git .
@endcode

2. Navigate to C++ pyclustering sources and create build folder:
@code{.sh}
    cd ccore
    mkdir build
@endcode

3. Generate makefiles using CMake:
@code{.sh}
    cmake ..
@endcode

4. Build pyclustering library using generated makefile (it automatically detects platform):
@code{.sh}
    make pyclustering
@endcode

5. Install pyclustering library:
@code{.sh}
    cd ../  # Return back to pyclustering's root folder when setup.py is located.
    python3 setup.py install
@endcode

@subsection subsection_build_msvc Build pyclustering using MSVC

1. Clone pyclustering library from the official repository:
@code{.sh}
    mkdir pyclustering
    cd pyclustering
    git clone https://github.com/annoviko/pyclustering.git .
@endcode

2. Navigate to `pyclustering/ccore`.

3. Open MSVC project `ccore.sln`.

4. Choose the following `Release` configuration and corresponding platform (`x64` or `x86`).

5. Build `pyclustering-shared` project.

@image html pyclustering_build_msvc.png

@section section_cite Cite the Library

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

This section contains few examples in order to demonstrate the interface of the library. The documentation contains
examples for every algorithm/method/model/etc. More examples of a functionality can be found on a corresponding page of
the function in this documentation.

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

import pathlib


## The current version of pyclustering library.
__version__ = '0.10.1.2'

## The current root directory of pyclustering library.
__PYCLUSTERING_ROOT_DIRECTORY__ = str(pathlib.Path(__file__).parent)
