# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os

# @author Harri Juutilainen 02/2018
# streamlined functional version of GA // not complete

# Given parameters
LOWER_BOUND = 1.0
UPPER_BOUND = 5.0
POPULATION_SIZE = 10
BIT_SIZE = 8
PROB_CROSSOVER = 0.8
PROB_MUTATION = 0.06
ITERATIONS = 50


def initialize_population():
    return [format(rng.getrandbits(16), '016b') for _ in range(POPULATION_SIZE)]


def eval_fit(ind):
    x = int(ind[:8], 2)
    y = int(ind[-8:], 2)
    value = x + y - (2 * x) ** 2 - y ** 2 + (x * y)
    return 1 / (1 + value)


def t_select(pop):
    competitors = pop[:]
    rng.shuffle(competitors)
    mating = []
    i = 0
    while len(mating) <= 10:
        t1 = competitors[i]
        t2 = pop[i]
        if eval_fit(t1) > eval_fit(t2):
            mating.append(t1)
        else:
            mating.append(t2)
    return mating


def pick_parents(pop):
    next_pop = []
    parents = pop[:]
    while len(next_pop) < len(pop):
        p1 = parents[0]
        p2 = parents[1]
        if rng.random() < PROB_CROSSOVER:
            next_pop += sp_crossover(p1, p2)
        else:
            next_pop += p1, p2
        parents = pop[2:]
    return next_pop


def sp_crossover(s1, s2):
    pos = round(rng.random() * 16)
    c1 = s1[:pos] + s2[pos:]
    c2 = s2[:pos] + s1[pos:]
    return [c1, c2]


def mutate(pop):
    for gene in pop:
        bin_arr = [int(digit, 2) for digit in gene]
        mutated = ''
        for digit in bin_arr:
            if rng.random() > PROB_MUTATION:
                if digit == 0:
                    digit = 1
                digit = 0
            mutated += str(digit)
        gene = mutated
    return pop


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
    population = initialize_population()
    next_gen = []
    for generation in range(ITERATIONS):
        mating = t_select(population)
        next_gen = pick_parents(mating)
        population = mutate(next_gen)


def main():
    clear()
    run_ga()

##############################################################################

if __name__ == "__main__":
    main()
