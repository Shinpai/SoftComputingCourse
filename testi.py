# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random as rng
import os
import math

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
##############################################################################

if __name__ == "__main__":
    main()
