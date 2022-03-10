
#C.H.A.O.S

import numpy as np
from datetime import datetime
import random
import os
import pickle
import sys
import matplotlib.pyplot as plt
from matplotlib import colors

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

#####things to do#####

#expand the row lengths for the cellular automata

#experiment with different view lengths

#experiments with different bases


#cellular automata generation functions

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


#folding functions

def fold(journal, row, goal, d_rule, v_rule, step_size, leash):

    page = []
    duration = 0
    match = 0

    page.append(row)

    if leash not in journal:
        journal[leash] = dict()

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

            journal[leash][v_rule] = page

            return -1

        duration += 1


def carve(journal, start_0, end_0, results, base, step_size):

    leash = 0
    valid = []

    start = rule_gen(start_0, base)[1]
    goal = rule_gen(end_0, base)[1]

    # print("start")
    # print(start)
    # print("goal")
    # print(goal)

    while len(valid) < results:

        # print(" ")
        # print("leash")
        # print(leash)
        # print(len(valid))

        for x in range(base ** base ** view):

            if leash == 0:

                row = start

            else:

                # print("journal[leash - 1]")
                # print(journal[leash - 1])

                if len(journal[leash - 1]) == 0:

                    valid = sorted(valid, key=lambda x: x[1])

                    return valid

                elif x in list(journal[leash - 1].keys()):

                    row = journal[leash - 1][x][-1][0]


                else:

                    continue

            d_rule, i_rule = rule_gen(x, base)

            span = fold(journal, row, goal, d_rule, x, step_size, leash)

            if span != -1:

                if leash != 0:
                    span = span + leash * (step_size + 1)

                valid.append((start_0, end_0, x, span + 1))

        leash += 1


    valid = sorted(valid, key=lambda x:x[0])

    return valid


def rolling_river(journal, dot, vector, validity, polar):

    valid = carve(journal, dot, vector, base ** base ** view, 2, base ** base ** view)

    # print(valid)
    if len(valid) == 0:
        validity.append([(dot, vector)])

    else:
        validity.append(valid)

    for v in valid:
        polar.append(v)

    validity = sorted(validity, key=lambda x:len(x) + len(x[0]))

    polar_u = []

    for p in polar:

        if p not in polar_u:
            polar_u.append(p)

    return validity, polar, polar_u

    # print("river")
    # print(river)


def bend(confluence, polar_u, elbows_0, v, v_0, depth, c_d=2):

    # print(" ")
    # print("currend_depth")
    # print(c_d)

    elbows_1 = []

    for e in elbows_0:

        for p in polar_u:

            # print("")
            # print("e")
            # print(e)
            # print("p")
            # print(p)

            if e[-1][1] == p[0] and p[1] != v[0][0]:
                # print("")
                # print("e")
                # print(e)
                # print("p")
                # print(p)

                e_p = e[::]
                e_p.append(p)

                # print("e_p")
                # print(e_p)

                elbows_1.append(e_p)

            if e[-1][1] == p[0] and p[1] == v[0][1]:

                confluence[v_0][c_d].append((e, p))

    c_d += 1

    if c_d == depth:

        # print(" ")
        # print('#####done#####')

        return elbows_1

    else:

        # print(" ")
        # print("#####recur#####")

        print(depth)

        bend(confluence, elbows_1, v, depth, c_d)


def converge(validity, confluence, depth, max_distance, polar_u):

    for v in validity:

        # print(validity.index(v))
        # print(len(validity))

        elbows = []

        v_0 = (v[0][0], v[0][1])

        if v_0 not in confluence:

            confluence[v_0] = dict()

            for r in range(depth):
                confluence[v_0][r] = []

        if len(v[0]) == 2:

            # print("dry")
            # print(v)

            for p in polar_u:

                if v[0][0] == p[0] and p[1] != v[0][0]:
                    p_list = [p]

                    elbows.append(p_list)

            if len(v[0]) == 2:

                if len(elbows) > 0:
                    # print("bend")
                    # print(v)
                    # print(r)
                    # print(depth)
                    # print(elbows)

                    bend(confluence, polar_u, elbows, v, v_0, depth)

                    elbows = []

            # print("elbows")

        if len(v[0]) == 4 and v[0][3] > max_distance:

            # print("flooding")
            # print(v)

            for p in polar_u:

                if v[0][0] == p[0] and p[1] != v[0][0]:
                    p_list = [p]

                    elbows.append(p_list)

        if len(v[0]) == 4:

            if len(elbows) > 0:
                # print("bend")
                # print(v)
                # print(r)
                # print(depth)
                # print(elbows)

                bend(confluence, polar_u, elbows, v, v_0, depth)

        confluence[v_0][1] = v


