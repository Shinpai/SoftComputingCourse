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
        self.size = len(self.individuals)
        for ind in self.individuals:
            gene1 = int(ind.gene[0][:8], 2)  # first 8 bits of GA- string
            gene2 = int(ind.gene[0][8:], 2)  # last 8 bits of GA- string
            x_1 = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * (gene1 / (2 ** BIT_SIZE))
            x_2 = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * (gene2 / (2 ** BIT_SIZE))
            f = self.funktio(x_1, x_2)
            ind.fitness = f

    def tournament_select(self):
        sorted_by_fitness = sorted(self.individuals, key=lambda x: x.fitness, reverse=False)
        t_1 = sorted_by_fitness.pop()
        t_2 = sorted_by_fitness.pop()
        if t_1.fitness > t_2.fitness:
            parent_1 = t_1
        else:
            parent_1 = t_2
        parent_2 = parent_1
        return parent_1, parent_2

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
        mutated = ind
        mutated.gene[0] = self.flip_bins(mutated.gene[0])
        return mutated

    def flip_bins(self, gene):
        ''' Flips random bits from a bit string '''
        bin_arr = [int(digit, 2) for digit in gene]
        for digit in bin_arr:
            if rng.random() > 0.5:
                if digit is 0:
                    digit = 1
                digit = 0
        return ''.join([str(d) for d in bin_arr])

    def print_gen(self):
        ''' Prints info of a population '''
        print('- Current generation -')
        for c in self.individuals:
            c.print_chr()


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
    pop = Population()
    pop.initialize_population()
    pop.evaluate()
    pop.print_gen()
    for generation in range(ITERATIONS):
        pop_size = len(pop.individuals)
        print('\nGENERATION %s' % (generation))
        print('-'*30)
        parent_1, parent_2 = pop.tournament_select()
        pop.evaluate()
        if rng.random() < PROB_CROSSOVER:
            child1, child2 = pop.sp_crossover(parent_1, parent_2)
            pop.newPop.append(child1)
            pop.newPop.append(child2)
        for ind in pop.individuals:
            if rng.random() < PROB_MUTATION:
                mutated = pop.mutate(parent_1)
                pop.newPop.append(mutated)
        pop.evaluate()
        pop.individuals = pop.newPop[:10]
        pop.print_gen()
        print('Individuals ' + str(len(pop.individuals)) +
              ', Crossovers ' + str(pop.crossovers) +
              ', Mutations ' + str(pop.mutations))
    print('*-'*30)


def main():
    clear()
    minimize_ga()

##############################################################################

if __name__ == "__main__":
    main()
