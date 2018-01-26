# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

# Given parameters
LOWER_BOUND = 1.0
UPPER_BOUND = 5.0
POPULATION_SIZE = 10
BIT_SIZE = 8
PROB_CROSSOVER = 0.8
PROB_MUTATION = 0.06
ITERATIONS = 50


class Individual:
    ''' Individual '''
    def __init__(self, num, gene=None):
        self.gene = [gene]
        if gene is None:
            self.gene = [format(rng.getrandbits(16), '016b')]
        self.num = num
        self.fitness = None

    def print_chr(self):
        ''' Print info of an Individual '''
        print('#' + str(self.num) + ' ' + str(self.gene) + ' with func value ' + str(self.fitness))


class Population:
    ''' Set of Individuals '''
    def __init__(self):
        self.individuals = []
        self.crossovers = 0
        self.mutations = 0
        self.newPop = []
        self.size = 0

    def initialize_population(self):
        ''' Initializes a population with size '''
        for i in range(POPULATION_SIZE):
            self.individuals.append(Individual(i))
    
    def funktio(self, x_1, x_2):
        '''RETURN : function value with given parameters '''
        return x_1 + x_2 - (2 * x_1) ** 2 - x_2 ** 2 + (x_1 * x_2)

    def evaluate(self):
        ''' Calculates fitness for each individual '''
        pass

    def tournament_select(self):
        pass

    def sp_crossover(self, parent_1, parent_2):
        ''' Single point crossover, creates 2 children from parents'''
        self.crossovers += 1
        pass

    def mutate(self, ind):
        ''' Mutate bits randomly from given individuals GA string'''
        self.mutations += 1
        pass

    def flip_bins(self, gene):
        ''' Flips random bits from a bit string '''
        pass

    def print_gen(self):
        ''' Prints info of a population '''
        print('- Current generation -')
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


def minimize_ga():
    ''' Minimizes a function with 50 iterations '''
    pass


def main():
    clear()
    minimize_ga()

##############################################################################

if __name__ == "__main__":
    main()
