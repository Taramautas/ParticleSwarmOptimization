import random
from matplotlib import pyplot as plt
from ParticleSwarmOptimization import ParticleSwarmOptimization
from ProblemGenerator import ProblemGenerator

pso_iterations = 10
swarm_size = 20
neighborhood_size = 0.1
problem_size = 50
iterations = 25
number_of_ants = 25

random.seed(1)

problem = ProblemGenerator().get_distance_matrix(problem_size)
position = random.randint(0, problem.shape[0] - 1)


pso = ParticleSwarmOptimization(swarm_size, neighborhood_size, problem_size, iterations, number_of_ants, problem, position)
pso.run(pso_iterations)

fig, ax = plt.subplots()
group_names = []
group_data = []
for p in pso.particles:
    group_name_tuple = (p.pbest["alpha"], p.pbest["beta"], p.pbest["evaporation_rate"])
    group_names.append(group_name_tuple)
for p in pso.particles:
    group_data.append(p.pbest["fitness"])
print(len(group_names))
print(len(group_data))
group_names_strings = []
for gn in group_names:
    mystring = "alpha: {} beta: {} eva_rate: {}".format(gn[0], gn[1], gn[2])
    group_names_strings.append(mystring)

for i in range(len(group_data)):
    print("Parameter: {} Fitness: {}".format(group_names_strings[i], group_data[i]))
ax.barh(group_names_strings, group_data)
