import random

import numpy as np


class Bat:
    def __init__(self, obj_function, f_min, f_max, loud_min, loud_max):
        self.obj_function = obj_function
        self.position = obj_function.sample()
        self.velocity = np.random.uniform(self.obj_function.min, self.obj_function.max, self.obj_function.dim)
        self.freq = np.random.uniform(f_min, f_max)
        self.rate = np.random.uniform(0, 1)
        self.loudness = np.random.uniform(loud_min, loud_max)
        self.t = 1

    def __str__(self):
        return "B(pos={}, vel={}, freq={}, rate={}, loud={})".format(
            self.position, self.velocity, self.freq, self.rate, self.loudness
        )


class BatAlgorithm:
    def __init__(self, obj_function, no_particles, f_min, f_max, loud_min, loud_max, alpha, gamma):
        self.obj_function = obj_function
        self.no_particles = no_particles
        self.f_min = f_min
        self.f_max = f_max
        self.loud_min = loud_min
        self.loud_max = loud_max
        self.alpha = alpha
        self.gamma = gamma
        self.dimensions = obj_function.dim
        self.particles = [Bat(obj_function, f_min, f_max, loud_min, loud_max) for _ in range(no_particles)]
        self.global_best_value = float('inf')
        self.global_best_position = obj_function.sample()
        self.set_global_best()
        self.optimality_tracking = []

    def set_global_best(self):
        for particle in self.particles:
            particle_value = self.obj_function(particle.position)
            if self.global_best_value > particle_value:
                self.global_best_value = particle_value
                self.global_best_position = particle.position.copy()

    def print_particles(self):
        for particle in self.particles:
            print(particle)

    def move_particles(self):
        for particle in self.particles:
            particle.freq = self.f_min + (self.f_max - self.f_min) * random.random()

            particle.velocity = particle.velocity + (self.global_best_position - particle.position) * particle.freq
            particle.position += particle.velocity

            x = particle.position.copy()

            if random.random() > particle.rate:
                x = self.global_best_position + np.random.uniform(-1, 1, self.dimensions) * self._avg_loudness() * 1e-6

            x += 1e-6 * np.random.uniform(-1, 1, self.dimensions)

            if random.random() < particle.loudness and self.obj_function(x) < self.global_best_value:
                particle.position = x

            particle.loudness = max(self.loud_min, self.alpha * particle.loudness)
            particle.rate = 0.01 * (1 - np.exp((-1) * self.gamma * particle.t))
            particle.t += 1

            if self.obj_function(particle.position) < self.global_best_value:
                self.global_best_position = particle.position.copy()
                self.global_best_value = self.obj_function(particle.position)
        self.optimality_tracking.append(self.global_best_value)

    def _avg_loudness(self):
        return sum(map(lambda particle: particle.loudness, self.particles)) / self.no_particles

    def optimize(self, no_iterations):
        for i in range(no_iterations):
            self.move_particles()
