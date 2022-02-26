import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import matplotlib
import pandas as pd
from datetime import datetime
import random
import pygame
pygame.font.init()
import os
import time



np.set_printoptions(linewidth=np.inf)

length = 8
#number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
#number of cells in a row
rule = 90
#number who's x_base transformation gives the rules dictionary its values
view = 3
#size of the view window that scans a row for rule application
base = 2
#numerical base of the rule set. number of colors each cell can be
start = length
#position for a row 0 cell value 1
direction = 0
#if ^ = 0 view scans from left to right: else view scans right to left

###to do###

#starting from most basic cell block contstruction record the repeating values genrated from rule implimentation
##replace the decimal translation of the binary to a number representing the pattern

#*parse rule results with ergodic_parse?
##order nth layer in valeu order not frequency

#find how to determine the length of the longest possible pattern from starting variables
##would true value pattern length correlate to center construction complexity?

#####remove the hard code for the 0 width cnvs#####


# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white


def base_x(n, b):
    e = n//b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, base = 2):

    rules = dict()

    if base == 2:

        int_rule = bin(rule).replace('0b', '')


    else:

        int_rule = base_x(rule, base)


    x = int_rule[::-1]

    while len(x) < base ** view:

        x += '0'

    bnr = x[::-1]
    int_rule = list(bnr)


    # print(" ")
    # print("int_rule")
    # [print(int_rule)]


    for x in reversed(range(len(int_rule))):

        key = tuple(base_x(x, base)[-view:])

        # print(" ")
        # print("key")
        # print(key)

        if len(key) < view:

            diff = view - len(key)
            key = list(key)

            for y in range(diff):

                key.insert(0, str(0))

        key = "".join(key)


        # print(" ")
        # print(x)
        # print("int_rule_x")
        # print(int_rule)
        # print(int_rule[x])

        rules[tuple(key)] = int_rule[-x - 1]

    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


def viewer(c_a, y, view, v_0):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(c_a) - 1:

            v_0.append('0')

        else:

            v_0.append(str(c_a[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < 0:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(c_a[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(c_a, y, view, v_0)

        return v_0


def map(length, width, rule, base, start, direction, cell_patterns, path, plot=0):


    file = str(rule) + '-' + str(base) + '-' + str(width) + "X" + str(length)
    path_name = os.path.join(path, file)

    rules = rule_gen(rule, base)
    int_rule = rules[1]
    rules = rules[0]

    # print(" ")
    # print("rules")
    # print(rules)

    cnvs = np.zeros((length, width), dtype='int8')

    cnvs[0, start] = 1

    # for x in range(width):
    #     cnvs[0, x] = x

    print(" ")
    print("cnvs")
    print(cnvs)

    for x in range(length - 1):

        c_a = cnvs[x]

        print(" ")
        print("c_a")
        print(c_a)
        print(len(c_a))

        for y in range(len(c_a)):

            if direction != 0:

                y = len(c_a) - y - 1

            v_0 = []

            # print(" ")
            # print("y")
            # print(y)

            v_0 = tuple(viewer(c_a, y, view, v_0))

            # print("v_0")
            # print(v_0)

            # print("rule")
            # print(rules[v_0])

            cnvs[x + 1, y] = rules[v_0]

    # cnvs = np.flip(cnvs, 0)
    # cnvs = np.flip(cnvs, 1)

    print("cnvs")
    print(cnvs)



#export pcolormesh of cells

    if plot !=0:

        if base == 3:
            cMap = c.ListedColormap(['k', 'c', 'm'], 'tri', 3)

        if base == 2:
            cMap = c.ListedColormap(['w', 'k'])

        plt.pcolormesh(cnvs, cmap=cMap)

        # matplotlib.axes.Axes.set_aspect(plt, 'auto')

        axes = plt.gca()
        axes.set_aspect('auto')

        # plt.xticks(np.arange(0, width, step=1))
        # plt.yticks(np.arange(0, length, step=1))

        # plt.figtext(.3, .925, int_rule, fontsize=14)
        # plt.figtext(.0075, .05, rules, fontsize=7)
        # plt.grid(visible=True, axis='both', )

        # c_plt.show()
        plt.savefig(path_name, dpi=900)
        plt.close()
        plt.clf()

        del cnvs


#generate dictionary of cell value patterns

    # if rule == 1:
    #     v_pattern = []
    #
    #     for z in range(length):
    #         w = ''
    #         for a in range(width):
    #             w += "0"
    #
    #         w = int(w, 2)
    #
    #         v_pattern.append(str(w))
    #
    #     cell_patterns[(width, 0)] = v_pattern
    #
    # v_pattern = []
    #
    # for x in reversed(range(length)):
    #
    #     v = list(cnvs[x])
    #
    #     w = ''
    #
    #     for n in v:
    #         w += str(n)
    #
    #     w = int(w, 2)
    #
    #     # print("w")
    #     # print(w)
    #     # print(type(w))
    #
    #     v_pattern.append(str(w))
    #
    # cell_patterns[(width, rule)] = v_pattern
    close = 0

    while close == 0:

        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print(time)
        close = 1

    return int_rule

cell_patterns = dict()
path = 'output'



m = map(length, width, rule, base, start, direction, cell_patterns, path)