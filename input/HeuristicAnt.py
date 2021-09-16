import numpy as np

from BaseAnt import BaseAnt


class HeuristicAnt(BaseAnt):

    def __init__(self, tsp_matrix):
        super().__init__(tsp_matrix, np.zeros(tsp_matrix.shape))

    def get_next_move(self):
        """Return the index to go next"""
        # Wähle die Bewegung die die geringste Distanz aufweist
        available_moves = self.get_remaining_cities(self.route)
        temp = []
        for i in available_moves:
            temp.append(self.tsp_matrix[self.position][i])
        index = temp.index(min(temp))
        return tuple(available_moves)[index]

    # Kopie aus AntColonyOptimization
    def get_route_length(self, route):
        """For a given route return the route's length."""
        route_length = 0
        for j in range(0, len(route) - 1):
            start = route[j]
            end = route[j + 1]
            route_length = route_length + self.tsp_matrix[start][end]
        return route_length
