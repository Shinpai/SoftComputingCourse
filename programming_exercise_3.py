# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

PI = math.pi
ITER = 1000
PROB_CROSSOVER = 0.8
PROB_MUTATION = 0.06
POPULATION_SIZE = 10
KURI_CONST = 10 ** 9


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

        def f1(x, y):
            return (y - ((5.1 * x ** 2) / (4 * PI ** 2)) + ((5 * x) / PI) - 6) ** 2 + (10 - (10 / 8 * PI)) * math.cos(x) ** 2 + 9

        def f2(x, y):
            return y + (x - 12 / 1.2)
        
        satisfied = 0
        if f1(x, y) <= 0:
            satisfied += 1
        if f2(x, y) <= 0:
            satisfied += 1
        
        if satisfied > 0:
            return [True, satisfied]
        else:
            return [False, 0]

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
        self.size = len(self.individuals)

    def evaluate(self, mode, generation):
        for ind in self.individuals:
            ind.fitness = self.f(ind.x, ind.y)
            passed, satisfied = ind.constraints()
            if passed:
                pass
            elif mode == 'dp':
                ind.fitness = 0
            elif mode == 'static':
                ind.fitness = KURI_CONST - sum([KURI_CONST / 2 for _ in range(satisfied)])
            elif mode == 'dynamic':
                C = .5
                a = 1
                b = 2
                ind.fitness = ind.fitness + (C * generation) ** a * SVC(b, ind)

    def find_fittest(self):
        for ind in self.individuals:
            if ind.fitness < self.fittest.fitness:
                self.fittest = ind

    def tournament_select(self):
        '''  '''
        pool = self.individuals[:]
        pool = sorted(pool, key=lambda x: x.fitness)
        return pool.pop()

    def BQI_prob(self):
        rand = rng.random()
        n = 2  # distribution index
        if rand <= .5:
            return (2 * rand) ** (1 / n + 1)
        else:
            return (1 / (2 * (1 - rand))) ** (1 / n + 1)

    def rc_crossover(self, par1, par2):
        prob = self.BQI_prob()
        self.size += 1
        c_1 = Individual(self.size)
        c_1.fitness = .5 * ((1 + prob) * par1.fitness + (1 - prob) * par2.fitness)

        self.size += 1
        c_2 = Individual(self.size)
        c_2.fitness = .5 * ((1 - prob) * par1.fitness + (1 + prob) * par2.fitness)
        return [c_1, c_2]

    def f(self, x, y):
        return x + y

    def print_gen(self):
        for ind in self.individuals:
            ind.print_chr()

    def print_fittest(self):
        self.fittest.print_chr()


def RCGA(mode):
    pop = Population()
    pop.initialize_population()
    pop.fittest = pop.individuals[0]

    for generation in range(ITER):
        pop.evaluate(mode, generation)
        next_population = Population()
        while len(next_population.individuals) < len(pop.individuals):
            parent1 = pop.tournament_select()
            if rng.random() < PROB_CROSSOVER:
                parent2 = pop.tournament_select()
                child1, child2 = pop.rc_crossover(parent1, parent2)
                next_population.individuals.append(child1)
                next_population.individuals.append(child2)
            else:
                next_population.individuals.append(parent1)
            '''
            if rng.random() < PROB_MUTATION:
                target = next_population.tournament_select()
                mutated = pop.mutate(target)
                next_population.individuals.append(mutated)
            '''
        next_population.evaluate(mode, generation)
        next_population.individuals = sorted(next_population.individuals, key=lambda x: x.fitness)
        # choose the top 10 individuals for the next population
        pop.individuals = next_population.individuals[:10]
        pop.find_fittest()
        if generation % 100 == 0:
            pop.print_fittest()


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
    open('RCGA_result.dat', 'w').close()

    mode = 'dp'
    with open('RCGA_result.dat', 'a') as f:
        print(mode.upper(), file=f)
        print('#'*30, file=f)
    RCGA(mode)

    mode = 'static'
    with open('RCGA_result.dat', 'a') as f:
        print(mode.upper(), file=f)
        print('#'*30, file=f)
    RCGA(mode)

##############################################################################

if __name__ == "__main__":
    main()
