# C++ PyClustering Library

## Introduction

C++ pyclustering is an open source library for data mining that is written in C++. The general aim of the project is to provide C++ developers an ability to use cluster analysis algorithms and other tools including bio-inspired algorithms that are based on oscillatory neural networks. Most of the algorithms and models are presented by parallel implementations that help to maximize the performance.

One of the client of C++ pyclustering is Python pyclustering library that uses the library in order to reach the maximum performance by using C++ advantages. The library is written in pure C++14 without any other third-party dependencies and it can be built for various platforms. The only requirement for a compiler is to support C++14.
The quality of the library is ensured by more than 3500+ unit and integration tests including memory leakage checks and static analyzers.

The C++ pyclustering library is distributed as a source code and can be easily built using makefile or MS Visual Studio. The library can be built as a dynamic library or as a static library.

## Functionality of the Library

There are two general namespaces where functionality focuses:

- `pyclustering::clst` - cluster analysis.
- `pyclustering::nnet` - oscillatory neural networks.

Following general algorithms are implemented in clustering namespace `pyclustering::clst`:

- Agglomerative (pyclustering::clst::agglomerative);
- BSAS (pyclustering::clst::bsas);
- CLIQUE (pyclustering::clst::clique);
- CURE (pyclustering::clst::cure);
- DBSCAN (pyclustering::clst::dbscan);
- Fuzzy C-Means (pyclustering::clst::fcm);
- G-Means (pyclustering::clst::gmeans);
- HSyncNet (bio-inspired algorithm pyclustering::clst::hsyncnet);
- K-Means (pyclustering::clst::kmeans);
- K-Means++ (pyclustering::clst::kmeans_plus_plus);
- K-Medians (pyclustering::clst::kmedians);
- K-Medoids (pyclustering::clst::kmedoids);
- MBSAS (pyclustering::clst::mbsas);
- OPTICS (pyclustering::clst::optics);
- ROCK (pyclustering::clst::rock);
- Silhouette (pyclustering::clst::silhouette, pyclustering::clst::silhouette_ksearch);
- SOM-SC (pyclustering::clst::somsc);
- SyncNet (bio-inspired algorithm pyclustering::clst::syncnet);
- TTSAS (pyclustering::clst::ttsas);
- X-Means (pyclustering::clst::xmeans);

Following general oscillatory network models are implemented in `pyclustering::nnet`:

- Oscillatory network based on Hodgkin-Huxley model (pyclustering::nnet::hhn);
- LEGION: Local Excitatory Global Inhibitory Oscillatory Network (pyclustering::nnet::legion);
- PCNN: Pulse-Coupled Neural Network (pyclustering::nnet::pcnn);
- SOM: Self-Organized Map (pyclustering::nnet::som);
- Sync: Oscillatory Network based on Kuramoto model (pyclustering::nnet::sync);
- SyncPR: Oscillatory Network based on Kuramoto model for pattern recognition (pyclustering::nnet::syncpr);

## Linux – How to Build the Library

1. Download Release source files from: https://github.com/annoviko/pyclustering/releases
2. Extract the archive.
3. Navigate to `pyclustering/ccore`:
```bash
$ cd pyclustering/ccore 
```

4. Execute one of the following command in order to build the library:
   * `make ccore_64bit` - to build shared library.
   * `make ccore_64bit_statis` - to build static library.
   * `make` - to print all available targets.

## MacOS – How to Build the Library

1. Download Release source files from: https://github.com/annoviko/pyclustering/releases
2. Extract the archive.
3. Navigate to `pyclustering/ccore`:
```bash
$ cd pyclustering/ccore 
```

4. Execute one of the following command in order to build the library:
   * `make ccore_64bit` - to build shared library.
   * `make ccore_64bit_statis` - to build static library.
   * `make` - to print all available targets.


## Windows – How to Build the Library
1. Download Release source files from: https://github.com/annoviko/pyclustering/releases
2. Extract the archive.
3. Navigate to `pyclustering/ccore`.
4. Open `ccore.sln` solution using Visual Studio.
5. Build `ccore` project using one of the following configuration:
   * `Release` - to build dynamic library.
   * `Release Static Library` - to build static library.

## Cite the Library

If you are using pyclustering library in a scientific paper, please, cite the library:

Novikov, A., 2019. PyClustering: Data Mining Library. Journal of Open Source Software, 4(36), p.1230. Available at: http://dx.doi.org/10.21105/joss.01230.

BibTeX entry:
```
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
```
