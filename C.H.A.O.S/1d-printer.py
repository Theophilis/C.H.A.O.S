import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import pandas as pd
import pickle


np.set_printoptions(linewidth=np.inf)
plt.ioff()


length = 2001
#number of times given rule is applied and number of initial rows generated
width = length
#number of cells in a row
rule = 21621
#number who's x_base transformation gives the rules dictionary its values
view = 3
#size of the view window that scans a row for rule application
base = 3
#numerical base of the rule set. number of colors each cell can be
start = int(width/2)
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


def decimal(n, b):

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

    return value


def rule_gen(rule, base = 2, width = 0, string = 0):

    rules = dict()

    if string != 0:
        int_rule = [l for l in rule]


    else:

        if base == 2:

            int_rule = bin(rule).replace('0b', '')


        else:

            int_rule = base_x(rule, base)


        x = int_rule[::-1]

        if width == 0:
            while len(x) < base ** view:

                x += '0'

            bnr = x[::-1]
            int_rule = list(bnr)

        else:
            while len(x) < width:
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


def viewer(c_a, y, view, v_0, edge):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(c_a) - 1:

            v_0.append(edge)

        else:

            v_0.append(str(c_a[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < 0:

            v_0.insert(0, edge)

        else:

            v_0.insert(0, str(c_a[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(c_a, y, view, v_0, edge)

        return v_0


def map(canvas, length, width, rule, base, start, direction, path, rc = 0, plot=0, edge='0'):

    if type(rule) != int:
        r_n = decimal(rule, base)

    else:
        r_n = rule

    start_0 = start
    file = str(width) + 'x' + str(length) + '-' + str(base) + '-' + 'colors' + '-' + str(r_n) + '-' + 'breathe'
    path_name = os.path.join(path, file)

    cell_patterns = dict()
    rule_patterns = dict()

    # print("rules")

    rules = rule_gen(rule, base, string=0)
    int_rule = rules[1]
    rules = rules[0]

    # print(int_rule)
    # print(rules)

    # print(" ")
    # print("start")

    start = rule_gen(abs(start), base, width)

    # print(" ")
    # print("rules")
    # print(rules)
    # print(int_rule)

    # print(" ")
    # print("start")
    # print(start[1])

    rc_val = dict()

    for x in range(base):
        rc_val[str(x)] = []

    for x in range(len(int_rule)):

        if int_rule[x] not in rc_val:
            rc_val[int_rule[x]] = [x]

        else:
            rc_val[int_rule[x]].append(x)

    # print(" ")
    # print("rc_val")
    # print(rc_val)

    rc_net = dict()

    for key in list(rules.keys()):

        # print(" ")
        # print(key)

        rc_net[list(rules.keys()).index(key)] = []

        for k in key:

            # print(' ')
            # print(k)

            rc_net[list(rules.keys()).index(key)].append(rc_val[k])

    # print(" ")
    # print("rc_net")
    # for x in range(len(rules)):
    #     print(rc_net[x])

    canvas_0 = np.copy(canvas)
    rule_call = np.zeros((length, width), dtype='int8')


    canvas_0[0, start_0] = 1
    rule_call[0] = start[1]

    # for x in range(width):
    #     cnvs[0, x] = x

    # print(" ")
    # print("canvas")
    # print(canvas_0)
    # print(' ')
    # print("rule_call")
    # print(rule_call)

    for x in range(length - 1):

        c_a = canvas_0[x]

        # print(" ")
        # print("c_a")
        # print(c_a)

        for y in range(len(c_a)):

            if direction != 0:

                y = len(c_a) - y - 1

            v_0 = []

            # print(" ")
            # print("y")
            # print(y)

            v_0 = tuple(viewer(c_a, y, view, v_0, edge))

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
                rule_call[x + 1, y] = list(rules.keys()).index(v_0)

    # print(" ")
    # print("cnvs")
    # print(cnvs)
    # print(" ")
    # print("rule_call")
    # print(rule_call)

    # print(" ")
    # print('canvas')
    # print(canvas)

    for x in range(length):
        for y in range(width):
            if canvas[x, y] == 1:
                canvas_0[x, y] = base

    # print(" ")
    # print("canvas_0")
    # print(canvas_0)

    canvas_0 = np.flip(canvas_0, 0)
    rule_call_f = np.flip(rule_call, 0)
    # cnvs = np.flip(cnvs, 1)

    # print("cnvs")
    # print(cnvs)



#export pcolormesh of cells

    if plot != 0:

        if rc == 0 or rc == 2:

            ax = plt.gca()
            ax.set_aspect(1)

            plt.margins(0, None)

            magenta = (1, 0, 1)
            yellow = (1, 1, 0)
            cyan = (0, 1, 1)
            red = (1, 0, 0)
            blue = (0, 0, 1)
            green = (0, 1, 0)
            black = (0, 0, 0)
            white = (1, 1, 1)
            grey = (.3, .3, .3)
            purple = (.6, 0, .6)
            turquoise = (0, .8, .8)
            light_grey = (.8 , .8, .8)

            if base == 5:
                cMap = c.ListedColormap([grey, magenta, cyan, yellow, red, black])

            if base == 4:
                cMap = c.ListedColormap([grey, cyan, magenta, green, black])

            if base == 3:
                cMap = c.ListedColormap([white, red, blue, green])

            if base == 2:
                cMap = c.ListedColormap([black, magenta, cyan])

            plt.pcolormesh(canvas_0, cmap=cMap)

            # plt.xticks(np.arange(0, width, step=1))
            # plt.yticks(np.arange(0, length, step=1))
            #
            # plt.figtext(.3, .925, int_rule, fontsize=14)
            # plt.figtext(.0075, .05, rules, fontsize=7)

            # plt.margins(0, None)
            # plt.grid(visible=True, axis='both', )
            # plt.xticks(np.arange(0, size, step=1))
            # plt.yticks(np.arange(0, size, step=1))

            # c_plt.show()
            plt.savefig(path_name, dpi=length)
            plt.close()

        if rc == 1 or rc == 2:
            file = 'RC' + "-" + str(rule) + '-' + str(start_0) + '-' + str(base) + '-' + str(length) + 'x' + str(width)
            path_name = os.path.join(path, file)
            plt.pcolormesh(rule_call_f)

            # plt.xticks(np.arange(0, width, step=1))
            # plt.yticks(np.arange(0, length, step=1))

            # plt.figtext(.3, .925, int_rule, fontsize=14)
            # plt.figtext(.0075, .05, rules, fontsize=7)
            # plt.grid(visible=True, axis='both', )

            # c_plt.show()
            plt.savefig(path_name, dpi=900)
            plt.close()

#generate dictionary of cell value patterns

    # if rc == 0 or rc == 2:
    #
    #     v_pattern = []
    #
    #     for x in reversed(range(length)):
    #
    #         v = list(cnvs[x])
    #
    #         w = ''
    #
    #         for n in v:
    #             w += str(n)
    #
    #         w = int(w, 2)
    #
    #         # print("w")
    #         # print(w)
    #         # print(type(w))
    #
    #         v_pattern.append(str(w))
    #
    #     cell_patterns = v_pattern
    #
    #
    # if rc == 1 or rc == 2:
    #     # if rule == 1:
    #     #     v_pattern = []
    #     #
    #     #     for z in range(length):
    #     #         w = ''
    #     #         for a in range(width):
    #     #             w += "0"
    #     #
    #     #         w = int(w, 2)
    #     #
    #     #         v_pattern.append(str(w))
    #     #
    #     #     cell_patterns[(width, 0)] = v_pattern
    #
    #     v_pattern = []
    #
    #     for x in range(length - 1):
    #
    #         v = list(rule_call[x])
    #
    #         # print("v")
    #         # print(v)
    #
    #         w = ''
    #
    #         for n in v:
    #             w += str(n)
    #
    #         # w = int(w, 2)
    #
    #         # print("w")
    #         # print(w)
    #         # print(type(w))
    #
    #         v_pattern.append(str(w))
    #
    #     rule_patterns = v_pattern


    return cell_patterns, rule_patterns, rule_call, rc_val, rc_net


path = 'plates'

journaling = 0
leveling = 0

size = length
l_size = 301
space = 20

offset_size = 24
density = 5
x_o = 40
y_o = 80

def kord_ami(size, l_size, space, offset_size, x_o, y_o):

    canvas = np.zeros((size, size), dtype='int8')

    # print(" ")
    # print("canvas")
    # print(canvas)

    def draw_k(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        k_coord_0 = (corner[1] + int(size/2), corner[0] + 1)

        canvas[k_coord_0] = 1

        k_legs = dict()

        for x in range(2):
            k_legs[x] = []

        for x in range(int(size/2)):

            if x == 0:

                k_legs[0].append(k_coord_0)
                k_legs[1].append(k_coord_0)

            k_legs[0].append((k_coord_0[0] + 1 + x, k_coord_0[1] + 1 + x))
            k_legs[1].append((k_coord_0[0] - 1 - x, k_coord_0[1] + 1 + x))

        # print(k_legs[0])
        # print(k_legs[1])

        for k in k_legs[0]:
            canvas[k] = 1

        for k in k_legs[1]:
            canvas[k] = 1


    def draw_o(size, canvas, corner):

        for x in range(int(size / 3) + 1):
            canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3) - x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

            canvas[corner[1] + int(size / 3) + x, corner[0]] = 1
            canvas[corner[1] + int(size / 3) + x, corner[0] + int(size / 3 * 2)] = 1

        for x in range(int(size / 3) + 2):
            canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
            canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1


    def draw_r(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        r_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)
        r_coord_1 = (corner[1], corner[0] + 1)
        r_coord_2 = (corner[1] + int(size / 2), corner[0] + 1 + int(size / 5))
        r_coord_3 = (corner[1], corner[0] + 1 + int(size / 5))

        # print(r_coord_1)
        # print(r_coord_2)

        canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1

        r_legs = dict()

        for x in range(3):
            r_legs[x] = []

        for x in range(int(size / 2) + 1):
            canvas[corner[1] + int(size / 2) + x, corner[0] + int(size / 5) + int(x / 2)] = 1

        for x in range(int(size / 4) + 1):
            canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
            canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1


    def draw_d(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        d_coord_0 = (corner[1], corner[0] + int(size/3))
        d_coord_1 = (corner[1] + size - 1, corner[0]+ int(size/3))

        canvas[d_coord_0] = 1
        canvas[d_coord_1] = 1

        canvas[corner[1], corner[0]:corner[0] + int(size/3)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size/3)] = 1


        d_legs = dict()

        for x in range(2):
            d_legs[x] = []

        for x in range(int(size/3)):

            if x == 0:

                d_legs[0].append(d_coord_0)
                d_legs[1].append(d_coord_1)

            d_legs[0].append((d_coord_0[0] + 1 + x, d_coord_0[1] + 1 + x))
            d_legs[1].append((d_coord_1[0] - 1 - x, d_coord_1[1] + 1 + x))

        # print(d_legs[0])
        # print(d_legs[1])

        for k in d_legs[0]:
            canvas[k] = 1

        for k in d_legs[1]:
            canvas[k] = 1

        canvas[d_legs[0][-1][0]:d_legs[1][-1][0], d_legs[0][-1][1]] = 1


    def draw_a(size, canvas, corner):

        apex = (corner[1], corner[0] + int(size/2))

        canvas[apex] = 1

        a_legs = dict()

        for x in range(2):
            a_legs[x] = []


        for x in range(size - 1):

            if x % 2 == 0:

                a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x/2)))
                a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x/2)))

            else:

                a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 -int(x/2)))
                a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x/2)))

        for x in range(2):
            for a in a_legs[x]:
                canvas[a] = 1

        canvas[a_legs[0][int(len(a_legs[0])/2)][0], a_legs[0][int(len(a_legs[0])/2)][1]:a_legs[1][int(len(a_legs[1])/2)][1]] = 1


    def draw_m(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1
        canvas[corner[1]:corner[1] + size, corner[0] + size - 1] = 1

        apex = (corner[1] + size - 1, corner[0] + int(size/2))

        canvas[apex] = 1

        m_legs = dict()

        for x in range(2):
            m_legs[x] = []

        for x in range(size - 2):

            if x % 2 == 0:

                m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x/2)))
                m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x/2)))

            else:

                m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 -int(x/2)))
                m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x/2)))

        for x in range(2):
            for m in m_legs[x]:
                canvas[m] = 1


    def draw_i(size, canvas, corner):

        canvas[corner[1], corner[0] + int(size/4):corner[0] + size - int(size/4)] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size/4):corner[0] + size - int(size/4)] = 1
        canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size/2)] = 1

    # draw_k(l_size, canvas, (2, 9))
    # draw_o(l_size, canvas, (2 + l_size + space, 9))
    # draw_r(l_size, canvas, (2 + l_size * 2 + space, 9))
    # draw_d(l_size, canvas, (2 + l_size * 3 + space, 9))
    # draw_a(l_size, canvas, (2, 9 + l_size + space * 3))
    # draw_m(l_size, canvas, (2 + l_size + space, 9 + l_size + space * 3))
    # draw_i(l_size, canvas, (2 + l_size * 2 + space, 9 + l_size + space * 3))

    for offset in range(0, offset_size, 3):

        draw_k(l_size, canvas, (x_o + offset, y_o))
        draw_o(l_size, canvas, (x_o + l_size + space + offset, y_o))
        draw_r(l_size, canvas, (x_o + l_size * 2 + space + offset, y_o))
        draw_d(l_size, canvas, (x_o + l_size * 3 + space + offset, y_o))
        draw_a(l_size, canvas, (x_o + offset, y_o + l_size + space * 3))
        draw_m(l_size, canvas, (x_o + l_size + space + offset, y_o + l_size + space * 3))
        draw_i(l_size, canvas, (x_o + l_size * 2 + space + offset, y_o + l_size + space * 3))

        draw_k(l_size, canvas, (x_o - offset, y_o))
        draw_o(l_size, canvas, (x_o + l_size + space - offset, y_o))
        draw_r(l_size, canvas, (x_o + l_size * 2 + space - offset, y_o))
        draw_d(l_size, canvas, (x_o + l_size * 3 + space - offset, y_o))
        draw_a(l_size, canvas, (x_o - offset, y_o + l_size + space * 3))
        draw_m(l_size, canvas, (x_o + l_size + space - offset, y_o + l_size + space * 3))
        draw_i(l_size, canvas, (x_o + l_size * 2 + space - offset, y_o + l_size + space * 3))

        draw_k(l_size, canvas, (x_o, y_o + offset))
        draw_o(l_size, canvas, (x_o + l_size + space, y_o + offset))
        draw_r(l_size, canvas, (x_o + l_size * 2 + space, y_o + offset))
        draw_d(l_size, canvas, (x_o + l_size * 3 + space, y_o + offset))
        draw_a(l_size, canvas, (x_o, y_o + l_size + space * 3 + offset))
        draw_m(l_size, canvas, (x_o + l_size + space, y_o + l_size + space * 3 + offset))
        draw_i(l_size, canvas, (x_o + l_size * 2 + space, y_o + l_size + space * 3 + offset))

        draw_k(l_size, canvas, (x_o , y_o - offset))
        draw_o(l_size, canvas, (x_o + l_size + space, y_o - offset))
        draw_r(l_size, canvas, (x_o + l_size * 2 + space, y_o - offset))
        draw_d(l_size, canvas, (x_o + l_size * 3 + space, y_o - offset))
        draw_a(l_size, canvas, (x_o, y_o + l_size + space * 3 - offset))
        draw_m(l_size, canvas, (x_o + l_size + space, y_o + l_size + space * 3 - offset))
        draw_i(l_size, canvas, (x_o + l_size * 2 + space, y_o + l_size + space * 3 - offset))

    return canvas

