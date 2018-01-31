# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
MAX_VELOC = 3
X_LOWER, Y_LOWER = -1
X_UPPER = 2
Y_UPPER = 1
DIMENSION = 2  # two variables


class Particle:
    def __init__(self, index):
        self.index = index
        self.position = [rng.uniform(X_LOWER, X_UPPER),
                         rng.uniform(Y_LOWER, Y_UPPER)]
        self.velocity = [rng.uniform(0, MAX_VELOC) for i in range(DIMENSION)]

        self.current_value = self.evaluate(self.x, self.y)
        self.pbest = []

    def evaluate(self, x, y):
        ''' Function to optimize (or minimize) '''
        return math.cos(x) * math.cos(y) - (x / (y ** 2 + 1))

    def compare_pbest(self):
        if self.pbest is None:
            self.pbest = self.current_value
        elif self.current_value < self.pbest:
                self.pbest = self.current_value

    def update_velocity(self):
        pass

    def print_par(self):
        ''' Print info of a particle '''
        print('\nParticle #' + str(round(self.index, 2)) +
              '\n** (x, y) = ' + str(round(self.x, 2)), str(round(self.y, 2)) +
              '\n** Velocity = ' + str(round(self.velocity, 2)) +
              '\n** Current value = ' + str(round(self.current_value, 2)))


class Swarm:
    ''' Set of Particles '''
    def __init__(self):
        self.particles = []
        self.gbest = None

    def initialize_swarm(self):
        ''' Initializes a swarm with size '''
        for i in range(POPULATION_SIZE):
            self.particles.append(Particle(i))

    def compare_gbest(particle):
        pass

    def print_gen(self):
        ''' '''
        print('Swarm best = ' + self.gbest.print_par())


def pso_gbest():
    swarm = Swarm()
    swarm.initialize_swarm()
    while (ITERATIONS > 0):
        for particle in swarm.particles:
            # evaluate particle position with function
            particle.evaluate()
            # compare value to particles best local value
            particle.compare_pbest()
            # compare value to swarms best global value
            swarm.compare_gbest(particle)
            # update velocity
            particle.update_velocity()
            # update position
            particle.move()
            # print info
            swarm.print_gen()
        ITERATIONS -= 1


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
    '''
    FRAMEWORK GBEST model
    1. Initialize an array of particles with random positions and velocities on D dimensions, 
    2. Evaluate the desired minimization function in D variables, 
    3. Compare evaluation with particle’s previous best value (PBEST[]): 
            If current value < PBEST[] then PBEST[] = current value and PBESTx[][d] = current position in D- dimensional hyperspace, 
    4. Compare evaluation with group’s previous best (PBEST[GBEST]): 
            If current value < PBESTCGBEST] then GBEST=particle’s array index, 
    5. Change velocity by the following formula:
            W[dI = W[dI + ACC-CONST*rand()*(PBESTx[] [d] - PresentX[] [d]) + ACC-CONST*rand()*(PBESTx[GBEST] [d] - PresentX[l[d]),
    6. Move to PresentX[][d] + v[][d]: Loop to step 2 and repeat until a criterion is met.    
    '''
    clear()
    # record 100 and 2000 iterations with local and global, compare results
    ITERATIONS = 2000
    pso_gbest(ITERATIONS)

##############################################################################

if __name__ == "__main__":
    main()
