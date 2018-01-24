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
PRINTING = False


class Chromosome:
    ''' Individual Chromosome '''
    def __init__(self, num, gene=None):
        self.gene = [gene]        
        if gene is None:
            self.gene = [format(rng.getrandbits(16), '016b')]
        self.num = num
        self.fitness = None

    def print_chr(self):
        ''' Print info of a Chromosome '''
        print('#' + str(self.gene) + ' with fitness ' + str(self.fitness))


class Population:
    ''' Set of Chromosomes '''
    def __init__(self):
        self.chromosomes = []
        self.crossovers = 0
        self.mutations = 0
        self.f_value = 0
        self.winner = None
        self.pairs = []
        self.size = 0

    def initialize_population(self):
        ''' Initializes a population with size '''
        for i in range(POPULATION_SIZE):
            self.chromosomes.append(Chromosome(i))
        self.size = len(self.chromosomes)

    def evaluate(self):
        ''' Calculates fitness for each chromosome '''
        self.size = len(self.chromosomes)
        for chrom in self.chromosomes:
            gene1 = int(chrom.gene[0][:8], 2)  # first 8 bits of GA- string
            gene2 = int(chrom.gene[0][8:], 2)  # last 8 bits of GA- string
            x_1 = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) *  gene1 / (2 ** BIT_SIZE)
            x_2 = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * gene2 / (2 ** BIT_SIZE)
            f = funktio(x_1, x_2)
            '''
            # only mark improvements on function value
            if self.f_value > f:
                self.f_value = f
            '''
            self.f_value = f
            fitness = 1.0 / (1.0 + self.f_value)
            # - because of minimum
            chrom.fitness = fitness
        if PRINTING:
            self.print_gen()

    def tournament_select(self):
        ''' All chromosomes against each other, max fitness value wins '''
        self.winner = self.chromosomes[0]
        chrom_competitors = [chrom for chrom in self.chromosomes]
        for chrom in self.chromosomes:
            for c in chrom_competitors:
                if c != chrom:
                    if c.fitness > self.winner.fitness:
                        self.winner = c
        if PRINTING:
            print()
            print('Winning gene:')
            self.winner.print_chr()
        return self.winner

    def pair_chroms(self):
        ''' Pair chromosomes for crossover '''
        self.chromosomes.sort(key=lambda x: x.fitness, reverse=True)
        tmp = []
        for chrom in self.chromosomes:
            p1 = self.chromosomes.pop(0)
            p2 = self.chromosomes.pop(0)
            self.pairs.append((p1, p2))
            tmp.append(p1)
            tmp.append(p2)
        self.chromosomes = tmp

    def sp_crossover(self, chrom1, chrom2):
        ''' Single point crossover '''
        self.crossovers += 1
        pos = round(rng.random() * (BIT_SIZE*2))
        gene1 = chrom1.gene[0][:pos] + chrom2.gene[0][pos:]
        gene2 = chrom2.gene[0][:pos] + chrom1.gene[0][pos:]
        child1 = Chromosome(self.size + 1, str(gene1))
        child2 = Chromosome(self.size + 2, str(gene2))
        return child1, child2

    def bitwise_mutate(self):
        ''' Mutate bits randomly '''
        # TODO
        self.mutations += 1
        for chrom in self.chromosomes:
            selected = chrom
            selected.gene[0] = self.flip_bins(chrom.gene[0])
            self.chromosomes.remove(chrom)
            self.chromosomes.append(selected)

    def flip_bins(self, gene):
        ''' Flips random bits from a bit string '''        
        bin_arr = [int(digit, 2) for digit in gene]
        for digit in bin_arr:
            if rng.random() > 0.5:
                if digit is 0:
                    digit = 1
                digit = 0
        return ''.join([str(d) for d in bin_arr])

    def remove_least_fitting(self):
        ''' Removes chromosomes with worst fitness from population '''
        removable = max((chrom.num, chrom.fitness) for chrom in self.chromosomes)
        self.chromosomes = [c for c in self.chromosomes if c.num != removable[0]]

    def print_gen(self):
        ''' Prints info of a population '''
        print('- Current generation -')
        for c in self.chromosomes:
            c.print_chr()


def funktio(x_1, x_2):
    '''RETURN : function value with given parameters '''
    return x_1 + x_2 - (2 * x_1) ** 2 - x_2 ** 2 + (x_1 * x_2)


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
    
    for generation in range(ITERATIONS):
        # clear()
        pop_size = len(pop.chromosomes)
        print('\nGENERATION %s' % (generation))
        print('-'*30)
        pop.evaluate()
        winner = pop.tournament_select()
        pop.pair_chroms()
        for pair in pop.pairs:
            if rng.random() < PROB_CROSSOVER:
                child1, child2 = pop.sp_crossover(pair[0], pair[1])
                pop.chromosomes.append(child1)
                pop.chromosomes.append(child2)
                pop.evaluate()
                # Limit chromosomes for reasonable computation time
                while len(pop.chromosomes) > 100:
                    pop.remove_least_fitting()
        if rng.random() < PROB_MUTATION:
            pop.bitwise_mutate()
        print('Chromosomes ' + str(len(pop.chromosomes)) +
              ', Crossovers ' + str(pop.crossovers) +
              ', Mutations ' + str(pop.mutations))
        print('Function Value : ' + str(pop.f_value))
    print('*-'*30)
    print('Final function value : ' + str(pop.f_value))


def main():
    clear()
    minimize_ga()

##############################################################################

if __name__ == "__main__":
    main()
