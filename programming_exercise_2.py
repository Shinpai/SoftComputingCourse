# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

# Given parameters
POPULATION_SIZE = 20
ACC_CONST = 2  # learning factor
MAX_VELOC = 3
# record 100 and 2000 iterations with local and global, compare results
ITERATIONS = 100


class Individual:
    ''' Individual '''
    def __init__(self):
        pass

    def print_chr(self):
        ''' Print info of an Individual '''
        pass


class Population:
    ''' Set of Individuals '''
    def __init__(self):
        pass

    def initialize_population(self):
        ''' Initializes a population with size '''
        pass
    
    def funktio(self, x_1, x_2):
        ''' Function to minimize '''
        pass

    def evaluate(self):
        '''  '''
        pass

    def tournament_select(self):
        pass

    def sp_crossover(self, parent_1, parent_2):
        ''' '''
        pass

    def mutate(self, ind):
        ''' '''
        pass

    def flip_bins(self, gene):
        ''' '''
        pass

    def print_gen(self):
        ''' '''
        pass


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
    pso_gbest()
    clear()

##############################################################################

if __name__ == "__main__":
    main()
