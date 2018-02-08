# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
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
        self.pbest_pos = []
        self.lbest = 0.0

    def evaluate(self):
        ''' Function to optimize (minimize) '''
        x = self.position[0]
        y = self.position[1]
        return math.cos(x) * math.cos(y) - (x / (y ** 2 + 1))

    def compare_pbest(self):
        '''
        Marks down the personal best value of a particle,
        moves to it if it is better than original
        '''
        # null check
        if self.pbest == 0.0 and self.pbest_pos == []:
            self.pbest = self.fitness
            self.pbest_pos = self.position
        # comparison
        if self.fitness < self.pbest:
            self.pbest = self.fitness
            self.pbest_pos = self.position
        else:
            self.fitness = self.pbest
            self.position = self.pbest_pos

    def update_velocity(self, vertailu):
        ''' Updates the velocity of a particle with weighted factors '''
        for i in range(DIM):
            # how much previous velocity affects new velocity
            part_1 = self.velocity[i]
            # accelerate towards personal best
            part_2 = ACC_CONST * rng.random() * (self.pbest - self.position[i])
            # accelerate towards local or global best
            part_3 = ACC_CONST * rng.random() * (vertailu - self.position[i])

            self.velocity[i] = part_1 + part_2 + part_3

    def move(self):
        ''' Update the position of a particle '''
        for i in range(DIM):
            self.position[i] = self.position[i] + self.velocity[i]
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
        ''' Compare particle value to best value of swarm '''
        # null check
        if self.gbest == 0.0 and self.gbest_pos == []:
            self.gbest = particle.fitness
            self.gbest_pos = particle.position
        # comparison
        if particle.fitness < self.gbest:
            self.gbest = particle.fitness
            self.gbest_pos = particle.position

    def compare_lbest(self, particle):
        ''' Compare particle value to neighboring particles '''
        indeksi = self.particles.index(particle)
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
                if par.lbest < min_l.lbest:
                    min_l = par
            print('\nRESULT\n', '-'*7)
            print(mode + ' fitness   : ', str(round(min_l.fitness, 3)))
            print(mode + ' X    : ', str(min_l.position[0]))
            print(mode + ' Y    : ', str(min_l.position[1]))
            print('iterations      : ', index)


def PSO(swarm, mode):
    frames = []
    i = 0
    while (i < ITERATIONS):
        # Main pso loop
        for particle in swarm.particles:
            # 2. Evaluate particle fitness
            particle.fitness = particle.evaluate()
            # 3. compare to personal best
            particle.compare_pbest()
            # 4. compare value to swarms best value
            if mode == 'gbest':
                swarm.compare_gbest(particle)
                vertailu = swarm.gbest
            # 4. or local best value
            else:
                swarm.compare_lbest(particle)
                vertailu = particle.lbest
            # 5. update velocity
            particle.update_velocity(vertailu)
            # 6. and position for particles
            particle.move()
        i += 1
        # *-* EXTRA *-* #
        # make a snapshot for visualisation, every 20 gens
        if i % 20 == 0:
            frames.append(make_frame(swarm))        
        # print defined levels of iteration
        if i == 100 or i == ITERATIONS:
            swarm.print_gen(i, mode)
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
    # initialize new swarm
    swarm = Swarm()
    swarm.initialize_swarm()
    swarm2 = swarm

    # global
    mode = 'gbest'
    frames = PSO(swarm, mode)
    # visualisation
    if drawing:
        animate(frames, mode)

    # local, using a copy of the same initial swarm
    mode = 'lbest'
    frames2 = PSO(swarm2, mode)
    # visualisation
    if drawing:
        animate(frames2, mode)

##############################################################################

if __name__ == "__main__":
    main()
