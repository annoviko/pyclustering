"""!

@brief Colors used by pyclustering library for visualization.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


class color:
    """!
    @brief Consists titles of colors that are used by pyclustering for visualization.
    
    """

    @staticmethod
    def get_color(sequential_index):
        """!
        @brief Returns color using round robin to avoid out of range exception.

        @param[in] sequential_index (uint): Index that should be converted to valid color index.

        @return (uint) Color from list color.TITLES.

        """
        return color.TITLES[sequential_index % len(color.TITLES)]


    ## List of color titles that are used by pyclustering for visualization.
    TITLES = [  'red', 'blue', 'darkgreen', 'gold', 'violet', 
                'deepskyblue', 'darkgrey', 'lightsalmon', 'deeppink', 'yellow',
                'black', 'mediumspringgreen', 'orange', 'darkviolet', 'darkblue',
                'silver', 'lime', 'pink', 'brown', 'bisque',
                'dimgray', 'firebrick', 'darksalmon', 'chartreuse', 'skyblue',
                'purple', 'fuchsia', 'palegoldenrod', 'coral', 'hotpink',
                'gray', 'tan', 'crimson', 'teal', 'olive']
