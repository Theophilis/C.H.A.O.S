# C.H.A.O.S

import numpy as np
import pygame
from datetime import datetime
import os
import pickle
import sys
import random

pygame.font.init()

length = 8
# number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
# number of cells in a row
rule = 90
# number who's x_base transformation gives the rules dictionary its values
view = 4
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

# prep journal data for analysis

# add a record feature and button to menu. allows for recorder of all key inputs in a text file.

# write a read.me and contributor guide, attatch a GNU open source license, and publish on github


#####map#####


def base_x(n, b):
    e = n // b
    q = str(n % b)
    if n == 0:
        return '0'
    elif e == 0:
        return q
    else:
        return base_x(e, b) + q


def rule_gen_2(rule, base=2, width=0):
    rules = dict()

    int_rule = base_x(rule, base)

    x = int_rule[::-1]

    if width == 0:
        while len(x) < base ** view:
            x += '0'

    else:
        while len(x) < width:
            x += '0'

    bnr = x[::-1]

    int_rule = [int(v) for v in bnr]

    for x in range(len(int_rule)):

        x = len(int_rule) - x - 1

        key = tuple(base_x(x, base)[-view:])

        if len(key) < view:

            diff = view - len(key)
            key = list(key)

            for y in range(diff):
                key.insert(0, str(0))

        key = "".join(key)

        rules[tuple(key)] = int_rule[-x - 1]

    return rules, int_rule


def fencing(zero, level=0):
    # print(" ")
    # print("zero")
    # print(zero)
    fence = []
    for x in range(4):
        if x % 2 == 0:
            if x < 2:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0], zero[0] + (y + 1))
                    # print("post")
                    # print(post)
                    fence.append(post)
            else:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0] + 2 * (level + 1), zero[0] + 2 * (level + 1) - (y + 1))
                    fence.append(post)

        else:
            if x < 2:
                # print(x)
                for y in range(2 * (level + 1)):
                    post = (zero[0] + (y + 1), zero[0] + 2 * (level + 1))
                    fence.append(post)
            else:
                # print(x)
                for y in range(2 * (level + 1) + 1):
                    post = (zero[0] + 2 * (level + 1) - (y + 1), zero[0])
                    fence.append(post)

    return tuple(fence)


def viewer_2(fence, size, views):

    canvas = np.zeros((size, size), dtype='int8')
    canvas[start] = 1

    for f in fence:

        if f[0] > 0:
            v_1 = (f[0] - 1, f[1])
        if f[0] < size - 1:
            v_3 = (f[0] + 1, f[1])
        if f[0] == 0:
            v_1 = 0
        if f[0] == size - 1:
            v_3 = 0

        if f[1] > 0:
            v_4 = (f[0], f[1] - 1)
        if f[1] < size - 1:
            v_2 = (f[0], f[1] + 1)
        if f[1] == 0:
            v_4 = 0
        if f[1] == size -1:
            v_2 = 0

        view = (v_1, v_2, v_3, v_4)

        # print(view)
        # print(canvas[f])

        views[f] = (view, canvas[f])
        # print(views[f])


def fence_map(size, start, order=0):
    if order == 0:
        fence = dict()

        for x in range(int(size / 2)):
            zero = (start[0] - (x + 1), start[0] - (x + 1))
            fence[x] = fencing(zero, x)

        full_fence = []
        for k in list(fence.keys()):
            for f in fence[k][:len(fence[k]) - 1]:
                full_fence.append(f)

        canvas_f = np.zeros((size, size), dtype='int8')
        full_fence.insert(0, start)

        # for f in full_fence:
        #     canvas_f[f] = full_fence.index(f)

        return full_fence

    elif order == 1:
        canvas_t = np.zeros((size, size), dtype='int8')

        t_fence = []

        for x in range(size):
            for y in range(size):
                t_fence.append((x, y))

        # for t in t_fence:
        #     canvas_t[t] = t_fence.index(t)

        return t_fence

    elif order == 2:
        canvas = np.zeros((size, size), dtype='int8')

        fence = []

        for x in range(size):
            for y in range(size):
                fence.append((x, y))

        fence = sorted(fence, key=lambda x: abs(x[0] * x[1]))

        # for f in fence:
        #     canvas[f] = fence.index(f)

        return fence


