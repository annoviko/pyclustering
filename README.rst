|Build Status Linux MacOS| |Build Status Win| |Coverage Status| |Documentation| |PyPi| |Download Counter| |JOSS|

PyClustering
============

**pyclustering** is a Python, C++ data mining library (clustering
algorithm, oscillatory networks, neural networks). The library provides
Python and C++ implementations (via CCORE library) of each algorithm or
model. CCORE library is a part of pyclustering and supported only for
Linux, Windows and MacOS operating systems.

**Version**: 0.9.3.1

**License**: GNU General Public License

**E-Mail**: pyclustering@yandex.ru

**Documentation**: https://pyclustering.github.io/docs/0.9.3/html/index.html

**Homepage**: https://pyclustering.github.io/

**PyClustering Wiki**: https://github.com/annoviko/pyclustering/wiki



Dependencies
============

**Required packages**: scipy, matplotlib, numpy, Pillow

**Python version**: >=3.5 (32-bit, 64-bit)

**C++ version**: >= 14 (32-bit, 64-bit)



Performance
===========

Each algorithm is implemented using Python and C/C++ language, if your platform is not supported then the Python
implementation is used, otherwise C/C++. The implementation can be chosen by **ccore** flag (by default it is always
'True' and it means that the C/C++ implementation is used), for example:

.. code:: python

    # As by default - C/C++ is used
    xmeans_instance_1 = xmeans(data_points, start_centers, 20, ccore=True);

    # The same - C/C++ is used by default
    xmeans_instance_2 = xmeans(data_points, start_centers, 20);

    # Switch off core - Python is used
    xmeans_instance_3 = xmeans(data_points, start_centers, 20, ccore=False);

**ccore** option runs ccore shared library (core of the pyclustering library). The core is maintained for Linux, Windows and MacOS.



Installation
============

Installation using pip3 tool:

.. code:: bash

    $ pip3 install pyclustering

Manual installation using GCC:

.. code:: bash

    # get sources of the pyclustering library, for example, from repository
    $ mkdir pyclustering
    $ cd pyclustering/
    $ git clone https://github.com/annoviko/pyclustering.git .

    # compile CCORE library (core of the pyclustering library)
    # you can specify platform (32-bit: 'ccore_32bit', 64-bit: 'ccore_64bit')
    $ cd ccore/
    $ make ccore_64bit    # compile CCORE for 64-bit
    # make ccore_32bit    # compile CCORE for 32-bit

    # return to parent folder of the pyclustering library
    cd ../

    # add current folder to python path
    PYTHONPATH=`pwd`
    export PYTHONPATH=${PYTHONPATH}

Manual installation using Visual Studio:

1. Clone repository from: https://github.com/annoviko/pyclustering.git
2. Open folder pyclustering/ccore
3. Open Visual Studio project ccore.sln
4. Select solution platform: 'x86' or 'x64'
5. Build 'ccore' project.
6. Add pyclustering folder to python path.



Proposals, Questions, Bugs
==========================

In case of any questions, proposals or bugs related to the pyclustering please contact to pyclustering@yandex.ru or create an issue here.



PyClustering Status
===================

+----------------------+------------------------------+------------------------------------+--------------------------------+
| Branch               | master                       | 0.9.dev                            | 0.9.3.rel                      |
+======================+==============================+====================================+================================+
| Build (Linux, MacOS) | |Build Status Linux MacOS|   | |Build Status Linux MacOS 0.9.dev| | |Build Status Linux 0.9.3.rel| |
+----------------------+------------------------------+------------------------------------+--------------------------------+
| Build (Win)          | |Build Status Win|           | |Build Status Win 0.9.dev|         | |Build Status Win 0.9.3.rel|   |
+----------------------+------------------------------+------------------------------------+--------------------------------+
| Code Coverage        | |Coverage Status|            | |Coverage Status 0.9.dev|          | |Coverage Status 0.9.3.rel|    |
+----------------------+------------------------------+------------------------------------+--------------------------------+



Cite the Library
================

If you are using pyclustering library in a scientific paper, please, cite the library:

Novikov, A., 2019. PyClustering: Data Mining Library. Journal of Open Source Software, 4(36), p.1230. Available at: http://dx.doi.org/10.21105/joss.01230.

BibTeX entry:

.. code::

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



Brief Overview of the Library Content
=====================================

**Clustering algorithms and methods (module pyclustering.cluster):**

