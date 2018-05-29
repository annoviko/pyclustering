|Documentation| |DOI|

PyClustering
============

**pyclustering** is a Python, C++ data mining library (clustering
algorithm, oscillatory networks, neural networks). The library provides
Python and C++ implementations (via CCORE library) of each algorithm or
model. CCORE library is a part of pyclustering and supported only for
32, 64-bit Linux and 32, 64-bit Windows operating systems.

Official repository: https://github.com/annoviko/pyclustering/

Dependencies
============

**Required packages**: scipy, matplotlib, numpy, PIL

**Python version**: >=3.4 (32-bit, 64-bit)

**C++ version**: >= 14 (32-bit, 64-bit)

Performance
===========

Each algorithm is implemented using Python and C/C++ language, if your platform is not supported then Python
implementation is used, otherwise C/C++. Implementation can be chosen by **ccore** flag (by default it is always
'True' and it means that C/C++ is used), for example:

.. code:: python

    # As by default - C/C++ is used
    xmeans_instance_1 = xmeans(data_points, start_centers, 20, ccore=True);

    # Switch off core - Python is used
    xmeans_instance_2 = xmeans(data_points, start_centers, 20, ccore=False);

Installation
============

Installation using pip3 tool:

.. code:: bash

    $ pip3 install pyclustering

Manual installation from official repository using GCC:

.. code:: bash

    # get sources of the pyclustering library, for example, from repository
    $ mkdir pyclustering
    $ cd pyclustering/
    $ git clone https://github.com/annoviko/pyclustering.git .

    # compile CCORE library (core of the pyclustering library).
    $ cd pyclustering/ccore
    $ make ccore_x64        # build for 64-bit OS

    # $ make ccore_x86      # build for 32-bit OS
    # $ make ccore          # build for both (32 and 64-bit)

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

In case of any questions, proposals or bugs related to the pyclustering
please contact to pyclustering@yandex.ru.

Issue tracker: https://github.com/annoviko/pyclustering/issues


Library Content
===============

**Clustering algorithms (module pyclustering.cluster):** 

- **Agglomerative** (pyclustering.cluster.agglomerative);
- **BANG** (pyclustering.cluster.bang);
- **BIRCH** (pyclustering.cluster.birch);
- **BSAS** (pyclustering.cluster.bsas);
- **CLARANS** (pyclustering.cluster.clarans);
- **CURE** (pyclustering.cluster.cure);
- **DBSCAN** (pyclustering.cluster.dbscan);
- **EMA** (pyclustering.cluster.ema);
- **GA (Genetic Algorithm)** (pyclustering.cluster.ga);
- **HSyncNet** (pyclustering.cluster.hsyncnet);
- **K-Means** (pyclustering.cluster.kmeans);
- **K-Means++** (pyclustering.cluster.center_initializer);
- **K-Medians** (pyclustering.cluster.kmedians);
- **K-Medoids (PAM)** (pyclustering.cluster.kmedoids);
- **MBSAS** (pyclustering.cluster.mbsas);
- **OPTICS** (pyclustering.cluster.optics);
- **ROCK** (pyclustering.cluster.rock);
- **SOM-SC** (pyclustering.cluster.somsc);
- **SyncNet** (pyclustering.cluster.syncnet);
- **Sync-SOM** (pyclustering.cluster.syncsom);
- **TTSAS** (pyclustering.cluster.ttsas);
- **X-Means** (pyclustering.cluster.xmeans);


**Oscillatory networks and neural networks (module pyclustering.nnet):**

- **Oscillatory network based on Hodgkin-Huxley model** (pyclustering.nnet.hhn);
- **fSync: Oscillatory Network based on Landau-Stuart equation and Kuramoto model** (pyclustering.nnet.fsync);
- **Hysteresis Oscillatory Network** (pyclustering.nnet.hysteresis);
- **LEGION: Local Excitatory Global Inhibitory Oscillatory Network** (pyclustering.nnet.legion);
- **PCNN: Pulse-Coupled Neural Network** (pyclustering.nnet.pcnn);
- **SOM: Self-Organized Map** (pyclustering.nnet.som);
- **Sync: Oscillatory Network based on Kuramoto model** (pyclustering.nnet.sync);
- **SyncPR: Oscillatory Network based on Kuramoto model for pattern recognition** (pyclustering.nnet.syncpr);
- **SyncSegm: Oscillatory Network based on Kuramoto model for image segmentation** (pyclustering.nnet.syncsegm);

**Graph Coloring Algorithms (module pyclustering.gcolor):**

- **DSATUR** (pyclustering.gcolor.dsatur);
- **Hysteresis Oscillatory Network for graph coloring** (pyclustering.gcolor.hysteresis);
- **Sync: Oscillatory Network based on Kuramoto model for graph coloring** (pyclustering.gcolor.sync);

**Containers (module pyclustering.container):**

- **CF-Tree** (pyclustering.container.cftree);
- **KD-Tree** (pyclustering.container.kdtree);


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


.. |Documentation| image:: https://codedocs.xyz/annoviko/pyclustering.svg
   :target: https://codedocs.xyz/annoviko/pyclustering/
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1254845.svg
   :target: https://doi.org/10.5281/zenodo.1254845
