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

The exponential growth of data leads to an appearance of new disciplines such as cluster analysis, machine learning, and therefore information requires processing in different areas like medicine, commercial, science, engineering, etc. Data processing is performed to extract patterns, clusters, internal structures to understand the nature of the data, make decisions or create models that help to predict further behavior. As a result, more and more algorithms and methods appear to resolve faced problems. PyClustering is an open source data mining library written in Python and C++ that provides a wide range of clustering algorithms and methods including bio-inspired oscillatory networks for data analysis. PyClustering mostly focused on cluster analysis to make it more accessible and understandable for users. The library is distributed under GNU Public License and provides a comprehended interface that makes it easy to use in every project.

# Summary

As it was mentioned in the introduction, PyClustering library is a Python, C++ data mining library focused on cluster analysis. The library provides an implementation of each algorithm and method on Python and C++ programming languages. By default C++ part of the library is used for processing to ensure maximum performance. This is especially relevant for algorithms that are based on oscillatory networks whose dynamic is described by a system of differential equations and where the C++ implementation is more suitable. If PyClustering detects that it is not possible to delegate computation to C++ part, for example, in case of unsupported hardware platform or operating system (current version 0.8.2 supports x86 and x86_64 for Windows and Linux operating systems), then the Python implementation is used. Python supports a wide range of platforms and operating systems and that fact ensures high portability of the library. Such architecture gives a balance between portability and performance. PyClustering uses NumPy [@Oliphant2006] package for computing to increase the performance of the Python implementation. NumPy is the fundamental package for scientific computing that provides efficient operations on large N-dimensional arrays.

PyClustering provides a separate highly optimized implementation of clustering algorithms using parallel computing on pure C++ language without any third parties and therefore it can be easily integrated to every C++ project as a library or as some part of it. In other words, PyClustering usage is not restricted by Python language and corresponding dependencies. The C++ implementation of the library is based on C++14 standard and can be built using well-known compilers, like gcc, clang, mingw, VS2015. Such flexibility allows developers or scientists to focus on their own projects and not to think about library integration and implementation details.

The Python implementation uses SciPy [@SciPy], MatPlotLib [@Hunter2007], NumPy and Pillow packages. SciPy and NumPy are mandatory packages that are used for computing purposes. MatPlotLib and Pillow packages are optional and they are used for visualization services. If these two packages are not installed then PyClustering visualization tools are not available. PyClustering visualization services display clustering results, for example, data and its clusters in N-dimensional space, image segments, histograms, algorithm-specific features, dynamic of oscillatory and neural network outputs, etc. Visualization makes clustering process more comprehensive and useful for research and educational purposes especially in case of complex clustering algorithms, for example, in case of algorithms that are based on oscillatory networks where synchronization processes should be visualized to explain clustering results.

One of the unique features of the library is a collection of oscillatory networks for cluster analysis, graph coloring, and image segmentation. Oscillatory networks are biologically plausible neural networks that use synchronization processes for solving practical problems. Formally, oscillatory neural networks are nonlinear dynamic systems in which neuron is an oscillating element called an oscillator. There is an assumption that the synchronization processes between neurons in the brain are used to implement cognitive functions [@Novikov2014][@Cumin2007]. Thus, oscillatory networks are of great interest because they allow to research mechanisms that synchronize the neuronal activity at the model level.

PyClustering library is available on PyPi and github repository. Since the first release on PyPi in 2014, it has been downloaded more than 141.000 times. Quality of the library is supported by static and dynamic analyzers such as cppcheck, scan-build, valgrid [@Nethercote2007], including compilers gcc, clang, VS2015. Code coverage is more than 93% that is ensured by unit and integration tests (total amount of tests is more than 2.200). Each commit to repository triggers building, analysis, and testing on CI services such as travis-ci, appveyor. PyClustering provides fully documented code for each library’s version including examples, math and algorithms description, installation instructions. The API documentation is generated by doxygen without any warnings and notes to ensure completeness.

# Clustering Algorithms

