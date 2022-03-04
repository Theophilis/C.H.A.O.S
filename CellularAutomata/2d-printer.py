import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import pickle

np.set_printoptions(linewidth=np.inf)
plt.ioff()

rule = 1001
base = 4
size = 505
view = 4
start = (int(size/2), int(size/2))
zero = (0, 0)

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


def rule_gen_2(rule, base = 2, width = 0):

    rules = dict()

    if type(rule) != int:
        int_rule = rule


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


def fencing(zero, level = 0):
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
    # print(fence)
    return fence


def viewer(f, canvas):

    if f[0] > 0:
        v_1 = canvas[(f[0] - 1, f[1])]
    if f[0] < size - 1:
        v_3 = canvas[(f[0] + 1, f[1])]
    if f[0] == 0:
        v_1 = 0
    if f[0] == size - 1:
        v_3 = 0

    if f[1] > 0:
        v_4 = canvas[(f[0], f[1] - 1)]
    if f[1] < size - 1:
        v_2 = canvas[(f[0], f[1] + 1)]
    if f[1] == 0:
        v_4 = 0
    if f[1] == size - 1:
        v_2 = 0

    # view = (canvas[c_1], canvas[c_2], canvas[c_3], canvas[c_4])
    view = (str(v_1), str(v_2), str(v_3), str(v_4))

    return view


def fence_map(start, order=0):

    if order == 0:
        fence = dict()

        for x in range(int(size/2)):
            zero = (start[0] - (x + 1), start[0] - (x + 1))
            fence[x] = fencing(zero, x)

        full_fence = []
        for k in list(fence.keys()):
            for f in fence[k][:len(fence[k]) - 1]:
                full_fence.append(f)

        canvas_f = np.zeros((size, size), dtype='int8')
        full_fence.insert(0, start)

        for f in full_fence:
            canvas_f[f] = full_fence.index(f)

        return full_fence, canvas_f

    elif order == 1:
        canvas_t = np.zeros((size, size), dtype='int8')

        t_fence = []

        for x in range(size):
            for y in range(size):
                t_fence.append((x, y))

        for t in t_fence:
            canvas_t[t] = t_fence.index(t)

        return t_fence, canvas_t

    elif order == 2:
        canvas = np.zeros((size, size), dtype='int8')

        fence = []

        for x in range(size):
            for y in range(size):
                fence.append((x, y))

        fence = sorted(fence, key=lambda x: abs(x[0] + x[1]))

        for f in fence:
            canvas[f] = fence.index(f)

        return fence, canvas


def map(size, rule, path, order, plot=0):

    if type(rule) != int:
        r_n = decimal(rule, base)

    else:
        r_n = rule

    file = str(size) + '-' + str(base) + '-' + 'colors' + '-' + str(r_n)
    path_name = os.path.join(path, file)
    print(path_name)

    canvas = np.zeros((size, size), dtype='int8')
    canvas[start] = 1

    d_rule, i_rule = rule_gen_2(rule, base)

    full_fence, canvas_f = fence_map(start, order)

    for f in full_fence:
        view = viewer(f, canvas)
        canvas[f] = d_rule[view]

    # print(canvas)

    if plot != 0:

        ax = plt.gca()
        ax.set_aspect(1)

        if base == 4:
            cMap = c.ListedColormap([(0, 0, 0), (1, 0, 1), (1, 1, 0), (0, 1, 1)], 'quad', 4)

        if base == 3:
            cMap = c.ListedColormap(['k', 'm', 'c'], 'tri', 3)

        if base == 2:
            cMap = c.ListedColormap(['w', 'k'])

        plt.pcolormesh(canvas, cmap=cMap)

        # plt.xticks(np.arange(0, size, step=1))
        # plt.yticks(np.arange(0, size, step=1))

        # plt.figtext(.3, .925, i_rule, fontsize=14)
        # plt.figtext(.0075, .05, d_rule, fontsize=7)
        # plt.grid(visible=True, axis='both', )

        # c_plt.show()
        plt.savefig(path_name, dpi=900)
        plt.close()

    return canvas


def step(views, f):

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

    v_0 = viewer(f, canvas)
    print(views[f])

    print(comp)
    print(v_0)

    print(d_rule[comp])
    print(d_rule[v_0])

    views[f] = (view, d_rule[comp])
    print(views[f])


def viewer_2(fence):

    canvas = np.zeros((size, size), dtype='int8')
    canvas[start] = 1

    for f in fence:

        print("")
        print(f)

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
        print(view)
        # print(canvas[f])

        views[f] = (view, canvas[f])
        # print(views[f])

    return views


# ##lattice fence
#
# canvas = np.zeros((size, size), dtype='int8')
#
# print("")
# print("fence")
# fence = dict()
#
# for x in range(int(size/2)):
#     fence[x] = []
#
#     corner_0 = (start[0] - (x+1), start[0] - (x+1))
#     corner_1 = (start[0] + (x+1), start[0] + (x+1))
#
#     fence[x].append(corner_0)
#     fence[x].append(corner_1)
#
#
# print(fence)
#
#
# for x in range(len(fence)):
#     links = []
#
#     fence_x = fence[x]
#     for f in fence_x:
#
#         if x == 0:
#             canvas[f] = fence_x.index(f) + 1
#         else:
#             canvas[f] = fence_x.index(f) + 9
#
#     print(" ")
#     print('canvas')
#     print(canvas)
#
#     for x in range(2):
#         if x % 2 == 0:
#             pol = 1
#         else:
#             pol = -1
#
#         for y in range(len(fence_x) + 1):
#             # print("condition")
#             if y < int((len(fence_x) + 1) / 2) + 1:
#                 # print("bingo")
#                 link = (fence_x[x][0], fence_x[x][1] + ((y + 1) * pol))
#                 # print(link)
#             else:
#                 # print('bongo')
#                 # print("y")
#                 # print(y)
#                 sub = int((len(fence_x) + 1) / 2) + 1
#                 z = y - sub
#                 # print("z")
#                 # print(z)
#                 link = (fence_x[x][0] + ((z + 1) * pol), fence_x[x][1])
#                 # print(link)
#
#             links.append(link)
#
#     links = sorted(links, key=lambda x: abs(x[0] - x[1]))
#
#     print(' ')
#     print('links')
#     print(links)
#
#     for l in links:
#         print(l)
#         canvas[l] = links.index(l) + 3
#
#     print('canvas')
#     print(canvas)


# for x in range(1, 2 ** 16):
#     print(x)
#

journaling = 0
lvling = 1
path = 'scarfs'

if journaling != 0:

    print('journaling')

    # map(length, width, rule, base, start, direction, path, 0, 1)

    infile = open("2d-journals\journal_8", "rb")
    journal = pickle.load(infile)
    infile.close


    journal = dict(sorted(journal.items(), key=lambda x:len(x[1][0]), reverse=True))

    print(len(list(journal.keys())))

    for k in list(journal.keys()):
        print('')
        print(list(journal.keys()).index(k))
        print(k)
        jk = journal[k]
        print(len(jk[0]))
        map(size, k, path, 0, 1)


if lvling != 0:
    print('lvling')

    lvl = os.listdir('scarfs/lvl-2')

    for l in lvl:

        print(lvl.index(l))
        print(l)
        l = int(l[13:-4])
        print(l)

        map(size, l, path, 0, 1)













