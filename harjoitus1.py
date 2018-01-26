# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os

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
        self.fitness = None
        self.function_value = None
        self.x_1 = 0
        self.x_2 = 0

    def print_chr(self):
        ''' Print info of an Individual '''
        print('#' + str(self.num) + ' Fitness : ' +
                    # str(format(self.fitness, '.2f')) + ' -- Value : ' +
                    str(format(self.function_value, '.2f')) + 
                    str(' -- (' + format(self.x_1, '.2f') + ',' + format(self.x_2, '.2f')) + ')')


class Population:
    ''' Set of Individuals '''
    def __init__(self):
        self.individuals = []
        self.crossovers = 0
        self.mutations = 0
        self.newPop = []
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
            ind.fitness = ind.function_value  # transform to maximize?

            if self.fittest is None:
                self.fittest = ind
            elif ind.fitness > self.fittest.fitness:
                self.fittest = ind

    def tournament_select(self):
        '''  '''
        pool = self.individuals[:]
        pool.sort(key=lambda x: x.fitness, reverse=True)
            
        '''
        sorted_by_fitness = sorted(self.individuals, key=lambda x: x.fitness, reverse=True)
        t_1 = sorted_by_fitness.pop(0)
        t_2 = sorted_by_fitness.pop(0)
        if t_1.fitness > t_2.fitness:
            parent_1 = t_1
        else:
            parent_1 = t_2
        parent_2 = parent_1
        '''

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
        print()


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
        if DEBUG:
            input('Press enter for next...')
        print('\nGENERATION %s' % (generation))
        print('-'*30)
        pop.tournament_select()
        pop.evaluate()
        pop.newPop.clear()
        for indi in pop.individuals:  # 'evolve' individuals in population
            if rng.random() < PROB_CROSSOVER:
                child1, child2 = pop.sp_crossover(pop.fittest, indi)
                pop.newPop.append(child1)
                pop.newPop.append(child2)
            if rng.random() < PROB_MUTATION:
                mutated = pop.mutate(indi)
                pop.newPop.append(mutated)
        pop.evaluate()
        pop.individuals.sort(key=lambda x: x.fitness, reverse=True)
        # top 10 out of new population for next starting population
        pop.individuals = pop.newPop[:10]
        pop.evaluate()
        pop.print_gen()
        print('Individuals ' + str(len(pop.individuals)) +
              ', Crossovers ' + str(pop.crossovers) +
              ', Mutations ' + str(pop.mutations))
        clear()
    return pop.fittest


def main():
    clear()
    # set of 10 * 50 generations for testing
    tests = []
    try:
        while len(tests) < 10:
            tests.append(run_ga())
    except KeyboardInterrupt as e:
        print('interrupted')
    tests.sort(key=lambda x: x.fitness, reverse=True)
    for i in tests:
        print(i.print_chr())

##############################################################################

if __name__ == "__main__":
    main()
