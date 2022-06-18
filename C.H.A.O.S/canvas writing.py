import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c

plt.ioff()

size = 2001

l_size = 901
x_space = 50
y_space = 50

offset_size = 3
density = 50
x_o = 300
y_o = 50

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

def draw_b(size, canvas, corner):

    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    canvas[corner[1], corner[0]:corner[0] + int(size/4)] = 1
    canvas[corner[1] + int(size/2), corner[0]:corner[0] + int(size/4)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size/4)] = 1

    for x in range(int(size/4) + 1):

        canvas[corner[1] + x, corner[0] + int(size/4) + int(x/2)] = 1
        canvas[corner[1] + int(size/2) - x, corner[0] + int(size/4) + int(x/2)] = 1

        canvas[corner[1] + x + int(size/2), corner[0] + int(size/4) + int(x/2)] = 1
        canvas[corner[1] + int(size) - x - 1, corner[0] + int(size/4) + int(x/2)] = 1

def draw_c(size, canvas, corner):

    for x in range(int(size/3) + 1):

        canvas[corner[1] + int(size/3) - x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2)] = 1

        canvas[corner[1] + int(size/3) + x, corner[0]] = 1


    for x in range(int(size/3) + 2):

        canvas[corner[1], corner[0] + int(size/3/2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size/3/2) + x] = 1

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

def draw_e(size, canvas, corner):

    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1], corner[0]:corner[0] + int(size/3)] = 1
    canvas[corner[1] + int(size/2), corner[0]:corner[0] + int(size/4)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size/3)] = 1

def draw_f(size, canvas, corner):

    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1], corner[0]:corner[0] + int(size/3)] = 1
    canvas[corner[1] + int(size/2), corner[0]:corner[0] + int(size/4)] = 1

def draw_g(size, canvas, corner):

    canvas[corner[1] + int(size/3 * 2), corner[0] + int(size/3):corner[0] + int(size/3 * 2)] = 1

    for x in range(int(size/3) + 1):

        canvas[corner[1] + int(size/3) - x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] - int(x/2) + int(size/3 * 2)] = 1

        canvas[corner[1] + int(size/3) + x, corner[0]] = 1

    for x in range(int(size/3) + 2):

        canvas[corner[1], corner[0] + int(size/3/2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size/3/2) + x] = 1

def draw_h(size, canvas, corner):

    canvas[corner[1]:corner[1] + size, corner[0]] = 1
    canvas[corner[1]:corner[1] + size, corner[0] + int(size/2)] = 1
    canvas[corner[1] + int(size/2), corner[0]:corner[0] + int(size/2)] = 1

def draw_i(size, canvas, corner):

    canvas[corner[1], corner[0] + int(size/4):corner[0] + size - int(size/4)] = 1
    canvas[corner[1] + size - 1, corner[0] + int(size/4):corner[0] + size - int(size/4)] = 1
    canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size/2)] = 1

def draw_j(size, canvas, corner):

    for x in range(int(size/3) + 1):

        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] - int(x/2) + int(size/3 * 2)] = 1

    for x in range(int(size/3*2)):
        canvas[corner[1] + x, corner[0] + int(size/3 * 2)] = 1

    for x in range(int(size/3) + 2):

        canvas[corner[1] + size - 1, corner[0] + int(size/3/2) + x] = 1

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

def draw_l(size, canvas, corner):
    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size / 2)] = 1

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

def draw_n(size, canvas, corner):

    canvas[corner[1]:corner[1] + size - 1, corner[0]] = 1
    canvas[corner[1]:corner[1] + size - 1, corner[0] + int(size/2)] = 1

    for x in range(size - 1):

        canvas[corner[1] + x, corner[0] + int(x/2)] = 1

def draw_o(size, canvas, corner):

    for x in range(int(size/3) + 1):

        canvas[corner[1] + int(size/3) - x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3) - x, corner[0] - int(x/2) + int(size/3 * 2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] - int(x/2) + int(size/3 * 2)] = 1


        canvas[corner[1] + int(size/3) + x, corner[0]] = 1
        canvas[corner[1] + int(size/3) + x, corner[0] + int(size/3 * 2)] = 1

    for x in range(int(size/3) + 2):

        canvas[corner[1], corner[0] + int(size/3/2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size/3/2) + x] = 1

def draw_p(size, canvas, corner):

    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    canvas[corner[1], corner[0]:corner[0] + int(size/4)] = 1
    canvas[corner[1] + int(size/2), corner[0]:corner[0] + int(size/4)] = 1

    for x in range(int(size/4) + 1):

        canvas[corner[1] + x, corner[0] + int(size/4) + int(x/2)] = 1
        canvas[corner[1] + int(size/2) - x, corner[0] + int(size/4) + int(x/2)] = 1

def draw_q(size, canvas, corner):

    for x in range(int(size/3) + 1):

        canvas[corner[1] + int(size/3) - x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3) - x, corner[0] - int(x/2) + int(size/3 * 2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] - int(x/2) + int(size/3 * 2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2) + int(size/3) + int(size/3/2)] = 1

        canvas[corner[1] + int(size/3) + x, corner[0]] = 1
        canvas[corner[1] + int(size/3) + x, corner[0] + int(size/3 * 2)] = 1

    for x in range(int(size/3) + 2):

        canvas[corner[1], corner[0] + int(size/3/2) + x] = 1
        canvas[corner[1] + size - 1, corner[0] + int(size/3/2) + x] = 1

