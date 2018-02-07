# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = .1  # learning factor
MAX_VELOC = 3
BOUNDS = [(-1, 2), (-1, 1)]
DIM = 2  # two variables
ITERATIONS = 2000


class Particle:
    def __init__(self, index):
        self.index = index
        self.position = [rng.uniform(BOUNDS[i][0],
                                     BOUNDS[i][1]) for i in range(DIM)]
        self.velocity = [rng.uniform(0, MAX_VELOC) for i in range(DIM)]

        self.fitness = 0.0
        self.pbest = 0.0
        self.lbest = 0.0

    def evaluate(self):
        ''' Function to optimize (minimize) '''
        x = self.position[0]
        y = self.position[1]
        return math.cos(x) * math.cos(y) - (x / (y ** 2 + 1))

    def compare_pbest(self):
        ''' Marks down the personal best value of a particle '''
        if self.fitness < self.pbest:
            self.pbest = self.fitness

    def update_velocity(self, gbest, mode):
        ''' Updates the velocity of a particle with weighted factors '''
        for i in range(DIM):
            w = .2
            c1 = ACC_CONST
            c2 = ACC_CONST
            # how much previous velocity affects new velocity
            part_1 = self.velocity[i] * w
            # accelerate towards personal best
            part_2 = c1 * rng.random() * (self.pbest - self.position[i])
            # accelerate towards local or global best
            if mode == 'gbest':
                part_3 = c2 * rng.random() * (gbest - self.position[i])
            else:
                part_3 = c2 * rng.random() * (self.lbest - self.position[i])
            self.velocity[i] = part_1 + part_2 + part_3
            # constraints for velocity
            if self.velocity[i] > MAX_VELOC:
                self.velocity[i] = MAX_VELOC

    def move(self):
        ''' Update the position of a particle '''
        for i in range(DIM):
            self.position[i] = self.velocity[i]
            # constraints for movement
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
        self.gbest_pos = []

    def initialize_swarm(self):
        ''' Initializes a swarm with particles '''
        for i in range(POPULATION_SIZE):
            self.particles.append(Particle(i))

    def compare_gbest(self, particle):
        ''' Compare value to best value of swarm '''
        if self.gbest == 0.0 and self.gbest_pos == []:
            self.gbest = particle.fitness
            self.gbest_pos = particle.position
        if particle.fitness < self.gbest:
            self.gbest = particle.fitness
            self.gbest_pos = particle.position

    def compare_lbest(self, particle):
        ''' Compare value to neighboring particles '''
        indeksi = self.particles.index(particle)
        # while not including first and last particle
        if indeksi != 0 and indeksi != len(self.particles) - 1:
            n1 = self.particles[indeksi - 1]
            n2 = self.particles[indeksi + 1]
            local_best = min([particle.fitness, n1.fitness, n2.fitness])
            particle.lbest = local_best
            n1.lbest = local_best
            n2.lbest = local_best

    def print_gen(self, index, mode):
        ''' prints out the necessary info for a generation '''
        if mode == 'gbest':
            print('\nRESULT\n', '-'*7)
            print(mode + ' fitness   : ', str(round(self.gbest, 3)))
            print(mode + ' X    : ', str(self.gbest_pos[0]))
            print(mode + ' Y    : ', str(self.gbest_pos[1]))
            print('iterations      : ', index)
        else:
            min_l = Particle(-1)
            for par in self.particles:
                if min_l.lbest > par.lbest:
                    min_l = par
            print('\nRESULT\n', '-'*7)
            print(mode + ' fitness   : ', str(round(min_l.lbest, 3)))
            print(mode + ' X    : ', str(min_l.position[0]))
            print(mode + ' Y    : ', str(min_l.position[1]))
            print('iterations      : ', index)


def PSO(swarm, mode):
    frames = []
    i = 0
    while (i < ITERATIONS):
        # calculate fitness for particles
        # and set a personal best
        for particle in swarm.particles:
            particle.fitness = particle.evaluate()
            particle.compare_pbest()
        # compare value to populations best value
        if mode == 'gbest':
            swarm.compare_gbest(particle)
        # or compare value to best neighboring particle
        else:
            for particle in swarm.particles:
                swarm.compare_lbest(particle)
        # update velocity and position for particles
        for particle in swarm.particles:
            particle.update_velocity(swarm.gbest, mode)
            particle.move()
        # make a snapshot for visualisation
        if i % 20 == 0:
            frames.append(make_frame(swarm, mode))
        i += 1
        # print defined levels of iteration
        if i == 100 or i == ITERATIONS:
            swarm.print_gen(i, mode)
    return frames


def make_frame(swarm, mode):
    ''' Create a snapshot of swarm particle positions '''
    x = [par.position[0] for par in swarm.particles]
    y = [par.position[1] for par in swarm.particles]
    # mark best of swarm for snapshot
    if mode == 'gbest':
        z = swarm.gbest_pos[0]
        k = swarm.gbest_pos[1]
    else:
        z = 0
        k = 0
    frame = (x, y, z, k)
    return frame


def clear():
    ''' Clears the console '''
    name = os.name
    if name == 'posix':
        os.system('clear')
    elif name == 'nt' or name == 'dos':
        os.system('cls')
    else:
        print("\n" * 30)


def animate(frames, mode):
    ''' Animate snapshots of the swarm with plt '''
    plt.ion()
    plt.axis([-3, 3, -3, 3])
    index = 0
    while index < len(frames):
        frame = frames[index]
        plt.title(str(index) + '/100, ' + mode)
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
    drawing = True
    # initialize new swarm
    swarm = Swarm()
    swarm.initialize_swarm()

    mode = 'lbest'
    frames = PSO(swarm, mode)    
    # visualisation
    if drawing:
        animate(frames, mode)

    # initialize new swarm
    swarm = Swarm()
    swarm.initialize_swarm()

    mode = 'gbest'
    frames2 = PSO(swarm, mode)
    # visualisation
    if drawing:
        animate(frames2, mode)

##############################################################################

if __name__ == "__main__":
    main()
