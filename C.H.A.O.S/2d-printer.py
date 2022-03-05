import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import pickle

np.set_printoptions(linewidth=np.inf)
plt.ioff()

rule = 6049069618215839565782842634507394848996362563177470174153113185201852971153494239366465579843681897245316220263433329934471947410885434974601214619829353
base = 4
size = 20001
view = 4
start = (int(size/2), int(size/2))
zero = (0, 0)

infile = open('2d-fences/full-fence_spiral_' + str(size), 'rb')
full_fence = pickle.load(infile)
infile.close()

infile = open('2d-fences/full-fence_spiral_9', 'rb')
origin = pickle.load(infile)
infile.close()

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


def map(size, rule, path, full_fence, canvas = 0, steps = 0, plot=0):

    if type(rule) != int:
        r_n = decimal(rule, base)

    else:
        r_n = rule

    file = str(size) + '-' + str(base) + '-' + str(steps) + '-' + str(r_n)
    path_name = os.path.join(path, file)
    print(path_name)

    check = 0

    if type(canvas) == int:
        canvas = np.zeros((size, size), dtype='int8')

        canvas[start] = 1

        if check != 0:
            for x in range(0, len(full_fence), 2):
                canvas[full_fence[x]] = 1

    d_rule, i_rule = rule_gen_2(rule, base)

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
        plt.savefig(path_name, dpi=1800)
        plt.close()


    if steps == 0:

        return canvas

    else:

        steps -= 1
        map(size, rule, path, full_fence, canvas, steps, plot)



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
lvling = 0
path = 'scarfs/quaternary'

if journaling != 0:

    print('journaling')

    # map(length, width, rule, base, start, direction, path, 0, 1)

    infile = open("2d-journals\journal_22", "rb")
    journal = pickle.load(infile)
    infile.close()


    journal = dict(sorted(journal.items(), key=lambda x:len(x[1][0]), reverse=True))

    print(len(list(journal.keys())))

    for k in list(journal.keys()):
        print('')
        print(list(journal.keys()).index(k))
        print(k)
        jk = journal[k]
        print(len(jk[0]))
        map(size, k, path, full_fence, 0, 0, 1)


if lvling != 0:
    print('lvling')

    lvl = os.listdir('scarfs/quaternary/lvl-1')

    for l in lvl:

        os.mkdir('scarfs/quaternary/' + str(l))
        path = 'scarfs/quaternary/' + str(l)

        print(" ")
        print(lvl.index(l))
        print(l)
        l = int(l[14:-4])
        print(l)

        map(size, l, path, full_fence, 0, 10, 1)

map(size, rule, path, full_fence, 0, 0, 1)









