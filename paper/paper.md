---
title: 'PyClustering: Data Mining Library'
tags:
  - pyclustering
  - data mining
  - clustering
  - cluster analysis
  - oscillatory network
  - machine learning
  - engineering
  - python
  - C++
authors:
 - name: Andrei V. Novikov
   orcid: 0000-0002-9666-9141
   affiliation: "1"
affiliations:
 - name: Independent Researcher
   index: 1
date: 22 January 2019
bibliography: paper.bib
---

# Introduction

A variety of scientific and industrial sectors continue to experience exponential growth in their data volumes, and so automatic categorization techniques have become standard tools for dataset exploration. Automatic categorization techniques -- typically referred to as clustering -- help expose the structure of a dataset. For example, the generated clusters might each correspond to a customer group with reasonably similar needs and behavior. Because the resulting clusters are often used as building blocks for higher-level -- often custom -- predictive models, researchers have continually tweaked and invented new clustering techniques. PyClustering is an open source data mining library written in Python and C++ that provides a wide range of clustering algorithms and methods, including bio-inspired oscillatory networks. PyClustering is mostly focused on cluster analysis to make it more accessible and understandable for users.

# Summary

The PyClustering library is a Python and C++ data mining library focused on cluster analysis. By default, the C++ part of the library is used for processing in order to achieve maximum performance. This is especially relevant for algorithms that are based on oscillatory networks, whose dynamics are governed by a system of differential equations. If support for a C++ compiler is not detected, PyClustering falls back to pure Python implementations of all kernels. In order to increase the performance of the Python implementations, PyClustering makes use of the NumPy (Oliphant, 2006) library for its array manipulations.

PyClustering provides optimized, parallel C++14 clustering implementations; on most platforms, threading is provided by std::thread, though the Parallel Patterns Library is used for Windows. Due to the standardization of these threading libraries, PyClustering is simple to integrate into pre-existing projects.

The core Python dependencies of PyClustering are NumPy and SciPy (Jones, Oliphant, Peterson, et al., 2019), and MatPlotLib (Hunter, 2007) and Pillow are required for visualization support. The visualization functionality includes 2D and 3D plots of the cluster embeddings, image segments, and, in the case of oscillatory networks, graphs of the synchronization processes.

The PyClustering library is available on PyPi and from a github repository. Since the first release on PyPi in 2014, it has been downloaded more than 141.000 times. The quality of the library is supported by static and dynamic analyzers, such as cppcheck, scan-build, and valgrind [@Nethercote2007]. More than 93% code coverage is provided by more than 2200 unit and integration tests. Each commit to the repository triggers building, analysis, and testing on CI services such as travis-ci or appveyor. PyClustering provides fully-documented code for each library version, including examples, math and algorithms description, and installation instructions.

# Clustering Algorithms

Algorithms and methods are located in the Python module `pyclustering.cluster` and in the C++ namespace `ccore::clst`.

+---------------------------------------------------------+--------------+--------------+
| Algorithm                                               | Python       | C++          |
+=========================================================+==============+==============+
| Agglomerative [@book_algorithms_for_clustering_data]    | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| BANG [@inproceedings_bang_1]                            | $\checkmark$ |              |
+---------------------------------------------------------+--------------+--------------+
| BIRCH [@article_birch_1]                                | $\checkmark$ |              |
+---------------------------------------------------------+--------------+--------------+
| BSAS [@book_pattern_recognition_2009]                   | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| CLARANS [@article_clarans_1]                            | $\checkmark$ |              |
+---------------------------------------------------------+--------------+--------------+
| CLIQUE [@article_clique_1]                              | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| CURE [@article_cure_1]                                  | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| DBSCAN [@inproceedings_dbscan_1]                        | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| Elbow [@article_cluster_elbow_1]                        | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| EMA [@article_ema_1]                                    | $\checkmark$ |              |
+---------------------------------------------------------+--------------+--------------+
| GA - Genetic Algorithm [@article_ga_2]                  | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| HSyncNet [@artcile_hsyncnet_1]                          | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| K-Means [@inproceedings_kmeans_1]                       | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| K-Means++ [@article_kmeans_plus_plus_1]                 | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| K-Medians [@book_algorithms_for_clustering_data]        | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| K-Medoids [@book_algorithms_for_clustering_data]        | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| MBSAS [@book_pattern_recognition_2009]                  | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| OPTICS [@article_optics_1]                              | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| ROCK [@inproceedings_rock_1]                            | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| Silhouette [@article_cluster_silhouette_1]              | $\checkmark$ |              |
+---------------------------------------------------------+--------------+--------------+
| SOM-SC [@article_nnet_som_1]                            | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| SyncNet [@article_syncnet_1]                            | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| Sync-SOM [@article_syncsom_1]                           | $\checkmark$ |              |
+---------------------------------------------------------+--------------+--------------+
| TTSAS [@book_pattern_recognition_2009]                  | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+
| X-Means [@article_xmeans_1]                             | $\checkmark$ | $\checkmark$ |
+---------------------------------------------------------+--------------+--------------+

# Oscillatory Networks and Neural Networks

Networks are located in the Python module `pyclustering.nnet` and in the C++ namespace `ccore::nnet`.

+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| Model                                                                                                                 | Python       | C++          |
+=======================================================================================================================+==============+==============+
| CNN - Chaotic Neural Network [@article_nnet_cnn_1]                                                                    | $\checkmark$ |              |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| fSync - Oscillatory network based on Landau-Stuart equation and Kuramoto model [@book_chemical_oscillatorions_waves]  | $\checkmark$ |              |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| HHN - Oscillatory network based on Hodgkin-Huxley model [@article_nnet_hnn_1]                                         | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| Hysteresis Oscillatory Network [@article_nnet_hysteresis_1]                                                           | $\checkmark$ |              |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| LEGION - Local Excitatory Global Inhibitory Oscillatory Network [@article_legion_1]                                   | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| PCNN - Pulse-Coupled Neural Network [@book_image_processing_using_pcnn]                                               | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| SOM - Self-Organized Map [@article_nnet_som_1]                                                                        | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| Sync - Oscillatory network based on Kuramoto model [@article_nnet_sync_1]                                             | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| SyncPR - Oscillatory network for pattern recognition [@article_nnet_syncpr_1]                                         | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+
| SyncSegm - Oscillatory network for image segmentation [@inproceedings_nnet_syncsegm_1]                                | $\checkmark$ | $\checkmark$ |
+-----------------------------------------------------------------------------------------------------------------------+--------------+--------------+

# Graph Coloring Algorithms

Algorithms are located in the Python module `pyclustering.gcolor`.

+----------------------------------------------+--------------+-----+
| Algorithm                                    | Python       | C++ |
+==============================================+==============+=====+
| DSatur [@article_gcolor_dsatur_1]            | $\checkmark$ |     |
+----------------------------------------------+--------------+-----+
| Hysteresis [@article_nnet_hysteresis_1]      | $\checkmark$ |     |
+----------------------------------------------+--------------+-----+
| GColorSync [@article_gcolor_sync_1]          | $\checkmark$ |     |
+----------------------------------------------+--------------+-----+

# Containers

Containers are located in the Python module `pyclustering.container` and in the C++ namespace `ccore::container`.

+------------------------------------------+--------------+--------------+
| Container                                | Python       | C++          |
+==========================================+==============+==============+
| KD Tree [@book_the_design_and_analysis]  | $\checkmark$ | $\checkmark$ |
+------------------------------------------+--------------+--------------+
| CF Tree [@article_birch_1]               | $\checkmark$ |              |
+------------------------------------------+--------------+--------------+

# References
