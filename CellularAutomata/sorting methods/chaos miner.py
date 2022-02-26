import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import math
import sys

sys.setrecursionlimit(10**6)

np.set_printoptions(linewidth=np.inf)

length = 16
#number of times given rule is applied and number of initial rows generated
width = length
#number of cells in a row
rule = 165
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

# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white


#cell gen


def base_x(n, b):
    e = n//b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, base = 2):

    rules = dict()

    if base == 2:

        int_rule = bin(rule).replace('0b', '')


    else:

        int_rule = base_x(rule, base)


    x = int_rule[::-1]

    while len(x) < base ** view:

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


def map(length, width, rule, base, start, direction, cell_patterns, path, plot = 0):


    file = str(width) + '-' + str(rule) + '-' + str(base) + '-' + "X" + str(length)
    path_name = os.path.join(path, file)

    rules = rule_gen(rule, base)
    int_rule = rules[1]
    rules = rules[0]

    # print(" ")
    # print("rules")
    # print(rules)

    cnvs = np.zeros((length, width), dtype='int8')

    cnvs[0, start] = 1

    # for x in range(width):
    #     cnvs[0, x] = x

    # print(" ")
    # print("cnvs")
    # print(cnvs)

    for x in range(length - 1):

        c_a = cnvs[x]

        # print(" ")
        # print("c_a")
        # print(c_a)
        # print(len(c_a))

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

            # print("rule")
            # print(rules[v_0])

            cnvs[x + 1, y] = rules[v_0]

    cnvs = np.flip(cnvs, 0)
    # cnvs = np.flip(cnvs, 1)

    # print("cnvs")
    # print(cnvs)


#export pcolormesh of cells

    if plot != 0:

        if base == 3:
            cMap = c.ListedColormap(['k', 'c', 'm'], 'tri', 3)

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
        plt.savefig(path_name, dpi=300)
        plt.close()


#generate dictionary of cell value patterns

    if rule == 1:
        v_pattern = []

        for z in range(length):
            w = ''
            for a in range(width):
                w += "0"

######## binary decimal switch ########
            w = int(w, 2)

            v_pattern.append(str(w))

        cell_patterns[(width, 0)] = v_pattern

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

    cell_patterns[(width, rule)] = v_pattern


    return int_rule


#chaos sieve


def cb_calc(s, t):

    s = int(s)
    t = int(t)

    if s == t:

        cb = (s, t)


    else:

        if s > t:

            cb = (t, s)

        else:

            cb = (s, t)

    return cb


def magnitude(passage):
    mag = []

    if len(passage) == 0:
        return mag

    elif type(passage[0]) == tuple:
        for p in passage:
            if p not in mag:
                mag.append(p)

        # how should tuples be sorted in magnitude?
        ##does it even matter?

        mag = sorted(mag, key=lambda x: x[1] + x[0])

    else:
        mag = []
        for p in passage:
            # p = int(p)
            if p not in mag:
                mag.append(p)
        mag = sorted(mag)

        # for m in mag_0:
        #     mag.append(str(m))

    # print(" ")
    # print("mag")
    # print(mag)

    return mag


def encode(passage):

    c_b = []
    cb_s = []


    for x in range(0, len(passage), 2):

        c_b.append((int(passage[x]), int(passage[x + 1])))
        cb = cb_calc(passage[x], passage[x + 1])

        cb_s.append(cb)

    # print(" ")
    # print("c_b")
    # print(c_b)
    # print(cb_s)

    # c_tuples = []
    # b_tuples = []
    #
    # for t in c_b:
    #     if t[0] > 0:
    #         c_tuples.append(t)
    #     else:
    #         t = (t[0], t[1])
    #         b_tuples.append(t)
    #
    # print("cb_t")
    # print(c_tuples)
    # print(b_tuples)
    #
    # c_mag = magnitude(c_tuples)
    # b_mag = magnitude(b_tuples)
    #
    # print("cb_mag")
    # print(c_mag)
    # print(b_mag)

    cb_mag = magnitude(cb_s)

    # print("cb_mag")
    # print(cb_mag)

    cb_index = []

    for tuple in c_b:

        if tuple[0] < tuple[1]:

            cb_index.append(str(cb_mag.index(tuple)))

        else:
            tuple = (tuple[1], tuple[0])

            cb_index.append(str(- cb_mag.index(tuple)))

    # print("cbi")
    # print(cb_index)

    # cbi_mag = magnitude(cb_index)
    #
    # print("cbi_mag")
    # print(cbi_mag)
    #
    # comp = []
    #
    # for cb in cb_index:
    #
    #     comp.append(cbi_mag.index(cb))
    #
    # print("comp")
    # print(comp)

    return cb_index, cb_mag


def encoder(passage, duration, d, full_encode):

    encode_1 = encode(passage)

    full_encode[duration - d] = encode_1

    d -= 1

    if d == 0:

        return encode_1, full_encode

    else:
        encoder(encode_1[0], duration, d, full_encode)

        return full_encode


def compress(passage, duration):

    mag_0 = magnitude(passage)

    # print("mag_0")
    # print(mag_0)

    p_0 = []

    for p in passage:
        p_0.append(str(mag_0.index(p)))

    full_encode = dict()

    encoder(p_0, duration, duration, full_encode)

    return full_encode


