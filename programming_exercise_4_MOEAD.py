# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri Juutilainen 03/2018 // WIP
# MOEA-D - Tchebycheff fitness evaluation, weighted sum evaluation

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


class Individual:
    def __init__(self, x, weigth):
        self.x = x
        self.weigth = weigth
        self.fitness = 0

    def print_info(self, index):
        with open('MOEAD_result.dat', 'a') as f:
            print("#{}: ({},{},{})\nFit {}\n".format(
                index, self.x[0], self.x[1], self.x[2], self.fitness
                ), file=f)


def print_data(data, title):
    with open('MOEAD_result.dat', 'a') as f:
        print('\n' + title, file=f)
        print('-'*30, file=f)
    if data is not []:
        i = 1
        for x in data:
            x.print_info(i)
            i += 1


def plot(data):
    x = []
    y = []
    x2 = []
    y2 = []
    for ind in data:
        if ind.rank == 0:
            x.append(ind.value[0])
            y.append(ind.value[1])
            plt.plot(x, y, 'ro')
        elif ind.rank == 1:
            x2.append(ind.value[0])
            y2.append(ind.value[1])
            plt.plot(x2, y2, 'bo')
    plt.show()


def constraints(x, i):
    x_pass = True if -5 <= x and x < 5 else False
    i_pass = True if i <= 1 and i <= 3 else False
    return True if x_pass and i_pass else False


def MOEA_D(data, weights, Z, approach):
    # Initialization
    pop = []
    for i in data:
        pop.append(Individual(data[i], weights[i]))
    EX_POP = pop

    func_list = [lambda x1, x2: -10 * math.exp(-0.2 * math.sqrt(x1 ** 2 + x2 ** 2)),
                 lambda x, y: abs(x) ** .8 + 5 * math.sin(x ** 3)]

    # evaluation functions
    def tchebycheff(ind):
        results = []
        for i in range(2):
            result = ind.weigth[i] * abs(func_list[i](ind.x[i], ind.x[i + 1]))
            if constraints(ind.x[i], i):
                results.append(result)
        return max(results)

    def weightedsum(ind):
        results = []
        for i in range(2):
            result = ind.weigth[i] * func_list[i](ind.x[i], ind.x[i + 1])
            if constraints(ind.x[i], i):
                results.append(result)
        return sum(results)

    for ind in pop:
        if approach is 'tchebycheff':
            ind.fitness = tchebycheff(ind)
        elif approach is 'weightedsum':
            ind.fitness = weightedsum(ind)

    print_data(pop, 'AFTER ' + approach)

    # things to maintain after iter:
    # list of points where x_i is the solution for subproblem i
    # list of function values for each i = F(x_i)    
    # vector z : best value found so far for objective
    # external population to store nondominated solutions   


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
    open('MOEAD_result.dat', 'w').close()
    keys = [x for x in range(1, 12)]
    _value = dict(zip(keys, MOEA_D_values))
    _weight = dict(zip(keys, MOEA_D_weights))
    Z = (-20, -12)
    MOEA_D(_value, _weight, Z, 'tchebycheff')
    MOEA_D(_value, _weight, Z, 'weightedsum')


##############################################################################

if __name__ == "__main__":
    main()
