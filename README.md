Project: PyClustering

Version: 0.6.dev0

License: GNU General Public License

E-Mail: pyclustering@yandex.ru

[![Build Status](https://travis-ci.org/annoviko/pyclustering.svg?branch=master)](https://travis-ci.org/annoviko/pyclustering)

------------------------------------------------

Based on:

- Python >= 3.4 windows 64-bit
- Python >= 3.4 linux 64-bit
- C++ 11 (MVS, GCC compilers)

------------------------------------------------

Required following packages by pyclustering:

- scipy, matplotlib, numpy, PIL

------------------------------------------------

Index of packages for Windows:

- http://www.lfd.uci.edu/~gohlke/pythonlibs/


Index of packages for Linux:
- sudo apt-get install python3-numpy
- sudo apt-get install python3-scipy
- sudo apt-get install python3-matplotlib
- sudo apt-get install python3-pil

------------------------------------------------

What is implemented in the project.

Clustering algorithms (module pyclustering.cluster):
- BIRCH [Python]
- CURE [Python, C++]
- DBSCAN [Python, C++]
- Agglomerative [Python, C++]
- HSyncNet [Python, C++]
- K-Means [Python, C++]
- K-Medians [Python]
- K-Medoids [Python]
- OPTICS [Python]
- ROCK [Python, C++]
- SyncNet [Python, C++]
- SyncSom [Python]
- X-Means [Python, C++]

Oscillatory networks and neural networks (module pyclustering.nnet):
- HHN (Oscillatory network based on Hodgkin-Huxley model) [Python]
- Hysteresis Oscillatory Network [Python]
- LEGION (Local Excitatory Global Inhibitory Oscillatory Network) [Python, C++]
- PCNN (Pulse-Coupled Neural Network) [Python, C++]
- SOM (Self-Organized Map) [Python, C++]
- Sync (Oscillatory network based on Kuramoto model) [Python, C++]
- SyncPR (Oscillatory network for pattern recognition) [Python, C++]

Graph Coloring Algorithms (module pyclustering.gcolor):
- DSatur [Python]
- Hysteresis [Python]
- Sync [Python]

Containers (module pyclustering.container):
- KD Tree [Python, C++]
- CF Tree [Python]

------------------------------------------------

In case of any questions or proposals related to the pyclustering please contact to pyclustering@yandex.ru.