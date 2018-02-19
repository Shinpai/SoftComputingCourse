# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt
import matplotlib.animation as animation

# @author Harri Juutilainen 02/2018
# OOP version PSO 
# working w/o printing for local

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
VMAX = 3
BOUNDS = [(-1, 2), (-1, 1)]
DIM = 2  # two variables
ITERATIONS = 2000
frames = []

fig, ax = plt.subplots()
ln, = plt.plot([], [], 'ro')


class Particle:
    def __init__(self, index):
        self.index = index
        self.position = [rng.uniform(BOUNDS[i][0],
                                     BOUNDS[i][1]) for i in range(DIM)]
        self.velocity = [rng.uniform(-VMAX, VMAX) for i in range(DIM)]

        self.fitness = 0.0
        self.pbest = self
        self.lbest = self

    def evaluate(self, x, y):
        '''
        Function to optimize (minimize),
        particles fitness set as function value,
        compares particle to its personal best after eval
        '''
        return math.cos(x) * math.cos(y) - (x / (y ** 2 + 1))

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
        vanha = [self.position[0], self.position[1]]

        # calculate new position with restrictions
        for i in range(DIM):
            self.position[i] += self.velocity[i]
            max_l = abs(BOUNDS[i][0] - BOUNDS[i][1])
            if self.position[i] > BOUNDS[i][0]:
                self.position[i] = BOUNDS[i][0] + (self.position[i] % max_l)
            elif self.position[i] < BOUNDS[i][1]:
                self.position[i] = BOUNDS[i][1] - (self.position[i] % max_l)

        uusi = [self.position[0], self.position[1]]

        vanha_f = self.evaluate(vanha[0], vanha[1])
        uusi_f = self.evaluate(uusi[0], uusi[1])
        # check if old pos is better than new
        if vanha_f < uusi_f:
            self.position = vanha
        else:
            self.position = uusi

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
    
    def compare_lbest(self, particle, p, n):
        ''' Compare particle value to neighboring particles '''
        best_fit = min([particle.fitness, p.fitness, n.fitness])
        lbest = [x for x in [particle, p, n] if x.fitness == best_fit]
        return lbest.pop()

    def print_gen(self, index, mode, file):
        ''' prints out the necessary info for a generation '''
        print("ITERS:{}\n* {} {} \n* ({},{})\n".format(
            index, mode, round(self.gbest.fitness, 3),
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
            particle.fitness = particle.evaluate(particle.position[0],
                                                 particle.position[1])
            particle.compare_pbest()
            # 4 compare value to global/local best value
            swarm.compare_gbest(particle)
            if mode == 'global':
                kohde = swarm.gbest
            elif mode == 'local':
                indeksi = swarm.particles.index(particle)
                if indeksi != 0 and indeksi < len(swarm.particles) - 1:
                    prev_ = swarm.particles[indeksi - 1]
                    next_ = swarm.particles[indeksi + 1]
                    lbest = swarm.compare_lbest(particle, prev_, next_)
                    particle.lbest = lbest
                    prev_.lbest = lbest
                    next_.lbest = lbest
                    kohde = lbest
                else:
                    kohde = particle
            # 5 update velocity ..
            particle.update_velocity(kohde)
            # 6 .. and position for particle
            particle.move()
        # print defined levels of iteration
        # if i == 100 or i == ITERATIONS:
        if i == 100 or i == ITERATIONS:
            with open('PSO_result.dat', 'a') as f:
                swarm.print_gen(i, mode, f)
        if i % 20 == 0:
            make_frame(swarm, mode)
        i += 1


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


def make_frame(swarm, mode):
    # *-* EXTRA *-* #
    ''' Create a snapshot of swarm particle positions '''
    x = [par.position[0] for par in swarm.particles]
    y = [par.position[1] for par in swarm.particles]
    frame = [x, y, mode]
    frames.append(frame)


def init():
    ax.set_xlim(-2, 3)
    ax.set_ylim(-2, 2)
    return ln,


def update(counter):
    if counter == len(frames) - 1:
        exit(0)
    counter += 1
    x = frames[counter][0]
    y = frames[counter][1]
    plt.title(frames[counter][2])
    ln.set_data(x, y)
    return ln,


def main():
    clear()
    # clear result file
    open('PSO_result.dat', 'w').close()
    # global
    PSO_global('global')
    # local
    PSO_global('local')

    ani = animation.FuncAnimation(fig, update, init_func=init, frames=len(frames), interval=60, repeat=True)
    ani.save('pso.mp4')
    plt.show()

##############################################################################

if __name__ == "__main__":
    main()
