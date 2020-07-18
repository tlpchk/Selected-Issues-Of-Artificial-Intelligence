import math
from abc import ABCMeta, abstractmethod

import numpy as np
from scipy import optimize
from six import add_metaclass


@add_metaclass(ABCMeta)
class ObjectiveFunction(object):

    def __init__(self, name, dim, min_value, max_value):
        self.name = name
        self.dim = dim
        self.min = min_value
        self.max = max_value

    def __call__(self, x):
        return self.evaluate(x)

    def sample(self):
        return np.random.uniform(low=self.min, high=self.max, size=self.dim)

    @abstractmethod
    def evaluate(self, x):
        pass


def get_objective(objective, dimension=30):
    objectives = {'Sphere': Sphere(dimension),
                  'Rastrigin': Rastrigin(dimension),
                  'Rosenbrock': Rosenbrock(dimension),
                  'Ackley' : Ackley(dimension)}
    return objectives[objective]


class Rastrigin(ObjectiveFunction):
    def __init__(self, dim, min_value=-5.12, max_value=5.12):
        super(Rastrigin, self).__init__('Rastrigin', dim, min_value, max_value)

    def evaluate(self, x):
        assert len(x) == self.dim
        return 10 * self.dim + np.sum(np.power(x, 2) - 10 * np.cos(2 * np.pi * np.array(x)))


class Sphere(ObjectiveFunction):

    def __init__(self, dim):
        super(Sphere, self).__init__('Sphere', dim, -100.0, 100.0)

    def evaluate(self, x):
        return sum(np.power(x, 2))


class Rosenbrock(ObjectiveFunction):

    def __init__(self, dim):
        super(Rosenbrock, self).__init__('Rosenbrock', dim, -30.0, 30.0)

    def evaluate(self, x):
        return optimize.rosen(x)


class Ackley(ObjectiveFunction):

    def __init__(self, dim):
        super(Ackley, self).__init__('Ackley', dim, -30.0, 30.0)

    def evaluate(self, x):
        a = 20
        b = 0.2
        c = 2 * math.pi
        sum_sq_term = -a * np.exp(-b * np.sqrt(np.power(x, 2).mean()))
        cos_term = -np.exp((np.cos(c * x).mean()))
        return a + np.exp(1) + sum_sq_term + cos_term