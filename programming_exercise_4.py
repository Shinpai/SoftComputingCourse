# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri Juutilainen 03/2018 // WIP
# NSGA-II - nondominated sorting algorithm, crowding distance calc
# MOEA-D - Tchebycheff fitness evaluation, weighted sum evaluation


NSGA_values = [
    [0, 1],
    [1, 0],
    [2, 1.5],
    [1.5, 3],
    [3, 1.6],
    [4, 3.5],
    [4.5, 3.1],
    [5, 2.5],
    [6, 5],
    [5.5, 7],
    [4.2, 6],
    [3.3, 6.5]
]

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
    def __init__(self, val):
        self.value = val
        self.rank = 0
        self.distance = 0
        self.order = 0
        self.dominated = []
        self.domination_count = 0

    def print_info(self):
        with open('NSGA_MOEAD_result.dat', 'a') as f:
            print("Value {}, Rank {},\nDomination count {}, Distance {}\n".format(
                self.value, self.rank, self.domination_count, self.distance
                ), file=f)


def nondom_sort(data):
        '''
        Fast nondominated sort, calculates rank and domination counts
        for Individual objects
        '''
        # evaluate dominations
        fronts = []
        for p in data:
            for q in data:
                if p.value[0] < q.value[0] and p.value[1] < q.value[1]:
                    p.dominated.append(q)
                elif p.value[0] > q.value[0] and p.value[1] > q.value[1]:
                    p.domination_count += 1
            if p.domination_count == 0:
                # p in front 1
                p.rank = 1
                fronts.append(p)
        # front counter
        i = 0
        while len(fronts) != 0:
            Q = []
            for p in fronts:
                for q in fronts:
                    q.domination_count -= 1
                    if q.domination_count == 0:
                        q.rank = i + 1
                        Q.append(q)
            i += 1
            fronts = Q
        return fronts


def crowding_dist(data, fronts):
    l = len(fronts)
    for ind in data:
        indeksi = data.index(ind)
        if indeksi != 0 and indeksi < len(data) - 1:
            for i in range(2):
                n = data[indeksi + 1].value[i]
                p = data[indeksi - 1]. value[i]
                ind.distance += (ind.distance + (p - n)) / (7 - 0)


def partial_order(data):
    for i in data:
        for j in data:
            if i.rank < j.rank or (i.rank == j.rank and i.distance > j.distance):
                i.order -= 1
                j.order += 1
    return sorted(data, key=lambda x: x.order, reverse=True)


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


def NSGA_II():
    data = []
    for i in NSGA_values:
        data.append(Individual(i))

    with open('NSGA_MOEAD_result.dat', 'a') as f:
        print('\nAFTER NONDOMINATED SORTING:', file=f)
        print('-'*30, file=f)
    fronts = nondom_sort(data)
    for ind in fronts:
        ind.print_info()

    crowding_dist(data, fronts)
    p_order = partial_order(data)

    with open('NSGA_MOEAD_result.dat', 'a') as f:
        print('\nSELECTED:', file=f)
        print('-'*30, file=f)
    for ind in p_order[:6]:
        ind.print_info()
    # return/print top 6 individuals


def MOEA_D(values, weights):
    def tchebycheff_eval(values):
        pass
    fitness = tchebycheff_eval(values)
    pass


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
    open('NSGA_MOEAD_result.dat', 'w').close()
    keys = [x for x in range(1, 12)]
    moead_value = dict(zip(keys, MOEA_D_values))
    moead_weight = dict(zip(keys, MOEA_D_weights))

    NSGA_II()
    MOEA_D(moead_value, moead_weight)


##############################################################################

if __name__ == "__main__":
    main()