def breathe(size, l_size, space, offset_size, density, x_o, y_o):

    canvas = np.zeros((size, size), dtype='int8')

    def draw_b(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 4)] = 1

        for x in range(int(size / 4) + 1):
            canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
            canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1

            canvas[corner[1] + x + int(size / 2), corner[0] + int(size / 4) + int(x / 2)] = 1
            canvas[corner[1] + int(size) - x - 1, corner[0] + int(size / 4) + int(x / 2)] = 1

    def draw_r(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        r_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)
        r_coord_1 = (corner[1], corner[0] + 1)
        r_coord_2 = (corner[1] + int(size / 2), corner[0] + 1 + int(size / 5))
        r_coord_3 = (corner[1], corner[0] + 1 + int(size / 5))

        # print(r_coord_1)
        # print(r_coord_2)

        canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1

        r_legs = dict()

        for x in range(3):
            r_legs[x] = []

        for x in range(int(size / 2) + 1):
            canvas[corner[1] + int(size / 2) + x, corner[0] + int(size / 5) + int(x / 2)] = 1

        for x in range(int(size / 4) + 1):
            canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
            canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1

    def draw_e(size, canvas, corner):

        canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
        canvas[corner[1], corner[0]:corner[0] + int(size / 2)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 3)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2)] = 1

    def draw_a(size, canvas, corner):

        apex = (corner[1], corner[0] + int(size / 2))

        canvas[apex] = 1

        a_legs = dict()

        for x in range(2):
            a_legs[x] = []

        for x in range(size - 1):

            if x % 2 == 0:

                a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x / 2)))
                a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x / 2)))

            else:

                a_legs[0].append((apex[0] + 1 + x, apex[1] - 1 - int(x / 2)))
                a_legs[1].append((apex[0] + 1 + x, apex[1] + 1 + int(x / 2)))

        for x in range(2):
            for a in a_legs[x]:
                canvas[a] = 1

        canvas[a_legs[0][int(len(a_legs[0]) / 2)][0],
        a_legs[0][int(len(a_legs[0]) / 2)][1]:a_legs[1][int(len(a_legs[1]) / 2)][1]] = 1

    def draw_t(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
        canvas[corner[1], corner[0] + int(size / 5):corner[0] + size - int(size / 5)] = 1

    def draw_h(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1
        canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 2)] = 1

    for offset in range(0, offset_size, density):

        draw_b(l_size, canvas, (x_o + offset + space, y_o))
        draw_r(l_size, canvas, (x_o + offset + space + l_size, y_o))
        draw_e(l_size, canvas, (x_o + offset + space + l_size * 2, y_o))
        draw_a(l_size, canvas, (x_o + offset + space + l_size * 3, y_o))
        draw_t(l_size, canvas, (x_o + offset + space + l_size * 4, y_o))
        draw_h(l_size, canvas, (x_o + offset + space + l_size * 5, y_o))
        draw_e(l_size, canvas, (x_o + offset + space + l_size * 6, y_o))

        draw_b(l_size, canvas, (x_o - offset + space, y_o))
        draw_r(l_size, canvas, (x_o - offset + space + l_size, y_o))
        draw_e(l_size, canvas, (x_o - offset + space + l_size * 2, y_o))
        draw_a(l_size, canvas, (x_o - offset + space + l_size * 3, y_o))
        draw_t(l_size, canvas, (x_o - offset + space + l_size * 4, y_o))
        draw_h(l_size, canvas, (x_o - offset + space + l_size * 5, y_o))
        draw_e(l_size, canvas, (x_o - offset + space + l_size * 6, y_o))

        draw_b(l_size, canvas, (x_o + space, y_o + offset))
        draw_r(l_size, canvas, (x_o + space + l_size, y_o + offset))
        draw_e(l_size, canvas, (x_o + space + l_size * 2, y_o + offset))
        draw_a(l_size, canvas, (x_o + space + l_size * 3, y_o + offset))
        draw_t(l_size, canvas, (x_o + space + l_size * 4, y_o + offset))
        draw_h(l_size, canvas, (x_o + space + l_size * 5, y_o + offset))
        draw_e(l_size, canvas, (x_o + space + l_size * 6, y_o + offset))

        draw_b(l_size, canvas, (x_o + space, y_o - offset))
        draw_r(l_size, canvas, (x_o + space + l_size, y_o - offset))
        draw_e(l_size, canvas, (x_o + space + l_size * 2, y_o - offset))
        draw_a(l_size, canvas, (x_o + space + l_size * 3, y_o - offset))
        draw_t(l_size, canvas, (x_o + space + l_size * 4, y_o - offset))
        draw_h(l_size, canvas, (x_o + space + l_size * 5, y_o - offset))
        draw_e(l_size, canvas, (x_o + space + l_size * 6, y_o - offset))

    return canvas