def step(views, f, d_rule, canvas=0):

    # print("")
    # print("step")
    # print(f)
    view = views[f][0]

    if type(views[view[0]]) == tuple:
        c_1 = views[view[0]][1]
    else:
        c_1 = views[view[0]]

    if type(views[view[1]]) == tuple:
        c_2 = views[view[1]][1]
    else:
        c_2 = views[view[1]]

    if type(views[view[2]]) == tuple:
        c_3 = views[view[2]][1]
    else:
        c_3 = views[view[2]]

    if type(views[view[3]]) == tuple:
        c_4 = views[view[3]][1]
    else:
        c_4 = views[view[3]]

    # try:
    #     c_1 = views[view[0]][1]
    # except:
    #     c_1 = views[view[0]]
    # try:
    #     c_2 = views[view[1]][1]
    # except:
    #     c_2 = views[view[1]]
    # try:
    #     c_3 = views[view[2]][1]
    # except:
    #     c_3 = views[view[2]]
    # try:
    #     c_4 = views[view[3]][1]
    # except:
    #     c_4 = views[view[3]]

    comp = (str(c_1), str(c_2), str(c_3), str(c_4))

    if canvas[f[1], f[0]] == 1:

        views[f] = (view, 0)

    else:
        views[f] = (view, d_rule[comp])
    # print(views[f])


