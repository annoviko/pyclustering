Warning - Attention Users
=========================

**Please be aware that the `pyclustering` library is no longer supported as of 2021 due to personal reasons. There will be no further maintenance, issue addressing, or feature development for this repository.**

**For continued usage, I recommend seeking alternative solutions.**

**Thank you for your understanding.**


Build Status
============

|Build Status Linux MacOS| |Build Status Win| |Coverage Status| |PyPi| |Download Counter| |JOSS|


PyClustering
============

**pyclustering** is a Python, C++ data mining library (clustering
algorithm, oscillatory networks, neural networks). The library provides
Python and C++ implementations (C++ pyclustering library) of each algorithm or
model. C++ pyclustering library is a part of pyclustering and supported for
Linux, Windows and MacOS operating systems.

**Version**: 0.11.dev

**License**: The 3-Clause BSD License

**E-Mail**: pyclustering@yandex.ru

**Documentation**: https://pyclustering.github.io/docs/0.10.1/html/

**Homepage**: https://pyclustering.github.io/

**PyClustering Wiki**: https://github.com/annoviko/pyclustering/wiki



Dependencies
============

**Required packages**: scipy, matplotlib, numpy, Pillow

**Python version**: >=3.6 (32-bit, 64-bit)

**C++ version**: >= 14 (32-bit, 64-bit)



Performance
===========

Each algorithm is implemented using Python and C/C++ language, if your platform is not supported then Python
implementation is used, otherwise C/C++. Implementation can be chosen by `ccore` flag (by default it is always
'True' and it means that C/C++ is used), for example:

.. code:: python

    # As by default - C/C++ part of the library is used
    xmeans_instance_1 = xmeans(data_points, start_centers, 20, ccore=True);

    # The same - C/C++ part of the library is used by default
    xmeans_instance_2 = xmeans(data_points, start_centers, 20);

    # Switch off core - Python is used
    xmeans_instance_3 = xmeans(data_points, start_centers, 20, ccore=False);



Installation
============

Installation using pip3 tool:

.. code:: bash

    $ pip3 install pyclustering

Manual installation from official repository using Makefile:

.. code:: bash

    # get sources of the pyclustering library, for example, from repository
    $ mkdir pyclustering
    $ cd pyclustering/
    $ git clone https://github.com/annoviko/pyclustering.git .

    # compile CCORE library (core of the pyclustering library).
    $ cd ccore/
    $ make ccore_64bit      # build for 64-bit OS

    # $ make ccore_32bit    # build for 32-bit OS

    # return to parent folder of the pyclustering library
    $ cd ../

    # install pyclustering library
    $ python3 setup.py install

    # optionally - test the library
    $ python3 setup.py test

Manual installation using CMake:

.. code:: bash

    # get sources of the pyclustering library, for example, from repository
    $ mkdir pyclustering
    $ cd pyclustering/
    $ git clone https://github.com/annoviko/pyclustering.git .

    # generate build files.
    $ mkdir build
    $ cmake ..

    # build pyclustering-shared target depending on what was generated (Makefile or MSVC solution)
    # if Makefile has been generated then
    $ make pyclustering-shared

    # return to parent folder of the pyclustering library
    $ cd ../

    # install pyclustering library
    $ python3 setup.py install

    # optionally - test the library
    $ python3 setup.py test

Manual installation using Microsoft Visual Studio solution:

1. Clone repository from: https://github.com/annoviko/pyclustering.git
2. Open folder `pyclustering/ccore`
3. Open Visual Studio project `ccore.sln`
4. Select solution platform: `x86` or `x64`
5. Build `pyclustering-shared` project.
6. Add pyclustering folder to python path or install it using setup.py

.. code:: bash

    # install pyclustering library
    $ python3 setup.py install

    # optionally - test the library
    $ python3 setup.py test



Proposals, Questions, Bugs
==========================

In case of any questions, proposals or bugs related to the pyclustering please contact to pyclustering@yandex.ru or create an issue here.



PyClustering Status
===================

