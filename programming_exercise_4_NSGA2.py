# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math
from matplotlib import pyplot as plt

# @author Harri Juutilainen 03/2018 // WIP
# NSGA-II - nondominated sorting algorithm, crowding distance calc


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


class Individual:
    def __init__(self, val):
        self.value = val
        self.rank = 0
        self.distance = 0
        self.order = 0
        self.dominated = []
        self.domination_count = 0

    def print_info(self, index):
        with open('NSGA2_result.dat', 'a') as f:
            print("#{}: Value {}, Rank {},\nDomination count {}, Distance {}\n".format(
                index, self.value, self.rank, self.domination_count, self.distance
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


def crowding_dist(data):
    for ind in data:
        indeksi = data.index(ind)
        if indeksi != 0 and indeksi < len(data) - 1:
            for i in range(2):
                n = data[indeksi + 1].value[i]
                p = data[indeksi - 1]. value[i]
                max_ = max([x.value[i] for x in data])
                min_ = min([x.value[i] for x in data])
                ind.distance += (ind.distance + (p - n)) / (max_ - min_)
                ind.distance = abs(ind.distance)


def partial_order(data):
    for i in data:
        for j in data:
            if i.rank < j.rank or (i.rank == j.rank and i.distance > j.distance):
                i.order -= 1
                j.order += 1
    return sorted(data, key=lambda x: x.order, reverse=True)


def NSGA_II():
    '''
    NSGA-II implementation to a set matrix of objectives.
    Nondominated sorting and crowding distance calculation.
    '''
    data = []
    for i in NSGA_values:
        data.append(Individual(i))
    print_data([], 'NSGA-II')

    # NONDOMINATED SORTING
    nondom_sort(data)
    print_data(data, 'AFTER NONDOMINATED SORTING')

    # CROWDING DISTANCE
    crowding_dist(data)
    p_order = partial_order(data)

    # PARTIAL ORDER AND SELECTION
    selected = p_order[:6]
    print_data(selected, 'SELECTED')

    plot(selected)


def print_data(data, title):
    with open('NSGA2_result.dat', 'a') as f:
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
    open('NSGA2_result.dat', 'w').close()
    NSGA_II()


##############################################################################

if __name__ == "__main__":
    main()
