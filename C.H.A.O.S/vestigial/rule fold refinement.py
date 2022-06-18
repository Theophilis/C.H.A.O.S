
import numpy as np
from datetime import datetime
import random
import os
import pickle
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation



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

        # print("color_cells")
        # print("y")
        # print(y)
        # print('len(row_1)')
        # print(len(row_1))
        # print("v_0")
        # print(v_0)

        row_1[y] = d_rule[v_0]

    return row_1, rc


def route_map(length, width, rule, base, start):

    canvas = np.zeros((width, length), dtype='int8')

    # print("")
    # print("canvas")
    # print(canvas)

    rules, int_rule = rule_gen(rule, base, length)

    start = rule_gen(abs(start), base, length)[1]

    canvas_0 = np.copy(canvas)

    canvas_0[0] = start

    # print(" ")
    # print('canvas_0')
    # print(canvas_0)

    for x in range(length - 1):

        c_a = canvas_0[x]

        # print(" ")
        # print("c_a")
        # print(c_a)

        for y in range(len(c_a)):

            v_0 = []

            # print(" ")
            # print("y")
            # print(y)

            v_0 = tuple(viewer(c_a, y, view, v_0))

            # print("v_0")
            # print(v_0)
            #
            # print("rule")
            # print(rules[v_0])
            # print("rc")
            # print(list(rules.keys()).index(v_0))

            if canvas[x + 1, y] == 1:
                continue

            else:
                canvas_0[x + 1, y] = rules[v_0]

    for x in range(length):
        for y in range(width):
            if canvas[x, y] == 1:
                canvas_0[x, y] = base

    canvas_0 = np.flip(canvas_0, 0)

    # print("")
    # print("canvas_0")
    # print(canvas_0)

    return canvas_0


def canvas_stream(front, back, front_row, back_row, max_steps):

    # print(" ")
    # print("stream")
    # print("front")
    # print(front_row)
    # print('back')
    # print(back_row)

    route = []

    for x in range(base ** base ** view):

        # print(" ")
        # print("x")
        # print(x)

        canvas = route_map(max_steps, length, x, base, front)

        for y in range(max_steps):

            # print("")
            # print('canvas_row')
            # print(list(canvas[y]))
            # print(back_row)

            if list(canvas[y]) == back_row:

                polar = (front, back, x, y + 1)

                route.append(polar)

    return route


def stream(front, back, front_row, back_row, max_steps, roam):

    # print(" ")
    # print("stream")
    # print("front")
    # print(front_row)
    # print('back')
    # print(back_row)

    infile = open("../organized-rules/roamers-2-3", "rb")
    roamers = pickle.load(infile)
    infile.close

    infile = open("../organized-rules/right_roam-2-3", "rb")
    right_roam = pickle.load(infile)
    infile.close

    infile = open("../organized-rules/left_roam-2-3", "rb")
    left_roam = pickle.load(infile)
    infile.close

    infile = open("../organized-rules/no_roam-2-3", "rb")
    no_roam = pickle.load(infile)
    infile.close

    route = []

    if roam == 0:

        for x in roamers:

            steps = []
            steps.append(front_row)

            done = 0
            step_count = 0

            while done == 0:

                step_count += 1

                # print("stream row")
                # print("rule_gen")
                # print(rule_gen(x, base, length)[0])
                # print("length")
                # print(length)
                # print("steps[-1]")
                # print(steps[-1])

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

    if roam == 1:

        for x in right_roam:

            steps = []
            steps.append(front_row)

            done = 0
            step_count = 0

            while done == 0:

                step_count += 1

                # print("stream row")
                # print("rule_gen")
                # print(rule_gen(x, base, length)[0])
                # print("length")
                # print(length)
                # print("steps[-1]")
                # print(steps[-1])

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

    if roam == 2:

        for x in left_roam:

            steps = []
            steps.append(front_row)

            done = 0
            step_count = 0

            while done == 0:

                step_count += 1

                # print("stream row")
                # print("rule_gen")
                # print(rule_gen(x, base, length)[0])
                # print("length")
                # print(length)
                # print("steps[-1]")
                # print(steps[-1])

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

    if roam == 3:

        for x in no_roam:

            steps = []
            steps.append(front_row)

            done = 0
            step_count = 0

            while done == 0:

                step_count += 1

                # print("stream row")
                # print("rule_gen")
                # print(rule_gen(x, base, length)[0])
                # print("length")
                # print(length)
                # print("steps[-1]")
                # print(steps[-1])

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


