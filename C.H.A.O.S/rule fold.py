
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


def decimal(n, b):

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

    return value


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


def stream(front, back, front_row, back_row, max_steps):

    # print(" ")
    # print("stream")
    # print("front")
    # print(front_row)
    # print('back')
    # print(back_row)

    route = []

    for x in range(base ** base ** view):

        steps = []
        steps.append(front_row)

        done = 0
        step_count = 0

        while done == 0:

            step_count += 1

            row = Color_cells(rule_gen(x, base, length)[0], length, steps[-1])[0]

            if row == back_row:

                # print(" ")
                # print('row')
                # print(row)
                # print(step_count)

                polar = (front, back, x, step_count)

                # print('polar')
                # print(polar)

                route.append(polar)

                done = 1

            elif step_count > max_steps:

                done = 1

            else:

                steps.append(row)

    return route


infile = open("polar maps/polar_u-16", "rb")
polar_u_i = pickle.load(infile)
infile.close


base = 2
view = 3

length = 16
max_steps = 16
scale = 3


def fold(message, base, view, length, max_steps, scale):

    message_i = [(ord(l) - 96) * scale for l in message]

    max = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # print("max")
    # print(max)
    # print(len(max))

    max = decimal(max, 2)

    for m in range(len(message_i)):

        if message_i[m] > max:

            # print("greater")
            # print(message_i[m])
            # print(max)
            # print(str(message_i[m] % max))

            message_i[m] = message_i[m] % max

    # message_i.append(67)

    for m in message_i:
        if m < 0:
            message_i[message_i.index(m)] = 0


    print(" ")
    print("message")
    print(message)
    print(" ")
    print("message_i")
    print(message_i)
    print("scale")
    print(scale)

    path = dict()

    for x in range(len(message_i) - 1):

        front = message_i[x]
        back = message_i[x + 1]

        fb = (front, back)

        # print(" ")
        # print("fb")
        # print(fb)

        path[fb] = dict()

        path[fb][1] = []
        path[fb][2] = []

        #pre forged paths
        for p in polar_u_i:

            #full path
            if p[0] == front and p[1] == back and p[-1] < max_steps:

                # print(" ")
                # print("p")
                # print(p)

                path[fb][1].append(p)

            #front half path
            elif p[0] == front and p[0] != p[1]:

                # print(" ")
                # print('front')
                # print(p)

                for o in polar_u_i:

                    if p[1] == o[0] and o[1] == back:

                        path[fb][2].append((p, o))

            #back half path
            elif p[1] == back and p[0] != p[1]:

                # print(" ")
                # print('back')
                # print(p)

                for o in polar_u_i:

                    if o[0] == front and o[1] == p[0]:

                        if (o, p) not in path[fb][2]:

                            path[fb][2].append((o, p))

                            # print("back match")


        #new forged paths
        if len(path[fb][1]) == 0 and len(path[fb][2]) == 0:

            # print("")
            # print("empty")
            # print(fb)

            front_row = rule_gen(front, base, length)[1]
            back_row = rule_gen(back, base, length)[1]

            # print(" ")
            # print('fb rows')
            # print(front_row)
            # print(back_row)

            #fresh path

            route = stream(front, back, front_row, back_row, max_steps)

            for r in route:

                path[fb][1].append(r)

                if r not in polar_u_i:

                    polar_u_i.append(r)


            #split path
            if len(path[fb][1]) == 0 and len(path[fb][2]) == 0:

                # print("")
                # print("split path")
                # print(fb)
                #
                # print('fb rows')
                # print(front_row)
                # print(back_row)

                for p in polar_u_i:

                    #back forge
                    if p[0] == front and p[0] != p[1] and p[-1] < int(max_steps/2):

                        p_1 = rule_gen(p[1], base, length)[1]

                        # print(" ")
                        # print("p")
                        # print(p)
                        # print(p_1)
                        #
                        # print("back")
                        # print(back)
                        # print(back_row)

                        route = stream(p[1], back, p_1, back_row, max_steps)

                        if len(route) > 0:

                            for r in route:

                                path[fb][2].append((p, r))

                                if r not in polar_u_i:

                                    polar_u_i.append(r)

                    #front forge
                    if p[1] == back and p[0] != p[1] and p[-1] < int(max_steps/2):

                        # print("front forge")

                        p_0 = rule_gen(p[0], base, length)[1]

                        route = stream(front, p[0], front_row, p_0, max_steps)

                        if len(route) > 0:

                            for r in route:

                                path[fb][2].append((r, p))

                                if r not in polar_u_i:
                                    polar_u_i.append(r)

            if len(path[fb][1]) == 0 and len(path[fb][2]) == 0:

                depth = 2

                routes = []

                joint = 0

                while len(routes) == 0:

                    route = []

                    joint_row = rule_gen(joint, base, length)[1]

                    for x in range(depth):

                        if x == 0:

                            front_route = stream(front, joint, front_row, joint_row, max_steps)

                            back_route = stream(joint, back, joint_row, back_row, max_steps)

                            if len(front_route) > 0 and len(back_route) > 0:

                                for f in front_route:

                                    if f not in polar_u_i:

                                        polar_u_i.append(f)

                                    for b in back_route:

                                        if b not in polar_u_i:

                                            polar_u_i.append(b)

                                        routes.append((f, b))

                    joint += 1

                for r in routes:

                    if len(r) not in path[fb]:

                        path[fb][len(r)] = []

                    path[fb][len(r)].append(r)

    frame = []

    for p in path:

        # print(" ")
        # print("path")

        path[p][1] = sorted(path[p][1], key=lambda x:x[-1])
        path[p][2] = sorted(path[p][2], key=lambda x:x[0][-1] + x[1][-1])

        # print(path[p][1][:10])
        # print(path[p][2][:10])

        if len(path[p][1]) > 0:

            frame.append(path[p][1][0])

        else:

            frame.append(path[p][2][0][0])
            frame.append(path[p][2][0][1])


    canvas = []
    sum = 0

    print(" ")
    print('frame')
    print(frame)

    for f in frame:

        # print(" ")
        # print('f')
        # print(f)

        sum += f[-1]

        steps = []
        step_count = 0

        f_0 = rule_gen(f[0], base, length)[1]
        steps.append(f_0)

        # print(f_0)

        while step_count < f[-1]:

            row = Color_cells(rule_gen(f[2], base, length)[0], length, steps[-1])[0]

            steps.append(row)

            step_count += 1

        for s in steps:

            canvas.append(s)


    print(" ")
    print('canvas')
    print(len(canvas))


    canvas = np.asarray(canvas)
    canvas = np.rot90(canvas)

    cMap = colors.ListedColormap(['w', 'k'])

    ax = plt.gca()
    ax.set_aspect(1)

    filename = 'polar maps/polar_u-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(polar_u_i, outfile)
    outfile.close()

    plt.pcolormesh(canvas, cmap=cMap)

    # plt.show()

    path = 'cell translation'

    file = str(message) + str('-') + str(scale)
    path_name = os.path.join(path, file)

    plt.savefig(path_name, dpi=200)
    plt.close()


message = ' beauty will save the world'

for x in range(1, 17):

    print(" ")
    print('x')
    print(x)

    fold(message, base, view, length, max_steps, x)