Algorithms and methods are located in module 'pyclustering.cluster' in case of Python and in namespace 'ccore.clst' in case of C++.

+------------------------+---------+-----+
| Algorithm              | Python  | C++ |
+========================+=========+=====+
| Agglomerative          | v       | v   |
+------------------------+---------+-----+
| BANG                   | v       |     |
+------------------------+---------+-----+
| BIRCH                  | v       |     |
+------------------------+---------+-----+
| BSAS                   | v       | v   |
+------------------------+---------+-----+
| CLARANS                | v       |     |
+------------------------+---------+-----+
| CLIQUE                 | v       | v   |
+------------------------+---------+-----+
| CURE                   | v       | v   |
+------------------------+---------+-----+
| DBSCAN                 | v       | v   |
+------------------------+---------+-----+
| Elbow                  | v       | v   |
+------------------------+---------+-----+
| EMA                    | v       |     |
+------------------------+---------+-----+
| GA (Genetic Algorithm) | v       | v   |
+------------------------+---------+-----+
| HSyncNet               | v       | v   |
+------------------------+---------+-----+
| K-Means                | v       | v   |
+------------------------+---------+-----+
| K-Means++              | v       | v   |
+------------------------+---------+-----+
| K-Medians              | v       | v   |
+------------------------+---------+-----+
| K-Medoids (PAM)        | v       | v   |
+------------------------+---------+-----+
| MBSAS                  | v       | v   |
+------------------------+---------+-----+
| OPTICS                 | v       | v   |
+------------------------+---------+-----+
| ROCK                   | v       | v   |
+------------------------+---------+-----+
| Silhouette             | v       |     |
+------------------------+---------+-----+
| SOM-SC                 | v       | v   |
+------------------------+---------+-----+
| SyncNet                | v       | v   |
+------------------------+---------+-----+
| Sync-SOM               | v       |     |
+------------------------+---------+-----+
| TTSAS                  | v       | v   |
+------------------------+---------+-----+
| X-Means                | v       | v   |
+------------------------+---------+-----+

# Oscillatory Networks and Neural Networks

Networks are located in module 'pyclustering.nnet' in case of Python and in namespace 'ccore.nnet' in case of C++.

+--------------------------------------------------------------------------------+---------+-----+
| Model                                                                          | Python  | C++ |
+================================================================================+=========+=====+
| CNN (Chaotic Neural Network)                                                   | v       |     |
+--------------------------------------------------------------------------------+---------+-----+
| fSync (Oscillatory network based on Landau-Stuart equation and Kuramoto model) | v       |     |
+--------------------------------------------------------------------------------+---------+-----+
| HHN (Oscillatory network based on Hodgkin-Huxley model)                        | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+
| Hysteresis Oscillatory Network                                                 | v       |     |
+--------------------------------------------------------------------------------+---------+-----+
| LEGION (Local Excitatory Global Inhibitory Oscillatory Network)                | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+
| PCNN (Pulse-Coupled Neural Network)                                            | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+
| SOM (Self-Organized Map)                                                       | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+
| Sync (Oscillatory network based on Kuramoto model)                             | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+
| SyncPR (Oscillatory network for pattern recognition)                           | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+
| SyncSegm (Oscillatory network for image segmentation)                          | v       | v   |
+--------------------------------------------------------------------------------+---------+-----+

# Graph Coloring Algorithms

Algorithms are located in module 'pyclustering.gcolor' in case of Python and in namespace 'ccore.container' in case of C++.

+------------------------+---------+-----+
| Algorithm              | Python  | C++ |
+========================+=========+=====+
| DSatur                 | v       |     |
+------------------------+---------+-----+
| Hysteresis             | v       |     |
+------------------------+---------+-----+
| GColorSync             | v       |     |
+------------------------+---------+-----+

# Containers

Algorithms are located in module 'pyclustering.container' in case of Python.

+------------------------+---------+-----+
| Algorithm              | Python  | C++ |
+========================+=========+=====+
| KD Tree                | v       | v   |
+------------------------+---------+-----+
| CF Tree                | v       |     |
+------------------------+---------+-----+

# References