+----------------------+------------------------------+-------------------------------------+---------------------------------+
| Branch               | master                       | 0.10.dev                            | 0.10.1.rel                      |
+======================+==============================+=====================================+=================================+
| Build (Linux, MacOS) | |Build Status Linux MacOS|   | |Build Status Linux MacOS 0.10.dev| | |Build Status Linux 0.10.1.rel| |
+----------------------+------------------------------+-------------------------------------+---------------------------------+
| Build (Win)          | |Build Status Win|           | |Build Status Win 0.10.dev|         | |Build Status Win 0.10.1.rel|   |
+----------------------+------------------------------+-------------------------------------+---------------------------------+
| Code Coverage        | |Coverage Status|            | |Coverage Status 0.10.dev|          | |Coverage Status 0.10.1.rel|    |
+----------------------+------------------------------+-------------------------------------+---------------------------------+



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



.. |Build Status Linux MacOS| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=master
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/master?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=master&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=master
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4280556.svg
   :target: https://doi.org/10.5281/zenodo.4280556
.. |PyPi| image:: https://badge.fury.io/py/pyclustering.svg
   :target: https://badge.fury.io/py/pyclustering
.. |Build Status Linux MacOS 0.10.dev| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=0.10.dev
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win 0.10.dev| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/0.10.dev?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/0.9.dev
.. |Coverage Status 0.10.dev| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=0.10.dev&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=0.9.dev
.. |Build Status Linux 0.10.1.rel| image:: https://travis-ci.org/annoviko/pyclustering.svg?branch=0.10.1.rel
   :target: https://travis-ci.org/annoviko/pyclustering
.. |Build Status Win 0.10.1.rel| image:: https://ci.appveyor.com/api/projects/status/4uly2exfp49emwn0/branch/0.10.1.rel?svg=true
   :target: https://ci.appveyor.com/project/annoviko/pyclustering/branch/0.10.1.rel
.. |Coverage Status 0.10.1.rel| image:: https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=0.10.1.rel&ts=1
   :target: https://coveralls.io/github/annoviko/pyclustering?branch=0.10.1.rel
.. |Download Counter| image:: https://pepy.tech/badge/pyclustering
   :target: https://pepy.tech/project/pyclustering
.. |JOSS| image:: http://joss.theoj.org/papers/10.21105/joss.01230/status.svg
   :target: https://doi.org/10.21105/joss.01230


