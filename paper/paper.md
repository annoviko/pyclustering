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

The exponential growth of data leads to an appearance of new disciplines such as cluster analysis, machine learning, and therefore information requires processing in different areas like medicine, commercial, science, engineering, etc. Data processing is performed to extract patterns, clusters, internal structures to understand the nature of the data, make decisions or create models that help to predict further behavior. As a result, more and more algorithms and methods appear to resolve faced problems. PyClustering is an open source data mining library written in Python and C++ that provides a wide range of clustering algorithms and methods including bio-inspired oscillatory networks for data analysis. PyClustering is mostly focused on cluster analysis to make it more accessible and understandable for users. The library is distributed under GNU Public License and provides a comprehensive interface that makes it easy to use in every project.

# Summary

The PyClustering library is a Python and C++ data mining library focused on cluster analysis. The library provides an implementation of each algorithm and method in the Python and C++ programming languages. By default, the C++ part of the library is used for processing in order to achieve maximum performance. This is especially relevant for algorithms that are based on oscillatory networks, whose dynamic is described by a system of differential equations and where the C++ implementation is more suitable. If PyClustering detects that it is not possible to delegate th computation to C++ part, for example, in case of an unsupported hardware platform or operating system (current version 0.8.2 supports x86 and x86_64 for Windows and Linux operating systems), then the Python implementation is used. Python supports a wide range of platforms and operating systems and that ensures high portability of the library. Such an architecture gives a balance between portability and performance. PyClustering uses the NumPy [@Oliphant2006] package to increase the performance of the Python implementation. NumPy is a fundamental package for scientific computing that provides efficient operations on large N-dimensional arrays.

PyClustering provides a separate and highly optimized implementation of clustering algorithms using parallel computing using pure C++, without any third-party code and it can therefore easily integrated in any C++ project as a library or as some part of it. In other words, PyClustering usage is not restricted to the Python language and corresponding dependencies. The C++ implementation of the library is based on the C++14 standard and can be built using common compilers, including gcc, clang, mingw, and VS2015. Such flexibility allows developers or scientists to focus on their own projects and not think about library integration and implementation details.

The Python implementation uses the SciPy [@SciPy], MatPlotLib [@Hunter2007], NumPy, and Pillow packages. SciPy and NumPy are mandatory dependencies that are used for computing purposes. The MatPlotLib and Pillow packages are optional and are used for visualization services. If these latter two packages are not installed, the PyClustering visualization tools are not available. The PyClustering visualization services display, for example, clustering results, data and its clusters in N-dimensional space, image segments, histograms, algorithm-specific features, dynamics of oscillatory and neural network outputs, etc. Visualization makes the clustering outcome easier to understand and useful for research and educational purposes, especially in case of complex clustering algorithms. For example, in the case of algorithms that are based on oscillatory networks, synchronization processes should be visualized in order to understand the clustering results.

One of the unique features of the library is a collection of oscillatory networks for cluster analysis, graph coloring, and image segmentation. Oscillatory networks are biologically plausible neural networks that use synchronization processes for solving practical problems. Formally, oscillatory neural networks are nonlinear dynamic systems in which the neuron is an oscillating element called an oscillator. There is an assumption that the synchronization processes between neurons in the brain are used to implement cognitive functions [@Novikov2014][@Cumin2007]. Thus, oscillatory networks are of great interest because they allow to research mechanisms that synchronize the neuronal activity at the model level.

The PyClustering library is available on PyPi and from a github repository. Since the first release on PyPi in 2014, it has been downloaded more than 141.000 times. The quality of the library is supported by static and dynamic analyzers, such as cppcheck, scan-build, and valgrid [@Nethercote2007], including compilers gcc, clang, and VS2015. Code coverage is more than 93% that is ensured by unit and integration tests (there are over 2.200 tests). Each commit to the repository triggers building, analysis, and testing on CI services such as travis-ci or appveyor. PyClustering provides fully-documented code for each library version, including examples, math and algorithms description, and installation instructions. The API documentation is generated by doxygen without any warnings and notes to ensure completeness.

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
| K-Medoids (PAM) [@book_algorithms_for_clustering_data]  | $\checkmark$ | $\checkmark$ |
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
| Hysteresis [@article_gcolor_hysteresis_1]    | $\checkmark$ |     |
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