def fold(message, base, view, length, max_steps, scale, level, polar_paths, polar_u_i, polar_d, plot=0):

    message_t = []

    if scale == 0:

        # print(" ")
        # print('scale = 0')
        # print("multiple")

        message_i = [(ord(l) - 96) * level for l in message]

    elif scale == 1:

        message_i = [(ord(l) - 96) * base ** level for l in message]

    elif scale == 2:

        message_i = [(ord(l) - 96) for l in message]

        # print("message_i")
        # print(message_i)

        for m in message_i:
            if m < 0:
                message_i[message_i.index(m)] = 0

        message_i = [n ** level for n in message_i]

    # print("message_i")
    # print(message_i)

    max = base ** length - 1

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

    for x in range(len(message_i) - 1):

        message_t.append((message_i[x], message_i[x + 1]))

    # print(" ")
    print("message")
    print(message)
    # print(" ")
    print("message_i")
    print(message_i)
    # print(len(message_i))
    print("message_t")
    print(message_t)
    # print("scale")
    # print(scale)

    path = dict()

    #path finder
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
        path[fb][3] = []

        if fb in polar_paths:

            pp_fb = polar_paths[fb][0]

            # print(" ")
            # print("pp_fb")
            # print(pp_fb)
            # print(len(pp_fb))

            if type(pp_fb[0]) == int:

                # print("one")

                path[fb][1].append(pp_fb)

            elif len(pp_fb) == 2:

                # print("two")

                path[fb][2].append(pp_fb)

            elif len(pp_fb) == 3:

                # print("three")

                path[fb][3].append(pp_fb)

        else:

            #pre forged paths
            for p in polar_u_i:

                #full path
                if p[0] == front and p[1] == back and p[-1] < max_steps:

                    # print(" ")
                    # print("p")
                    # print(p)

                    path[fb][1].append(p)

                #front half path
                elif p[0] == front and p[0] != p[1] and p[1] != back:

                    # print(" ")
                    # print('front')
                    # print(p)

                    p1_b = (p[1], back)

                    if p1_b in polar_paths:

                        pp_fb = polar_paths[p1_b][0]

                        # print(" ")
                        # print("pp_fb")
                        # print(pp_fb)
                        # print(len(pp_fb))

                        if type(pp_fb[0]) == int:
                            # print("one")

                            path[fb][2].append((p, pp_fb))

                    else:

                        for o in polar_u_i:

                            if p[1] == o[0] and o[1] == back:

                                path[fb][2].append((p, o))

                            if len(path[fb][3]) < max_steps:

                                if p[1] == o[0] and o[0] != o[1]:

                                    for l in polar_u_i:

                                        if o[1] == l[0] and l[1] == back:

                                            # print(" ")
                                            # print("triple")

                                            path[fb][3].append((p, o, l))


                #back half path
                elif p[1] == back and p[0] != p[1]:

                    # print(" ")
                    # print('back')
                    # print(p)

                    f_p0 = (front, p[0])

                    if f_p0 in polar_paths:

                        pp_fb = polar_paths[f_p0][0]

                        # print(" ")
                        # print("pp_fb")
                        # print(pp_fb)
                        # print(len(pp_fb))

                        if type(pp_fb[0]) == int:
                            # print("one")

                            path[fb][2].append((pp_fb, p))

                    else:

                        for o in polar_u_i:

                            if o[0] == front and o[1] == p[0]:

                                if (o, p) not in path[fb][2]:

                                    path[fb][2].append((o, p))

                                    # print("back match")

                            if len(path[fb][3]) < max_steps:

                                if o[1] == p[0] and o[0] != o[1]:

                                    for l in polar_u_i:

                                        if l[0] == front and l[1] == o[0]:

                                            # print("")
                                            # print("triple")

                                            if (l, o, p) not in path[fb][3]:

                                                path[fb][3].append((l, o, p))


            #fresh forged paths
            if len(path[fb][1]) == 0 and len(path[fb][2]) == 0 and len(path[fb][3]) == 0:

                print("")
                print(fb)
                print("fresh forged")

                front_row = rule_gen(front, base, length)[1]
                back_row = rule_gen(back, base, length)[1]

                # print(" ")
                # print('fb rows')
                # print(front_row)
                # print(back_row)

                #fresh path
                roam = 0
                route = []

                while len(route) == 0:

                    route = stream(front, back, front_row, back_row, max_steps, roam)

                    roam += 1

                    if roam > 3:

                        break

                #one step path
                for r in route:

                    path[fb][1].append(r)

                    if r not in polar_u_i:

                        # print("new")
                        # print("r")
                        # print(r)

                        polar_u_i.append(r)
                        polar_d[r] = 0

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

                            roam = 0
                            route = []

                            while len(route) == 0:

                                route = stream(p[1], back, p_1, back_row, max_steps, roam)

                                roam += 1

                                if roam > 3:

                                    break

                            if len(route) > 0:

                                for r in route:

                                    path[fb][2].append((p, r))

                                    if r not in polar_u_i:

                                        # print("new")
                                        # print("r")
                                        # print(r)

                                        polar_u_i.append(r)
                                        polar_d[r] = 0

                        #front forge
                        if p[1] == back and p[0] != p[1] and p[-1] < int(max_steps/2):

                            # print("front forge")

                            p_0 = rule_gen(p[0], base, length)[1]

                            roam = 0

                            while len(route) == 0:

                                route = stream(front, p[0], front_row, p_0, max_steps, roam)

                                roam += 1

                                if roam > 3:

                                    break

                            if len(route) > 0:

                                for r in route:

                                    path[fb][2].append((r, p))

                                    if r not in polar_u_i:

                                        # print("new")
                                        # print("r")
                                        # print(r)

                                        polar_u_i.append(r)
                                        polar_d[r] = 0

                #n step paths
                if len(path[fb][1]) == 0 and len(path[fb][2]) == 0:

                    # print("n step paths")
                    # print("joint")

                    routes = []

                    joint = 0

                    while len(routes) == 0:

                        print(joint)

                        joint_row = rule_gen(joint, base, length)[1]

                        roam = 0
                        front_route = []
                        back_route = []

                        while len(front_route) == 0:

                            front_route = stream(front, joint, front_row, joint_row, max_steps, roam)

                            roam += 1

                            if roam > 3:

                                break

                        # print(" ")
                        # print('stream, back_route')
                        # print("joint")
                        # print(joint)
                        # print("back")
                        # print(back)
                        # print('joint row')
                        # print(joint_row)
                        # print("back row")
                        # print(back_row)
                        # print('max steps')
                        # print(max_steps)

                        roam = 0

                        while len(back_route) == 0:

                            back_route = stream(joint, back, joint_row, back_row, max_steps, roam)

                            roam += 1

                            if roam > 3:

                                break

                        # print(len(front_route))
                        # print(len(back_route))

                        # if len(front_route) > 0 or len(back_route) > 0:
                        #
                        #     print((len(front_route), len(back_route)))


                        if len(front_route) > 0 and len(back_route) > 0:

                            # print("valid route")

                            for f in front_route:

                                if f not in polar_u_i:

                                    # print("new")
                                    # print("f")
                                    # print(f)

                                    polar_u_i.append(f)
                                    polar_d[f] = 0

                                for b in back_route:

                                    if b not in polar_u_i:

                                        # print("new")
                                        # print("b")
                                        # print(b)

                                        polar_u_i.append(b)
                                        polar_d[b] = 0

                                    routes.append((f, b))


                        if joint > base ** length:

                            # print("broken")

                            break

                        joint += 1


                    if len(routes) == 0:

                        for y in range(base ** length):

                            if len(routes) > 0:

                                break

                            joint_row_0 = rule_gen(y, base, length)[1]

                            for z in range(base ** length):

                                if len(routes) > 0:

                                    break

                                joint_row_1 = rule_gen(z, base, length)[1]

                                roam = 0

                                while len(front_route) == 0:

                                    front_route = stream(front, joint, front_row, joint_row, max_steps, roam)

                                    roam += 1

                                    if roam > 3:
                                        break

                                roam = 0

                                while len(middle_route) == 0:

                                    middle_route = stream(y, z, joint_row_0, joint_row_1, max_steps, roam)

                                    roam += 1

                                    if roam > 3:
                                        break

                                roam = 0

                                while len(back_route) == 0:

                                    back_route = stream(joint, back, joint_row, back_row, max_steps, roam)

                                    roam += 1

                                    if roam > 3:
                                        break

                                if len(front_route) > 0 and len(middle_route) > 0 and len(back_route) > 0:

                                    for f in front_route:

                                        if f not in polar_u_i:

                                            # print("new")
                                            # print("f")
                                            # print(f)

                                            polar_u_i.append(f)
                                            polar_d[f] = 0

                                            for m in middle_route:

                                                if m not in polar_u_i:

                                                    polar_u_i.append(m)
                                                    polar_d[m] = 0

                                                for b in back_route:

                                                    if b not in polar_u_i:

                                                        # print("new")
                                                        # print("b")
                                                        # print(b)

                                                        polar_u_i.append(b)
                                                        polar_d[b] = 0

                                                        print(" ")
                                                        print("triple")
                                                        print((f, m, b))

                                                    routes.append((f, m, b))


                    for r in routes:

                        if len(r) not in path[fb]:

                            path[fb][len(r)] = []

                        path[fb][len(r)].append(r)


    frame = []

    # print("")
    # print("path")
    # print(len(list(path.keys())))
    # print(list(path.keys()))

    pos = 0

    for m in message_t:

        # print(" ")
        # print("path")

        path[m][1] = sorted(path[m][1], key=lambda x:x[-1])
        path[m][2] = sorted(path[m][2], key=lambda x:x[0][-1] + x[1][-1])
        path[m][3] = sorted(path[m][3], key=lambda x:x[0][-1] + x[1][-1] + x[2][-1])
        #
        # print(" ")
        # print("m")
        # print(m)
        # print(path[m][1][:10])
        # print(path[m][2][:10])
        # print(path[m][3][:10])


        if len(path[m][1]) > 0:

            frame.append(path[m][1][0])

            # message_l[pos].append(path[m][1][0][-1] + 1)

        elif len(path[m][2]) > 0:

            frame.append(path[m][2][0])

            # message_l[pos].append(path[m][2][0][0][-1] + path[m][2][0][1][-1] + 2)

        else:

            frame.append(path[m][3][0])

        pos += 1

    # print("")
    # print('message_l')
    # print(message_l)


    filename = 'polar maps/polar_u_c-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(polar_u_i, outfile)
    outfile.close()

    if plot != 0:

        canvas = []
        sum = 0

        print(" ")
        print('frame')
        print(frame)

        for f in frame:

            print(" ")
            print('f')
            print(f)

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

        plt.pcolormesh(canvas, cmap=cMap)

        # plt.show()

        path = '../cell translation'

        file = str(message) + str('-') + str(level)
        path_name = os.path.join(path, file)

        plt.savefig(path_name, dpi=200)
        plt.close()

    print("")
    print("frame")
    print(frame)

    return frame


