import random

import numpy as np

from Ant import Ant
from EvaluationAnt import EvaluationAnt


class AntColonyOptimization(object):

    def __init__(self, tsp_matrix, number_of_ants, tau_null, evaporation_rate, alpha, beta, heuristic_length, position):
        self.tsp_matrix = tsp_matrix
        self.number_of_ants = number_of_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.heuristic_length = heuristic_length
        self.pheromone_matrix = np.full(tsp_matrix.shape, tau_null)
        np.fill_diagonal(self.pheromone_matrix, -1.0)
        self.ants = []

        self.eval_data = []
        self.position = position

    def run(self, iterations):
        self.setup_ants()

        # Setup der EvaluationAnt und erster Durchlauf
        eval_ant = EvaluationAnt(self.tsp_matrix, self.pheromone_matrix)
        eval_ant.move_to(self.position)
        for i in range(self.tsp_matrix.shape[0] - 1):
            next_position = eval_ant.get_next_move()
            eval_ant.move_to(next_position)
        self.eval_data.append(eval_ant.get_route_length(eval_ant.route))
        eval_ant.reset_route()

        for it in range(iterations):
            routes = []

            # Every ant ...
            for ant in self.ants:
                # constructs a route
                for i in range(self.tsp_matrix.shape[0] - 1):
                    next_position = ant.get_next_move()
                    ant.move_to(next_position)

                # Ant starts at the beginning again
                ant.move_to(ant.route[0])
                # Collect all routes
                routes.append(ant.route)
                # Delete old route
                ant.reset_route()

            # Apply global update role after each iteration
            self.apply_global_update(routes)

            # Füge neue beste Route der EvaluationAnt zu Daten hinzu
            for i in range(self.tsp_matrix.shape[0] - 1):
                next_position = eval_ant.get_next_move()
                eval_ant.move_to(next_position)
            self.eval_data.append(eval_ant.get_route_length(eval_ant.route))
            eval_ant.reset_route()

    def setup_ants(self):
        for m in range(self.number_of_ants):
            ant = Ant(self.tsp_matrix, self.pheromone_matrix, self.alpha, self.beta)
            # Place ants in a random city at first
            ant.move_to(random.randint(0, self.tsp_matrix.shape[0] - 1))
            self.ants.append(ant)

    def apply_global_update(self, routes):
        """TODO: Apply the global pheromone update for a given list of constructed routes including evaporation."""
        x, y = self.pheromone_matrix.shape
        # Berechnung der Summen der abgelegten Pheromone pro Zelle mit Hilfe der Routen
        delta_tau = np.zeros((x, y))
        for i in range(len(routes)):
            route_len = self.get_route_length(routes[i])
            for j in range(len(routes[i]) - 1):
                delta_tau[routes[i][j]][routes[i][j + 1]] += self.heuristic_length / route_len
        # Durchlaufe Pheromon Matrix und update die Mengen mit der delta_tau Matrix
        for i in range(x):
            for j in range(y):
                self.pheromone_matrix[i][j] = (1 - self.evaporation_rate) * self.pheromone_matrix[i][j] \
                                              + delta_tau[i][j]

    def get_route_length(self, route):
        """For a given route return the route's length."""
        route_length = 0
        for j in range(0, len(route) - 1):
            start = route[j]
            end = route[j + 1]
            route_length = route_length + self.tsp_matrix[start][end]
        return route_length