def flow(input, depth, max_distance, w_s = 0):

    journal = dict()
    confluence = dict()
    polarity = dict()

    validity = []
    polar = []

    # print("")

    for z in range(len(input) - 1):

        x = input[z]
        y = input[z + 1]

        # print((x, y))

        validity, polar, polar_u = rolling_river(journal, x, y, validity, polar)

    converge(validity, confluence, depth, max_distance, polar_u)

    # print("")
    # print("confluence")
    #
    # for c in list(confluence.keys())[:10]:
    #
    #     print(" ")
    #     print("c_r")
    #
    #     for r in range(1, depth):
    #
    #         if len(confluence[c][r]) > 0:
    #
    #             confluence[c][r] = sorted(confluence[c][r], key=lambda x:x[3])
    #
    #             print(c)
    #             print(confluence[c][r][:5])


    for p in polar:

        cell = (p[2], p[3])

        if cell not in polarity:

            polarity[cell] = 1

        else:

            polarity[cell] += 1

    polarity = dict(sorted(polarity.items(), key=lambda x:x[1], reverse=True))

    # print(" ")
    # print("polarity")
    # print(len(polarity))
    #
    # for p in list(polarity.items())[:10]:
    #     print(p)

    return confluence, polarity


def cell_translate(depth, max_distance, message):
    message_i = [ord(l) - 96 for l in message]

    for m in message_i:
        if abs(m) == 64:
            message_i[message_i.index(m)] = 255

    print("")
    print(message_i)

    confluence, polarity = flow(message_i, depth, max_distance)

    sum = 0
    basin = []

    for c in confluence:

        print(" ")
        print("confluence")
        print(confluence[c][1])
        print(confluence[c][2])

        if len(confluence[c][1][0]) == 2:

            basin.append(confluence[c][2][0])

            print(confluence[c][2][0])
            print(confluence[c][2][0][0][0][3])

            sum += confluence[c][2][0][0][0][3]
            sum += confluence[c][2][0][1][3]

        else:

            basin.append(confluence[c][1][0])

            sum += confluence[c][1][0][3]


    basin_o = []
    for m in range(len(message_i) - 1):

        x = message_i[m]
        y = message_i[m + 1]

        for b in basin:

            if b[0] == x and b[1] == y:

                basin_o.append(b)


    print(" ")
    print("sum")
    print(sum)

    print('basin')
    print(basin_o)
    print(" ")

    canvas = []

    for b in basin_o:

        print(basin_o.index(b))
        print(b)

        d_rule, i_rule = rule_gen(b[2], base)
        row = rule_gen(b[0], base)[1]
        letter_break = [2 for n in range(len(row))]

        canvas.append(row)

        steps = 0

        while steps < b[3]:

            row = Color_cells(d_rule, len(row), row)[0]

            canvas.append(row)

            steps += 1

        canvas.append(letter_break)
        # canvas.append(letter_break)
        # canvas.append(letter_break)

    print(" ")
    print('canvas')

    for c in canvas:
        print(c)

    canvas = np.asarray(canvas)
    # canvas = np.flip(canvas, 0)
    canvas = np.rot90(canvas)

    print("")
    print(canvas)

    path = 'cellular-script'
    file = message + '_cellular-script'
    path_name = os.path.join(path, file)

    ax = plt.gca()
    ax.set_aspect(1)

    plt.margins(0, None)

    if base == 4:
        cMap = colors.ListedColormap(['k', (0, .5, 1), (0, 1, .5), (1, 0, .5)], 'quad', 4)

    # if base == 3:
    cMap = colors.ListedColormap(['k', 'm', 'c'], 'tri', 3)

    # if base == 2:
    #     cMap = colors.ListedColormap(['w', 'k'])

    plt.pcolormesh(canvas, cmap=cMap)

    # plt.xticks(np.arange(0, width, step=1))
    # plt.yticks(np.arange(0, length, step=1))
    #
    plt.figtext(.125, .625, message, fontsize=16)
    # plt.figtext(.0075, .05, rules, fontsize=7)
    # plt.grid(visible=True, axis='both', )

    # c_plt.show()
    plt.savefig(path_name, dpi=900)
    plt.close()


depth = 3
max_distance = 10
domain = 64

journal = dict()
confluence = dict()
polarity = dict()

validity = []
polar = []


for x in range(domain):

    print(x)

    for y in range(domain):
        validity, polar, polar_u = rolling_river(journal, x, y, validity, polar)


print(" ")
print("polar_u")
print(len(polar_u))


filename = 'polar maps/polar_u-' + str(domain)
outfile = open(filename, 'wb')
pickle.dump(polar_u, outfile)
outfile.close()
