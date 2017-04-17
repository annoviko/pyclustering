### Project: PyClustering

Version: 0.7.dev0

License: GNU General Public License

E-Mail: pyclustering@yandex.ru

PyClustering Wiki: https://github.com/annoviko/pyclustering/wiki

------------------------------------------------

### Proposals, questions, bugs:

In case of any questions, proposals or bugs related to the pyclustering please contact to pyclustering@yandex.ru or create an issue here.

------------------------------------------------

### PyClustering CI:

[![Build Status](https://travis-ci.org/annoviko/pyclustering.svg?branch=master)](https://travis-ci.org/annoviko/pyclustering)
[![Coverage Status](https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=master)](https://coveralls.io/github/annoviko/pyclustering?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/annoviko/pyclustering/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/annoviko/pyclustering/?branch=master)

------------------------------------------------

### Based on:

- Python >= 3.4 windows 64-bit
- Python >= 3.4 linux 64-bit
- C++ 14 (MVS, GCC compilers)

------------------------------------------------

### Required packages:

- scipy, matplotlib, numpy, PIL


**Index of packages for Windows:**

- http://www.lfd.uci.edu/~gohlke/pythonlibs/

**Index of packages for Linux:**
- sudo apt-get install python3-numpy
- sudo apt-get install python3-scipy
- sudo apt-get install python3-matplotlib
- sudo apt-get install python3-pil

------------------------------------------------

### What is implemented in the project.

**Clustering algorithms (module pyclustering.cluster):**
- Agglomerative [Python, C++]
- BIRCH [Python]
- CLARANS [Python]
- CURE [Python, C++]
- DBSCAN [Python, C++]
- HSyncNet [Python, C++]
- K-Means [Python, C++]
- K-Medians [Python, C++]
- K-Medoids [Python, C++]
- OPTICS [Python, C++]
- ROCK [Python, C++]
- SOM-SC [Python, C++]
- SyncNet [Python, C++]
- Sync-SOM [Python]
- X-Means [Python, C++]

**Oscillatory networks and neural networks (module pyclustering.nnet):**
- CNN (Chaotic Neural Network) [Python]
- HHN (Oscillatory network based on Hodgkin-Huxley model) [Python]
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

**Travelling Salesman Problem Algorithms (module pyclustering.tsp):**
- AntColony [Python, C++]

**Containers (module pyclustering.container):**
- KD Tree [Python, C++]
- CF Tree [Python]

------------------------------------------------

### Examples:

The library contains examples for each algorithm and oscillatory network model:

**Clustering examples:** `pyclustering/cluster/examples`

**Graph coloring examples:** `pyclustering/gcolor/examples`

**Oscillatory network examples:** `pyclustering/nnet/examples`

![alt text](https://github.com/annoviko/pyclustering/blob/master/docs/img/example_cluster_place.png "Where are examples?")

------------------------------------------------

### Illustrations:

**Cluster allocation on FCPS dataset collection by DBSCAN:**

![alt text](https://github.com/annoviko/pyclustering/blob/master/docs/img/fcps_cluster_analysis.png "Clustering by DBSCAN")

**Cluster allocation by OPTICS using cluster-ordering diagram:**

![alt text](https://github.com/annoviko/pyclustering/blob/master/docs/img/optics_example_clustering.png "Clustering by OPTICS")

**Image segmentation by Sync-SOM algorithm:**

![alt text](https://github.com/annoviko/pyclustering/blob/master/docs/img/sync_som_image_segmentation.png "Image segmentation by Sync-SOM")

**Partial synchronization (clustering) in Sync oscillatory network:**

![alt text](https://github.com/annoviko/pyclustering/blob/master/docs/img/sync_partial_synchronization.png "Partial synchronization in Sync oscillatory network")

**Cluster visualization by SOM (Self-Organized Feature Map)**

![alt text](https://github.com/annoviko/pyclustering/blob/master/docs/img/target_som_processing.png "Cluster visualization by SOM")

------------------------------------------------

### Code examples:

**Data clustering by CURE algorithm**
```python
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
```

**Data clustering by SYNC-SOM (bio-inspired) algorithm**
```python
from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.syncsom import syncsom;

from pyclustering.samples.definitions import FCPS_SAMPLES;

from pyclustering.utils import read_sample, draw_dynamics;

# Input data in following format [ [0.1, 0.5], [0.3, 0.1], ... ].
input_data = read_sample(FCPS_SAMPLES.SAMPLE_TARGET);

# Create oscillatory network for cluster analysis
# where the first layer has size 9x9. Radius
# connectivity (similarity parameter) is 0.9.
# CCORE library (C/C++ part of the pyclustering library)
# is used to ensure high performance.
network = syncsom(input_data, 9, 9, 0.9, ccore = True);

# Simulate network (start processing) with collecting
# output dynamic.
(dyn_time, dyn_phase) = network.process(True, 0.999);

# Show structure of the first layer
network.show_som_layer();

# Show structure of the second layer
network.show_sync_layer();

# Show results of clustering
clusters = network.get_clusters();
visualizer = cluster_visualizer();
visualizer.append_clusters(clusters, input_data);
visualizer.show();

# Show output dynamic of the network (that is obtained
# from the second layer).
draw_dynamics(dyn_time, dyn_phase, x_title = "Time", y_title = "Phase", y_lim = [0, 2 * 3.14]);
```

**Simulation of oscillatory network PCNN**
```python
from pyclustering.nnet.pcnn import pcnn_network, pcnn_visualizer;

# Create Pulse-Coupled neural network with 10 oscillators.
net = pcnn_network(10, ccore = ccore_flag);

# Perform simulation during 100 steps using binary external stimulus.
dynamic = net.simulate(100, [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]);

# Allocate synchronous ensembles in the network.
ensembles = dynamic.allocate_sync_ensembles();

# Show output dynamic.
pcnn_visualizer.show_output_dynamic(dynamic); 
```

**Simulation of chaotic neural network CNN**
```python
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
```
