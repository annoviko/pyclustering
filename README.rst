|Build Status Linux| |Build Status Win| |Coverage Status| |Code
Quality| |Documentation| |PyPi| |DOI|

PyClustering
============

**pyclustering** is a Python, C++ data mining library (clustering
algorithm, oscillatory networks, neural networks). The library provides
Python and C++ implementations (via CCORE library) of each algorithm or
model. CCORE library is a part of pyclustering and supported only for
32, 64-bit Linux and 32, 64-bit Windows operating systems.

**Version**: 0.8.x

**License**: GNU General Public License

**E-Mail**: pyclustering@yandex.ru

**Gitter**: https://gitter.im/pyclustering/pyclustering

**PyClustering Wiki**: https://github.com/annoviko/pyclustering/wiki



Dependencies
============

**Required packages**: scipy, matplotlib, numpy, PIL

**Python version**: >=3.4 (32, 64-bit)

**C++ version**: >= 14 (32, 64-bit)



Performance
===========

Each algorithm is implemented using Python and C/C++ language, if your platform is not supported then Python
implementation is used, otherwise C/C++. Implementation can be chosen by **ccore** flag (by default it is always
'True' and it means that C/C++ is used), for example:

.. code:: python

    xmeans_instance_1 = xmeans(data_points, start_centers, 20, ccore=True);   # As by default - C/C++ is used
    xmeans_instance_2 = xmeans(data_points, start_centers, 20, ccore=False);  # Switch off the core - Python is used

**ccore** option runs ccore shared library (core of the pyclustering library). The core is maintained for Linux 32, 64-bit and Windows 32, 64-bit.



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
    # you can specify platform (32-bit: 'ccore_x86', 64-bit: 'ccore_x64')
    $ cd pyclustering/ccore
    $ make ccore_x64    # compile CCORE for 64-bit
    # make ccore_x86    # compile CCORE for 32-bit
    # make ccore        # compile CCORE for both platforms if you do not know which is required

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

+-----------------+------------------------------+--------------------------------+
| Branch          | master                       | 0.8.dev                        |
+=================+==============================+================================+
| Build (Linux)   | |Build Status Linux|         | |Build Status Linux 0.8|       |
+-----------------+------------------------------+--------------------------------+
| Build (Win)     | |Build Status Win|           | |Build Status Win 0.8|         |
+-----------------+------------------------------+--------------------------------+
| Code Coverage   | |Coverage Status|            | |Coverage Status 0.8|          |
+-----------------+------------------------------+--------------------------------+
| Code Quality    | |Code Quality|               | |Code Quality 0.8|             |
+-----------------+------------------------------+--------------------------------+



Brief Overview of the Library Content
=====================================

**Clustering algorithms (module pyclustering.cluster):** 

- Agglomerative [Python, C++]
- BANG [Python]
- BIRCH [Python]
- BSAS [Python, C++]
- CLARANS [Python]
- CURE [Python, C++]
- DBSCAN [Python, C++]
- EMA [Python]
- GA (Genetic Algorithm) [Python, C++]
- HSyncNet [Python, C++]
- K-Means [Python, C++]
- K-Means++ [Python, C++]
- K-Medians [Python, C++]
- K-Medoids (PAM) [Python, C++]
- MBSAS [Python, C++]
- OPTICS [Python, C++]
- ROCK [Python, C++]
- SOM-SC [Python, C++]
- SyncNet [Python, C++]
- Sync-SOM [Python]
- TTSAS [Python, C++]
- X-Means [Python, C++]


**Oscillatory networks and neural networks (module pyclustering.nnet):**

- CNN (Chaotic Neural Network) [Python] 
- fSync (Oscillatory network based on Landau-Stuart equation and Kuramoto model) [Python] 
- HHN (Oscillatory network based on Hodgkin-Huxley model) [Python, C++]
- Hysteresis Oscillatory Network [Python]
- LEGION (Local Excitatory Global Inhibitory Oscillatory Network) [Python, C++]
- PCNN (Pulse-Coupled Neural Network) [Python, C++]
- SOM (Self-Organized Map) [Python, C++]
- Sync (Oscillatory network based on Kuramoto model) [Python, C++]
- SyncPR (Oscillatory network for pattern recognition) [Python, C++]
- SyncSegm (Oscillatory network for image segmentation) [Python, C++]

**Graph Coloring Algorithms (module pyclustering.gcolor):**