+------------------------+---------+-----+
| Algorithm              | Python  | C++ |
+========================+=========+=====+
| Agglomerative          | ✓       | ✓   |
+------------------------+---------+-----+
| BANG                   | ✓       |     |
+------------------------+---------+-----+
| BIRCH                  | ✓       |     |
+------------------------+---------+-----+
| BSAS                   | ✓       | ✓   |
+------------------------+---------+-----+
| CLARANS                | ✓       |     |
+------------------------+---------+-----+
| CLIQUE                 | ✓       | ✓   |
+------------------------+---------+-----+
| CURE                   | ✓       | ✓   |
+------------------------+---------+-----+
| DBSCAN                 | ✓       | ✓   |
+------------------------+---------+-----+
| Elbow                  | ✓       | ✓   |
+------------------------+---------+-----+
| EMA                    | ✓       |     |
+------------------------+---------+-----+
| Fuzzy C-Means          | ✓       | ✓   |
+------------------------+---------+-----+
| GA (Genetic Algorithm) | ✓       | ✓   |
+------------------------+---------+-----+
| G-Means                | ✓       | ✓   |
+------------------------+---------+-----+
| HSyncNet               | ✓       | ✓   |
+------------------------+---------+-----+
| K-Means                | ✓       | ✓   |
+------------------------+---------+-----+
| K-Means++              | ✓       | ✓   |
+------------------------+---------+-----+
| K-Medians              | ✓       | ✓   |
+------------------------+---------+-----+
| K-Medoids              | ✓       | ✓   |
+------------------------+---------+-----+
| MBSAS                  | ✓       | ✓   |
+------------------------+---------+-----+
| OPTICS                 | ✓       | ✓   |
+------------------------+---------+-----+
| ROCK                   | ✓       | ✓   |
+------------------------+---------+-----+
| Silhouette             | ✓       | ✓   |
+------------------------+---------+-----+
| SOM-SC                 | ✓       | ✓   |
+------------------------+---------+-----+
| SyncNet                | ✓       | ✓   |
+------------------------+---------+-----+
| Sync-SOM               | ✓       |     |
+------------------------+---------+-----+
| TTSAS                  | ✓       | ✓   |
+------------------------+---------+-----+
| X-Means                | ✓       | ✓   |
+------------------------+---------+-----+


**Oscillatory networks and neural networks (module pyclustering.nnet):**

+--------------------------------------------------------------------------------+---------+-----+
| Model                                                                          | Python  | C++ |
+================================================================================+=========+=====+
| CNN (Chaotic Neural Network)                                                   | ✓       |     |
+--------------------------------------------------------------------------------+---------+-----+
| fSync (Oscillatory network based on Landau-Stuart equation and Kuramoto model) | ✓       |     |
+--------------------------------------------------------------------------------+---------+-----+
| HHN (Oscillatory network based on Hodgkin-Huxley model)                        | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+
| Hysteresis Oscillatory Network                                                 | ✓       |     |
+--------------------------------------------------------------------------------+---------+-----+
| LEGION (Local Excitatory Global Inhibitory Oscillatory Network)                | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+
| PCNN (Pulse-Coupled Neural Network)                                            | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+
| SOM (Self-Organized Map)                                                       | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+
| Sync (Oscillatory network based on Kuramoto model)                             | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+
| SyncPR (Oscillatory network for pattern recognition)                           | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+
| SyncSegm (Oscillatory network for image segmentation)                          | ✓       | ✓   |
+--------------------------------------------------------------------------------+---------+-----+


**Graph Coloring Algorithms (module pyclustering.gcolor):**

+------------------------+---------+-----+
| Algorithm              | Python  | C++ |
+========================+=========+=====+
| DSatur                 | ✓       |     |
+------------------------+---------+-----+
| Hysteresis             | ✓       |     |
+------------------------+---------+-----+
| GColorSync             | ✓       |     |
+------------------------+---------+-----+


**Containers (module pyclustering.container):**

+------------------------+---------+-----+
| Algorithm              | Python  | C++ |
+========================+=========+=====+
| KD Tree                | ✓       | ✓   |
+------------------------+---------+-----+
| CF Tree                | ✓       |     |
+------------------------+---------+-----+



Examples in the Library
=======================

The library contains examples for each algorithm and oscillatory network model:

**Clustering examples:** ``pyclustering/cluster/examples``

**Graph coloring examples:** ``pyclustering/gcolor/examples``

**Oscillatory network examples:** ``pyclustering/nnet/examples``

.. image:: https://github.com/annoviko/pyclustering/blob/master/docs/img/example_cluster_place.png
   :alt: Where are examples?



Code Examples
=============

**Data clustering by CURE algorithm**

.. code:: python

    from pyclustering.cluster import cluster_visualizer;
    from pyclustering.cluster.cure import cure;
    from pyclustering.utils import read_sample;
    from pyclustering.samples.definitions import FCPS_SAMPLES;

    # Input data in following format [ [0.1, 0.5], [0.3, 0.1], ... ].
    input_data = read_sample(FCPS_SAMPLES.SAMPLE_LSUN);

    # Allocate three clusters.
    cure_instance = cure(input_data, 3);
    cure_instance.process();
    clusters = cure_instance.get_clusters();

    # Visualize allocated clusters.
    visualizer = cluster_visualizer();
    visualizer.append_clusters(clusters, input_data);
    visualizer.show();

**Data clustering by K-Means algorithm**

.. code:: python

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

**Data clustering by OPTICS algorithm**

