# !/usr/bin/env python3
# -  *  - coding:utf-8 -  *  - 
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri Juutilainen 03/2018 // WIP
# MOEA - D - Tchebycheff fitness evaluation, weighted sum evaluation

MOEA_D_values = [
    [-1.0074, -3.0188, 4.8305], 
    [0.2688, -0.1031, -1.9855], 
    [-0.8320, -1.6051, 2.0110], 
    [1.5686, 4.5163, 1.6634], 
    [1.2797, 4.2033, 0.3913], 
    [-2.0802, -4.4732, 1.9811], 
    [-0.6835, 2.3786, 1.6653], 
    [-4.8451, -2.3088, -3.2187], 
    [4.806, -0.7716, -3.7199], 
    [-3.3283, 0.4787, 4.9908], 
    [-3.9378, 4.4274, -3.2888], 
    [-1.2759, -0.8226, -4.6740]
]

MOEA_D_weights = [
    [0, 1.0000], 
    [0.0909, 0.9091], 
    [0.1818, 0.8182], 
    [0.2727, 0.7273], 
    [0.3636, 0.6364], 
    [0.4545, 0.5455], 
    [0.5455, 0.4545], 
    [0.6364, 0.3636], 
    [0.7273, 0.2727], 
    [0.8182, 0.1818], 
    [0.9091, 0.0909], 
    [1.0000, 0]
]

T = 4
# evaluation functions
func_list = [lambda x1, x2:-10 * math.exp(-0.2 * math.sqrt(x1 ** 2 + x2 ** 2)),
             lambda x, y:abs(x) ** .8 + 5 * math.sin(x ** 3)]


class Individual:
    def __init__(self, x, weigth):
        self.x = x
        self.weigth = weigth
        self.fitness = 0
        self.neighbors = []

    def print_info(self, index, neighbool):
        with open('MOEAD_result.dat', 'a') as f:
            print("#{}: ({},{},{}),\n-- Fitness: {}".format(
                index, self.x[0], self.x[1], self.x[2], self.fitness
                ), file=f)
            if neighbool:
                print("Neighbors:", file=f)
                for i in self.neighbors:
                    print('-- {}, dist: {}'.format(i[1].x, i[0]), file=f)
                print('', file=f)


def print_data(data, title, neighbool):
    '''
    Print all info from a generation
    '''
    with open('MOEAD_result.dat', 'a') as f:
        print('\n' + title, file=f)
        print('-' * 30, file=f)
    if data is not []:
        i = 1
        for x in data:
            x.print_info(i, neighbool)
            i += 1


def evaluate(ind, approach):
    results = []
    for i in range(2):
        if approach is 'tchebycheff':
            result = ind.weigth[i] * abs(func_list[i](ind.x[i], ind.x[i + 1]))
        elif approach is 'weightedsum':
            result = ind.weigth[i] * func_list[i](ind.x[i], ind.x[i + 1])
        if constraints(ind.x[i], i):
            results.append(result)
    if approach is 'tchebycheff':
        return max(results)
    elif approach is 'weightedsum':
        return sum(results)


def eval_neighbors(ind, pop):
    # self is in neighbors?
    # distances = [[0, ind]]
    distances = []
    for i in pop:
        distances.append((distance(ind.weigth, i.weigth), i))
    srtd = sorted(distances, key=lambda tup: tup[0])
    return srtd[:T]


def dominates(first, second):
    for i in range(3):
        if first.x[i] > second.x[i]:
            return False
    return True


def constraints(x, i):
    x_pass = True if-5 <= x and x < 5 else False
    i_pass = True if i <= 1 and i <= 3 else False
    return True if x_pass and i_pass else False


def distance(a, b):
    return math.hypot(a[1] - a[0], b[1] - b[0])


def crossover(a, b):
    def repair(y):
        for i in range(2):
            # Torque repair from PSO
            max_l = 10
            while not constraints(y.x[i], i):
                if y.x[i] < 5:
                    y.x[i] = 5 - (y.x[i] % max_l)
                elif y.x[i] > -5:
                    y.x[i] = -5 + (y.x[i] % max_l)
        return y

    parent1 = a[1]
    parent2 = b[1]
    y = Individual(parent1.x, parent2.weigth)

    rand = rng.random()
    # BQI probability from RCGA implementation
    prob = (2 * rand) ** 1.5 if rand <= .5 else (1 / (2 * (1 - rand))) ** 1.5
    y.fitness = .5 * ((1 + prob) * par1.fitness + (1 - prob) * par2.fitness)
    return repair(y)


def MOEA_D(data, weights, approach):
    # INITIALIZATION
    pop = []
    for i in data:
        pop.append(Individual(data[i], weights[i]))
    Z = [-20, -12]
    for ind in pop:
        # Initialize population fitness with given approach
        ind.fitness = evaluate(ind, approach)
        # Calculate euclidian distances for weight vectors
        # Add neighbors (including self ?)
        ind.neighbors += eval_neighbors(ind, pop)
    EX_POP = pop  # set initialized pop as external pop
    print_data(EX_POP, approach.upper(), False)

    # UPDATE LOOP
    ITERS = 20
    while ITERS < 20:
        for ind in pop:
            # Random sample of 2 solutions from neighbors
            kl = rng.sample(ind.neighbors, 2)
            # Reproduce a new solution
            y = crossover(kl[0], kl[1])
            # Evaluate
            y.fitness = evaluate(y, approach)

            # update z
            for i in range(2):
                fy = func_list[i](y.x[i], y.x[i + 1])
                if Z[i] < fy:
                    Z[i] = fy
            # update neighbors
            for n in ind.neighbors:
                if y.fitness < n[1].fitness:
                    n[1].fitness = y.fitness
            # update external population
            for solution in EX_POP:
                if dominates(y, solution):
                    EX_POP.append(y)
                else:
                    EX_POP.remove(solution)
        ITERS += 1
    # END UPDATE LOOP
    print_data(EX_POP, approach.upper(), True)


def clear():
    '''
    Tyhjää konsolin
    '''
    name = os.name
    if name == 'posix':
        os.system('clear')
    elif name == 'nt'or name == 'dos':
        os.system('cls')
    else:
        print("\n" * 30)


def main():
    clear()
    open('MOEAD_result.dat', 'w').close()
    keys = [x for x in range(12)]
    _value = dict(zip(keys, MOEA_D_values))
    _weight = dict(zip(keys, MOEA_D_weights))

    MOEA_D(_value, _weight, 'tchebycheff')
    MOEA_D(_value, _weight, 'weightedsum')


##############################################################################

if __name__ == "__main__":
    main()