def paint(cellexicon, cell_key, message, base, view, length, max_steps, depth, polar_paths, polar_u_i, polar_d, scale, vid=0):

    canvas = dict()
    rcanvas = dict()

    final_height = len(message) * length
    final_length = 0

    for m in message:

        print(m)
        print(message.index(m))

        canvas[message.index(m) + 1] = dict()
        rcanvas[message.index(m) + 1] = dict()

        frames = []
        message_l = dict()

        # print(list(polar_d)[:10])
        # print(list(polar_d)[0])
        # print(list(polar_d)[0][1])

        for x in range(len(m) - 1):

            message_l[x] = []

        for x in range(depth):

            bibliod = 0
            x = x + 1

            print(" ")
            print('x')
            print(x)

            if m not in cellexicon[cell_key]:

                cellexicon[cell_key][m] = dict()

                if x not in cellexicon[cell_key][m]:

                    cellexicon[cell_key][m][x] = []

            else:

                # print("message is in cellexicon")

                if x not in cellexicon[cell_key][m]:

                    cellexicon[cell_key][m][x] = []

                else:

                    # print("depth is in cellexicon")
                    #
                    # print(" ")
                    # print('bibliod')
                    # print(message)
                    # print(x)

                    bibliod = 1

                    # message_l = cellexicon[cell_key][message][x][0][1]

            if bibliod == 1:

                # print(cellexicon[cell_key][message][x])

                try:

                    frames.append(cellexicon[cell_key][m][x][0])

                except:

                    frames.append(fold(m, base, view, length, max_steps, scale, x, polar_paths, polar_u_i, polar_d))

                # print('cellexicon message')
                # print(cellexicon[message])
                # print(cellexicon[message][x][0])
                # print(cellexicon[message][x][0][0])
                # print(cellexicon[message][x][0][1])

            else:

                frames.append(fold(m, base, view, length, max_steps, scale, x, polar_paths, polar_u_i, polar_d))

        # print(" ")
        # print('message_l')

        l_l = []
        sum = len(m) - 1


        for frame in frames:

            pos = 0

            # print("")
            # print("frame")
            # print(frame)

            for f in frame:

                if type(f[0]) == int:

                    # print("single")
                    # print(f[-1])

                    message_l[pos].append(f[-1] + 1)

                else:

                    # print('double')
                    # print(f[0][-1] + f[1][-1])

                    message_l[pos].append(f[0][-1] + f[1][-1] + 2)

                pos += 1

        for ml in message_l:

            message_l[ml] = sorted(message_l[ml], reverse=True)

            l_l.append(message_l[ml][0])
            sum += message_l[ml][0]

            # print(" ")
            # print(m)
            # print(message_l[m])

        print(" ")
        print("l_l")
        print(l_l)
        print(sum)


        # print(" ")
        # print('letter length')
        # print(l_l)
        # print(sum)
        # print(" ")
        # print(len(frames))
        # print(frames)

        pos = 1

        for frame in frames:

            # print(" ")
            # print("frame")
            # print(frames.index(frame))
            # print(frame)

            print("pos")
            print(pos)

            if frame not in cellexicon[cell_key][m][pos]:

                    cellexicon[cell_key][m][pos].append(frame)

            canvas[message.index(m) + 1][pos] = []
            rcanvas[message.index(m) + 1][pos] = []

            for x in range(len(frame)):

                # print(" ")
                # print("x ")
                # print(x)
                # print(l_l[x])
                # print(frame[x])

                f = frame[x]

                # print(" ")
                # print("f")
                # print(f)

                if type(frame[x][0]) == int:

                    # print("")
                    # print('single')

                    if f not in polar_d:

                        polar_d[f] = 0

                    polar_d[f] += 1

                    steps = []
                    rcs = []
                    step_count = 0

                    row = rule_gen(f[0], base, length)[1]
                    f_1 = rule_gen(f[1], base, length)[1]
                    # steps.append(f_0)

                    # print(f_0)

                    while step_count < f[-1]:

                        row, rc = Color_cells(rule_gen(f[2], base, length)[0], length, row)

                        steps.append(row)
                        rcs.append(rc)

                        # print("rc")
                        # print(rc)
                        # print(step_count)

                        step_count += 1

                    # while step_count < f[-1]:
                    #
                    #     row, rc = Color_cells(rule_gen(f[2], base, length)[0], length, steps[-1])
                    #
                    #     steps.append(row)
                    #     rcs.append(rc)
                    #
                    #     # print("rc")
                    #     # print(rc)
                    #     # print(step_count)
                    #
                    #     step_count += 1

                    # print(" ")
                    # print("steps")
                    # print(steps)
                    # print(len(steps))

                    while len(steps) - 1 < l_l[x]:

                        # print("short 1")

                        steps.append(f_1)
                        rcs.append(rc)

                        # print("rc")
                        # print(rc)



                    # print("")
                    # print(l_l[x])
                    # print(len(steps))

                    # print(steps)
                    # print(len(steps))

                    # print(" ")
                    # print("len steps rcs")
                    # print(len(steps))
                    # print(len(rcs))
                    # print("steps")
                    # print(steps)
                    # print('rcs')
                    # print(rcs)

                    for s in steps:

                        canvas[message.index(m) + 1][pos].append(s)

                    for r in rcs:

                        rcanvas[message.index(m) + 1][pos].append(r)


                else:

                    # print("")
                    # print('double')

                    # print(" ")
                    # print('double')
                    # print(f)

                    if f[0] not in polar_d:

                        polar_d[f[0]] = 0

                    if f[1] not in polar_d:
                        polar_d[f[1]] = 0

                    polar_d[f[0]] += 1
                    polar_d[f[1]] += 1

                    steps = []
                    rcs = []

                    f_1 = rule_gen(f[1][1], base, length)[1]

                    for y in range(2):

                        step_count = 0

                        row = rule_gen(f[y][0], base, length)[1]

                        # steps.append(f_0)

                        # print(f_0)

                        while step_count < f[y][-1]:

                            row, rc = Color_cells(rule_gen(f[y][2], base, length)[0], length, row)

                            steps.append(row)
                            rcs.append(rc)

                            # print(" ")
                            # print("len steps rcs")
                            # print(len(steps))
                            # print(len(rcs))

                            step_count += 1

                    # print(" ")
                    # print("steps")
                    # print(steps)
                    # print(len(steps))

                    while len(steps) - 1 < l_l[x]:

                        # print("short 2")

                        steps.append(f_1)
                        rcs.append(rc)

                        # print("rc")
                        # print(rc)

                    # print("")
                    # print(l_l[x])
                    # print(len(steps))

                    # print(steps)
                    # print(len(steps))

                    # print(" ")
                    # print("len steps rcs")
                    # print(len(steps))
                    # print(len(rcs))
                    # print("steps")
                    # print(steps)
                    # print('rcs')
                    # print(rcs)

                    for s in steps:

                        canvas[message.index(m) + 1][pos].append(s)

                    for r in rcs:

                        rcanvas[message.index(m) + 1][pos].append(r)

            # print(" ")
            # print('len canvas rcanvas')
            # print(pos)
            # print(len(canvas[pos]))
            # print(len(rcanvas[pos]))

            pos += 1

        if sum > final_length:

            final_length = sum

    magenta = (1, 0, 1)
    yellow = (1, 1, 0)
    cyan = (0, 1, 1)
    red = (1, 0, 0)
    blue = (0, 0, 1)
    green = (0, 1, 0)
    black = (0, 0, 0)
    white = (1, 1, 1)
    grey = (.2, .2, .2)
    purple = (.6, 0, .6)
    turquoise = (0, .8, .8)
    light_grey = (.8, .8, .8)
    moss = (.2, .4, .2)
    orange = (1, .5, .1)

    album = []

    # print("height length")
    # print(final_height)
    # print(final_length)

    for x in range(depth):

        print("")
        print("x")
        print(x)

        collage = []
        mural = np.zeros((final_height, final_length), dtype='int8')

        for y in range(len(message)):

            # print(canvas[y+1][x+1])

            line = np.asarray(canvas[y+1][x+1])

            line = np.rot90(line)
            line = np.flip(line, 0)

            l_s = line.shape
            start = int((final_length - l_s[1])/2)

            # print("ls")
            # print(l_s)

            collage.append(line)
            mural[length * y:length * (y+1), start:line.shape[1] + start] = line

        album.append(mural)

    path = '../cell translation'

    cMap = colors.ListedColormap([black, cyan, magenta, yellow, blue, green, red])


    if vid == 0:

        for c in canvas:

            # print(" ")
            # print('canvas-' + str(c))
            # print(canvas[c])
            # print(len(canvas[c]))

            file = str(message) + str('-') + str(list(canvas.keys()).index(c) + 1)
            path_name = os.path.join(path, file)

            canvas_c = canvas[c]

            canvas_c = np.asarray(canvas_c)
            canvas_c = np.rot90(canvas_c)

            ax = plt.gca()
            ax.set_aspect(1)

            plt.pcolormesh(canvas_c, cmap=cMap)

            plt.axis('off')

            # plt.show()

            plt.savefig(path_name, dpi=200, bbox_inches='tight',pad_inches = 0)
            plt.close()

    else:

        # print("vid")
        gal = []
        gallery = []
        fig = plt.figure()

        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        ax.set_aspect('auto')
        fig.add_axes(ax)

        # # values
        # for c in canvas:
        #
        #     print(c)
        #     print(canvas[c])
        #
        #     canvas_c = canvas[c]
        #
        #     canvas_c = np.asarray(canvas_c)
        #
        #     # print(canvas_c)
        #
        #     canvas_c = np.rot90(canvas_c)
        #     canvas_c = np.flip(canvas_c, 0)
        #
        #     file = str(message) + str('-') + str(depth) + 'val.mp4'
        #     path_name = os.path.join(path, file)
        #
        #     gal.append([plt.imshow(canvas_c, cmap=cMap, animated=True)])
        #
        # # rule calls
        # for r in rcanvas:
        #
        #     # print(r)
        #     # print(rcanvas[r])
        #
        #     rcanvas_r = rcanvas[r]
        #
        #     rcanvas_r = np.asarray(rcanvas_r)
        #     rcanvas_r = np.rot90(rcanvas_r)
        #     rcanvas_r = np.flip(rcanvas_r, 0)
        #
        #     file = str(message) + str('-') + str(depth) + 'rc.mp4'
        #     path_name = os.path.join(path, file)
        #
        #     gal.append([plt.imshow(rcanvas_r, animated=True, cmap=cMap)])

        # print("")
        # print("album")

        for a in album:

            # print("")
            # print("a")
            # print(a)

            gal.append([plt.imshow(a, animated=True, cmap=cMap)])

        for g in gal:
            gallery.append(g)

        # for g in reversed(gal):
        #     gallery.append(g)



        ani = animation.ArtistAnimation(fig, gallery, interval=150, blit=True,
                                        repeat_delay=0)

        # writer = animation.PillowWriter(fps=8)
        #
        # ani.save('cell translation/fire-and-ice.gif', dpi=500, writer=writer)

        plt.show()


    # print(list(polar_d.items())[:10])
    # print(list(polar_d.items())[0])
    # print(list(polar_d.items())[0][1])

    p_d = dict(sorted(list(polar_d.items()), key=lambda x:x[1], reverse=True))
    polar_u_i = list(p_d.keys())

    for p in polar_u_i:

        fb = (p[0], p[1])

        # print(fb)

        if fb not in polar_paths:

            # print("new")

            polar_paths[fb] = []

            if p not in polar_paths[fb]:
                # print("append")

                polar_paths[fb].append(p)

        else:

            if p not in polar_paths[fb]:
                # print("append")

                polar_paths[fb].append(p)

    # print("polar_u_i")
    # print(polar_u_i[:10])
    #
    # print("p_d")
    # print(list(p_d)[:10])

    filename = 'polar maps/polar_u_c-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(polar_u_i, outfile)
    outfile.close()

    filename = 'polar maps/polar_d-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(p_d, outfile)
    outfile.close()

    filename = 'cellexicon/cellexicon-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(cellexicon, outfile)
    outfile.close()

    filename = '../polar maps/polar_paths-16'
    outfile = open(filename, 'wb')
    pickle.dump(polar_paths, outfile)
    outfile.close()