## 🌐 Web Resources & Interactive Index
- [SNIPER ELITE 3D](https://thequizzone.pages.dev/sniper-elite-3d.html)
- [CAPYBARA BLOCK BLAST](https://themindplays.pages.dev/capybara-block-blast.html)
- [CATEGORY MATCH 3117](https://themindplays.pages.dev/category-match-3117.html)
- [PIXEL FLOW](https://thequizzone.pages.dev/pixel-flow.html)
- [MICKEY RUN ADVENTURE GAME](https://theskillquest.pages.dev/mickey-run-adventure-game.html)
- [CATEGORY COOKING](https://themindplays.pages.dev/category-cooking.html)
- [BLACKRIVER MYSTERY HIDDEN OBJECTS](https://theskillquest.pages.dev/blackriver-mystery-hidden-objects.html)
- [BACKFLIP MASTER](https://ilearnworldjp.pages.dev/backflip-master.html)
- [FISHING BARON REAL FISHING](https://iskillquest.pages.dev/fishing-baron-real-fishing.html)
- [CATEGORY COOKING46](https://themindplays.pages.dev/category-cooking46.html)
- [SITEMAP](https://themindplays.pages.dev/sitemap.html)
- [CATEGORY CARE](https://themindplays.pages.dev/category-care.html)
- [MAGIC KINGDOM HEX MATCH](https://iskillquest.pages.dev/magic-kingdom-hex-match.html)
- [AMERICAN BLOCK SNIPER ONLINE](https://theskillquest.pages.dev/american-block-sniper-online.html)
- [BOMBY](https://themindplaying.web.app/bomby.html)
- [CATEGORY CRAFTING45](https://themindplay.github.io/category-crafting45.html)
- [COOKING RESTAURANT KITCHEN](https://studyquests.github.io/cooking-restaurant-kitchen.html)
- [CLONEUP STACK YOURSELF](https://thequizzone.pages.dev/cloneup-stack-yourself.html)
- [MAGIC FINGER PUZZLE 3D](https://themindplaying.web.app/magic-finger-puzzle-3d.html)
- [CATEGORY QUIZ](https://themindzone.pages.dev/category-quiz.html)
- [BUBBLE BLITZ GALAXY](https://theskillquest.pages.dev/bubble-blitz-galaxy.html)
- [MAGIC BEAUTY MAKEUP](https://themindplaying.web.app/magic-beauty-makeup.html)
- [FOAM AND FIND](https://themindplay.github.io/foam-and-find.html)
- [SOKOBAN PUSH THE BOX](https://studyquests.github.io/sokoban-push-the-box.html)
- [VIKINGS AN ARCHERS JOURNEY](https://thequizzone.pages.dev/vikings-an-archers-journey.html)
- [CATEGORY UNBLOCKERS](https://quizverses-9d2f2.web.app/category-unblockers.html)
- [ARROW SURVIVAL 15 SECONDS](https://learnquester.github.io/arrow-survival-15-seconds.html)
- [MONSTER GIRLS BACK TO SCHOOL](https://themindzone.pages.dev/monster-girls-back-to-school.html)
- [TAXI DRIVER SIMULATOR](https://theskillquest.pages.dev/taxi-driver-simulator.html)
- [CATEGORY CUTE](https://themindplays.pages.dev/category-cute.html)
- [TILE FRUITS](https://studyquests.github.io/tile-fruits.html)
- [CATEGORY CASUAL 15](https://themindplays.pages.dev/category-casual-15.html)
- [CAR JAM ESCAPE](https://quizverses.github.io/car-jam-escape.html)
- [POOL DUEL](https://iskillquest.pages.dev/pool-duel.html)
- [MOLANG MATCHN MUNCH](https://themindplay.github.io/molang-matchn-munch.html)
- [CATEGORY 204828](https://theskillquest.pages.dev/category-204828.html)
- [CAT VS GRANNY CAT SIMULATOR](https://themindplaying.web.app/cat-vs-granny-cat-simulator.html)
- [CATEGORY QUIZ](https://studyquests.pages.dev/category-quiz.html)
- [CS COMMAND SNIPERS](https://learnquester.pages.dev/cs-command-snipers.html)
- [TCG CARD CLICKER](https://themindplaying.web.app/tcg-card-clicker.html)
- [SQUID GAME PLAYGROUND SHOOTER](https://thelearnquesters.pages.dev/squid-game-playground-shooter.html)
- [BLOCK MANIA](https://themindplay.github.io/block-mania.html)
- [BARK BLAST](https://thequizzone.pages.dev/bark-blast.html)
- [CATEGORY FLASH](https://themindplays.pages.dev/category-flash.html)
- [CATEGORY ANIMAL216](https://studyplayings.web.app/category-animal216.html)
- [SLAP MAN](https://themindplay.github.io/slap-man.html)
- [NEON BLAST](https://studyplaying.github.io/neon-blast.html)
- [SLIDE RABBIT](https://studyplayings.pages.dev/slide-rabbit.html)
- [PIMPLE SQUEEZE](https://studyplaying.github.io/pimple-squeeze.html)
- [CATEGORY GROW99](https://quizverses.github.io/category-grow99.html)
- [CATEGORY CARDS](https://themindplays.pages.dev/category-cards.html)
- [OBBY CARDS THE LEGEND HUNT](https://studyplaying.github.io/obby-cards-the-legend-hunt.html)
- [ITALIAN BRAINROT JIGSAW](https://themindplaying.web.app/italian-brainrot-jigsaw.html)
- [TRUCK STACK COLORS](https://theskillquest.pages.dev/truck-stack-colors.html)
- [CATEGORY MAHJONG 2](https://quizverses.github.io/category-mahjong-2.html)
- [CATEGORY COLLECT565](https://themindplay.pages.dev/category-collect565.html)
- [ICE FISHING 3D](https://studyplayings.web.app/ice-fishing-3d.html)
- [BOYFRIEND FOR HIRE](https://iskillquest.pages.dev/boyfriend-for-hire.html)
- [BOLTS UNSCREW IT](https://theskillquest.pages.dev/bolts-unscrew-it.html)
- [ARROW TAP PUZZLE](https://thequizzone.pages.dev/arrow-tap-puzzle.html)
- [PUZZLEJAM](https://thequizzone.pages.dev/puzzlejam.html)
- [CUTE CATS ADVENTURES](https://quizverses.github.io/cute-cats-adventures.html)
- [CATEGORY WAR137](https://quizverses.pages.dev/category-war137.html)
- [UNCLE BULLET 007](https://quizverses-9d2f2.web.app/uncle-bullet-007.html)
- [CATEGORY FARMING87](https://themindplays.pages.dev/category-farming87.html)
- [WORM ESCAPE](https://thelearnquesters.pages.dev/worm-escape.html)
- [FAR ORION NEW WORLDS](https://learnquester.pages.dev/far-orion-new-worlds.html)
- [KINGDOM WARS TD](https://studyquesthub.web.app/kingdom-wars-td.html)
- [MADNESS SHERIFFS COMPOUND OFFICIAL](https://themindplaying.web.app/madness-sheriffs-compound-official.html)
- [CATEGORY PUZZLE 2](https://thequizzone.pages.dev/category-puzzle-2.html)
- [BUBBLE IT JAM](https://thequizzone.pages.dev/bubble-it-jam.html)
- [CAKE SORT](https://themindzone.pages.dev/cake-sort.html)
- [MONKEY BUBBLE DEFENSE](https://studyplayings.web.app/monkey-bubble-defense.html)
- [UFO IO ARMADA](https://themindzone.pages.dev/ufo-io-armada.html)
- [SAMURAI MADNESS](https://studyquesthub.web.app/samurai-madness.html)
- [YOUR DREAM ROOM](https://thequizzone.pages.dev/your-dream-room.html)
- [SUPERHERO PHONE SIMULATOR](https://thelearnquesters.pages.dev/superhero-phone-simulator.html)
- [MERGE HAVEN](https://quizverses.github.io/merge-haven.html)
- [CATEGORY PREMIUM PERKS74](https://learnquester.pages.dev/category-premium-perks74.html)
- [MATCH DREAM GARDEN](https://themindplaying.web.app/match-dream-garden.html)
- [MONEY MAKER](https://thelearnquester.web.app/money-maker.html)
- [CATEGORY BUILDING182](https://themindplay.pages.dev/category-building182.html)
- [NETQUEL COM](https://studyquesthub.web.app/netquel-com.html)
- [MERGE BRICK BREAKER](https://studyquests.github.io/merge-brick-breaker.html)
- [PIZZA MAKER](https://thelearnquesters.pages.dev/pizza-maker.html)
- [CATEGORY SIMULATION 2](https://studyplayings.pages.dev/category-simulation-2.html)
- [DUNGEON MASTER KNIGHT](https://thequizzone.pages.dev/dungeon-master-knight.html)
- [CATEGORY TOWER DEFENSE 2](https://quizverses.github.io/category-tower-defense-2.html)
- [SOLITAIRE MAHJONG FARM 2](https://studyplaying.github.io/solitaire-mahjong-farm-2.html)
- [BANK BOOM TUNG TUNG SAHUR](https://themindplaying.web.app/bank-boom-tung-tung-sahur.html)
- [CATEGORY ESCAPE](https://theskillquest.pages.dev/category-escape.html)
- [FAIRY WINGERELLA](https://thelearnquester.web.app/fairy-wingerella.html)
- [WORM PUZZLE SNAKE APPLE](https://theskillquest.pages.dev/worm-puzzle-snake-apple.html)
- [CATEGORY JIGSAW10](https://quizverses.github.io/category-jigsaw10.html)
- [BRAWL BROS SQUAD](https://thequizzone.pages.dev/brawl-bros-squad.html)
- [CATEGORY ANIMAL](https://themindplay.pages.dev/category-animal.html)
- [POP THEM](https://studyquests.github.io/pop-them.html)
- [MR DRIFTER CAR CHASE SIMULATOR](https://learnquester.github.io/mr-drifter-car-chase-simulator.html)
- [KINGDOM OF PIXELS](https://quizverses.github.io/kingdom-of-pixels.html)
- [SNIPER FREEZE](https://themindplay.github.io/sniper-freeze.html)
- [MR DUDE KING OF THE HILL](https://themindplaying.web.app/mr-dude-king-of-the-hill.html)
- [BOOM STICK BAZOOKA](https://quizverses.github.io/boom-stick-bazooka.html)
- [INDEX6](https://studyplayings.pages.dev/index6.html)
- [CATEGORY BOARDGAMES](https://iskillquest.pages.dev/category-boardgames.html)
- [CATEGORY PUZZLE 2](https://thelearnquester.web.app/category-puzzle-2.html)
- [CUBEREALM IO](https://studyquesthub.web.app/cuberealm-io.html)
- [FRUIT CAFE MATCH 3](https://learnquester.pages.dev/fruit-cafe-match-3.html)
- [SAVE THE DADDY](https://theskillquest.pages.dev/save-the-daddy.html)
- [STICKMAN SHOOTER BROS](https://themindplaying.web.app/stickman-shooter-bros.html)
- [RACE TIME](https://studyplaying.github.io/race-time.html)
- [MAGIC AND WIZARDS MAHJONG](https://themindplay.github.io/magic-and-wizards-mahjong.html)
- [COLOR IT IN 3D](https://learnquester.pages.dev/color-it-in-3d.html)
- [COOL ORANGE BALL BOUNCE ADVENTURE](https://studyplaying.github.io/cool-orange-ball-bounce-adventure.html)
- [ROBLOX CRAFT RUN](https://studyquests.github.io/roblox-craft-run.html)
- [SUPER RACING GT DRAG PRO](https://themindplay.github.io/super-racing-gt-drag-pro.html)
- [CATEGORY POOL](https://studyquests.pages.dev/category-pool.html)
- [WORDMEISTER HD](https://themindplaying.web.app/wordmeister-hd.html)
- [ZOMBIES WEAPON MERGE 4](https://studyquesthub.web.app/zombies-weapon-merge-4.html)
- [STUNT FURY](https://themindzone.pages.dev/stunt-fury.html)
- [CATEGORY TRAFFIC34](https://quizverses-9d2f2.web.app/category-traffic34.html)
- [MONEY CHASER CITY PARKOUR GAME](https://themindzone.pages.dev/money-chaser-city-parkour-game.html)
- [ITALIAN BRAINROT BABY CLICKER](https://themindplaying.web.app/italian-brainrot-baby-clicker.html)
- [SOLITAIRE STORY TRIPEAKS 6](https://skillplay.github.io/solitaire-story-tripeaks-6.html)
- [TIMEWARRIORS](https://studyquesthub.web.app/timewarriors.html)
- [MEMORY MATCH MAGIC](https://thelearnquesters.pages.dev/memory-match-magic.html)
- [CATEGORY CASUAL](https://studyquests.pages.dev/category-casual.html)
- [SNAKE 2048IO](https://iskillquest.pages.dev/snake-2048io.html)
- [RAGDOLL BEAT SIMULATOR](https://iskillquest.pages.dev/ragdoll-beat-simulator.html)
- [PLAYGROUND PARKOUR](https://themindplay.github.io/playground-parkour.html)
- [ICE SKATING BALLERINA](https://studyplaying.github.io/ice-skating-ballerina.html)
