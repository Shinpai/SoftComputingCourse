# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri Juutilainen 02/2018

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
VMAX = 3
BOUNDS = [(-1, 2), (-1, 1)]
DIM = 2  # two variables
ITERATIONS = 2000


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

        # check to see if particle is at personal best fitness
        self.compare_pbest()

    def compare_pbest(self):
        '''
        Check if particle is at pb fitness
        '''
        if self.fitness < self.pbest.fitness:
            self.pbest = self
        else:
            self = self.pbest

    def update_velocity(self, v_kohde):
        ''' Updates the velocity of a particle with weighted factors '''
        for i in range(DIM):
            p_1 = self.velocity[i]
            # accelerate towards personal best
            p_2 = ACC_CONST * rng.random() * (self.pbest.position[i] - self.position[i])
            # accelerate towards local or global best
            p_3 = ACC_CONST * rng.random() * (v_kohde.position[i] - self.position[i])

            new = p_1 + p_2 + p_3
            self.velocity[i] = max(-VMAX, min(VMAX, new))

    def move(self):
        ''' Update the position of a particle '''
        for i in range(DIM):
            self.position[i] += self.velocity[i]
            # constraints for movement
            # BOUNDS = [(-1, 2), (-1, 1)]
            max_l = abs(BOUNDS[i][1] - BOUNDS[i][0])
            if self.position[i] > BOUNDS[i][1]:
                self.position[i] = BOUNDS[i][1] - (self.position[i] % max_l)
            elif self.position[i] < BOUNDS[i][0]:
                self.position[i] = BOUNDS[i][0] + (self.position[i] % max_l)

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
    gbest = None

    def __init__(self):
        self.particles = []
        self.initialize_swarm()

    def initialize_swarm(self):
        ''' Initializes a swarm with particles '''
        for i in range(POPULATION_SIZE):
            self.particles.append(Particle(i))
        # set first as initial best
        self.gbest = self.particles[0]

    def compare_gbest(self, particle):
        ''' Compare particle value to best value of swarm '''
        if particle.fitness < self.gbest.fitness:
            self.gbest = particle

    def compare_lbest(self, particle, p, n):
        ''' Compare particle value to neighboring particles '''
        local_best = particle.lbest
        if particle.fitness < local_best.fitness:
            local_best = particle
        elif p.fitness < local_best.fitness:
            local_best = p
        elif n.fitness < local_best.fitness:
            local_best = n
        particle.lbest = local_best

    def print_gen(self, index, mode, file):
        ''' prints out the necessary info for a generation '''
        if mode == 'global':
            print('\nRESULT\n', '-'*7, file=file)
            print('iterations      : ', index, file=file)
            print(mode + ' fitness   : ', str(round(self.gbest.fitness, 3)), file=file)
            print(mode + ' X         : ', str(self.gbest.position[0]), file=file)
            print(mode + ' Y         : ', str(self.gbest.position[1]), file=file)
        else:
            min_l = Particle(-1)
            for par in self.particles:
                if par.lbest.fitness < min_l.lbest.fitness:
                    min_l = par
            print('\nRESULT\n', '-'*7, file=file)
            print(mode + ' fitness   : ', str(round(min_l.fitness, 3)), file=file)
            print(mode + ' X    : ', str(min_l.position[0]), file=file)
            print(mode + ' Y    : ', str(min_l.position[1]), file=file)
            print('iterations      : ', index, file=file)


def PSO_global(mode):
    '''
    Main PSO loop for global scheme
    '''
    # 1 initialize a swarm of particles
    swarm = Swarm()
    frames = []
    v_kohde = None
    i = 0
    while (i < ITERATIONS):
        for particle in swarm.particles:
            # 2,3 Evaluate particle fitness and compare to pb
            particle.evaluate()
            # 4 compare value to global best value ..
            swarm.compare_gbest(particle)
            # 5 update velocity ..
            particle.update_velocity(swarm.gbest)
            # 6 .. and position for particles
            particle.move()
        i += 1

        # *-* EXTRA *-* #
        # make a snapshot for visualisation, every n gens
        if i % 20 == 0:
            frames.append(make_frame(swarm))
        # print defined levels of iteration
        if i == 100 or i == ITERATIONS:
            with open('result.dat', 'a') as f:
                swarm.print_gen(i, 'local', f)
    return frames


def PSO_local(mode):
    '''
    Main PSO loop for local scheme
    '''
    # 1 initialize a swarm of particles
    swarm = Swarm()
    frames = []
    v_kohde = None
    i = 0
    while (i < ITERATIONS):
        for particle in swarm.particles:
            # 2,3 Evaluate particle fitness and compare to pb
            particle.evaluate()
            # 4 compare value to local best value ..
            if i != 0 and i < len(swarm.particles) - 1:
                prev = swarm.particles[i - 1]
                next = swarm.particles[i + 1]
                swarm.compare_lbest(particle, prev, next)
            # 5 update velocity ..
            particle.update_velocity(particle.lbest)
            # 6 .. and position for particles
            particle.move()
        i += 1

        # *-* EXTRA *-* #
        # make a snapshot for visualisation, every n gens
        if i % 20 == 0:
            frames.append(make_frame(swarm))
        # print defined levels of iteration
        if i == 100 or i == ITERATIONS:
            with open('result.dat', 'a') as f:
                swarm.print_gen(i, 'local', f)
    return frames


def make_frame(swarm):
    # *-* EXTRA *-* #
    ''' Create a snapshot of swarm particle positions '''
    x = [par.position[0] for par in swarm.particles]
    y = [par.position[1] for par in swarm.particles]
    frame = (x, y)
    return frame


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


def animate(frames, mode):
    # *-* EXTRA *-* #
    ''' Animate snapshots of the swarm with plt '''
    plt.ion()
    index = 0
    while index < len(frames):
        frame = frames[index]
        plt.title(str(index) + '/100, ' + mode)
        # draw particles - red
        plt.plot(frame[0], frame[1], 'ro')
        plt.axis([-1.5, 2.5, -1.5, 1.5])
        plt.pause(0.01)
        plt.clf()
        index += 1


def main():
    clear()
    drawing = True

    # global
    mode = 'global'
    frames = PSO_global(mode)
    # visualisation
    if drawing:
        animate(frames, mode)

    # local
    mode = 'local'
    # using a copy of the same initial swarm
    frames2 = PSO_local(mode)
    # visualisation
    if drawing:
        animate(frames2, mode)

##############################################################################

if __name__ == "__main__":
    main()