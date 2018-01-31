# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
MAX_VELOC = 3
X_LOWER = -1
Y_LOWER = -1
X_UPPER = 2
Y_UPPER = 1
DIMENSION = 2  # two variables


class Particle:
    def __init__(self, index):
        self.index = index
        self.position = [rng.uniform(X_LOWER, X_UPPER),
                         rng.uniform(Y_LOWER, Y_UPPER)]
        self.velocity = [rng.uniform(0, MAX_VELOC) for i in range(DIMENSION)]

        self.fitness = 0.0
        self.pbest = 0.0

    def evaluate(self):
        ''' Function to optimize (minimize) '''
        x = self.position[0]
        y = self.position[1]
        self.fitness = (math.cos(x) * math.cos(y) - (x / (y ** 2 + 1)))

    def compare_pbest(self):
        ''' marks down the personal best value of a particle '''        
        if self.fitness < self.pbest:
            self.pbest = self.fitness

    def update_velocity(self, gbest):
        ''' randomly updates the velocity of a particle '''
        for i in range(DIMENSION):
            self.velocity[i] = self.velocity[i]
            + ACC_CONST * rng.random() * (self.pbest - self.position[i])
            + ACC_CONST * rng.random() * (gbest - self.position[i])

    def move(self):
        self.position = self.position + self.velocity

    def print_par(self):
        ''' Print info of a particle '''
        print('\nParticle #' + str(self.index) +
              '\n** (x, y) = ' + str(round(self.position[0], 3)) +
              ',' + str(round(self.position[1], 3)) +
              '\n** Velocity x = ' + str(round(self.velocity[0], 3)) +
              '\n** Velocity y = ' + str(round(self.velocity[1], 3)) +
              '\n** Current value = ' + str(round(self.fitness, 3)))


class Swarm:
    ''' Set of Particles '''
    def __init__(self):
        self.particles = []
        self.gbest = 0.0
        self.gbest_pos = 0.0

    def initialize_swarm(self):
        ''' Initializes a swarm with size '''
        for i in range(POPULATION_SIZE):
            self.particles.append(Particle(i))

    def compare_gbest(self, particle):
        ''' Compare value to best of swarm '''
        if particle.fitness < self.gbest:
            self.gbest = particle.fitness
            self.gbest_pos = particle.position

    def compare_lbest(self, particle):
        ''' Compare value to neighboring particles '''
        if particle.index > 2:
            n1 = self.particles[particle.index - 1]
            n2 = self.particles[particle.index + 1]
            if self.lbest is None:
                self.lbest = particle.fitness
            if particle.fitness < self.lbest:
                self.lbest = particle.fitness

    def print_gen(self, index):
        ''' prints out the necessary info for a generation '''
        print('\nRESULTS\n', '-'*7)
        print('gbest fitness   : ', str(round(self.gbest, 3)))
        print('gbest params    : ', str(self.gbest_pos))
        print('iterations      : ', index)


def PSO(ITERATIONS, index, mode):
    swarm = Swarm()
    swarm.initialize_swarm()
    for particle in swarm.particles:
        # evaluate particle position with function
        particle.evaluate()
        if mode == 'gbest':
            # compare value to populations best value
            particle.compare_pbest()
        else:
            # compare value to best neighboring particle
            swarm.compare_lbest(particle)
        # compare value to swarms best global value
        swarm.compare_gbest(particle)
        # update velocity
        particle.update_velocity(swarm.gbest)
        # update position
        particle.move()
    if index == 100 or index == ITERATIONS:
        swarm.print_gen(index)


def clear():
    '''
    Tyhjää konsolin
    '''
    name = os.name
    if name == 'posix':
        os.system('clear')
    elif name == 'nt' or name == 'dos':
        os.system('cls')
    else:
        print("\n" * 30)


def main():
    clear()
    ITERATIONS = 2000
    mode = 'gbest'
    for i in range(ITERATIONS + 1):
        PSO(ITERATIONS, i, mode)

##############################################################################

if __name__ == "__main__":
    main()