- DSatur [Python]
- Hysteresis [Python]
- GColorSync [Python]

**Containers (module pyclustering.container):**

- KD Tree [Python, C++]
- CF Tree [Python]



Cite the Library
================

If you are using pyclustering library in a scientific paper, please, cite the library.

BibTeX entry:

.. code::

    @misc{andrei_novikov_2018_1254845,
        author       = {Andrei Novikov},
        title        = {annoviko/pyclustering: pyclustering 0.8.1 release},
        month        = may,
        year         = 2018,
        doi          = {10.5281/zenodo.1254845},
        url          = {https://doi.org/10.5281/zenodo.1254845}
    }



Examples:
=========

The library contains examples for each algorithm and oscillatory network
model:

**Clustering examples:** ``pyclustering/cluster/examples``

**Graph coloring examples:** ``pyclustering/gcolor/examples``

**Oscillatory network examples:** ``pyclustering/nnet/examples``

.. image:: https://github.com/annoviko/pyclustering/blob/master/docs/img/example_cluster_place.png
   :alt: Where are examples?



Illustrations:
==============

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




Code Examples:
==============

**Data clustering by CURE algorithm**

.. code:: python

    from pyclustering.cluster import cluster_visualizer;
    from pyclustering.cluster.cure import cure;

    from pyclustering.utils import read_sample;

    from pyclustering.samples.definitions import FCPS_SAMPLES;

    # Input data in following format [ [0.1, 0.5], [0.3, 0.1], ... ].
    input_data = read_sample(FCPS_SAMPLES.SAMPLE_LSUN);

    # Allocate three clusters:
    cure_instance = cure(input_data, 3);
    cure_instance.process();
    clusters = cure_instance.get_clusters();

    # Visualize clusters:
    visualizer = cluster_visualizer();
    visualizer.append_clusters(clusters, None);
    visualizer.show();

**Simulation of oscillatory network PCNN**

.. code:: python

    from pyclustering.nnet.pcnn import pcnn_network, pcnn_visualizer;

    # Create Pulse-Coupled neural network with 10 oscillators.
    net = pcnn_network(10, ccore = ccore_flag);

    # Perform simulation during 100 steps using binary external stimulus.
    dynamic = net.simulate(100, [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]);

    # Allocate synchronous ensembles in the network.
    ensembles = dynamic.allocate_sync_ensembles();

    # Show output dynamic.
    pcnn_visualizer.show_output_dynamic(dynamic); 

**Simulation of chaotic neural network CNN**

.. code:: python

    from pyclustering.samples.definitions import FCPS_SAMPLES;

    from pyclustering.utils import read_sample;

    from pyclustering.nnet.cnn import cnn_network, cnn_visualizer;

    # load stimulus from file
    stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
            
    # create chaotic neural network, amount of neurons should be equal to amout of stimulus
    network_instance = cnn_network(len(stimulus));
            
    # simulate it during 100 steps
    output_dynamic = network_instance.simulate(steps, stimulus);
            
    # display output dynamic of the network
    cnn_visualizer.show_output_dynamic(output_dynamic);
            
    # dysplay dynamic matrix and observation matrix to show clustering
    # phenomenon.
    cnn_visualizer.show_dynamic_matrix(output_dynamic);
    cnn_visualizer.show_observation_matrix(output_dynamic); 

.. |Build Status Linux| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=master
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/master?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=master&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=master
.. |Code Quality| image:: https://scrutinizer-ci.com/g/annoviko/pyclustering/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/annoviko/pyclustering/?branch=master
.. |Documentation| image:: https://codedocs.xyz/annoviko/pyclustering.svg
   :target: https://codedocs.xyz/annoviko/pyclustering/
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1254845.svg
   :target: https://doi.org/10.5281/zenodo.1254845
.. |PyPi| image:: https://badge.fury.io/py/pyclustering.svg
   :target: https://badge.fury.io/py/pyclustering
.. |Build Status Linux 0.8| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=0.8.dev
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win 0.8| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/0.8.dev?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/0.8.dev
.. |Coverage Status 0.8| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=0.8.dev&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=0.8.dev
.. |Code Quality 0.8| image:: https://scrutinizer-ci.com/g/annoviko/pyclustering/badges/quality-score.png?b=0.8.dev
   :target: https://scrutinizer-ci.com/g/annoviko/pyclustering/?branch=0.8.dev