canvas = breathe(size, l_size, space, offset_size, density, x_o, y_o)



if journaling != 0:

    infile = open("/Users/edwardmaclean/PycharmProjects/GitHub/C.H.A.O.S/journals/journal_hb1802", "rb")
    journal = pickle.load(infile)
    infile.close


    journal = dict(sorted(journal.items(), key=lambda x:len(x[1][0]), reverse=True))

    print(len(list(journal.keys())))

    for k in list(journal.keys())[20:]:
        print('')
        print(list(journal.keys()).index(k))
        print(k[0])
        jk = journal[k]
        print(len(jk[0]))
        map(length, width, k[0], base, start, direction, path, 0, 1)

#folders to level
##pentary lvl-3
##quaternary lvl-1

elif leveling != 0:

    lvl = os.listdir('/Users/edwardmaclean/PycharmProjects/GitHub/C.H.A.O.S/scarfs/quaternary/lvl-1')

    path = 'plates'

    print(len(lvl))

    for l in lvl:

        print(" ")
        print(lvl.index(l))

        print(l)
        # print(len(l))

        try:

            l = int(l[19:-4])

        except:

            continue

        print(l)

        map(canvas, length, width, l, base, start, direction, path, 0, 1)


else:

    for x in range(1):
        print(" ")
        print(x)
        map(canvas, length, width, rule, base, start, direction, path, 0, 1)


##qb syles for dark frames