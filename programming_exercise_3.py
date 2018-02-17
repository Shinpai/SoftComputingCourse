# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

PI = math.pi
ITER = 1
PROB_CROSSOVER = 0.8
PROB_MUTATION = 0.06
POPULATION_SIZE = 10


class Individual:
    ''' Individual '''
    def __init__(self, num):
        self.num = num
        self.fitness = None
        self.x = rng.uniform(-5, 10)
        self.y = rng.uniform(0, 15)

    def constraints(self):
        x = self.x
        y = self.y

        if f1(x, y) <= 0 and f2(x, y) <= 0:
            return true
        return false

        def f1(x, y):
            return (y - ((5.1 * x ** 2) / (4 * PI ** 2)) + ((5 * x) / PI) - 6) ** 2 + (10 - (10 / 8 * PI)) * math.cos(x) ** 2 + 9

        def f2(x, y):
            return y + (x - 12 / 1.2)

    def print_chr(self):
        ''' Print info of an Individual '''
        with open('RCGA_result.dat', 'a') as f:
            print("#{} - fit {}\n ({}, {})\n".format(self.num, self.fitness,
                                                     self.x, self.y), file=f)


class Population:
    ''' Set of Individuals '''
    def __init__(self):
        self.individuals = []
        self.crossovers = 0
        self.mutations = 0
        self.fittest = None
        self.size = 0

    def initialize_population(self):
        ''' Initializes a population with size '''
        for i in range(POPULATION_SIZE):
            self.individuals.append(Individual(i))

    def evaluate(self, mode):
        for ind in self.individuals:
            ind.fitness = self.f(ind.x, ind.y)
            if mode == 'dp':
                if not ind.constraints:
                    ind.fitness = 0

    def tournament_select(self):
        '''  '''
        pool = self.individuals[:]
        pool = sorted(pool, key=lambda x: x.fitness)
        return pool.pop()

    def f(self, x, y):
        return x + y
    
    def print_gen(self):
        for ind in self.individuals:
            ind.print_chr()


def RCGA(mode):
    pop = Population()
    pop.initialize_population()
    for generation in range(ITER):
        pop.evaluate(mode)
        pop.print_gen()


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
    clear()
    RCGA('dp')

##############################################################################

if __name__ == "__main__":
    main()
