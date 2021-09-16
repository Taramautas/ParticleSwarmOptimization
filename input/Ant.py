import random

from BaseAnt import BaseAnt


class Ant(BaseAnt):

    def __init__(self, tsp_matrix, pheromone_matrix, alpha, beta):
        super().__init__(tsp_matrix, pheromone_matrix)
        self.alpha = alpha
        self.beta = beta

    def get_next_move(self):
        """Return the index to go next"""
        available_moves = self.get_remaining_cities(self.route)
        # TODO: Choose the next move according to the pheromone level and the visibility
        # Summe über Pheromonlevel und Sichtbarkeit aller noch nicht besuchten Kanten
        res = []
        temp_res = []
        for i in available_moves:
            temp_res.append((self.pheromone_matrix[self.position][i] ** self.alpha) *
                            ((1 / self.tsp_matrix[self.position][i]) ** self.beta))
        sum_all = sum(temp_res)
        # Wahrescheinlichkeit pro Element
        for i in temp_res:
            res.append(i / sum_all)
        # Auswahl eines der verfügaren Moves mit Hilfe der berechneten Wahrscheinlichkeiten
        return random.choices(population=tuple(available_moves), weights=res, k=1)[0]
