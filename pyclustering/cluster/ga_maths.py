
import numpy as np


class GAMath:
    """
    """

    @staticmethod
    def get_centres(chromosomes, data, count_clusters):
        """ """

        # Initialize centres
        centres = np.zeros((len(chromosomes), count_clusters, len(data[0])))

        # Calc centers for next chromosome
        for _idx in range(len(chromosomes)):
            centres[_idx] = GAMath.calc_centers_for_chromosome(chromosomes[_idx], data, count_clusters)

        return centres

    @staticmethod
    def calc_centers_for_chromosome(chromosome, data, count_clusters):
        """ """

        # Initialize centers
        centers = np.zeros((count_clusters, len(data[0])))

        # Next cluster
        for _idx_cluster in range(count_clusters):
            centers[_idx_cluster] = GAMath.calc_center(chromosome, data, _idx_cluster)

        return centers

    @staticmethod
    def calc_center(chromosome, data, cluster_num):
        """ """

        # Initialize center
        center = np.zeros(len(data[0]))

        # Get count data in clusters
        count_data_in_cluster = 0

        # Next data point
        for _idx in range(len(chromosome)):

            # If data associated with current cluster
            if chromosome[_idx] == cluster_num:
                center += data[_idx]
                count_data_in_cluster += 1

        # If has no data in cluster
        if count_data_in_cluster == 0:
            return center

        # Normalize center
        center /= count_data_in_cluster

        return center

    @staticmethod
    def calc_probability_vector(fitness):
        """  """

        if len(fitness) == 0:
            raise AttributeError("Has no any fitness functions.")

        # Get 1/fitness function
        inv_fitness = np.zeros(len(fitness))

        #
        for _idx in range(len(inv_fitness)):

            if fitness[_idx] != 0.0:
                inv_fitness[_idx] = 1.0 / fitness[_idx]
            else:
                inv_fitness[_idx] = 0.0

        # Initialize vector
        prob = np.zeros(len(fitness))

        # Initialize first element
        prob[0] = inv_fitness[0]

        # Accumulate values in probability vector
        for _idx in range(1, len(inv_fitness)):
            prob[_idx] = prob[_idx - 1] + inv_fitness[_idx]

        # Normalize
        prob /= prob[-1]

        GAMath.set_last_value_to_one(prob)

        return prob

    @staticmethod
    def set_last_value_to_one(probabilities):
        """!
        @brief Update the last same probabilities to one.
        @details All values of probability list equals to the last element are set to 1.
        """

        # Start from the last elem
        back_idx = - 1

        # All values equal to the last elem should be set to 1
        last_val = probabilities[back_idx]

        # for all elements or if a elem not equal to the last elem
        for _idx in range(-1, -len(probabilities) - 1):
            if probabilities[back_idx] == last_val:
                probabilities[back_idx] = 1
            else:
                break

    @staticmethod
    def get_uniform(probabilities):
        """!
        @brief Returns index in probabilities.

        @param[in] probabilities (list): List with segments in increasing sequence with val in [0, 1],
                   for example, [0 0.1 0.2 0.3 1.0].
        """

        # Initialize return value
        res_idx = None

        # Get random num in range [0, 1)
        random_num = np.random.rand()

        # Find segment with  val1 < random_num < val2
        for _idx in range(len(probabilities)):
            if random_num < probabilities[_idx]:
                res_idx = _idx
                break

        if res_idx is None:
            print('Probabilities : ', probabilities)
            raise AttributeError("'probabilities' should contain 1 as the end of last segment(s)")

        return res_idx

