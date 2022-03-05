
#C.H.A.O.S

import numpy as np
from datetime import datetime
import random
import os
import pickle
import sys

rule = 90
#number who's x_base transformation gives the rules dictionary its values
view = 3
#size of the view window that scans a row for rule application
base = 2
#numerical base of the rule set. number of colors each cell can be
direction = 0
#if ^ = 0 view scans from left to right: else view scans right to left
match = 0

start_0 = 1
end_0 = 100


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


def viewer(row, y, view, v_0):

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

        if y - len(v_0) < 0:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(row[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(row, y, view, v_0)

        return v_0


def Color_cells(d_rule, cell_row_width, row_0):

    rc = []
    row_1 = [0 for x in range(cell_row_width)]


    for y in range(len(row_0)):

        if direction != 0:
            y = len(row_0) - y - 1

        v_0 = []

        # print(" ")
        # print("y")
        # print(y)

        v_0 = tuple(viewer(row_0, y, view, v_0))

        # print("v_0")
        # print(v_0)
        #
        # print("rule")
        # print(d_rule[v_0])

        rc.append(list(d_rule.keys()).index(v_0))

        row_1[y] = d_rule[v_0]

    return row_1, rc

duration = 0
rand_count = 0

journal = dict()
valid = dict()
page = []

def fold(row, goal, d_rule, v_rule, step_size, leash):

    page = []
    duration = 0
    match = 0

    page.append(row)

    while match == 0:

        row, rc = Color_cells(d_rule, len(goal), row)

        line = (row, rc)

        if row == goal:

            return duration

        if line in page:

            return -1

        else:

            page.append(line)

        if duration == step_size:

            if leash not in journal:

                journal[leash] = dict()

            journal[leash][v_rule] = page

            return -1

        duration += 1


def explore(start_0, end_0, results, base, step_size):

    leash = 0
    valid = dict()

    start = rule_gen(start_0, base)[1]
    goal = rule_gen(end_0, base)[1]

    print("start")
    print(start)
    print("goal")
    print(goal)

    while len(valid) < results:

        # print(" ")
        # print("leash")
        # print(leash)
        # print(len(valid))

        for x in range(base ** base ** view):

            if leash == 0:

                row = start

            else:

                if len(journal) == 0:

                    valid = dict(sorted(valid.items(), key=lambda x: x[1]))

                    return valid

                elif x in list(journal[leash - 1].keys()):

                    row = journal[leash - 1][x][-1][0]


                else:

                    continue

            d_rule, i_rule = rule_gen(x, base)

            span = fold(row, goal, d_rule, x, step_size, leash)

            if span != -1:

                if leash != 0:
                    span = span + leash * (step_size + 1)

                valid[x] = span

        if leash > 5:
            break

        leash += 1


    valid = dict(sorted(valid.items(), key=lambda x:x[1]))

    return valid


valid = explore(1, 100, 10, 2, 11)

print(" ")
print(valid)
print(len(valid))
