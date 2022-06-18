# C.H.A.O.S

import numpy as np
from datetime import datetime
import random
import pygame
import os
import pickle
import sys
import pygame.midi
import time
from collections import deque

sys.setrecursionlimit(999999999)

pygame.font.init()

length = 8
# number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
# number of cells in a row
rule = 90
# number who's x_base transformation gives the rules dictionary its values
view = 3
# size of the view window that scans a row for rule application
base = 2
# numerical base of the rule set. number of colors each cell can be
start = length
# position for a row 0 cell value 1
direction = 0


# if ^ = 0 view scans from left to right: else view scans right to left


#####to do#####
# translate complex numbers (pi, phi, e) to a base n digit sequence(where n is the number of possible rule states to be called).
##Then, trigger a rotation of a rule state based on the rule position given by the digit in the complex number

# add a record feature and button to menu. allows for recorder of all key inputs in a text file.


#####map#####

def base_x(n, b):

    e = n // b
    q = n % b

    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def base_x_10(coord, n, b):

    e = n // b
    q = n % b

    if n == 0:
        coord.append(0)
        return coord

    elif e == 0:
        coord.append(q)
        return coord

    else:
        coord.append(q)
        coord = base_x_10(coord, e, b)
        return coord


def decimal(n, b):

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

    return value


def rule_gen(rule, base=2):

    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(int(rule), (base))

    x = int_rule[::-1]

    while len(x) < base ** view:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        int_rule.append(int(i))

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
        rules[tuple(key)] = int(int_rule[-x - 1])
    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


def rule_gen_2(rule, base, length):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(rule, base)

    x = int_rule[::-1]

    while len(x) < length:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        int_rule.append(int(i))

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
        rules[tuple(key)] = int(int_rule[-x - 1])
    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


def rule_gen_10(rule, base, length):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = list(reversed(base_x_10([], rule, base)))

    x = int_rule[::-1]

    while len(x) < length:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        int_rule.append(int(i))

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
        rules[tuple(key)] = int(int_rule[-x - 1])
    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


def viewer_1d(row, y, view, v_0):
    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(row) - 1:

            v_0.append('0')

        else:

            v_0.append(str(row[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < -1:

            v_0.insert(0, '1')

        else:

            v_0.insert(0, str(row[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer_1d(row, y, view, v_0)

        return v_0


def Color_cells_1d(d_rule, cell_row_width, row_0):

    # print("")
    # print("row_0")
    # print(row_0)

    row_1 = np.zeros((1, cell_row_width), dtype='int8')

    row_1[0] = [d_rule[tuple(viewer_1d(row_0, x, view, []))] for x in range(len(row_0))]

    return row_1

bbv = base ** base ** view
domain = 8

start = 7
goal = 22

d_rule, i_rule = rule_gen(30, base)

start_row = rule_gen_2(start, base, domain)[1]
goal_row = rule_gen_2(goal, base, domain)[1]

print(start_row)
print(goal_row)




theory_board_size = []

for x in range(base):

    theory_board_size.append(base ** view)

theory_board_size.append(base)

print("###theory_board###")
print(theory_board_size)
# print(theory_board)


coords = []

for x in range((base ** view) * (base ** view) * base):

    coords.append(tuple(reversed(rule_gen_10(x, base ** view, base + 1)[1])))

print("")
print("coords")
print(coords)
print(len(coords))

theory_board = np.zeros((theory_board_size), dtype='uint8')

rc_count = dict()
for k in d_rule:
    rc_count[k] = 0

for x in range(len(start_row)):
    v_0 = tuple(viewer_1d(start_row, x, view, []))

    rc_count[v_0] += 1

base_scores = {}
for x in range(base):
    base_scores[x] = 0

    for y in range(len(i_rule)):

        if i_rule[y] == x:
            base_scores[x] += list(rc_count.values())[y]

for c in coords:

    # print("")
    # print("c")
    # print(c)

    deflect = 0

    # print("")
    # print('c')
    # print(c)
    # print('base_scores')
    # print(base_scores[c[-1]])
    # print('i_rule')
    # print(i_rule)
    # print('rc_count.values()')
    # print(list(rc_count.values()))

    theory_score = base_scores[c[-1]]

    polarity = []

    for o in c[:-1]:

        # print('o')
        # print(o)

        if c[:-1].count(o) > 1:
            deflect = 1

    if deflect == 0:

        # print("")
        # print("hit")

        for x in range(base):

            # print('x')
            # print(x)

            if x == c[-1] and i_rule[-(c[x] + 1)] != c[-1]:

                # print("gain")
                # print(list(rc_count.values())[-(c[x] + 1)])

                theory_score += list(rc_count.values())[-(c[x] + 1)]

            elif x != c[-1] and i_rule[-(c[x] + 1)] == c[-1]:

                # print('loss')
                # print(list(rc_count.values())[-(c[x] + 1)])

                theory_score -= list(rc_count.values())[-(c[x] + 1)]

    theory_board[tuple(c)] = theory_score


print(theory_board)
