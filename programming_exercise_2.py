# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri Juutilainen 02/2018
# OOP version PSO // not complete

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
VMAX = 3
BOUNDS = [(-1, 2), (-1, 1)]
DIM = 2  # two variables
ITERATIONS = 10


class Particle:
    def __init__(self, index):
        self.index = index
        self.position = [rng.uniform(BOUNDS[i][0],
                                     BOUNDS[i][1]) for i in range(DIM)]
        self.velocity = [rng.uniform(-VMAX, VMAX) for i in range(DIM)]

        self.fitness = 0.0
        self.pbest = self
        self.lbest = self

    def evaluate(self):
        '''
        Function to optimize (minimize),
        particles fitness set as function value,
        compares particle to its personal best after eval
        '''
        x = self.position[0]
        y = self.position[1]
        self.fitness = math.cos(x) * math.cos(y) - (x / (y ** 2 + 1))

    def compare_pbest(self):
        '''
        Check if particle is at pb fitness
        '''
        if self.fitness < self.pbest.fitness:
            self.pbest = self

    def update_velocity(self, v_kohde):
        ''' Updates the velocity of a particle with weighted factors '''
        for i in range(DIM):
            p_1 = self.velocity[i]
            # accelerate towards personal best
            p_2 = ACC_CONST * rng.random() * (self.pbest.position[i] - self.position[i])
            # accelerate towards local or global best
            p_3 = ACC_CONST * rng.random() * (v_kohde.position[i] - self.position[i])
            self.velocity[i] = p_1 + p_2 + p_3

    def move(self):
        ''' Update the position of a particle '''
        for i in range(DIM):
            self.position[i] += self.velocity[i]

            max_len = abs(BOUNDS[i][0] - BOUNDS[i][1])
            if self.position[i] < BOUNDS[i][0]:
                self.position[i] = BOUNDS[i][0] + (self.position[i] % max_len)
            elif self.position[i] > BOUNDS[i][1]:
                self.position[i] = BOUNDS[i][1] - (self.position[i] % max_len)

    def print_par(self):
        ''' Print info of a particle '''
        print("#{}\nPOS ({},{})\nvalue: {}\n".format(
            self.index, round(self.position[0], 3),
            round(self.position[1], 3), round(self.fitness, 3)
        ))


class Swarm:
    ''' Set of Particles '''
    def __init__(self):
        self.particles = []
        self.gbest = None

    def initialize_swarm(self):
        ''' Initializes a swarm with random particles '''
        for i in range(POPULATION_SIZE):
            self.particles.append(Particle(i))

    def compare_gbest(self, particle):
        ''' Compare particle value to best value of swarm '''
        if particle.fitness < self.gbest.fitness:
            self.gbest = particle

    def print_gen(self, index, mode, file):
        ''' prints out the necessary info for a generation '''
        print("ITERS:{}\n* gbest {} \n* ({},{})\n".format(
            index, round(self.gbest.fitness, 3),
            self.gbest.position[0], self.gbest.position[1]
        ), file=file)


def PSO_global(mode):
    '''
    Main PSO loop for global scheme
    '''
    # 1 initialize a swarm of particles
    swarm = Swarm()
    swarm.initialize_swarm()
    swarm.gbest = swarm.particles[0]
    i = 0
    while (i < ITERATIONS):
        for particle in swarm.particles:
            # 2,3 Evaluate particle fitness and compare to pb
            particle.evaluate()
            particle.compare_pbest()
            # 4 compare value to global best value
            swarm.compare_gbest(particle)
            # 5 update velocity ..
            particle.update_velocity(swarm.gbest)
            # 6 .. and position for particle
            particle.move()
        i += 1
        # print defined levels of iteration
        if i == 100 or i == ITERATIONS:
            with open('result.dat', 'a') as f:
                swarm.print_gen(i, 'global', f)


def clear():
    # *-* EXTRA *-* #
    ''' Clears the console '''
    name = os.name
    if name == 'posix':
        os.system('clear')
    elif name == 'nt' or name == 'dos':
        os.system('cls')
    else:
        print("\n" * 30)


def main():
    clear()
    # clear result file
    with open('result.dat', 'w') as f:
        f.write('')
    # global
    mode = 'global'
    PSO_global(mode)

##############################################################################

if __name__ == "__main__":
    main()