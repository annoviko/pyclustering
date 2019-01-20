---
title: 'PyClustering: Data Mining Library'
tags:
  - pyclustering
  - data mining
  - clustering
  - cluster analysis
  - oscillatory network
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
date: 19 January 2019
bibliography: paper.bib
---

# Introduction

The last years exponential growth of data leads to appearance of new disciplines, for example, cluster analysis, machine learning, because of this information requires processing in different areas like medicine, commercial, science, engineering, etc. Data processing is performed to extract patterns, clusters, internal structures to understand nature of the data, make decisions or create models that help to predict further behavior. As a result more and more algorithms and methods appears to resolve faced problems. PyClustering is an open source data mining library written in Python and C++ that provides wide range of clustering algorithms and methods including bio-inspired oscillatory networks for data analysis. PyClustering focuses mostly on cluster analysis to make it more accessible and understandable for users. The library is distributed using GNU Public License and provides comprehended interface that makes it easy to use in every project.

# Summary

PyClustering library is a Python, C++ data mining library that focuses on clustering algorithms as it was mentioned above. The library provides implementation of each algorithm and method on Python and C++ programming languages. By default C++ part of the library is used for processing to ensure maximum performance. This is especially relevant for oscillatory network based algorithms whose dynamic is described by a system of differential equations and where C++ implementation is more suitable. But if PyClustering detects that it is not possible to delegate computation to C++ part, for example, in case of unsupported hardware platform or operating system (current version 0.8.2 supports x86 and x86_64 for Windows and Linux operating systems), then the Python implementation is used. Python supports wide range of platforms and operating systems that ensures high portability of the library. Such architecture gives balance between portability and performance. PyClustering uses NumPy package for computing to increase performance of the Python implementation. NumPy is the fundamental package for scientific computing that provides efficient operations on large N-dimensional arrays.

PyClustering provides separate highly optimized implementation of clustering algorithms using parallel computing on pure C++ language without any third-parties and therefore it can be easily integrated to every C++ project as a library or as sources. The C++ implementation of the library is based on C++14 standard and can be built using well-known compilers, like gcc, clang, mingw, VS2015. Such flexibility allows developers or scientists to focus on their own projects and not to think about library integration and implementation details.

Python implementation is built on SciPy, MatPlotLib, NumPy and Pillow. Packages SciPy and NumPy are mandatory for the library that are used for computing purposes. Package MatPlotLib and Pillow are optional and used for visualization services, if these two packages are not installed then PyClustering visualization tools are not available. PyClustering visualization services display clustering results, for example, data and its clusters in N-dimensional space, image segmentation, histograms, algorithm-specific features, dynamic of oscillatory and neural network outputs, etc. Visualization makes clustering process more comprehensive and useful for research and educational purposes especially in case of complex clustering algorithms, for example, in case of algorithms that are based on oscillatory networks where synchronization processes should be visualized to explain clustering results.

One of the unique feature of the library is collection of oscillatory networks for cluster analysis, graph coloring and image segmentation. Oscillatory networks are biologically plausible neural networks that uses synchronization processes for solving practical problems. Formally oscillatory neural networks are nonlinear dynamic systems in which neuron is an oscillating element called an oscillator. There is assumption that the synchronization processes between neurons in the brain are used to implement cognitive functions [@Novikov2014][@Cumin2007]. Thus, oscillatory networks are of great interest because they allow to research mechanisms that synchronize the neuronal activity at the model level.

PyClustering library includes following clustering algorithms: agglomerative, BANG, BIRCH, BSAS, CLARANS, CURE, CURE, DBSCAN, Elbow, expectation-maximization algorithm, genetic algorithm, hierarchical SyncNet, K-Means, K-Means++, K-Medians, K-Medoids (PAM), MBSAS, OPTICS, ROCK, Silhouette, SOM-SC, SyncNet, Sync-SOM, TTSAS, X-Means. These algorithms and methods are located in module 'pyclustering.cluster' in case of Python and in namespace 'ccore.clst' in case of C++.

Following oscillatory networks and neural networks are implemented in PyClustering: CNN (chaotic neural network), fSync (oscillatory network based on Landau-Stuart equation and Kuramoto model), HHN (oscillatory network based on Hodgkin-Huxley model), hysteresis oscillatory network, LEGION (local excitatory global inhibitory oscillatory network), PCNN (pulse-coupled neural network), SOM (self-organized map), Sync (oscillatory network based on Kuramoto model), SyncPR (oscillatory network based on Kuramoto model for pattern recognition), SyncSegm (oscillatory network based on Kuramoto model for image segmentation).

Additionally the library contains several graph coloring algorithms: DSatur, Hysteresis, GColorSync.

PyClustering library is available on PyPi and github repository. Since the first release on PyPi in 2014, it has been downloaded more than 138.000 times. Quality of the library is supported by static analyzers, memory analyzers, unit and integration tests (more than 2.200 tests, code coverage more than 93%). Each commit to repository triggers build, analysis and testing processes on CI services (travis-ci, appveyor).

# References