from abc import ABCMeta
from copy import deepcopy

import numpy as np
from six import add_metaclass

from si import ObjectiveFunction


@add_metaclass(ABCMeta)
class Bee(object):
    def __init__(self, obj_function: ObjectiveFunction):
        self.obj_function = obj_function
        self.dim = obj_function.dim
        self.min = obj_function.min
        self.max = obj_function.max
        self.pos = obj_function.sample()
        self.best_fitness = 0
        self.trial = 0

    def round_to_boundaries(self, pos):
        pos[pos > self.max] = self.max
        pos[pos < self.min] = self.min
        return pos

    def update_bee(self, pos, fitness):
        if self.best_fitness <= fitness:
            self.pos = pos
            self.best_fitness = fitness
            self.trial = 0
        else:
            self.trial += 1

    def reset_bee(self, max_trials=None):
        if max_trials is None or self.trial >= max_trials:
            self.pos = self.obj_function.sample()
            self.best_fitness = 0
            self.trial = 0

    def explore(self, max_trials):
        if self.trial <= max_trials:
            # i = np.random.randint(low=0, high=self.dim)
            # phi = np.random.uniform(low=-1, high=1)
            # n_pos = deepcopy(self.pos)
            # n_pos[i] = self.pos[i] + (self.pos[i] - self.obj_function.sample()[i]) * phi

            component = np.random.choice(self.pos)
            phi = np.random.uniform(low=-1, high=1, size=len(self.pos))
            n_pos = self.pos + (self.pos - component) * phi

            n_pos = self.round_to_boundaries(n_pos)
            n_fitness = self.fitness(n_pos)
            self.update_bee(n_pos, n_fitness)

    def fitness(self, pos):
        evaluation = self.obj_function(pos)
        return 1 / (1 + evaluation) if evaluation >= 0 else 1 + np.abs(evaluation)


class Employee(Bee):

    def __init__(self, obj_function: ObjectiveFunction):
        super().__init__(obj_function)


class Onlooker(Bee):
    def onlook(self, employees, max_trials):
        fintesses = np.array([e.best_fitness for e in employees])
        p = fintesses / sum(fintesses)

        candidate = np.random.choice(employees, p=p)
        self.pos, self.best_fitness = candidate.pos, candidate.best_fitness

        self.explore(max_trials)


class ABC(object):

    def __init__(self, obj_function, no_particles, max_trials=100):
        self.no_particles = no_particles
        self.obj_function = obj_function

        self.max_trials = max_trials

        self.optimal_solution = None
        self.optimality_tracking = []

        self.employee_bees = [Employee(self.obj_function)] * (self.no_particles // 2)
        self.onlooker_bees = [Onlooker(self.obj_function)] * (self.no_particles - len(self.employee_bees))

    def optimize(self, no_iterations):
        self.reset()
        for itr in range(no_iterations):
            self.employee_bees_phase()
            self.onlooker_bees_phase()

            self.update_optimal_solution()
            self.update_optimality_tracking()

            self.scout_bees_phase()

    def reset(self):
        self.optimal_solution = None
        self.optimality_tracking = []

    def employee_bees_phase(self):
        for bee in self.employee_bees:
            bee.explore(self.max_trials), self.employee_bees

    def onlooker_bees_phase(self):
        for bee in self.onlooker_bees:
            bee.onlook(self.employee_bees, self.max_trials),

    def scout_bees_phase(self):
        for bee in self.onlooker_bees + self.employee_bees:
            bee.reset_bee(self.max_trials)

    def update_optimal_solution(self):
        n_optimal_solution = min(self.onlooker_bees + self.employee_bees, key=lambda bee: bee.best_fitness)
        if not self.optimal_solution \
                or n_optimal_solution.best_fitness > self.optimal_solution.best_fitness:
            self.optimal_solution = deepcopy(n_optimal_solution)

    def update_optimality_tracking(self):
        evaluation = self.obj_function(self.optimal_solution.pos)
        self.optimality_tracking.append(evaluation)
