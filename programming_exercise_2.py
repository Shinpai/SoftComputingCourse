# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
MAX_VELOC = 3
BOUNDS = [(-1, 2), (-1, 1)]
DIM = 2  # two variables
ITERATIONS = 100


class Particle:
    def __init__(self, index):
        self.index = index
        self.position = [rng.uniform(BOUNDS[0][0], BOUNDS[0][1]),
                         rng.uniform(BOUNDS[1][0], BOUNDS[1][1])]
        self.velocity = [rng.uniform(0, MAX_VELOC) for i in range(DIM)]

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
        for i in range(DIM):
            self.velocity[i] = self.velocity[i]
            + ACC_CONST * rng.random() * (self.pbest - self.position[i])
            + ACC_CONST * rng.random() * (gbest - self.position[i])
            if self.velocity[i] > MAX_VELOC:
                self.velocity[i] = MAX_VELOC

    def move(self):
        for i in range(DIM):
            self.position[i] = self.position[i] + self.velocity[i]

            if self.position[i] > BOUNDS[i][1]:
                self.position[i] = BOUNDS[i][1]
            if self.position[i] < BOUNDS[i][0]:
                self.position[i] = BOUNDS[i][0]

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

    def print_gen(self, index, mode):
        ''' prints out the necessary info for a generation '''
        print('\nRESULTS\n', '-'*7)
        print(mode + ' fitness   : ', str(round(self.gbest, 3)))
        print(mode + ' X    : ', str(self.gbest_pos[0]))
        print(mode + ' Y    : ', str(self.gbest_pos[1]))
        print('iterations      : ', index)


def PSO(swarm, mode):
    frames = []
    i = 0
    while (i < ITERATIONS):
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
        i += 1
        frames.append(make_frame(swarm))
        if i == 100 or i == ITERATIONS:
            swarm.print_gen(i, mode)
    return frames


def make_frame(swarm):
    x = [par.position[0] for par in swarm.particles]
    y = [par.position[1] for par in swarm.particles]
    z = swarm.gbest_pos[0]
    k = swarm.gbest_pos[1]
    frame = (x, y, z, k)
    return frame


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


def animate(frames):
    plt.ion()
    plt.axis([-3, 3, -3, 3])
    index = 0
    while index < len(frames):
        frame = frames[index]
        plt.title(index)
        # draw particles - red
        plt.plot(frame[0], frame[1], 'ro')
        # draw swarm best - blue
        plt.plot(frame[2], frame[3], 'bo')
        plt.axis([-1.5, 2.5, -1.5, 1.5])
        plt.pause(0.01)
        plt.clf()
        index += 1


def main():
    clear()
    drawing = False
    mode = 'gbest'
    swarm = Swarm()
    swarm.initialize_swarm()
    frames = PSO(swarm, mode)
    if drawing:
        # visualisaatio
        animate(frames)
    exit(0)

    mode = 'lbest'
    swarm = Swarm()
    swarm.initialize_swarm()
    frames = PSO(swarm, mode)
    if drawing:
        # visualisaatio
        animate(frames)

##############################################################################

if __name__ == "__main__":
    main()
