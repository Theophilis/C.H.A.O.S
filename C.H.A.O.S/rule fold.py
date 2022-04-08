
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


def fold(message, base, view, length, max_steps, scale, level, polar_u_i, polar_d, plot=0):

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


    max = base ** length

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


        #fresh forged paths
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

                        route = stream(p[1], back, p_1, back_row, max_steps)

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

                        route = stream(front, p[0], front_row, p_0, max_steps)

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

                depth = 2

                routes = []

                joint = 0

                while len(routes) == 0:

                    joint_row = rule_gen(joint, base, length)[1]

                    for x in range(depth):

                        if x == 0:

                            front_route = stream(front, joint, front_row, joint_row, max_steps)

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

                            back_route = stream(joint, back, joint_row, back_row, max_steps)

                            # print(len(front_route))
                            # print(len(back_route))

                            if len(front_route) > 0 and len(back_route) > 0:

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

                    joint += 1

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
        #
        # print(" ")
        # print(path[m][1][:10])
        # print(path[m][2][:10])

        if len(path[m][1]) > 0:

            frame.append(path[m][1][0])

            # message_l[pos].append(path[m][1][0][-1] + 1)

        else:

            frame.append(path[m][2][0])

            # message_l[pos].append(path[m][2][0][0][-1] + path[m][2][0][1][-1] + 2)

        pos += 1

    # print("")
    # print('message_l')
    # print(message_l)


    filename = 'polar maps/polar_u-' + str(length)
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

        path = 'cell translation'

        file = str(message) + str('-') + str(level)
        path_name = os.path.join(path, file)

        plt.savefig(path_name, dpi=200)
        plt.close()

    return frame


