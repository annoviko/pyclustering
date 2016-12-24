###Project: PyClustering###

Version: 0.7.dev0

License: GNU General Public License

E-Mail: pyclustering@yandex.ru

-------------------------------------------------

###PyClustering CI:###

[![Build Status](https://travis-ci.org/annoviko/pyclustering.svg?branch=master)](https://travis-ci.org/annoviko/pyclustering)
[![Coverage Status](https://coveralls.io/repos/github/annoviko/pyclustering/badge.svg?branch=master)](https://coveralls.io/github/annoviko/pyclustering?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/annoviko/pyclustering/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/annoviko/pyclustering/?branch=master)

------------------------------------------------

###Based on:###

- Python >= 3.4 windows 64-bit
- Python >= 3.4 linux 64-bit
- C++ 11 (MVS, GCC compilers)

------------------------------------------------

###Required packages:###

- scipy, matplotlib, numpy, PIL


**Index of packages for Windows:**

- http://www.lfd.uci.edu/~gohlke/pythonlibs/

**Index of packages for Linux:**
- sudo apt-get install python3-numpy
- sudo apt-get install python3-scipy
- sudo apt-get install python3-matplotlib
- sudo apt-get install python3-pil

------------------------------------------------

###What is implemented in the project.###

**Clustering algorithms (module pyclustering.cluster):**
- Agglomerative [Python, C++] each object is treated as a single cluster and are then merged (agglomerate) http://nlp.stanford.edu/IR-book/html/htmledition/hierarchical-agglomerative-clustering-1.html
- BIRCH [Python] balanced iterative reducing and clustering using hierarchies https://en.wikipedia.org/wiki/BIRCH_(data_clustering)
- CLARANS [Python] Clustering Large Applications based on RAN-
domized   Search http://www.cs.ecu.edu/~dingq/CSCI6905/readings/CLARANS.pdf
- CURE [Python, C++] Clustering Using REpresentatives https://en.wikipedia.org/wiki/CURE_data_clustering_algorithm
- DBSCAN [Python, C++] Density-based spatial clustering of applications with noise https://en.wikipedia.org/wiki/DBSCAN
- HSyncNet [Python, C++]  Hierarchical Sync (Synchronization-Inspired Partitioning and Hierarchical Clustering) https://www.computer.org/csdl/trans/tk/2013/04/ttk2013040893-abs.html 
- K-Means [Python, C++]  to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster https://en.wikipedia.org/wiki/K-means_algorithm 
- K-Medians [Python, C++] uses the median in each dimension instead of the mean https://en.wikipedia.org/wiki/K-medians_clustering
- K-Medoids [Python, C++] https://en.wikipedia.org/wiki/K-medoids Mediods are representative objects of a data set or a cluster with a data set whose average dissimilarity to all the objects in the cluster is minimal https://en.wikipedia.org/wiki/Medoids
- OPTICS [Python]  Ordering points to identify the clustering structure (OPTICS) https://en.wikipedia.org/wiki/OPTICS_algorithm
- ROCK [Python, C++] ROCK: A Robust Clustering Algorithm for Categorical Attributes http://www.cis.upenn.edu/%7Esudipto/mypapers/categorical.pdf
- SyncNet [Python, C++] SyncNet is bio-inspired algorithm that is based on oscillatory network that uses modified Kuramoto https://annoviko.wordpress.com/2016/07/08/oscillatory-networks-based-on-kuramoto-model-1-introduction/
- SyncSom [Python] Double-layer oscillatory network for cluster analysis https://www.researchgate.net/publication/274066759_SYNC-SOM_Double-layer_oscillatory_network_for_cluster_analysis
- X-Means [Python, C++] The X-Means clustering algorithm (Pelleg & Moore, 2000) is an extension of the K-Means clustering algorithm http://cse-wiki.unl.edu/wiki/index.php/Clustering_Techniques#X-Means_Clustering

**Oscillatory networks and neural networks (module pyclustering.nnet):**
- CNN (Chaotic Neural Network) [Python] https://www.researchgate.net/publication/221053550_Clustering_by_Chaotic_Neural_Networks_with_Mean_Field_Calculated_Via_Delaunay_Triangulation and https://www.researchgate.net/publication/225675697_Large-dimension_image_clustering_by_means_of_fragmentary_synchronization_in_chaotic_systems 
- HHN (Oscillatory network based on Hodgkin-Huxley model) [Python] https://www.researchgate.net/publication/24193858_Selective_attention_model_with_spiking_elements
- Hysteresis Oscillatory Network [Python] https://www.researchgate.net/publication/3952789_Oscillatory_hysteresis_associative_memory
- LEGION (Local Excitatory Global Inhibitory Oscillatory Network) [Python, C++] https://www.researchgate.net/publication/3301932_Locally_excitatory_globally_inhibitory_oscillator_networks_IEEE_Trans_Neural_Netw_6283-286
- PCNN (Pulse-Coupled Neural Network) [Python, C++] https://www.researchgate.net/publication/220693457_Image_processing_using_pulse-coupled_neural_networks
- SOM (Self-Organized Map) [Python, C++] is a type of artificial neural network (ANN) that is trained using unsupervised learning to produce a low-dimensional (typically two-dimensional), discretized representation of the input space of the training samples, called a map. https://en.wikipedia.org/wiki/Self-organizing_map
- Sync (Oscillatory network based on Kuramoto model) [Python, C++] http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.313.1857 
- SyncPR (Oscillatory network for pattern recognition) [Python, C++] https://www.researchgate.net/publication/264902330_Phase_Oscillatory_Network_and_Visual_Pattern_Recognition
- SyncSegm (Oscillatory network for image segmentation) [Python, C++] https://www.researchgate.net/publication/283803971_Oscillatory_Network_Based_on_Kuramoto_Model_for_Image_Segmentation

**Graph Coloring Algorithms (module pyclustering.gcolor):**
- DSatur [Python] https://www.researchgate.net/publication/213877046_New_methods_to_color_the_vertices_of_a_graph
- Hysteresis [Python] https://www.researchgate.net/publication/221374466_Dynamical_hysteresis_neural_networks_for_graph_coloring_problem
- GColorSync [Python] https://www.researchgate.net/publication/232384859_Clustering_dynamics_of_nonlinear_oscillator_network_Application_to_graph_coloring_problem

**Travelling Salesman Problem Algorithms (module pyclustering.tsp):**
- AntColony [Python, C++] https://www.researchgate.net/publication/13987583_Ant_Colonies_for_the_Traveling_Salesman_Problem

**Containers (module pyclustering.container):**
- KD Tree [Python, C++] https://en.wikipedia.org/wiki/Kd-tree
- CF Tree [Python] CF tree is a height-balanced tree that stores the clustering features for a hierarchical clustering  https://en.wikipedia.org/wiki/BIRCH_(data_clustering)

------------------------------------------------

###Code examples:###

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

**Examples for each algorithm or model can be found in following modules of the library:**
- Cluster analysis examples: `pyclustering/cluster/examples/`
- Graph coloring examples: `pyclustering/gcolor/examples/`
- Oscillatory or neural network examples: `pyclustering/nnet/examples/`
- Travelling salesman problem examples: `/pyclustering/tsp/examples/`

------------------------------------------------

###Proposals, questions, bugs:###

In case of any questions, proposals or bugs related to the pyclustering please contact to pyclustering@yandex.ru or create an issue here.
