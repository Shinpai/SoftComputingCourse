# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri partuutilainen 02/2018
# functional version // not complete

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
VMAX = 3
BOUNDS = [(-1, 2), (-1, 1)]
DIM = 2  # two variables
ITERATIONS = 10


def func(pos):
        '''
        Function to optimize (minimize),
        particles fitness set as function value,
        compares particle to its personal best after eval
        '''
        x = pos[0]
        y = pos[1]
        return math.cos(x) * math.cos(y) - (x / (y ** 2 + 1))


def veloc(gbest, pbest, part):
    for i in range(DIM):
        p_1 = part['V'][i]
        p_2 = ACC_CONST * rng.random() * (pbest['pos'][i] - part['pos'][i])
        p_3 = ACC_CONST * rng.random() * (gbest['pos'][i] - part['pos'][i])
        part['V'][i] = max(-VMAX, min(VMAX, p_1 + p_2 + p_3))

    return part['V']


def move(pos, vel):
    for i in range(DIM):
        pos[i] += vel[i]
        max_l = abs(BOUNDS[i][1] - BOUNDS[i][0])
        if pos[i] > BOUNDS[i][1]:
            pos[i] = BOUNDS[i][1] #  - (part['pos'][i] % max_l)
        elif pos[i] < BOUNDS[i][0]:
            pos[i] = BOUNDS[i][0] # + (part['pos'][i] % max_l)
    return pos


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


def PSO():
    particle = {'pos': [0.0, 0.0],
                'V': [0.0, 0.0],
                'F': 0.0}
    swarm = [particle for _ in range(POPULATION_SIZE)]
    gbest = 0
    pbest = 0
    # lbest = swarm[0]
    for p in swarm:
        p['pos'] = [rng.uniform(-1, 2), rng.uniform(-1, 1)]
        p['F'] = func(p['pos'])
    n = 0
    while n < ITERATIONS:
        for i in range(POPULATION_SIZE):
            # EVAL
            current_val = func(swarm[i]['pos'])
            # PBEST
            if current_val < swarm[pbest]['F']:
                pbest = i
            # GBEST
            if current_val < swarm[gbest]['F']:
                gbest = i
            # VELOCITY
            swarm[i]['V'] = veloc(swarm[gbest], swarm[pbest], swarm[i])
            # MOVE
            swarm[i]['pos'] = move(swarm[i]['pos'], swarm[i]['V'])
        n += 1
        print(swarm[gbest]['F'])
        
    print('*'*30)
    print('X = ' + str(swarm[gbest]['pos'][0]))
    print('Y = ' + str(swarm[gbest]['pos'][1]))
    print('Val = ' + str(swarm[gbest]['F']))
    print('*'*30)


def main():
    clear()
    PSO()

##############################################################################

if __name__ == "__main__":
    main()