base = 2
view = 3

length = 32
max_steps = 16
scale = 1
depth = 16

try:

    infile = open("polar maps/polar_u-" + str(length), "rb")
    polar_u_i = pickle.load(infile)
    infile.close
except:
    polar_u_i = []

try:

    infile = open("polar maps/polar_d-" + str(length), "rb")
    polar_d = pickle.load(infile)
    infile.close
except:
    polar_d = dict()

try:

    infile = open("polar maps/polar_paths-" + str(length), "rb")
    polar_paths = pickle.load(infile)
    infile.close
except:
    polar_paths = dict()

try:
    infile = open("cellexicon/cellexicon-" + str(length), "rb")
    cellexicon = pickle.load(infile)
    infile.close
except:
    cellexicon = dict()

# cellexicon = dict()

print(" ")
print("polars")
print(list(polar_d.items())[:10])
print(len(list(polar_d)))
print(list(polar_u_i[:10]))
print(len(list(polar_u_i)))

cell_key = (base, view, length, scale)

print(" ")
print("cell_key")
print(cell_key)

if cell_key not in cellexicon:

    cellexicon[cell_key] = dict()

message = ['Some say the world will end in fire', 'Some say in ice', 'From what Ive tasted of desire', 'I hold with those who favor fire',
'But if it had to perish twice', 'I think I know enough of hate', 'To say that for destruction ice', 'Is also great', 'And would suffice']

message = ['breath']

# cellexicon = dict()

# polar_d = dict(sorted(polar_d.items(), key=lambda x: x[1], reverse=True))
# polar_u_i = list(polar_d.keys())

paint(cellexicon, cell_key, message, base, view, length, max_steps, depth, polar_paths, polar_u_i, polar_d, scale, vid=1)


print("")
print("cellexicon")

for cell in cellexicon:

    print(' ')
    print("cell")
    print(cell)

    for word in cellexicon[cell]:

        print("word")
        print(word)

    # for depth in cellexicon[cell]:
    #
    #     print('depth')
    #     print(depth)
    #     print(cellexicon[cell][depth])