def paint(cellexicon, cell_key, message, base, view, length, max_steps, depth, polar_u_i, polar_d, scale, vid=0):

    frames = []
    message_l = dict()

    # print(list(polar_d)[:10])
    # print(list(polar_d)[0])
    # print(list(polar_d)[0][1])

    for x in range(len(message) - 1):

        message_l[x] = []

    for x in range(depth):

        bibliod = 0
        x = x + 1

        print(" ")
        print('x')
        print(x)

        if message not in cellexicon[cell_key]:

            cellexicon[cell_key][message] = dict()

            if x not in cellexicon[cell_key][message]:

                cellexicon[cell_key][message][x] = []

        else:

            # print("message is in cellexicon")

            if x not in cellexicon[cell_key][message]:

                cellexicon[cell_key][message][x] = []

            else:

                # print("depth is in cellexicon")
                #
                # print(" ")
                # print('bibliod')
                # print(message)
                # print(x)

                bibliod = 0

                # message_l = cellexicon[cell_key][message][x][0][1]

        if bibliod == 1:

            print(cellexicon[cell_key][message][x])

            try:

                frames.append(cellexicon[cell_key][message][x][0])

            except:

                frames.append(fold(message, base, view, length, max_steps, scale, x, polar_u_i, polar_d))

            # print('cellexicon message')
            # print(cellexicon[message])
            # print(cellexicon[message][x][0])
            # print(cellexicon[message][x][0][0])
            # print(cellexicon[message][x][0][1])

        else:

            frames.append(fold(message, base, view, length, max_steps, scale, x, polar_u_i, polar_d))

    # print(" ")
    # print('message_l')

    l_l = []
    sum = 0


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

    for m in message_l:

        message_l[m] = sorted(message_l[m], reverse=True)

        l_l.append(message_l[m][0])
        sum += message_l[m][0]

        print(" ")
        print(m)
        print(message_l[m])

    print(" ")
    print("l_l")
    print(l_l)


    # print(" ")
    # print('letter length')
    # print(l_l)
    # print(sum)

    canvas = dict()

    # print(" ")
    # print(len(frames))
    # print(frames)

    pos = 1

    for frame in frames:

        # print(" ")
        # print("frame")
        # print(frames.index(frame))
        # print(frame)

        if frame not in cellexicon[cell_key][message][pos]:

                cellexicon[cell_key][message][pos].append(frame)

        canvas[pos] = []

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

                # print('single')

                if f not in polar_d:

                    polar_d[f] = 0

                polar_d[f] += 1

                steps = []
                step_count = 0

                f_0 = rule_gen(f[0], base, length)[1]
                f_1 = rule_gen(f[1], base, length)[1]
                steps.append(f_0)

                # print(f_0)

                while step_count < f[-1]:
                    row = Color_cells(rule_gen(f[2], base, length)[0], length, steps[-1])[0]

                    steps.append(row)

                    step_count += 1

                # print(" ")
                # print("steps")
                # print(steps)
                # print(len(steps))

                while len(steps) - 1 < l_l[x]:
                    # print("short")
                    steps.append(f_1)

                # print("")
                # print(l_l[x])
                # print(len(steps))

                # print(steps)
                # print(len(steps))

                for s in steps:
                    canvas[pos].append(s)


            else:

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

                f_1 = rule_gen(f[1][1], base, length)[1]

                for y in range(2):

                    step_count = 0

                    f_0 = rule_gen(f[y][0], base, length)[1]
                    steps.append(f_0)

                    # print(f_0)

                    while step_count < f[y][-1]:
                        row = Color_cells(rule_gen(f[y][2], base, length)[0], length, steps[-1])[0]

                        steps.append(row)

                        step_count += 1

                # print(" ")
                # print("steps")
                # print(steps)
                # print(len(steps))

                while len(steps) - 1 < l_l[x]:
                    # print("short")
                    steps.append(f_1)

                # print("")
                # print(l_l[x])
                # print(len(steps))

                # print(steps)
                # print(len(steps))

                for s in steps:
                    canvas[pos].append(s)

        pos += 1


    path = 'cell translation'

    cMap = colors.ListedColormap(['k', 'm'])

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
        for c in canvas:

            canvas_c = canvas[c]

            canvas_c = np.asarray(canvas_c)
            canvas_c = np.rot90(canvas_c)
            canvas_c = np.flip(canvas_c, 0)

            file = str(message) + str('-') + str(depth) + '.mp4'
            path_name = os.path.join(path, file)

            gal.append([plt.imshow(canvas_c, cmap=cMap, animated=True)])

        for g in gal:
            gallery.append(g)
        #
        # for g in reversed(gal):
        #     gallery.append(g)

        ani = animation.ArtistAnimation(fig, gallery, interval=100, blit=True,
                                        repeat_delay=0)
        # ani.save()
        plt.show()


    # print(list(polar_d.items())[:10])
    # print(list(polar_d.items())[0])
    # print(list(polar_d.items())[0][1])

    p_d = dict(sorted(list(polar_d.items()), key=lambda x:x[1], reverse=True))
    polar_u_i = list(p_d.keys())

    # print("polar_u_i")
    # print(polar_u_i[:10])
    #
    # print("p_d")
    # print(list(p_d)[:10])

    filename = 'polar maps/polar_u-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(polar_u_i, outfile)
    outfile.close()

    filename = 'polar maps/polar_d-' + str(length)
    outfile = open(filename, 'wb')
    pickle.dump(p_d, outfile)
    outfile.close()

    filename = 'cellexicon/cellexicon'
    outfile = open(filename, 'wb')
    pickle.dump(cellexicon, outfile)
    outfile.close()

    b = 0

    # for p in polar_d:
    #     b += 1
    #
    #     print("")
    #     print(p)
    #     print(polar_d[p])


infile = open("polar maps/polar_u-16", "rb")
polar_u_i = pickle.load(infile)
infile.close

infile = open("polar maps/polar_d-16", "rb")
polar_d = pickle.load(infile)
infile.close

infile = open("cellexicon/cellexicon", "rb")
cellexicon = pickle.load(infile)
infile.close

# cellexicon = dict()

print(" ")
print("polars")
print(list(polar_d.items())[:10])
print(list(polar_u_i[:10]))

base = 2
view = 3

length = 32
max_steps = 8
scale = 1
depth = 16

cell_key = (base, view, length, max_steps, scale)

print(" ")
print("cell_key")
print(cell_key)

if cell_key not in cellexicon:

    cellexicon[cell_key] = dict()

message = ' breathe '

# cellexicon = dict()

# polar_d = dict(sorted(polar_d.items(), key=lambda x: x[1], reverse=True))
# polar_u_i = list(polar_d.keys())
#
# filename = 'polar maps/polar_u-' + str(length)
# outfile = open(filename, 'wb')
# pickle.dump(polar_u_i, outfile)
# outfile.close()
#
# filename = 'polar maps/polar_d-' + str(length)
# outfile = open(filename, 'wb')
# pickle.dump(polar_d, outfile)
# outfile.close()


paint(cellexicon, cell_key, message, base, view, length, max_steps, depth, polar_u_i, polar_d, scale, vid=1)

    # if b > 10:
    #     break

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












