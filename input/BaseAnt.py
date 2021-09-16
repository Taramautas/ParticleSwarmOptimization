from abc import ABCMeta, abstractmethod


class BaseAnt(object, metaclass=ABCMeta):
    def __init__(self, tsp_matrix, pheromone_matrix):
        self.tsp_matrix = tsp_matrix
        self.pheromone_matrix = pheromone_matrix
        self.position = None
        self.route = []

    @abstractmethod
    def get_next_move(self):
        """Return the index to go next"""
        pass

    def move_to(self, new_position):
        """Change the ant's position to new_position and append new_position to the ant's route"""
        self.position = new_position
        self.route.append(self.position)

    def reset_route(self):
        """Reset the ants route. Postcondition: The ant's route consists of its position"""
        self.route = [self.position]

    def get_remaining_cities(self, route):
        all_cities = set(range(0, self.tsp_matrix.shape[0]))
        return all_cities - set(route)
