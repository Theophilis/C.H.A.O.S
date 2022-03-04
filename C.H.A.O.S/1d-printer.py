import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import pandas as pd
import pickle


np.set_printoptions(linewidth=np.inf)
plt.ioff()


length = 100
#number of times given rule is applied and number of initial rows generated
width = 101
#number of cells in a row
rule = '0033200310331332120011303330002233013233212323030123103103222313'
#number who's x_base transformation gives the rules dictionary its values
view = 5
#size of the view window that scans a row for rule application
base = 4
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

    value = 0

    for c in n:

        value += int(c) * n.index(c) ** b

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


def map(length, width, rule, base, start, direction, path, rc = 0, plot=0, edge='0'):

    r_n = decimal(rule, base)

    start_0 = start
    file = str(width) + 'x' + str(length) + '-' + str(base) + '-' + 'colors' + '-' + str(r_n)
    path_name = os.path.join(path, file)

    cell_patterns = dict()
    rule_patterns = dict()

    # print("rules")

    rules = rule_gen(rule, base, string=1)
    int_rule = rules[1]
    rules = rules[0]

    print(int_rule)
    print(rules)

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


    cnvs = np.zeros((length, width), dtype='int8')
    rule_call = np.zeros((length, width), dtype='int8')

    cnvs[0, start_0] = 1
    rule_call[0] = start[1]

    # for x in range(width):
    #     cnvs[0, x] = x

    # print(" ")
    # print("cnvs")
    # print(cnvs)
    # print(' ')
    # print("rule_call")
    # print(rule_call)

    for x in range(length - 1):

        c_a = cnvs[x]

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

            cnvs[x + 1, y] = rules[v_0]
            rule_call[x + 1, y] = list(rules.keys()).index(v_0)

    # print(" ")
    # print("cnvs")
    # print(cnvs)
    # print(" ")
    # print("rule_call")
    # print(rule_call)

    cnvs = np.flip(cnvs, 0)
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

            if base == 4:
                cMap = c.ListedColormap(['k', (0, .5, 1), (0, 1, .5), (1, 0, .5)], 'quad', 4)

            if base == 3:
                cMap = c.ListedColormap(['k', 'm', 'c'], 'tri', 3)

            if base == 2:
                cMap = c.ListedColormap(['w', 'k'])

            plt.pcolormesh(cnvs, cmap=cMap)

            # plt.xticks(np.arange(0, width, step=1))
            # plt.yticks(np.arange(0, length, step=1))
            #
            # plt.figtext(.3, .925, int_rule, fontsize=14)
            # plt.figtext(.0075, .05, rules, fontsize=7)
            # plt.grid(visible=True, axis='both', )

            # c_plt.show()
            plt.savefig(path_name, dpi=2000)
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


path = 'scarfs'

# map(length, width, rule, base, start, direction, path, 0, 1)

infile = open("journals\journal_6", "rb")
journal = pickle.load(infile)
infile.close


journal = dict(sorted(journal.items(), key=lambda x:len(x[1][0]), reverse=True))

print(len(list(journal.keys())))

for k in list(journal.keys())[660:1000]:
    print('')
    print(list(journal.keys()).index(k))
    print(k[0])
    jk = journal[k]
    print(len(jk[0]))
    map(length, width, k[0], base, start, direction, path, 0, 1)
