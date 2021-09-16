import random

import numpy as np


class ProblemGenerator(object):

    def get_distance_matrix(self, cities):
        matrix = np.zeros((cities, cities))
        for i in range(cities):
            for j in range(cities):
                if i != j:
                    val = int(random.uniform(1, 1001))
                    matrix[i][j] = val
                    matrix[j][i] = val
        return matrix