def draw_r(size, canvas, corner):

    canvas[corner[1]:corner[1] + size, corner[0]] = 1

    r_coord_0 = (corner[1] + int(size/2), corner[0] + 1)
    r_coord_1 = (corner[1], corner[0] + 1)
    r_coord_2 = (corner[1] + int(size/2), corner[0] + 1 + int(size/5))
    r_coord_3 = (corner[1], corner[0] + 1 + int(size/5))

    # print(r_coord_1)
    # print(r_coord_2)


    canvas[corner[1], corner[0]:corner[0] + int(size/4)] = 1
    canvas[corner[1] + int(size/2), corner[0]:corner[0] + int(size/4)] = 1


    r_legs = dict()

    for x in range(3):
        r_legs[x] = []

    for x in range(int(size/2) + 1):

        canvas[corner[1] + int(size/2) + x, corner[0] + int(size/5) + int(x/2)] = 1

    for x in range(int(size/4) + 1):

        canvas[corner[1] + x, corner[0] + int(size/4) + int(x/2)] = 1
        canvas[corner[1] + int(size/2) - x, corner[0] + int(size/4) + int(x/2)] = 1

def draw_s(size, canvas, corner):

    canvas[corner[1] + int(size/6):corner[1] + int(size/6) * 2, corner[0]] = 1
    canvas[corner[1] + int(size/6) * 4:corner[1] + int(size/6) * 5, corner[0] + int(size/2)] = 1
    canvas[corner[1], corner[0] + int(size/6):corner[0] + int(size/2)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size/2) - int(size/6)] = 1

    for x in range(int(size/2)):
        canvas[corner[1] + int(size/6) * 2 + int(5 * x/6) - 1, corner[0] + x] = 1

    for x in range(int(size/6)):

        canvas[corner[1] + int(size/6) - x, corner[0] + x] = 1
        canvas[corner[1] + int(size/6) * 5 + x, corner[0] + int(size/2) - x - 1] = 1

def draw_t(size, canvas, corner):

    canvas[corner[1]:corner[1] + size, corner[0] + int(size/2)] = 1
    canvas[corner[1], corner[0] + int(size/5):corner[0] + size - int(size/5)] = 1

def draw_u(size, canvas, corner):

    for x in range(int(size/3) + 1):

        canvas[corner[1] + int(size/3 * 2) + x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + int(size/3 * 2) + x, corner[0] - int(x/2) + int(size/3 * 2)] = 1

    for x in range(int(size/3*2)):
        canvas[corner[1] + x, corner[0]] = 1
        canvas[corner[1] + x, corner[0] + int(size/3 * 2)] = 1

    for x in range(int(size/3) + 2):

        canvas[corner[1] + size - 1, corner[0] + int(size/3/2) + x] = 1

def draw_v(size, canvas, corner):

    for x in range(size - 1):
        canvas[corner[1] + x, corner[0] + int(x/3)] = 1
        canvas[corner[1] + x, corner[0] + int(size/3*2) - int(x/3) - 1] = 1

def draw_w(size, canvas, corner):

    for x in range(size):

        canvas[corner[1] + x, corner[0] + int(x/4)] = 1
        canvas[corner[1] + x, corner[0] + int(size/2) - int(x/4)] = 1
        canvas[corner[1] + x, corner[0] + int(x/4) + int(size/2)] = 1
        canvas[corner[1] + x, corner[0] + int(size) - int(x/4) - 1] = 1

def draw_x(size, canvas, corner):

    for x in range(size - 1):
        canvas[corner[1] + x, corner[0] + int(x/2)] = 1
        canvas[corner[1] + x, corner[0] + int(size/2) - int(x/2) - 1] = 1

def draw_y(size, canvas, corner):

    canvas[corner[1] + int(size/2):corner[1] + int(size), corner[0] + int(size/2)] = 1

    for x in range(int(size/2)):
        canvas[corner[1] + x, corner[0] + int(size/4) + int(x/2)] = 1
        canvas[corner[1] + x, corner[0] + int(size/4*3) - int(x/2)] = 1

def draw_z(size, canvas, corner):
    canvas[corner[1], corner[0]:corner[0] + int(size/3*2)] = 1
    canvas[corner[1] + size - 1, corner[0]:corner[0] + int(size/3*2)] = 1

    for x in range(size):
        canvas[corner[1] + x, corner[0] + int(size/3*2) - int(2*x/3)] = 1



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

# canvas = breathe(size, l_size, space, 10, 2, 10, 20)

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


message = 'zu zu'

canvas = canvas_write(message, size, l_size, x_space, y_space, offset_size, density, x_o, y_o)


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

# plt.margins(0, None)
# plt.grid(visible=True, axis='both', )
# plt.xticks(np.arange(0, size, step=1))
# plt.yticks(np.arange(0, size, step=1))

plt.show()