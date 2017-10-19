|Build Status Linux| |Build Status Win| |Coverage Status| |Code
Quality| |Documentation| |DOI| 

PyClustering
============

**pyclustering** is a Python, C++ data mining library (clustering
algorithm, oscillatory networks, neural networks). The library provides
Python and C++ implementations (via CCORE library) of each algorithm or
model. CCORE library is a part of pyclustering and supported only for
64-bit Linux and 64-bit Windows operating systems.

Dependencies
============

**Required packages**: scipy, matplotlib, numpy, PIL

**Python version**: >=3.4 (64-bit)

**C++ version**: >= 14 (64-bit)

Installation
============

Installation using pip3 tool:

.. code:: bash

    $ pip3 install pyclustering

Manual installation from official repository:

.. code:: bash

    # get sources of the pyclustering library, for example, from repository
    $ mkdir pyclustering
    $ cd pyclustering/
    $ git clone https://github.com/annoviko/pyclustering.git .

    # compile CCORE library (core of the pyclustering library).
    $ cd pyclustering/ccore
    $ make ccore

    # return to parent folder of the pyclustering library
    cd ../

    # add current folder to python path
    PYTHONPATH=`pwd`
    export PYTHONPATH=${PYTHONPATH}


Proposals, Questions, Bugs
==========================

In case of any questions, proposals or bugs related to the pyclustering
please contact to pyclustering@yandex.ru.

Issue tracker: https://github.com/annoviko/pyclustering


Library Content
===============

**Clustering algorithms (module pyclustering.cluster):** 

- **Agglomerative** (pyclustering.cluster.agglomerative);
- **BIRCH** (pyclustering.cluster.birch);
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
- **OPTICS** (pyclustering.cluster.optics);
- **ROCK** (pyclustering.cluster.rock);
- **SOM-SC** (pyclustering.cluster.somsc);
- **SyncNet** (pyclustering.cluster.syncnet);
- **Sync-SOM** (pyclustering.cluster.syncsom);
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

**Travelling Salesman Problem Algorithms (module pyclustering.tsp):**

- **AntColony** (pyclustering.tsp.antcolony);

**Containers (module pyclustering.container):**

- **CF-Tree** (pyclustering.container.cftree);
- **KD-Tree** (pyclustering.container.kdtree);


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
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1026162.svg
   :target: https://doi.org/10.5281/zenodo.1026162
