import random;


class random_center_initializer:
    def __init__(self, data, amount_centers):
        self.__data = data;
        self.__amount = amount_centers;


    def initialize(self):
        return [ self.__create_center() for _ in range(len(self.__amount)) ];


    def __create_center(self):
        return [ random.random() for _ in range(len(self.__data[0])) ];


class kmeans_plusplus_initializer:
    def __init__(self, data, amount_centers):
        self.__data = data;
        self.__amount = amount_centers;


    def initialize(self):
        """
        kmeans++ method for center initialization;
        
        """
        return None;