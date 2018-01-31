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

        self.current_value = None
        self.pbest = None

    def evaluate(self):
        ''' Function to optimize (or minimize) '''
        x = self.position[0]
        y = self.position[1]
        self.current_value = (math.cos(x) * math.cos(y) - (x / (y ** 2 + 1)))

    def compare_pbest(self):
        ''' marks down the personal best value of a particle '''
        if self.pbest is None:
            self.pbest = self.current_value
        if self.current_value < self.pbest:
            self.pbest = self.current_value

    def update_velocity(self, gbest):
        ''' randomly updates the velocity of a particle '''
        for i in range(DIMENSION):
            self.velocity[i] = self.velocity[i]
            + ACC_CONST * rng.random() * (self.pbest - self.current_value)
            + ACC_CONST * rng.random() * (gbest - self.current_value)

    def move(self):
        for i in range(DIMENSION):
            self.position[i] += self.velocity[i]

    def print_par(self):
        ''' Print info of a particle '''
        print('\nParticle #' + str(self.index) +
              '\n** (x, y) = ' + str(round(self.position[0], 3)) +
              ',' + str(round(self.position[1], 3)) +
              '\n** Velocity x = ' + str(round(self.velocity[0], 3)) +
              '\n** Velocity y = ' + str(round(self.velocity[1], 3)) +
              '\n** Current value = ' + str(round(self.current_value, 3)))


class Swarm:
    ''' Set of Particles '''
    def __init__(self):
        self.particles = []
        self.gbest = None

    def initialize_swarm(self):
        ''' Initializes a swarm with size '''
        for i in range(POPULATION_SIZE):
            self.particles.append(Particle(i))

    def compare_gbest(self, particle):
        '''  '''
        if self.gbest is None:
            self.gbest = particle.current_value
        if particle.current_value < self.gbest:
            self.gbest = particle.current_value

    def print_gen(self):
        ''' prints out the necessary info for a generation '''
        print('Swarm best: ' + str(round(min(i.pbest for i in self.particles), 3)))


def pso_gbest(ITERATIONS):
    swarm = Swarm()
    swarm.initialize_swarm()
    ITERATION = 0
    while(ITERATION < ITERATIONS):
        for particle in swarm.particles:
            # evaluate particle position with function
            particle.evaluate()
            # compare value to particles best local value
            particle.compare_pbest()
            # compare value to swarms best global value
            swarm.compare_gbest(particle)
            # update velocity
            particle.update_velocity(swarm.gbest)
            # update position
            particle.move()
        ITERATION += 1
    return round(swarm.gbest, 3)


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
    # record 100 and 2000 iterations with local and global, compare results
    ITERATIONS = 100
    tests = []
    for i in range(10):
        tests.append(pso_gbest(ITERATIONS))
    print('Test on ' + str(ITERATIONS) + ' iterations')
    for k in tests:
        print('Swarm best value = ' + str(k))
    
    ITERATIONS = 2000
    tests = []
    for i in range(10):
        tests.append(pso_gbest(ITERATIONS))
    print('Test on ' + str(ITERATIONS) + ' iterations')
    for k in tests:
        print('Swarm best value = ' + str(k))


##############################################################################

if __name__ == "__main__":
    main()
