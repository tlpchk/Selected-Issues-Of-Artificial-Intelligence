import random

import numpy as np


class PSOParticle:
    def __init__(self, obj_function):
        self.position = obj_function.sample()
        self.velocity = np.random.uniform(-20, 20, obj_function.dim)
        self.best_value = float('inf')
        self.best_position = self.position

    def __str__(self):
        return f'I\'m at {self.position}, best position: {self.best_position}'

    def move(self):
        self.position += self.velocity


class PSO:
    def __init__(self, obj_function, no_particles, weight, phi_p, phi_g):
        self.obj_function = obj_function
        self.no_particles = no_particles
        self.weight = weight
        self.phi_p = phi_p
        self.phi_g = phi_g
        self.particles = [PSOParticle(self.obj_function) for _ in range(no_particles)]
        self.global_best_value = float('inf')
        self.global_best_position = np.random.uniform(-100, 100, obj_function.dim)
        self.optimality_tracking = []

        self.set_global_best()

    def print_particles(self):
        for particle in self.particles:
            print(particle)

    def set_global_best(self):
        for particle in self.particles:
            particle_value = self.obj_function(particle.position)
            particle.best_value = particle_value
            if self.global_best_value > particle_value:
                self.global_best_value = particle_value
                self.global_best_position = particle.position.copy()

    def move_particles(self):
        for particle in self.particles:
            velocity = self.weight * particle.velocity
            velocity += self.phi_p * random.random() * (particle.best_position - particle.position)
            velocity += self.phi_g * random.random() * (self.global_best_position - particle.position)
            particle.velocity = velocity
            particle.move()

            particle_value = self.obj_function(particle.position)
            if particle_value < particle.best_value:
                particle.best_value = particle_value
                particle.best_position = particle.position.copy()

                if particle_value < self.global_best_value:
                    self.global_best_value = particle_value
                    self.global_best_position = particle.position.copy()

    def optimize(self, iterations):
        for i in range(iterations):
            self.move_particles()
            self.optimality_tracking.append(self.global_best_value)
