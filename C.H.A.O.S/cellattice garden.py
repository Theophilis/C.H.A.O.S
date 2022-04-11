import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import math
import sys

sys.setrecursionlimit(10**6)

np.set_printoptions(linewidth=np.inf)

length = 8
#number of times given rule is applied and number of initial rows generated
width = 8
#number of cells in a row
rule = 90
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
##order nth layer in value order not frequency

#find how to determine the length of the longest possible pattern from starting variables
##would true value pattern length correlate to center construction complexity?

#####remove the hard code for the 0 width cnvs#####

#add adjustable unit size for chaos mesh
##unit: the number of parts required to be considered a whole

#arrange each order agnostic tulple in the cb_mag
##apply negatives to the index of cb_mag based on tuple value order

#how should tuples be sorted in magnitude?
##does it even matter?

#create sibling arrays whose values are the rule called at each step

#merge individual rules cib values into a master dict?

#####create a hybrid scoring system based on a weighted simlarity rating of a rules comp and cbi values for each level

#####are negative zeros causing issues with the results?

#check that the chaos mesh scoring polarities match

#remove hard code for dictionary length in net_val and chaos_mesh

# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white


#qof


def sort_d(d):

    d = dict(sorted(d.items(), key=lambda x:x[1], reverse=True))

    return d


#cell gen


def axiom_gen(view):
    two_1 = []
    two_0 = []

    for x in range(1, 2 ** view):

        origin = (2 ** x) + 1

        # print(" ")
        # print("origin")
        # print(origin)

        two_1.append(origin)

        for y in range(x - 1):

            if y == 0:
                origin += 1

            else:
                origin += 2 ** y

            two_1.append(origin)

    for t in two_1:
        two_0.append(255 - t)

    return two_1, two_0


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

    # print(" ")
    # print("rc_net_val")
    # print(rc_net_val)

    rcnv_k = list(rc_net_val.keys())

    return rcnv_k, rc_net_val


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


def map(length, width, rule, base, start, direction, path, rc=0, plot=0):

    start_0 = start
    file = str(width) + "X" + str(length) + '-' + str(rule) + '-' + str(base) + '-' + str(start)
    path_name = os.path.join(path, file)
    length += 1

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

            v_pattern.append(w)

        cell_patterns = v_pattern[:len(v_pattern) - 1]


    if rc == 1 or rc == 2:

        v_pattern = []

        for x in range(length):

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

            v_pattern.append(int(w))

        rule_patterns = v_pattern[1:]


    return cell_patterns, rule_patterns, rule_call, rc_val, rc_net



structure = dict()

path = 'lattice-garden'

axioms = axiom_gen(view)

two_1 = axioms[0]
two_0 = axioms[1]

cell_patterns = dict()
rule_patterns = dict()

cell_patterns[rule] = []
rule_patterns[rule] = []

for x in range(1):

    print(x)

    m = map(length, width, rule, base, start, direction, path, 0, 0)

    # print(m[0])
    # print(m[1])

    # cellec = []
    # for c in m[0]:
    #     cellec.append(c)
    # for c in reversed(m[0]):
    #     cellec.append(c)
    #
    # rulelur = []
    # for r in m[1]:
    #     rulelur.append(r)
    # for r in reversed(m[1]):
    #     rulelur.append(r)

    # print("ms")

    cell_patterns[rule] = m[0]
    rule_patterns[rule] = m[1]

    # cell_patterns[rule].append(m[0])
    # rule_patterns[rule].append(m[1])

print("cell patterns")

for cell in cell_patterns:

    print(" ")
    print(cell)
    cp_c = cell_patterns[cell]

    for c in cp_c:

        print(c)
# print("two_1")
# for t in two_1:
#
#     print(" ")
#     print(two_1.index(t))
#     print(t)
#
#     m = map(length, width, t, base, start, direction, path, 2)
#
#     cell_patterns[t] = m[0]
#
#     structure[t] = (m[0], m[1], m[2], m[3], m[4])
#
#
# path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/axioms/0'
#
# print(" ")
# print("two_0")
# for t in two_0:
#
#     print(" ")
#     print(two_0.index(t))
#     print(t)
#
#     m = map(length, width, t, base, start, direction, path, 2)
#
#     cell_patterns[t] = m[0]
#
#     structure[t] = (m[0], m[1], m[2], m[3], m[4])


#####absolute occurance#####


