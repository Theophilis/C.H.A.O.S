
import numpy as np
from datetime import datetime
import random
import os
import pickle
import sys
import matplotlib.pyplot as plt
from matplotlib import colors


def base_x(n, b):
    e = n//b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, base, length):
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

        # if direction != 0:
        #     y = len(row_0) - y - 1

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


infile = open("polar maps/polar_u-64-16", "rb")
polar_u_i = pickle.load(infile)
infile.close


base = 2
view = 3

length = 16
max_steps = 8


message = ' the'

message_i = [ord(l) - 96 for l in message]

for m in message_i:
    if abs(m) == 64:
        message_i[message_i.index(m)] = 65

print(" ")
print("message")
print(message)
print(" ")
print("message_i")
print(message_i)

path = dict()

for x in range(len(message_i) - 1):

    front = message_i[x]
    back = message_i[x + 1]

    fb = (front, back)

    path[fb] = dict()

    path[fb][1] = []
    path[fb][2] = []

    for p in polar_u_i:

        if p[0] == front and p[1] == back:

            # print(" ")
            # print("p")
            # print(p)

            path[fb][1].append(p)

        elif p[0] == front and p[0] != p[1]:

            # print(" ")
            # print('front')
            # print(p)

            for o in polar_u_i:

                if p[1] == o[0] and o[1] == back:

                    path[fb][2].append((p, o))

        elif p[1] == back and p[0] != p[1]:

            # print(" ")
            # print('back')
            # print(p)

            for o in polar_u_i:

                if o[0] == front and o[1] == p[0]:

                    if (o, p) not in path[fb][2]:

                        path[fb][2].append((o, p))

                        # print("back match")

    if len(path[fb][1]) == 0 and len(path[fb][2]) == 0:

        print("")
        print("empty")
        print(fb)

        front_row = rule_gen(front, base, length)[1]
        back_row = rule_gen(back, base, length)[1]


        print(" ")
        print('fb rows')
        print(front_row)
        print(back_row)

        for x in range(base ** base ** view):

            steps = []
            steps.append(front_row)

            done = 0
            step_count = 0

            while done == 0:

                row = Color_cells(rule_gen(x, base, length)[0], length, steps[-1])[0]

                if row == back_row:

                    print(" ")
                    print('row')
                    print(row)
                    print(step_count)

                    polar = (front, back, x, step_count)

                    print('polar')
                    print(polar)

                    path[fb][1].append(polar)

                    if polar not in polar_u_i:

                        polar_u_i.append(polar)

                    done = 1

                elif step_count > max_steps:

                    done = 1

                else:

                    steps.append(row)
                    step_count += 1

                continue

        if len(path[fb][1]) == 0 and len(path[fb][2]) == 0:

            print("")
            print("empty 2")
            print(fb)

            print(" ")
            print('fb rows')
            print(front_row)
            print(back_row)

            for p in polar_u_i:

                if p[0] == front and p[0] != p[1] and p[-1] < int(max_steps/2):

                    p_1 = rule_gen(p[1], base, length)

                    for x in range(base ** base ** view):

                        steps = []
                        steps.append(front_row)

                        done = 0
                        step_count = 0

                        while done == 0:

                            row = Color_cells(rule_gen(x, base, length)[0], length, steps[-1])[0]

                            if row == back_row:

                                print(" ")
                                print('row')
                                print(row)
                                print(step_count)

                                polar = (front, back, x, step_count)

                                print('polar')
                                print(polar)

                                path[fb][1].append(polar)

                                if polar not in polar_u_i:
                                    polar_u_i.append(polar)

                                done = 1

                            elif step_count > max_steps:

                                done = 1

                            else:

                                steps.append(row)
                                step_count += 1

                            continue

                    continue

                if p[1] == back and p[0] != p[1] and p[-1] < int(max_steps/2):

                    continue










for p in path:
    print(" ")
    print("path")

    path[p][1] = sorted(path[p][1], key=lambda x:x[-1])
    path[p][2] = sorted(path[p][2], key=lambda x:x[0][-1] + x[1][-1])

    print(path[p][1][:10])
    print(path[p][2][:10])












