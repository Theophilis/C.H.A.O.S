import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import pandas as pd
import pickle

infile = open('c_i_s', 'rb')
c_i_s = pickle.load(infile)
infile.close

#kath ssid:4247 by:1981

np.set_printoptions(linewidth=np.inf)

length = 128
#number of times given rule is applied and number of initial rows generated
width = 128
#number of cells in a row
rule = 137
#number who's x_base transformation gives the rules dictionary its values
view = 3
#size of the view window that scans a row for rule application
base = 2
#numerical base of the rule set. number of colors each cell can be
start = -1
#position for a row 0 cell value 1
direction = 1
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


def rule_gen(rule, base = 2, width = 0):

    rules = dict()

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


def viewer(c_a, y, view, v_0):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(c_a) - 1:

            v_0.append('0')

        else:

            v_0.append(str(c_a[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < 0:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(c_a[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(c_a, y, view, v_0)

        return v_0


def map(length, width, rule, base, start, direction, path, rc = 0, plot=0):

    start_0 = start
    file = str(width) + '-' + str(rule) + '-' + str(base) + '-' + "X" + str(length)
    path_name = os.path.join(path, file)

    cell_patterns = dict()
    rule_patterns = dict()

    # print("rules")

    rules = rule_gen(rule, base)
    int_rule = rules[1]
    rules = rules[0]

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

    cnvs[0] = start[1]
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

            v_0 = tuple(viewer(c_a, y, view, v_0))

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
            if base == 3:
                cMap = c.ListedColormap(['k', 'c', 'm'], 'tri', 3)

            if base == 2:
                cMap = c.ListedColormap(['w', 'k'])

            plt.pcolormesh(cnvs, cmap=cMap)

            plt.xticks(np.arange(0, width, step=1))
            plt.yticks(np.arange(0, length, step=1))

            plt.figtext(.3, .925, int_rule, fontsize=14)
            plt.figtext(.0075, .05, rules, fontsize=7)
            plt.grid(visible=True, axis='both', )

            # c_plt.show()
            plt.savefig(path_name, dpi=300)
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

    if rc == 0 or rc == 2:

        v_pattern = []

        for x in reversed(range(length)):

            v = list(cnvs[x])

            w = ''

            for n in v:
                w += str(n)

            w = int(w, 2)

            # print("w")
            # print(w)
            # print(type(w))

            v_pattern.append(str(w))

        cell_patterns = v_pattern


    if rc == 1 or rc == 2:
        # if rule == 1:
        #     v_pattern = []
        #
        #     for z in range(length):
        #         w = ''
        #         for a in range(width):
        #             w += "0"
        #
        #         w = int(w, 2)
        #
        #         v_pattern.append(str(w))
        #
        #     cell_patterns[(width, 0)] = v_pattern

        v_pattern = []

        for x in range(length - 1):

            v = list(rule_call[x])

            # print("v")
            # print(v)

            w = ''

            for n in v:
                w += str(n)

            # w = int(w, 2)

            # print("w")
            # print(w)
            # print(type(w))

            v_pattern.append(str(w))

        rule_patterns = v_pattern


    return cell_patterns, rule_patterns, rule_call, rc_val, rc_net


path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/rc_net'

rc_net_map = dict()
rcv_dex = dict()
val_dex = dict()

length = 8
width = 8

for x in range(0, 256):

    print(" ")
    print("x")
    print(x)

    rc_net_map[x] = []

    r_map = map(length, width, x, base, start, direction, path, rc=2, plot=0)

    cell_patterns = r_map[0]
    rule_patterns = r_map[1]
    rule_call = r_map[2]
    rc_val = r_map[3]
    rc_net = r_map[4]

    # rcv_dex[x] = rc_val

    # print(cell_patterns)
    # print(rule_patterns)
    # print(rule_call)
    # print(rc_val)
    # print(rc_net)

    val_dex[x] = abs(len(rc_val['0']) - len(rc_val['1']))

val_dex = dict(sorted(val_dex.items(), key=lambda x:x[1], reverse=True))

print(val_dex)

length = 128
width = 128

for key in list(val_dex.keys()):


    print(" ")
    print(list(val_dex.keys()).index(key))
    print(key)

    m = map(length, width, key, base, start, direction, path, rc=1, plot=1)


    # print(" ")
    # print("rule_call")
    # print(rule_call)

    # rc_net_map[x].append(rule_call)


# for x in range(1, 255):
#     print(" ")
#     print(x)
#     print(rcv_dex[x])

#####Net_Val#####

def net_val(rc_net_map):

    rc_net_val = dict()

    for x in range(1, 255):

        # print(" ")
        # print("rc_net-" + str(x))

        score = 0

        for y in range(1):

            # print(" ")
            # print("rcn")
            # print(rc_net[x][y])

            rcnm = rc_net_map[x][y]

            for a in range(len(rcnm)):

                # print(' ')
                # print("a")
                # print(a)

                m = []

                for b in range(a, len(rcnm)):

                    # print("b")
                    # print(b)
                    #
                    # print("rcn")
                    # print(rcn[a])
                    # print(rcn[b])

                    if rcnm[a].all() == rcnm[b].all():

                        m.append(b)

                if len(m) > 1:

                    m = sorted(m)

                    index = list(np.where((rcnm == rcnm[m[1]]).all(axis=1)))[0]

                    # print(" ")
                    # print("index")
                    # print(index)

                    # for z in range(1, len(index)):
                    #     score += index[z]
                    score += index[0]

                else:

                    score += length

        rc_net_val[x] = score


    rc_net_val = dict(sorted(rc_net_val.items(), key=lambda x:x[1], reverse=True))

    print(" ")
    print("rc_net_val")
    print(rc_net_val)

    rcnv_k = list(rc_net_val.keys())

    return rcnv_k, rc_net_val