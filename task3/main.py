from copy import deepcopy

import matplotlib.pyplot as plt

import numpy as np
from si.ABC import ABC
from si.BAT import BatAlgorithm
from si.ObjectiveFunction import get_objective
from si.PSO import PSO


def simulate(optimizer, no_iterations=100, no_simulations=1, skip_first_ratio=0.05):
    origin_optimizer = optimizer
    itr = range(no_iterations)
    values = np.zeros(no_iterations)
    for _ in range(no_simulations):
        optimizer = deepcopy(origin_optimizer)
        optimizer.optimize(no_iterations)
        values += np.array(optimizer.optimality_tracking)

    values /= no_simulations

    i = int(skip_first_ratio * no_iterations)
    itr = itr[i:]
    values = values[i:]

    plt.plot(itr, values, lw=0.5, label=type(optimizer).__name__)
    plt.legend(loc='upper right')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
    plt.xticks(rotation=45)

    return values[-1]


def simulate_all(title, optimizers, no_simulations=10, no_iterations=100):
    plt.figure(figsize=(10, 7))
    plt.title(title)

    for optimizer in optimizers:
        simulate(optimizer, no_iterations, no_simulations)
    plt.show()


if __name__ == '__main__':
    no_particles = 30
    no_simulations = 10
    no_iterations = 100
    dimensions = 5

    obj_function_names = ['Rastrigin', 'Sphere', 'Rosenbrock', 'Ackley']

    for obj_function_name in obj_function_names:
        obj_function = get_objective(obj_function_name, dimensions)
        optimizers = [
            BatAlgorithm(obj_function, no_particles, f_min=0, f_max=2, loud_min=0, loud_max=100, alpha=0.9, gamma=0.9),
            ABC(obj_function, no_particles, max_trials=100),
            PSO(obj_function, no_particles, weight=0.5, phi_p=0.4, phi_g=0.9)
        ]
        simulate_all(obj_function_name, optimizers, no_simulations, no_iterations)