def canvas_write(message, size, l_size, x_space, y_space, offset_size, density, x_o, y_o, canvas = 0):

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

    def draw_c(size, canvas, corner):

        for x in range(int(size / 3) + 1):
            canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1

            canvas[corner[1] + int(size / 3) + x, corner[0]] = 1

        for x in range(int(size / 3) + 2):
            canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
            canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1

    def draw_d(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        d_coord_0 = (corner[1], corner[0] + int(size / 3))
        d_coord_1 = (corner[1] + size - 1, corner[0] + int(size / 3))

        canvas[d_coord_0] = 1
        canvas[d_coord_1] = 1

        canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3)] = 1

        d_legs = dict()

        for x in range(2):
            d_legs[x] = []

        for x in range(int(size / 3)):

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

    def draw_e(size, canvas, corner):

        canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
        canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3)] = 1

    def draw_f(size, canvas, corner):

        canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
        canvas[corner[1], corner[0]:corner[0] + int(size / 3)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1

    def draw_g(size, canvas, corner):

        canvas[corner[1] + int(size / 3 * 2), corner[0] + int(size / 3):corner[0] + int(size / 3 * 2)] = 1

        for x in range(int(size / 3) + 1):
            canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

            canvas[corner[1] + int(size / 3) + x, corner[0]] = 1

        for x in range(int(size / 3) + 2):
            canvas[corner[1], corner[0] + int(size / 3 / 2) + x] = 1
            canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1

    def draw_h(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1
        canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 2)] = 1

    def draw_i(size, canvas, corner):

        canvas[corner[1], corner[0] + int(size / 4):corner[0] + size - int(size / 4)] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size / 4):corner[0] + size - int(size / 4)] = 1
        canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size / 2)] = 1

    def draw_j(size, canvas, corner):

        for x in range(int(size / 3) + 1):
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

        for x in range(int(size / 3 * 2)):
            canvas[corner[1] + x, corner[0] + int(size / 3 * 2)] = 1

        for x in range(int(size / 3) + 2):
            canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1

    def draw_k(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        k_coord_0 = (corner[1] + int(size / 2), corner[0] + 1)

        canvas[k_coord_0] = 1

        k_legs = dict()

        for x in range(2):
            k_legs[x] = []

        for x in range(int(size / 2)):

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

    def draw_l(size, canvas, corner):
        canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2)] = 1

    def draw_m(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1
        canvas[corner[1]:corner[1] + size, corner[0] + size - 1] = 1

        apex = (corner[1] + size - 1, corner[0] + int(size / 2))

        canvas[apex] = 1

        m_legs = dict()

        for x in range(2):
            m_legs[x] = []

        for x in range(size - 2):

            if x % 2 == 0:

                m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x / 2)))
                m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x / 2)))

            else:

                m_legs[0].append((apex[0] - 1 - x, apex[1] - 1 - int(x / 2)))
                m_legs[1].append((apex[0] - 1 - x, apex[1] + 1 + int(x / 2)))

        for x in range(2):
            for m in m_legs[x]:
                canvas[m] = 1

    def draw_n(size, canvas, corner):

        canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
        canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size / 2)] = 1

        for x in range(size - 1):
            canvas[corner[1] + x, corner[0] + int(x / 2)] = 1

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

    def draw_p(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0]] = 1

        canvas[corner[1], corner[0]:corner[0] + int(size / 4)] = 1
        canvas[corner[1] + int(size / 2), corner[0]:corner[0] + int(size / 4)] = 1

        for x in range(int(size / 4) + 1):
            canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
            canvas[corner[1] + int(size / 2) - x, corner[0] + int(size / 4) + int(x / 2)] = 1

    def draw_q(size, canvas, corner):

        for x in range(int(size / 3) + 1):
            canvas[corner[1] + int(size / 3) - x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3) - x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2) + int(size / 3) + int(size / 3 / 2)] = 1

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

    def draw_s(size, canvas, corner):

        canvas[corner[1] + int(size / 6):corner[1] + int(size / 6) * 2, corner[0]] = 1
        canvas[corner[1] + int(size / 6) * 4:corner[1] + int(size / 6) * 5, corner[0] + int(size / 2)] = 1
        canvas[corner[1], corner[0] + int(size / 6):corner[0] + int(size / 2)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2) - int(size / 6)] = 1

        for x in range(int(size / 2)):
            canvas[corner[1] + int(size / 6) * 2 + int(5 * x / 6) - 1, corner[0] + x] = 1

        for x in range(int(size / 6)):
            canvas[corner[1] + int(size / 6) - x, corner[0] + x] = 1
            canvas[corner[1] + int(size / 6) * 5 + x, corner[0] + int(size / 2) - x - 1] = 1

    def draw_t(size, canvas, corner):

        canvas[corner[1]:corner[1] + size, corner[0] + int(size / 2)] = 1
        canvas[corner[1], corner[0] + int(size / 5):corner[0] + size - int(size / 5)] = 1

    def draw_u(size, canvas, corner):

        for x in range(int(size / 3) + 1):
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + int(size / 3 * 2) + x, corner[0] - int(x / 2) + int(size / 3 * 2)] = 1

        for x in range(int(size / 3 * 2)):
            canvas[corner[1] + x, corner[0]] = 1
            canvas[corner[1] + x, corner[0] + int(size / 3 * 2)] = 1

        for x in range(int(size / 3) + 2):
            canvas[corner[1] + size - 1, corner[0] + int(size / 3 / 2) + x] = 1

    def draw_v(size, canvas, corner):

        for x in range(size - 1):
            canvas[corner[1] + x, corner[0] + int(x / 3)] = 1
            canvas[corner[1] + x, corner[0] + int(size / 3 * 2) - int(x / 3) - 1] = 1

    def draw_w(size, canvas, corner):

        for x in range(size):
            canvas[corner[1] + x, corner[0] + int(x / 4)] = 1
            canvas[corner[1] + x, corner[0] + int(size / 2) - int(x / 4)] = 1
            canvas[corner[1] + x, corner[0] + int(x / 4) + int(size / 2)] = 1
            canvas[corner[1] + x, corner[0] + int(size) - int(x / 4) - 1] = 1

    def draw_x(size, canvas, corner):

        for x in range(size - 1):
            canvas[corner[1] + x, corner[0] + int(x / 2)] = 1
            canvas[corner[1] + x, corner[0] + int(size / 2) - int(x / 2) - 1] = 1

    def draw_y(size, canvas, corner):

        canvas[corner[1] + int(size / 2):corner[1] + int(size), corner[0] + int(size / 2)] = 1

        for x in range(int(size / 2)):
            canvas[corner[1] + x, corner[0] + int(size / 4) + int(x / 2)] = 1
            canvas[corner[1] + x, corner[0] + int(size / 4 * 3) - int(x / 2)] = 1

    def draw_z(size, canvas, corner):
        canvas[corner[1], corner[0]:corner[0] + int(size / 3 * 2)] = 1
        canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 3 * 2)] = 1

        for x in range(size):
            canvas[corner[1] + x, corner[0] + int(size / 3 * 2) - int(2 * x / 3)] = 1


    if canvas == 0:
        canvas = np.zeros((size, size), dtype='int8')

    m_list = message.split()

    print("")
    print("m_list")
    print(m_list)

    line = 0

    for m in m_list:

        l_place = 0

        for c in m:

            if c == 'a':

                for offset in (0, offset_size, density):
                    draw_a(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_a(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_a(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_a(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'b':

                for offset in (0, offset_size, density):
                    draw_b(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_b(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_b(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_b(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'c':

                for offset in (0, offset_size, density):
                    draw_c(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_c(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_c(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_c(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'd':

                for offset in (0, offset_size, density):
                    draw_d(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_d(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_d(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_d(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'e':

                for offset in (0, offset_size, density):
                    draw_e(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_e(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_e(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_e(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'f':

                for offset in (0, offset_size, density):
                    draw_f(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_f(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_f(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_f(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'g':

                for offset in (0, offset_size, density):
                    draw_g(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_g(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_g(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_g(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'h':

                for offset in (0, offset_size, density):
                    draw_h(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_h(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_h(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_h(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'i':

                for offset in (0, offset_size, density):
                    draw_i(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_i(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_i(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_i(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'j':

                for offset in (0, offset_size, density):
                    draw_j(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_j(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_j(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_j(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'k':

                for offset in (0, offset_size, density):
                    draw_k(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_k(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_k(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_k(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'l':

                for offset in (0, offset_size, density):
                    draw_l(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_l(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_l(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_l(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'm':

                for offset in (0, offset_size, density):
                    draw_m(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_m(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_m(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_m(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'n':

                for offset in (0, offset_size, density):
                    draw_n(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_n(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_n(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_n(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'o':

                for offset in (0, offset_size, density):
                    draw_o(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_o(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_o(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_o(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'p':

                for offset in (0, offset_size, density):
                    draw_p(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_p(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_p(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_p(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'q':

                for offset in (0, offset_size, density):
                    draw_q(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_q(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_q(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_q(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'r':

                for offset in (0, offset_size, density):
                    draw_r(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_r(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_r(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_r(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 's':

                for offset in (0, offset_size, density):
                    draw_s(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_s(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_s(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_s(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 't':

                for offset in (0, offset_size, density):
                    draw_t(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_t(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_t(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_t(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'u':

                for offset in (0, offset_size, density):
                    draw_u(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_u(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_u(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_u(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'v':

                for offset in (0, offset_size, density):
                    draw_v(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_v(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_v(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_v(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'w':

                for offset in (0, offset_size, density):
                    draw_w(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_w(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_w(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_w(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'x':

                for offset in (0, offset_size, density):
                    draw_x(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_x(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_x(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_x(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'y':

                for offset in (0, offset_size, density):
                    draw_y(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_y(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_y(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_y(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == 'z':

                for offset in (0, offset_size, density):
                    draw_z(l_size, canvas, (x_o + offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_z(l_size, canvas, (x_o - offset + (l_size + x_space) * l_place, y_o + l_size * line + y_space * line))
                    draw_z(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o + offset + l_size * line + y_space * line))
                    draw_z(l_size, canvas, (x_o + (l_size + x_space) * l_place, y_o - offset + l_size * line + y_space * line))

            if c == '-':

                True

            l_place += 1

        line += 1

    return canvas


# for f in fence:
#     step(views, f)
#     canvas[f] = views[f][1]


#####game#####

pygame.init()
pygame.display.init()

current_display = pygame.display.Info()
# WIDTH , HEIGHT = current_display.current_w - 50, current_display.current_h - 100
size = 7
WIDTH, HEIGHT = (size * 30 + 3) * 2, (size * 30 + 3) * 2
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
letter_values = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9, 'a': 10, 's': 11,
                 'd': 12, 'f': 13,
                 'g': 14, 'h': 15, 'j': 16, 'k': 17, 'l': 18, 'z': 19, 'x': 20, 'c': 21, 'v': 22, 'b': 23, 'n': 24,
                 'm': 25, ' ': 26}

pygame.display.set_caption("C.H.A.O.S")

click = False


def Chaos_Window(base, pixel_res):

    run, FPS, rule, clock, journal, press, view = 1, 3840, 74059875469082347291091262374908567234, pygame.time.Clock(), dict(), dict(), 4
    cell_row_width, cell_rows = int(WIDTH / pixel_res), int(HEIGHT / pixel_res)
    d_rule, i_rule = rule_gen_2(rule, base)
    canvas = np.zeros((cell_rows, cell_row_width), dtype='int8')
    start = (int(cell_rows / 2), int(cell_row_width / 2))

    infile = open('2d-fences/full-fence_spiral_' + str(int(WIDTH/2)), 'rb')
    full_fence = pickle.load(infile)
    infile.close()

    canvas[start] = 1
    views = dict()
    views[0] = 0

    viewer_2(full_fence, cell_rows, views)

    cells = dict()

    page = []
    rand_count = 0
    steps = 0

    color_1 = (0, 0, 0)
    color_2 = (255, 0, 255)
    color_3 = (0, 255, 255)
    color_4 = (255, 255, 255)
    color_l = (255, 255, 255)

    message = '--ray --and frances'

    size = 303
    l_size = 21
    x_space = 5
    y_space = 50
    offset_size = 4
    density = 1
    x_o = 7
    y_o = 20

    if len(message) > 0:
        canvas = canvas_write(message, size, l_size, x_space, y_space, offset_size, density, x_o, y_o)

    print(" ")
    print("d_rule")
    print(d_rule)
    print("i_rule")
    print(i_rule)
    print(len(i_rule))

    def redraw_window():

        rule_label_0_b = text_font.render(f"RUL3:{i_rule[0:int((base ** view) / 2)]}", 1, (255, 255, 255))
        rule_label_1_b = text_font.render(f"          {i_rule[int((base ** view) / 2):int((base ** view))]}", 1,
                                          (255, 255, 255))

        step_label_b = text_font.render(f"5T3P: {steps}", 1, (255, 255, 255))
        rand_count_l = text_font.render(f"{rand_count}", 1, (255, 255, 255))

        # WIN.blit(rule_label_0_b, (10, HEIGHT - 40))
        # WIN.blit(rule_label_1_b, (7, HEIGHT - 25))

        # WIN.blit(step_label_b, (0, 0))
        WIN.blit(rand_count_l, (WIDTH, 0))

        pygame.display.update()

    def input(letter, base):

        bv = base ** view

        if letter not in press:
            press[letter] = 0
        else:
            press[letter] += 1

        place = int((letter_values[letter] + ((press[letter] % (int(bv / len(letter_values)) + 1)) * int(
            (bv / int(bv / len(letter_values) + 1))))) % bv)

        if i_rule[place] == 0:

            i_rule[place] = 1
            d_rule[list(d_rule.keys())[place]] = 1

        elif i_rule[place] == 1:

            if base == 2:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 2
                d_rule[list(d_rule.keys())[place]] = 2

        elif i_rule[place] == 2:

            if base == 3:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 3
                d_rule[list(d_rule.keys())[place]] = 3

        else:
            i_rule[place] = 0
            d_rule[list(d_rule.keys())[place]] = 0

        r_0 = tuple(i_rule)

        if r_0 in page:

            journal[r_0].append(page)

        else:

            journal[r_0] = []
            journal[r_0].append(page)

    for f in full_fence:

        cell = pygame.Rect(f[0] * pixel_res, f[1] * pixel_res, pixel_res, pixel_res)
        cells[f] = cell

        if canvas[f] == 0:
            pygame.draw.rect(WIN, color_1, cell)

        if canvas[f] == 1:
            pygame.draw.rect(WIN, color_2, cell)

        if canvas[f] == 2:
            pygame.draw.rect(WIN, color_3, cell)

        if canvas[f] == 3:
            pygame.draw.rect(WIN, color_4, cell)

    pygame.display.update()

    while run == 1:

        steps += 1
        WIN.fill((0, 0, 0))
        clock.tick(FPS)

        cnvs = []

        for f in full_fence:

            cnvs.append(views[f][1])

            step(views, f, d_rule, canvas)

            cell = cells[f]

            # if canvas[f[1], f[0]] == 1:
            #     pygame.draw.rect(WIN, color_l, cell)

            if views[f][1] == 0:
                pygame.draw.rect(WIN, color_1, cell)

            elif views[f][1] == 1:
                pygame.draw.rect(WIN, color_2, cell)

            elif views[f][1] == 2:
                pygame.draw.rect(WIN, color_3, cell)

            elif views[f][1] == 3:
                pygame.draw.rect(WIN, color_4, cell)

        cnvs = tuple(cnvs)

        if cnvs in page:

            rand_count += 1
            r_0 = tuple(i_rule)
            rand = random.randrange(0, base ** view - 1)

            if r_0 in page:

                journal[r_0].append(page)

            else:

                journal[r_0] = []
                journal[r_0].append(page)

            page = []

            if base == 2:
                if i_rule[rand] == 0:
                    i_rule[rand] = 1
                    d_rule[list(d_rule.keys())[rand]] = 1
                elif i_rule[rand] == 1:
                    i_rule[rand] = 0
                    d_rule[list(d_rule.keys())[rand]] = 0

            if base == 3:
                if i_rule[rand] == 0:
                    i_rule[rand] = 1
                    d_rule[list(d_rule.keys())[rand]] = 1
                elif i_rule[rand] == 1:
                    i_rule[rand] = 2
                    d_rule[list(d_rule.keys())[rand]] = 2
                elif i_rule[rand] == 2:
                    i_rule[rand] = 0
                    d_rule[list(d_rule.keys())[rand]] = 0

            if base == 4:
                if i_rule[rand] == 0:
                    i_rule[rand] = 1
                    d_rule[list(d_rule.keys())[rand]] = 1
                elif i_rule[rand] == 1:
                    i_rule[rand] = 2
                    d_rule[list(d_rule.keys())[rand]] = 2
                elif i_rule[rand] == 2:
                    i_rule[rand] = 3
                    d_rule[list(d_rule.keys())[rand]] = 3
                elif i_rule[rand] == 3:
                    i_rule[rand] = 0
                    d_rule[list(d_rule.keys())[rand]] = 0

        else:
            page.append(cnvs)

        redraw_window()
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    run = 2

                if event.key == pygame.K_q:
                    input('q', base)
                    page = []

                if event.key == pygame.K_w:
                    input('w', base)
                    page = []

                if event.key == pygame.K_e:
                    input('e', base)
                    page = []

                if event.key == pygame.K_r:
                    input('r', base)
                    page = []

                if event.key == pygame.K_t:
                    input('t', base)
                    page = []

                if event.key == pygame.K_y:
                    input('y', base)
                    page = []

                if event.key == pygame.K_u:
                    input('u', base)
                    page = []

                if event.key == pygame.K_i:
                    input('i', base)
                    page = []

                if event.key == pygame.K_o:
                    input('o', base)
                    page = []

                if event.key == pygame.K_p:
                    input('p', base)
                    page = []

                if event.key == pygame.K_a:
                    input('a', base)
                    page = []

                if event.key == pygame.K_s:
                    input('s', base)
                    page = []

                if event.key == pygame.K_d:
                    input('d', base)
                    page = []

                if event.key == pygame.K_f:
                    input('f', base)
                    page = []

                if event.key == pygame.K_g:
                    input('g', base)
                    page = []

                if event.key == pygame.K_h:
                    input('h', base)
                    page = []

                if event.key == pygame.K_j:
                    input('j', base)
                    page = []

                if event.key == pygame.K_k:
                    input('k', base)
                    page = []

                if event.key == pygame.K_l:
                    input('l', base)
                    page = []

                if event.key == pygame.K_z:
                    input('z', base)
                    page = []

                if event.key == pygame.K_x:
                    input('x', base)
                    page = []

                if event.key == pygame.K_c:
                    input('c', base)
                    page = []

                if event.key == pygame.K_v:
                    input('v', base)
                    page = []

                if event.key == pygame.K_b:
                    input('b', base)
                    page = []

                if event.key == pygame.K_n:
                    input('n', base)
                    page = []

                if event.key == pygame.K_m:
                    input('m', base)
                    page = []

                if event.key == pygame.K_SPACE:
                    input(' ', base)
                    page = []

    j_num = len(os.listdir('2d-journals'))

    filename = '2d-journals/journal_' + str(j_num)
    outfile = open(filename, 'wb')
    pickle.dump(journal, outfile)
    outfile.close


# menus

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)


def draw_text(text, font, color_dt, surface, x, y):
    textobj = font.render(text, 1, color_dt)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def menu():
    click = False
    input_text = ''

    while True:

        WIN.fill((0, 0, 0))
        t_line = pygame.Rect(WIDTH / 2 - 633, 200, 1360, 2)
        draw_text('C311UL4R H4PT1C 4UT0M4T4 0P3R4T1NG 5Y5T3M', TITLE_FONT, (10, 100, 10), WIN, WIDTH / 2 - 655, 100)
        pygame.draw.rect(WIN, (10, 100, 10), t_line)

        text_surface = main_font.render(input_text, True, (100, 10, 100))
        mx, my = pygame.mouse.get_pos()

        size_2 = pygame.Rect(WIDTH / 2 - 300, 400, 200, 50)
        size_3 = pygame.Rect(WIDTH / 2 - 300, 500, 200, 50)
        size_5 = pygame.Rect(WIDTH / 2 - 300, 600, 200, 50)
        size_10 = pygame.Rect(WIDTH / 2 - 300, 700, 200, 50)
        size_2_i = pygame.Rect(WIDTH / 2 - 300, 400, 197, 43)
        size_3_i = pygame.Rect(WIDTH / 2 - 300, 500, 197, 43)
        size_5_i = pygame.Rect(WIDTH / 2 - 300, 600, 197, 43)
        size_10_i = pygame.Rect(WIDTH / 2 - 300, 700, 197, 43)

        binary = pygame.Rect(WIDTH / 2 + 100, 400, 200, 50)
        ternary = pygame.Rect(WIDTH / 2 + 100, 500, 200, 50)
        quaternary = pygame.Rect(WIDTH / 2 + 100, 600, 200, 50)
        binary_i = pygame.Rect(WIDTH / 2 + 100, 400, 197, 43)
        ternary_i = pygame.Rect(WIDTH / 2 + 100, 500, 197, 43)
        quaternary_i = pygame.Rect(WIDTH / 2 + 100, 600, 197, 43)

        vel_rect = pygame.Rect(WIDTH / 2 + 100, 700, 200, 50)
        vel_rect_i = pygame.Rect(WIDTH / 2 + 100, 700, 197, 43)

        enter = pygame.Rect(WIDTH / 2 - 100, 850, 200, 50)
        enter_i = pygame.Rect(WIDTH / 2 - 100, 850, 197, 43)

        underline_1 = pygame.Rect(WIDTH / 2 + 100, 385, 200, 2)
        underline_2 = pygame.Rect(WIDTH / 2 - 300, 385, 200, 2)

        pygame.draw.rect(WIN, (10, 100, 10), size_2)
        pygame.draw.rect(WIN, (10, 100, 10), size_3)
        pygame.draw.rect(WIN, (10, 100, 10), size_5)
        pygame.draw.rect(WIN, (10, 100, 10), size_10)
        pygame.draw.rect(WIN, (0, 0, 0), size_2_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_3_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_5_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_10_i)
        draw_text(' small', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 400)
        draw_text(' medium', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 500)
        draw_text(' large', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 600)
        draw_text(' X-large', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 700)
        draw_text('Cell Size', main_font, (10, 100, 10), WIN, WIDTH / 2 - 280, 340)
        pygame.draw.rect(WIN, (10, 100, 10), underline_2)

        pygame.draw.rect(WIN, (100, 10, 10), binary)
        pygame.draw.rect(WIN, (100, 10, 10), ternary)
        pygame.draw.rect(WIN, (100, 10, 10), quaternary)
        pygame.draw.rect(WIN, (0, 0, 0), binary_i)
        pygame.draw.rect(WIN, (0, 0, 0), ternary_i)
        pygame.draw.rect(WIN, (0, 0, 0), quaternary_i)
        draw_text(' Two', main_font, (100, 10, 10), WIN, WIDTH / 2 + 100, 400)
        draw_text(' Three', main_font, (100, 10, 10), WIN, WIDTH / 2 + 100, 500)
        draw_text(' Four', main_font, (100, 10, 10), WIN, WIDTH / 2 + 100, 600)
        draw_text('Number of Colors', main_font, (100, 10, 10), WIN, WIDTH / 2 + 80, 340)
        pygame.draw.rect(WIN, (100, 10, 10), underline_1)

        pygame.draw.rect(WIN, (100, 10, 100), vel_rect)
        pygame.draw.rect(WIN, (0, 0, 0), vel_rect_i)
        draw_text('^place mouse-pointer on box to type;', small_font, (100, 10, 100), WIN, WIDTH / 2 + 200, 775)
        draw_text('numbers between 1-10 recommended', small_font, (100, 10, 100), WIN, WIDTH / 2 + 210, 800)

        pygame.draw.rect(WIN, (10, 10, 100), enter)
        pygame.draw.rect(WIN, (0, 0, 0), enter_i)
        draw_text(' Enter', main_font, (10, 10, 100), WIN, WIDTH / 2 - 100, 850)

        draw_text('Instructions:', small_font, (200, 200, 200), WIN, 50, 275)
        draw_text('1. Choose a cell-size. [GREEN]', small_font, (200, 200, 200), WIN, 50, 325)
        draw_text('     -Start with X-large to be safe. Smaller cells', text_font, (200, 200, 200), WIN, 50, 365)
        draw_text('         may cause issues on slower computers.', text_font, (200, 200, 200), WIN, 50, 390)
        draw_text('2. Choose the number of cell colors. [RED]', small_font, (200, 200, 200), WIN, 50, 425)
        draw_text('3. Set a desired speed. [PURPLE]', small_font, (200, 200, 200), WIN, 50, 475)
        draw_text('4. Press Enter [BLUE]', small_font, (200, 200, 200), WIN, 50, 525)
        draw_text('     The program will have loaded once you see Step & Count', text_font, (200, 200, 200), WIN, 50,
                  575)
        draw_text('     in the top right, and Rule in the bottom left.', text_font, (200, 200, 200), WIN, 50, 600)
        draw_text('     Typing has no effect until the first row of colored', text_font, (200, 200, 200), WIN, 50, 625)
        draw_text('     cells reach the bottom of the page.', text_font, (200, 200, 200), WIN, 50, 650)
        draw_text('     Two cell colors uses the keys (asdf-jkl;) to change the rules.', text_font, (200, 200, 200),
                  WIN, 50, 675)
        draw_text('     For three colors+, the best effects are seen while typing full sentences', text_font,
                  (200, 200, 200), WIN, 50, 700)
        draw_text('     Press the escape key to exit the program at any time.', text_font, (200, 200, 200), WIN, 50,
                  725)
        draw_text('     Enjoy!', text_font, (200, 200, 200), WIN, 50, 750)

        if size_2.collidepoint((mx, my)):
            if click:
                print("size_2")
                pixel_res = 2
                draw_text(' small', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 400)
        if size_3.collidepoint((mx, my)):
            if click:
                print("size_3")
                pixel_res = 3
                draw_text(' medium', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 500)
        if size_5.collidepoint((mx, my)):
            if click:
                print("size_5")
                pixel_res = 5
                draw_text(' large', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 600)
        if size_10.collidepoint((mx, my)):
            if click:
                print("size_10")
                pixel_res = 10
                draw_text(' X-large', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 700)

        if binary.collidepoint((mx, my)):
            if click:
                print("binary")
                base = 2
                draw_text(' Two', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 400)
        if ternary.collidepoint((mx, my)):
            if click:
                print("ternary")
                base = 3
                draw_text(' Three', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 500)
        if quaternary.collidepoint((mx, my)):
            if click:
                print("quaternary")
                base = 4
                draw_text(' Four', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 600)

        if vel_rect.collidepoint((mx, my)):
            draw_text('Speed:', main_font, (100, 10, 100), WIN, WIDTH / 2 + 100, 700)
            WIN.blit(text_surface, (WIDTH / 2 + 200, 700))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text += '1'
                    if event.key == K_2:
                        input_text += '2'
                    if event.key == K_3:
                        input_text += '3'
                    if event.key == K_4:
                        input_text += '4'
                    if event.key == K_5:
                        input_text += '5'
                    if event.key == K_6:
                        input_text += '6'
                    if event.key == K_7:
                        input_text += '7'
                    if event.key == K_8:
                        input_text += '8'
                    if event.key == K_9:
                        input_text += '9'
                    if event.key == K_0:
                        input_text += '0'
                    if event.key == K_BACKSPACE:
                        input_text = input_text[:len(input_text) - 1]
                    print(input_text)

            if len(input_text) > 0:
                cell_vel = int(input_text)

        if enter.collidepoint((mx, my)):
            if click:
                print("enter")
                print("pixel_res")
                print(pixel_res)
                draw_text('Enter', main_font, (255, 255, 255), WIN, WIDTH / 2 - 100, 800)
                Chaos_Window(base, pixel_res, cell_vel)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        mainClock.tick(60)


# menu()

Chaos_Window(4, 2)
