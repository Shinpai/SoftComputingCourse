# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

# @author Harri Juutilainen 02/2018
# Real-coded GA with 3 different constraint handling methods

PI = math.pi
PROB_CROSSOVER = 0.8
PROB_MUTATION = 0.06
POPULATION_SIZE = 10
KURI_CONST = 10 ** 9


class Individual:
    '''
    Individual-object
    '''
    def __init__(self, num):
        self.num = num
        self.fitness = None
        self.x = rng.uniform(-5, 10)
        self.y = rng.uniform(0, 15)

    def constraints(self):
        '''
        Checks if constraints are met by the Individual
        returns the amount of satisfied constraints.
        RETURNS: [bool, int]
        '''
        x = self.x
        y = self.y

        satisfied = 0
        if self.f1(x, y) <= 0:
            satisfied += 1
        if self.f2(x, y) <= 0:
            satisfied += 1

        if satisfied > 0:
            return [True, satisfied]
        else:
            return [False, 0]

    def f1(self, x, y):
        '''
        Function for subjecting to constraints
        RETURNS: float
        '''
        p1 = (y - ((5.1 * x ** 2) / (4 * PI ** 2)) + ((5 * x) / PI) - 6)
        p2 = ((10 - (10 / 8 * PI)) * math.cos(x)) + 9
        return p1 ** 2 + p2

    def f2(self, x, y):
        '''
        Function for subjecting to constraints
        RETURNS: float
        '''
        return y + (x - 12 / 1.2)

    def print_chr(self, gen):
        '''
        Print info of an Individual-object
        '''
        with open('RCGA_result.dat', 'a') as f:
            print("GEN #{} - fit {}\n ({}, {})\n".format(gen, self.fitness,
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
        '''
        Initializes a population of individuals
        '''
        for i in range(POPULATION_SIZE):
            self.individuals.append(Individual(i))
        self.size = len(self.individuals)

    def evaluate(self, mode, generation):
        '''
        Calculates fitness for individuals,
        does 3 types of constraint handling
        depending on mode given to RCGA()
        '''
        for ind in self.individuals:
            def KURI(satisfied):
                '''
                Helper function for static constraint
                RETURNS: float
                '''
                return KURI_CONST - sum([KURI_CONST / 2 for _ in range(satisfied)])

            def JOINESHOUCK(ind, gen):
                '''
                Helper function for dynamic constraint
                RETURNS: float
                '''
                C = .5
                a = 2
                b = 2
                C_1 = 0 if ind.f1(ind.x, ind.y) <= 0 else abs(ind.f1(ind.x, ind.y))
                C_2 = 0 if ind.f2(ind.x, ind.y) <= 0 else abs(ind.f2(ind.x, ind.y))

                SVC = C_1 + C_2
                result = ind.fitness + (C * gen) ** a * SVC
                return result

            ind.fitness = self.f(ind.x, ind.y)
            passed, satisfied = ind.constraints()
            if passed:
                continue
            elif mode == 'dp':
                ind.fitness = 0
            elif mode == 'static':
                ind.fitness = KURI(satisfied)
            elif mode == 'dynamic':
                ind.fitness = JOINESHOUCK(ind, generation)

    def find_fittest(self):
        '''
        Sets the Individual-object in population
        with the best fitness as the fittest of the
        population.
        '''
        for ind in self.individuals:
            if ind.fitness < self.fittest.fitness:
                self.fittest = ind

    def tournament_select(self):
        '''
        Returns the Individual in population with the best fitness
        RETURNS: Individual-object
        '''
        pool = self.individuals[:]
        pool = sorted(pool, key=lambda x: x.fitness)
        return pool.pop()

    def BQI_prob(self):
        '''
        Calculates distributed probability for the crossover
        operation.
        RETURNS: float
        '''
        rand = rng.random()
        n = 2  # distribution index
        if rand <= .5:
            return (2 * rand) ** (1 / n + 1)
        else:
            return (1 / (2 * (1 - rand))) ** (1 / n + 1)

    def mutate(self, target):
        '''
        Randomizes the x and y of an Individual
        RETURNS: Individual-object
        '''
        target.x = rng.uniform(-5, 10)
        target.y = rng.uniform(0, 15)
        target.fitness = self.f(target.x, target.y)
        return target

    def rc_crossover(self, par1, par2):
        '''
        Calculates children from two float according to
        distributed probability.
        RETURNS: list
        '''
        prob = self.BQI_prob()
        self.size += 1
        c_1 = Individual(self.size)
        c_1.fitness = .5 * ((1 + prob) * par1.fitness + (1 - prob) * par2.fitness)

        self.size += 1
        c_2 = Individual(self.size)
        c_2.fitness = .5 * ((1 - prob) * par1.fitness + (1 + prob) * par2.fitness)
        return [c_1, c_2]

    def f(self, x, y):
        '''
        Function that is minimized
        RETURNS: float
        '''
        return x + y

    def print_gen(self):
        '''
        Prints the current generation of objects.
        '''
        for ind in self.individuals:
            ind.print_chr()

    def print_fittest(self, gen):
        '''
        Prints the fittest object in the population.
        '''
        self.fittest.print_chr(gen)


def RCGA(mode, epochs):
    '''
    Minimizes function with given mode as a
    constraint handling method.
    * 'dp' = Death penalty
    * 'static' = Kuri's static penalty
    * 'dynamic' = Joine's and Houck's dynamic penalty

    Prints info of every 200 generations in 'RCGA_result.dat'
    '''
    pop = Population()
    pop.initialize_population()
    pop.fittest = pop.individuals[0]

    for generation in range(epochs):
        pop.evaluate(mode, generation)
        next_pop = Population()

        while len(next_pop.individuals) < len(pop.individuals):
            parent1 = pop.tournament_select()
            # CROSSOVER
            if rng.random() < PROB_CROSSOVER:
                parent2 = pop.tournament_select()
                child1, child2 = pop.rc_crossover(parent1, parent2)
                next_pop.individuals.append(child1)
                next_pop.individuals.append(child2)
            else:
                next_pop.individuals.append(parent1)
            # MUTATION
            if rng.random() < PROB_MUTATION:
                target = next_pop.tournament_select()
                mutated = pop.mutate(target)
                next_pop.individuals.append(mutated)

        next_pop.evaluate(mode, generation)
        # ELITIST STRATEGY - always keep fittest
        pop.find_fittest()
        next_pop.individuals.append(pop.fittest)

        # choose the top 10 individuals for the next population
        next_pop.individuals = sorted(next_pop.individuals, key=lambda x: x.fitness)
        pop.individuals = next_pop.individuals[:10]
    pop.print_fittest(generation)


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
    epochs = 2000

    mode = 'dp'
    with open('RCGA_result.dat', 'a') as f:
        print(mode.upper(), file=f)
        print('-'*30, file=f)
    RCGA(mode, epochs)

    mode = 'static'
    with open('RCGA_result.dat', 'a') as f:
        print(mode.upper(), file=f)
        print('-'*30, file=f)
    RCGA(mode, epochs)

    mode = 'dynamic'
    with open('RCGA_result.dat', 'a') as f:
        print(mode.upper(), file=f)
        print('-'*30, file=f)
    RCGA(mode, epochs)

##############################################################################

if __name__ == "__main__":
    main()