.. code:: python

    from pyclustering.cluster import cluster_visualizer
    from pyclustering.cluster.optics import optics, ordering_analyser, ordering_visualizer
    from pyclustering.samples.definitions import FCPS_SAMPLES
    from pyclustering.utils import read_sample

    # Read sample for clustering from some file
    sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

    # Run cluster analysis where connectivity radius is bigger than real
    radius = 2.0
    neighbors = 3
    amount_of_clusters = 3
    optics_instance = optics(sample, radius, neighbors, amount_of_clusters)

    # Performs cluster analysis
    optics_instance.process()

    # Obtain results of clustering
    clusters = optics_instance.get_clusters()
    noise = optics_instance.get_noise()
    ordering = optics_instance.get_ordering()

    # Visualize ordering diagram
    analyser = ordering_analyser(ordering)
    ordering_visualizer.show_ordering_diagram(analyser, amount_of_clusters)

    # Visualize clustering results
    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, sample)
    visualizer.show()

**Simulation of oscillatory network PCNN**

.. code:: python

    from pyclustering.nnet.pcnn import pcnn_network, pcnn_visualizer

    # Create Pulse-Coupled neural network with 10 oscillators.
    net = pcnn_network(10)

    # Perform simulation during 100 steps using binary external stimulus.
    dynamic = net.simulate(50, [1, 1, 1, 0, 0, 0, 0, 1, 1, 1])

    # Allocate synchronous ensembles from the output dynamic.
    ensembles = dynamic.allocate_sync_ensembles()

    # Show output dynamic.
    pcnn_visualizer.show_output_dynamic(dynamic, ensembles)

**Simulation of chaotic neural network CNN**

.. code:: python

    from pyclustering.cluster import cluster_visualizer
    from pyclustering.samples.definitions import SIMPLE_SAMPLES
    from pyclustering.utils import read_sample
    from pyclustering.nnet.cnn import cnn_network, cnn_visualizer

    # Load stimulus from file.
    stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

    # Create chaotic neural network, amount of neurons should be equal to amount of stimulus.
    network_instance = cnn_network(len(stimulus))

    # Perform simulation during 100 steps.
    steps = 100
    output_dynamic = network_instance.simulate(steps, stimulus)

    # Display output dynamic of the network.
    cnn_visualizer.show_output_dynamic(output_dynamic)

    # Display dynamic matrix and observation matrix to show clustering phenomenon.
    cnn_visualizer.show_dynamic_matrix(output_dynamic)
    cnn_visualizer.show_observation_matrix(output_dynamic)

    # Visualize clustering results.
    clusters = output_dynamic.allocate_sync_ensembles(10)
    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, stimulus)
    visualizer.show()



Illustrations
=============

**Cluster allocation on FCPS dataset collection by DBSCAN:**

.. image:: https://github.com/annoviko/pyclustering/blob/master/docs/img/fcps_cluster_analysis.png
   :alt: Clustering by DBSCAN

**Cluster allocation by OPTICS using cluster-ordering diagram:**

.. image:: https://github.com/annoviko/pyclustering/blob/master/docs/img/optics_example_clustering.png
   :alt: Clustering by OPTICS


**Partial synchronization (clustering) in Sync oscillatory network:**

.. image:: https://github.com/annoviko/pyclustering/blob/master/docs/img/sync_partial_synchronization.png
   :alt: Partial synchronization in Sync oscillatory network


**Cluster visualization by SOM (Self-Organized Feature Map)**

.. image:: https://github.com/annoviko/pyclustering/blob/master/docs/img/target_som_processing.png
   :alt: Cluster visualization by SOM



.. _scikit-learn: https://scikit-learn.org/stable/
.. _ELKI: https://elki-project.github.io/

.. |Build Status Linux MacOS| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=master
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/master?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=master&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=master
.. |Documentation| image:: https://codedocs.xyz/annoviko/pyclustering.svg
   :target: https://codedocs.xyz/annoviko/pyclustering/
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1491324.svg
   :target: https://doi.org/10.5281/zenodo.1491324
.. |PyPi| image:: https://badge.fury.io/py/pyclustering.svg
   :target: https://badge.fury.io/py/pyclustering
.. |Build Status Linux MacOS 0.9.dev| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=0.9.dev
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win 0.9.dev| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/0.9.dev?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/0.9.dev
.. |Coverage Status 0.9.dev| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=0.9.dev&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=0.9.dev
.. |Build Status Linux 0.9.3.rel| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=0.9.3.rel
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win 0.9.3.rel| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/0.9.3.rel?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/0.9.3.rel
.. |Coverage Status 0.9.3.rel| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=0.9.3.rel&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=0.9.3.rel
.. |Download Counter| image:: https://pepy.tech/badge/pyclustering
   :target: https://pepy.tech/project/pyclustering
.. |JOSS| image:: http://joss.theoj.org/papers/10.21105/joss.01230/status.svg
   :target: https://doi.org/10.21105/joss.01230