def pairing(cells, co):
    for k in list(cells.keys()):
        ck = cells[k]
        lvl = []
        for x in range(0, len(ck), 2):
            pair = (ck[x], ck[x + 1])
            lvl.append(pair)
        co[k] = lvl

    return co


def substitute(pairs, new_cells, ap):
    for k in list(pairs.keys()):
        new_line = []
        pk = pairs[k]
        # print(pk)

        for p in pk:
            new_line.append(round(list(ap.keys()).index(p)/len(ap), 4))
        # print(new_line)
        new_cells[k] = new_line
    return new_cells


def occur(cells, pairs, co):
    pairs = pairing(cells, pairs)
    for k in list(pairs.keys()):
        pk = pairs[k]
        for p in pk:
            if p not in co:
                co[p] = 1
            else:
                co[p] += 1

    co = dict(sorted(co.items(), key=lambda x:int(x[1]), reverse=True))

    return co, pairs


def absolution(co, ao, ap):
    for k in list(co.keys()):
        if k not in ao:
            ao[k] = []
            ao[k].append(list(co.keys()).index(k))
        else:
            ao[k].append(list(co.keys()).index(k))

    for k in list(ao.keys()):
        s = 0
        aok = ao[k]
        for v in aok:
            s += v
        s = round(s/len(aok), 4)
        ap[k] = s

    ao = dict(sorted(ao.items(), key=lambda x: len(x[1]), reverse=True))
    ap = dict(sorted(ap.items(), key=lambda x:x[1]))

    return ao, ap


def absolute_position(ao, ap, co, cells, d, duration, cell_patterns_2):

    new_cells = dict()
    print(" ")
    print("duration")
    print(d)

    pairs = dict()

    if d != 0:

        co, pairs = occur(cells, pairs, co)
        ao, ap = absolution(co, ao, ap)
        new_cells = substitute(pairs, new_cells, ap)

        cell_patterns_2[d].append(new_cells)

        d -= 1

        # print(" ")
        # print(d)
        # print("co")
        # print(co)
        # print('ao')
        # print(ao)
        # print("ap")
        # print(ap)

        ap, co, ao, new_cells = absolute_position(ao, ap, co, new_cells, d, duration, cell_patterns_2)

        return ap, co, ao, new_cells

    else:

        # print(" ")
        # print(d)
        # print("co")
        # print(co)
        # print('ao')
        # print(ao)
        # print("ap")
        # print(ap)

        return ap, co, ao, new_cells


#absolute occurance
ao = dict()
#absolute position
ap = dict()
#current occurance
co = dict()
pairs = dict()
duration = int(math.log(length, 2))
cell_patterns_2 = dict()
rule_patterns_2 = dict()

for d in range(duration + 1):
    cell_patterns_2[d] = []
    rule_patterns_2[d] = []

ap, co, ao, new_cells = absolute_position(ao, ap, co, cell_patterns, duration, duration, cell_patterns_2)
ap, co, ao, new_cells = absolute_position(ao, ap, co, rule_patterns, duration, duration, rule_patterns_2)

#
# print("")
# print("ap")
# print(ap)
# print("co")
# print(co)
# print("ao")
# print(ao)


print(" ")
print("patterns_2")
vapor = dict()
for d in range(duration + 1):
    cp2d = cell_patterns_2[d]
    rp2d = rule_patterns_2[d]

    # print(" ")
    # print(d)
    # print(cp2d)
    # print(rp2d)

    for c in cp2d:
        for k in list(c.keys()):
            # print(c[k])
            if k not in vapor:
                vapor[k] = []
                vapor[k].append(c[k])
            else:
                vapor[k].append(c[k])

    for r in rp2d:
        for k in list(r.keys()):
            if k not in vapor:
                vapor[k] = []
                vapor[k].append(r[k])
            else:
                vapor[k].append(r[k])


scores = dict()
for k in list(vapor.keys()):
    # print(" ")
    # print(k)
    # print(vapor[k])
    vk = vapor[k]
    score = 0
    for v in vk:
        for s in v:
            score += s
    scores[k] = score

scores = dict(sorted(scores.items(), key=lambda x:x[1], reverse=True))
# print(scores)


path = 'lattice-garden'

print("map")
for k in list(scores.keys()):

    print(" ")
    print(list(scores.keys()).index(k))
    print(k)

    m = map(length, width, k, base, start, direction, path, 1, 0)

















