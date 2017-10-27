"""!

@brief Cluster analysis algorithm: Ant-Mean
@details Implementation based on article:
         - W.A.Tao, Y.Ma, J.H.Tian, M.Y.Li, W.S.Duan, Y.Y.Liang. An improved ant colony clustering algorithm. 2012.
         
@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
@date 2014-2017
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


import pyclustering.core.antmean_wrapper as wrapper;


class antmean_clustering_params:
    """!
    @brief Ant-Mean algorithm parameters.
    
    """
    
    def __init__(self):
        """!
        @brief Constructs Ant-Mean algorithm parameters.
        
        """
        
        ## Used for pheramone evaporation
        self.ro = 0.9;
        
        ## Initial value for pheramones
        self.pheramone_init = 0.1;
        
        ## Amount of iterations that is used for solving
        self.iterations = 50;
        
        ## Amount of ants that is used on each iteration
        self.count_ants = 20;


class antmean:
    """!
    @brief The ant colony clustering algorithm is a swarm-intelligent method used for clustering problems that is inspired 
           by the behavior of ant colonies that cluster their corpses and sort their larvae.
    
    @details
    
    Code example:
    @code
        # Define ant-colony parameters
        params = antmean_clustering_params();
        params.iterations = 300;
        params.count_ants = 200;
        params.pheramone_init = 0.1;
        params.ro = 0.9;
        
        # Read data from text file
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        
        # Create instance of the algorithm
        algo = antmean(sample, 3, params);
        
        # Start clustering process
        algo.process();
        
        # Obtain allocated clusters by the colony
        res = algo.get_clusters();
        
        # Display output result (allocated clusters)
        print(res);
    @endcode
    
    """
    
    def __init__(self, sample, count_clusters, parameters):
        """!
        @brief Construct ant mean clustering algorithm using colony parameters.
        @details This algorithm is implemented on core side only (C/C++ part of the library).
        
        @warning Ant-Mean is working using core of the library - CCORE.
        
        @param[in] sample (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] count_clusters (uint): Amount of clusters that should be allocated.
        @param[in] parameters (antmean_clustering_params): Ant colony parameters.
        
        """
        
        self.__parameters = parameters if parameters is not None else antmean_clustering_params();
        self.__clusters = [];
        self.__sample = sample;
        self.__count_clusters = count_clusters;


    def process(self):
        """!
        @brief Performs cluster analysis using ant-mean colony.
        
        @see get_clusters
        
        """
        
        self.__clusters = wrapper.antmean_clustering_process(self.__parameters, self.__count_clusters, self.__sample);


    def get_clusters(self):
        """!
        @brief Returns allocated clusters after processing.
        
        @see process
        
        """
        return self.__clusters;
