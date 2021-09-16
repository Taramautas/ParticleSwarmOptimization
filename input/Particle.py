import random


class Particle():

    def __init__(self, position):
        self.position = position
        self.pbest = position
        self.velocity = {"alpha": 0, "beta": 0, "evaporation_rate": 0}



    def update_pbest(self):
        if self.position["fitness"] < self.pbest["fitness"]:
            self.pbest = self.position

    def update_position_velocity(self, neighbour):
        # randomize rs and rt
        rs = random.uniform(0.1, 1)
        rt = random.uniform(0.1, 1)

        # calculate velocity
        for key in self.velocity:
            self.velocity[key] = self.velocity[key] + rs * (self.pbest[key] - self.position[key]) + rt * (neighbour.pbest[key] - self.position[key])

        # calculate new position
        for key in self.velocity:
            self.position[key] = self.position[key] + self.velocity[key]