#rewrite variables to increase legibility
#comitt each section, denoted by variable being written to, to their own function call
def chaos_mesh(cell_patterns, length, width, run):


    compendium = dict()
    cp_k = list(cell_patterns.keys())

    for x in range(0, run):

        passage = cell_patterns[cp_k[x]]

        duration = int(math.log(len(passage), 2))

        full_encode = compress(passage, duration)

        cbi_mag = []
        comp = []

        for z in range(duration):

            code = full_encode[z]

            # print(" ")
            # print("code " + str(x) + " " + str(z))
            # print(code)

            cbi_mag.append(code[1])
            comp.append(code[0])

        composition = (comp, cbi_mag)

        compendium[(width, x)] = composition

        # print(" ")
        # print("composition")
        # print(composition)


    comp_mesh = dict()

    for x in range(duration):
        comp_mesh[x] = dict()

    for x in range(0, run):

        comp = compendium[(width, x)][0]
        cbi = compendium[(width, x)][1]

        for z in range(len(comp)):

            comp_z = tuple(comp[z])
            # print(" ")
            # print("comp_z")
            # print(comp_z)

            cbi_z = tuple(cbi[z])

            # print(cbi_z)

            if comp_z not in comp_mesh[z]:

                comp_mesh[z][comp_z] = [(width, x)]

            else:
                comp_mesh[z][comp_z].append((width, x))


    c_i = dict()
    #comp-index dictionary. with the x, y (width, rule) tuples as keys, store the cbi_diff tuples with thier comp values

    for x in range(duration):

        comp_mesh[x] = dict(sorted(comp_mesh[x].items(), key=lambda x: len(x[1]), reverse=True))

        # print(" ")
        # print("#_#_#_#_#_#_#_#_#_#")
        # print("mesh: " + str(x))
        # print(comp_mesh[x])
        # print("#_#_#_#_#_#_#_#_#_#")

        mesh = comp_mesh[x]
        mesh_k = list(mesh.keys())

        for k in mesh_k:

            # print(" ")
            # print("###k###")
            # print(k)
            # print(mesh[k])
            # print(len(mesh[k]))

            # if len(mesh[k]) < 10 and len(mesh[k]) != 1:
            # print(" ")
            # print("mk")
            for mk in mesh[k]:

                cbi_dif = compendium[mk][1][x]

                # print(" ")
                # print('cbi_c')
                # print(mk)
                # print(x)
                # print(cbi_dif)


                if mk not in c_i:

                    c_i[mk] = []

                else:

                    ci = []

                    for y in range(len(k)):

                        k_y = int(k[y])

                        # print(k[y])

#should the polarity of the comp value be kept past this point?

                        ci.append((k_y, cbi_dif[abs(k_y)]))

                    # print(" ")
                    # print("ci")
                    # print(ci)

                    c_i[mk].append(ci)


    c_i_k = sorted(list(c_i.keys()), key=lambda x: x[1])

    # print(" ")
    # print("c_i_k")
    # print(" ")


    lvl_scores = []

    for x in range(duration - 1):

        c_i_dex = dict()

        for k in c_i_k:

            # print(" ")
            # print("k")
            # print(k)
            # print(c_i[k])

            ci_k = c_i[k]

            for y in range(len(ci_k[x])):

                if ci_k[x][y] not in c_i_dex:

                    c_i_dex[ci_k[x][y]] = 1

                else:

                    c_i_dex[ci_k[x][y]] += 1

        c_i_dex = dict(sorted(c_i_dex.items(), key=lambda x: x[1], reverse=True))

        lvl_scores.append(c_i_dex)

    # print(" ")
    # print("lvl_scores")

    for x in range(len(lvl_scores)):

        # print(" ")
        # print(x)
        # print(lvl_scores[x])

        sum = 0

        for k in list(lvl_scores[x].keys()):
            sum += lvl_scores[x][k]

        # print(sum)

        for k in list(lvl_scores[x].keys()):
            lvl_scores[x][k] = round(lvl_scores[x][k] / sum * 100, 4)

        # print(lvl_scores[x])

    c_i_s = dict()
    # c_i_score

    for k in c_i_k:

        ci_k = c_i[k]

        # print("ci_k")
        # print(ci_k)

        final_score = 0

        for x in range(len(ci_k)):

            # print("ci_k[x]")
            # print(ci_k[x])
            score = 0

            for y in range(len(ci_k[x])):
                cik = ci_k[x][y]

                score += lvl_scores[x][cik]

            # final_score += score * 2 ** x

            # if x == 0 and x == 1:
            final_score += score

        c_i_s[k] = round(final_score, 4)

    c_i_s = dict(sorted(c_i_s.items(), key=lambda x: x[1], reverse=True))

    return c_i_s


path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/chaos sieve test output'

cell_patterns = dict()

for x in range(1, 256):

    print(x)

    m = map(length, width, x, base, start, direction, cell_patterns, path)

print(" ")

c_i_s = chaos_mesh(cell_patterns, length, width, 256)


cell_patterns = dict()
cis_k = list(c_i_s.keys())

for key in cis_k:

    print(key)
    print(cis_k.index(key))

    m = map(length, width, key[1], base, start, direction, cell_patterns, path, 1)

# c_i_s_2 = chaos_mesh(cell_patterns, length, width, len(cis_k[140:]))
#
#
# cell_patterns = dict()
# cis_k_2 = list(c_i_s_2.keys())
#
# for key in cis_k_2[46:]:
#
#     print(key)
#     print(cis_k_2.index(key))
#
#     m = map(length, width, key[1], base, start, direction, cell_patterns, path)
#
# c_i_s_3 = chaos_mesh(cell_patterns, length, width, len(cis_k_2[46:]))
#
#
# cell_patterns = dict()
# cis_k_3 = list(c_i_s_3.keys())
#
# for key in cis_k_3:
#
#     print(key)
#     print(cis_k_3.index(key))
#
#     m = map(length, width, key[1], base, start, direction, cell_patterns, path, 1)




