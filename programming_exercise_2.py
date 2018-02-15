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

    def print_par(self):
        ''' Print info of a particle '''
        print("#{}\n({},{})\n({},{})\n{}".format(
            self.index, round(self.position[0], 3),
            round(self.position[1], 3), round(self.velocity[0], 3),
            round(self.velocity[1], 3), round(self.fitness, 3)
        ))


class Swarm:
    ''' Set of Particles '''
    def __init__(self):
        self.particles = []
        self.initialize_swarm()

    def initialize_swarm(self):
        ''' Initializes a swarm with random particles '''
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
        best_fit = min([particle.fitness, p.fitness, n.fitness])
        lbest = [x for x in [particle, p, n] if x.fitness == best_fit]
        return lbest.pop()

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
    frames = []
    i = 0
    while (i < ITERATIONS):
        for particle in swarm.particles:
            # 2,3 Evaluate particle fitness and compare to pb
            particle.evaluate()
            # 4 compare value to global best value
            swarm.compare_gbest(particle)
            old = particle
            # 5 update velocity ..
            particle.update_velocity(swarm.gbest)
            # 6 .. and position for particles
            particle.move()
            particle.evaluate()
            new = particle
            if old.fitness < new.fitness:
                particle = old
            else:
                particle = new
        i += 1
        # *-* EXTRA *-* #
        # make a snapshot for visualisation, every n gens
        if i % 20 == 0:
            frames.append(make_frame(swarm))
        # print defined levels of iteration
        if i == 100 or i == ITERATIONS:
            with open('result.dat', 'a') as f:
                swarm.print_gen(i, 'global', f)
    return frames


def PSO_local(mode):
    '''
    Main PSO loop for local scheme
    '''
    # 1 initialize a swarm of particles
    swarm = Swarm()
    frames = []
    i = 0
    while (i < ITERATIONS):
        for particle in swarm.particles:
            # 2,3 Evaluate particle fitness and compare to pb
            particle.evaluate()
            # 4 compare value to local best value ..
            if i != 0 and i < len(swarm.particles) - 1:
                prev = swarm.particles[i - 1]
                next = swarm.particles[i + 1]
                lbest = swarm.compare_lbest(particle, prev, next)
                prev.lbest = lbest
                next.lbest = lbest
                particle.lbest = lbest
            # 5 update velocity ..
            particle.update_velocity(particle.lbest)
            # 6 .. and position for particles
            particle.move()
        i += 1

        # *-* EXTRA *-* #
        # make a snapshot for visualisation, every 20 gens
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
    drawing = False
    # clear result file
    with open('result.dat', 'w') as f:
        f.write('')
    # global
    mode = 'global'
    frames = PSO_global(mode)
    # visualisation
    if drawing:
        animate(frames, mode)
    # local
    mode = 'local'
    frames2 = PSO_local(mode)
    # visualisation
    if drawing:
        animate(frames2, mode)


##############################################################################

if __name__ == "__main__":
    main()