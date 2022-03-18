import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c


size = 39
l_size = 11

canvas = np.zeros((size, size))

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

    canvas[corner[1]:corner[1] + size, corner[0]] = 1
    canvas[corner[1]:corner[1] + size, corner[0] + size - 1 - int(size/2) + int(size/4)] = 1

    canvas[corner[1], corner[0]:corner[0] + size - int(size/2) + int(size/4)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + size - int(size/2) + int(size/4)] = 1


def draw_r(size, canvas, corner):

    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    r_coord_0 = (corner[1] + int(size/2) + 1, corner[0] + 1)
    r_coord_1 = (corner[1] + int(size/2), corner[0] + 2)
    r_coord_2 = (corner[1], corner[0] + 2)

    canvas[r_coord_0] = 1
    canvas[r_coord_1] = 1
    canvas[(r_coord_1[0], r_coord_1[1] - 1)] = 1
    canvas[r_coord_2] = 1
    canvas[(r_coord_2[0], r_coord_2[1] - 1)] = 1

    r_legs = dict()

    for x in range(3):
        r_legs[x] = []

    for x in range(int(size/2) - 1):

        if x == 0:

            r_legs[0].append(r_coord_0)
            r_legs[1].append(r_coord_1)
            r_legs[2].append(r_coord_2)

        r_legs[0].append((r_coord_0[0] + 1 + x, r_coord_0[1] + 1 + x))
        r_legs[1].append((r_coord_1[0] - x, r_coord_1[1] + x))
        r_legs[2].append((r_coord_2[0] + x, r_coord_2[1] + x))

    r_legs[1] = r_legs[1][:-1]
    r_legs[2] = r_legs[2][:-1]

    # print(r_legs[0])
    # print(r_legs[1])
    # print(r_legs[2])

    for k in r_legs[0]:
        canvas[k] = 1

    for k in r_legs[1]:
        canvas[k] = 1

    for k in r_legs[2]:
        canvas[k] = 1


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


draw_k(l_size, canvas, (2, 5))
draw_o(l_size, canvas, (11, 5))
draw_r(l_size, canvas, (22, 5))
draw_d(l_size, canvas, (30, 5))

draw_a(l_size, canvas, (2, 23))
draw_m(l_size, canvas, (16, 23))
draw_i(l_size, canvas, (28, 23))








magenta = (1, 0, 1)
yellow = (1, 1, 0)
cyan = (0, 1, 1)
red = (1, 0, 0)
blue = (0, 0, 1)
green = (0, 1, 0)
black = (0, 0, 0)
white = (1, 1, 1)
grey = (.5, .5, .5)

cMap = c.ListedColormap([white, red, green, black])

canvas = np.flip(canvas, 0)
plt.pcolormesh(canvas, cmap=cMap)

ax = plt.gca()
ax.set_aspect(1)

plt.margins(0, None)
plt.grid(visible=True, axis='both', )
plt.xticks(np.arange(0, size, step=1))
plt.yticks(np.arange(0, size, step=1))

plt.show()