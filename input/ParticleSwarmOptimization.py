from matplotlib import pyplot as plt
from AntColonyOptimization import AntColonyOptimization
import random
from HeuristicAnt import HeuristicAnt
from Particle import Particle


class ParticleSwarmOptimization(object):

    def __init__(self, swarm_size, neighborhood_size, problem_size, iterations, number_of_ants, problem, position):
        self.swarm_size = swarm_size
        self.neighbourhood_size = neighborhood_size
        self.problem_size = problem_size
        self.iterations = iterations
        self.number_of_ants = number_of_ants
        self.particles = []
        self.problem = problem
        self.position = position


        # initialize particles with random numbers
        for i in range(self.swarm_size):
            alpha = random.uniform(0.1, 10)
            beta = random.uniform(0.1, 10)
            evaporation_rate = random.uniform(0, 1)
            position = {"alpha": alpha, "beta": beta, "evaporation_rate": evaporation_rate, "fitness": 0}

            particle = Particle(position)
            self.particles.append(particle)

        self.heuristic_length = 1
        heuristic_ant = HeuristicAnt(self.problem)
        heuristic_ant.move_to(self.position)
        for i in range(self.problem.shape[0] - 1):
            next_position = heuristic_ant.get_next_move()
            heuristic_ant.move_to(next_position)
        self.heuristic_length = heuristic_ant.get_route_length(heuristic_ant.route)

        self.tau0 = pow(self.problem_size * self.heuristic_length, -1)

    def run(self, pso_iterations):
        for i in range(pso_iterations):

            # Calculate fitness
            for p in self.particles:
                print("{} {} {}".format(p.position["evaporation_rate"], p.position["alpha"], p.position["beta"]))
                aco = AntColonyOptimization(self.problem, self.number_of_ants, self.tau0, p.position["evaporation_rate"], p.position["alpha"], p.position["beta"], self.heuristic_length,
                                            self.position)
                aco.run(self.iterations)
                eval_data = aco.eval_data
                heuristic_data = [self.heuristic_length] * len(aco.eval_data)
                print(sum(eval_data) / len(eval_data))

                p.position["fitness"] = sum(eval_data[-5:]) / len(eval_data[-5:])


            # update pbest
            for j, p in enumerate(self.particles):
                p.update_pbest()

            # get best neighbour
            for j, p in enumerate(self.particles):
                # look for best neighbour in social neighbourhood
                num_neighbours = int((self.neighbourhood_size * self.swarm_size) // 2)    # berechne die Anzahl der Nachbarn auf beiden Seiten
                neighbours = []
                # catching indexing out of bounds
                if j - num_neighbours < 0:
                    rest = int((j - num_neighbours))
                    neighbours += (self.particles[rest:])
                    neighbours += (self.particles[0:j])
                    if j + num_neighbours < len(self.particles):
                        neighbours += (self.particles[j:int(j + num_neighbours)])
                    else:
                        overflow = (j + num_neighbours) - len(self.particles)
                        neighbours += (self.particles[j:len(self.particles) - 1])
                        neighbours += (self.particles[0:overflow])
                elif j + num_neighbours >= len(self.particles):
                    neighbours += (self.particles[j - num_neighbours:j])
                    overflow = (j + num_neighbours) - len(self.particles)
                    neighbours += (self.particles[j:len(self.particles) - 1])
                    neighbours += (self.particles[0:overflow])
                else:
                    neighbours = self.particles[j - num_neighbours: j + num_neighbours]

                # find the best neighbour
                best_neighbour = neighbours[0]
                for n in neighbours:
                    if n.pbest["fitness"] < best_neighbour.pbest["fitness"]:
                        best_neighbour = n
                p.update_position_velocity(best_neighbour)


        pbest_data = [self.heuristic_length]
        pbest_label = ["heuristic"]

        self.particles = sorted(self.particles, key=lambda par: par.pbest["fitness"])
        print(self.particles[:5])

        top_5 = self.particles[:5]

        for p in top_5:
            pbest_data.append(p.pbest["fitness"])
            pbest_label.append("alpha: {:0.3f}\n beta: {:0.3f}\n eva_rate: {:0.3f}".format(p.pbest["alpha"], p.pbest["beta"], p.pbest["evaporation_rate"]))

        plt.bar(pbest_label, pbest_data)
        plt.show()