# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os

# @author Harri Juutilainen 01/2018
# more OOP version of GA // not complete

# Given parameters
LOWER_BOUND = 1.0
UPPER_BOUND = 5.0
POPULATION_SIZE = 10
BIT_SIZE = 8
PROB_CROSSOVER = 0.8
PROB_MUTATION = 0.06
ITERATIONS = 50
DEBUG = False


class Individual:
    ''' Individual '''
    def __init__(self, num, gene=None):
        self.gene = [gene]
        if gene is None:
            self.gene = [format(rng.getrandbits(16), '016b')]
        self.num = num
        self.function_value = None
        self.x_1 = 0
        self.x_2 = 0

    def print_chr(self):
        ''' Print info of an Individual '''
        with open('GA_result.dat', 'a') as f:
            print('#' + str(self.num) + ' Func value : ' +
                  str(format(self.function_value, '.2f')) +
                  str(' -- (' + format(self.x_1, '.2f') + ',' +
                  format(self.x_2, '.2f')) + ')', file=f)


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
        self.evaluate()

    def funktio(self, x_1, x_2):
        '''RETURN : function value with given parameters '''
        return x_1 + x_2 - (2 * x_1) ** 2 - x_2 ** 2 + (x_1 * x_2)

    def evaluate(self):
        ''' Calculates fitness for each individual '''
        self.size = len(self.individuals)
        for ind in self.individuals:
            gene1 = int(ind.gene[0][:8], 2)  # first 8 bits of GA- string
            gene2 = int(ind.gene[0][8:], 2)  # last 8 bits of GA- string
            x_1 = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * (gene1 / (2 ** BIT_SIZE))
            x_2 = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * (gene2 / (2 ** BIT_SIZE))
            ind.x_1 = x_1
            ind.x_2 = x_2
            ind.function_value = abs(self.funktio(x_1, x_2))

    def tournament_select(self):
        '''  '''
        pool = self.individuals[:]
        pool = sorted(pool, key=lambda x: x.function_value)
        return pool.pop()

    def sp_crossover(self, parent_1, parent_2):
        ''' Single point crossover, creates 2 children from parents'''
        self.crossovers += 1
        pos = round(rng.random() * (BIT_SIZE*2))
        gene1 = parent_1.gene[0][:pos] + parent_2.gene[0][pos:]
        gene2 = parent_2.gene[0][:pos] + parent_1.gene[0][pos:]
        child1 = Individual(self.size + 1, str(gene1))
        child2 = Individual(self.size + 2, str(gene2))
        return child1, child2

    def mutate(self, ind):
        ''' Mutate bits randomly from given individuals GA string'''
        self.mutations += 1
        gene = ind.gene[0]
        bin_arr = [int(digit, 2) for digit in gene]
        mutated = ''
        for digit in bin_arr:
            if rng.random() > 0.5:
                if digit == 0:
                    digit = 1
                digit = 0
            mutated += str(digit)
        ind.gene[0] = mutated
        return ind

    def print_gen(self):
        ''' Prints info of a population '''
        for c in self.individuals:
            c.print_chr()


def clear():
    ''' Tyhjää konsolin '''
    name = os.name
    if name == 'posix':
        os.system('clear')
    elif name == 'nt' or name == 'dos':
        os.system('cls')
    else:
        print("\n" * 30)


def run_ga():
    ''' Minimizes a function with 50 iterations '''
    pop = Population()
    pop.initialize_population()
    pop.print_gen()
    for generation in range(ITERATIONS):
        pop.evaluate()
        next_population = Population()
        while len(next_population.individuals) < len(pop.individuals):
            parent1 = pop.tournament_select()
            if rng.random() < PROB_CROSSOVER:
                parent2 = pop.tournament_select()
                child1, child2 = pop.sp_crossover(parent1, parent2)
                next_population.individuals.append(child1)
                next_population.individuals.append(child2)
            else:
                next_population.individuals.append(parent1)
            next_population.evaluate()
            if rng.random() < PROB_MUTATION:
                target = next_population.tournament_select()
                mutated = pop.mutate(target)
                next_population.individuals.append(mutated)
        next_population.evaluate()
        next_population.individuals = sorted(next_population.individuals, key=lambda x: x.function_value)
        # choose the top 10 individuals for the next population
        pop.individuals = next_population.individuals[:10]
        pop.evaluate()
        pop.print_gen()


def main():
    clear()
    open('GA_result.dat', 'w').close()
    run_ga()
    exit(0)

##############################################################################

if __name__ == "__main__":
    main()
