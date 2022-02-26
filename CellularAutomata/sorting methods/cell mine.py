import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import math
import sys

sys.setrecursionlimit(10**6)

np.set_printoptions(linewidth=np.inf)

length = 256
#number of times given rule is applied and number of initial rows generated
width = 256
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
    file = str(width) + '-' + str(rule) + '-' + str(base) + '-' + "X" + str(length)
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


def in_freq(passage):

    freq = dict()

    for p in passage:

        if p not in freq:

            freq[p] = 1

        else:
            freq[p] += 1

    freq = dict(sorted(freq.items(), key=lambda x:x[1], reverse=True))

    return list(freq.keys())


def encode(passage):

    c_b = []
    cb_s = []

    # print(" ")
    # print("passage")
    # print(passage)
    # print(len(passage))

    for x in range(0, len(passage), 2):

        # print(x)

        c_b.append((int(passage[x]), int(passage[x + 1])))
        cb = cb_calc(passage[x], passage[x + 1])

        cb_s.append(cb)

    # print(" ")
    # print("c_b")
    # print(c_b)
    # print(cb_s)

    cb_mag = magnitude(cb_s)
    cb_freq = in_freq(cb_s)

    # print("cb_mag")
    # print(cb_mag)

    cb_index = []

    for tuple in c_b:

        if tuple[0] < tuple[1]:

            cb_index.append(cb_freq.index(tuple))

        else:
            tuple = (tuple[1], tuple[0])

            cb_index.append(- cb_freq.index(tuple))

    # print("cbi")
    # print(cb_index)

    return cb_index, cb_mag, cb_freq


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

    # print(" ")
    # print("duration")
    # print(duration)
    #
    # print(passage)
    mag_0 = magnitude(passage)

    # print("mag_0")
    # print(mag_0)

    freq = in_freq(passage)

    # print("freq")
    # print(freq)

    p_0 = []

    for p in passage:
        p_0.append(freq.index(p))

    full_encode = dict()

    # print("p_0")
    # print(p_0)

    encoder(p_0, duration, duration, full_encode)

    return full_encode


#mesh


def binder(cell_patterns, layer, run):

        compendium = dict()

        if layer == 0:

            cp_k = list(cell_patterns.keys())

        for x in range(run):

            if x not in list(cell_patterns.keys()):
                continue

            # print(" ")
            # print(x)

            if layer ==0:

                passage = cell_patterns[cp_k[x]]

            else:

                passage = cell_patterns[x][layer - 1]

            # print("p")
            # print(passage)

            duration = int(math.log(len(passage), 2))

            full_encode = compress(passage, duration)

            # print("fe")
            # print(full_encode)

            cbi_mag = []
            comp = []

            for z in range(duration):

                code = full_encode[z]

                # print(" ")
                # print("code " + str(cp_k[x]) + " " + str(z))
                # print(code)

                cbi_mag.append(code[1])
                comp.append(code[0])

                # print(" ")
                # print(cbi_mag)
                # print(comp)

            composition = (comp, cbi_mag)

            compendium[x] = composition

            # print(" ")
            # print("composition")
            # print(composition)

        return compendium, duration


#make comp_mesh keys polarity, direction, and length agnostic
#find the absolute occurance of tuples. use ao as dex for new vapor analysis.
def mesh(cell_patterns, compendium, duration, run):

    comp_mesh = dict()
    ao = dict()
    #absolute occurance

    for x in range(duration):
        comp_mesh[x] = dict()

    for x in range(0, run):

        if x not in list(cell_patterns.keys()):
            continue

        comp = compendium[x][0]
        cbi = compendium[x][1]

        for z in range(len(comp)):

            comp_z = tuple(comp[z])
            # print(" ")
            # print("comp_z")
            # print(comp_z)

            cbi_z = tuple(cbi[z])

            # print(" ")
            # print("cbi_z")
            # print(cbi_z)

            for t in cbi_z:
                if t not in ao:
                    ao[t] = 1
                else:
                    ao[t] += 1

            if comp_z not in comp_mesh[z]:

                comp_mesh[z][comp_z] = [x]

            else:
                comp_mesh[z][comp_z].append(x)

    # print('comp_mesh[x]')
    for x in range(duration):

        # print(x)
        # print(comp_mesh[x])

        comp_mesh[x] = dict(sorted(comp_mesh[x].items(), key=lambda x:len(x[1]), reverse=True))

        # print(comp_mesh[x])

    ao = dict(sorted(ao.items(), key=lambda x:x[1], reverse=True))

    return comp_mesh, ao


def index(compendium, comp_mesh, duration):

    c_i = dict()
    #comp-index dictionary. with the x, y (width, rule) tuples as keys, store the cbi_diff tuples with thier comp values

    for x in range(duration):

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

    # print(" ")
    # print("ci")
    # print(c_i)

    # print(" ")
    # print("c_i_k")
    # print(" ")

    return c_i


def lvl_score(c_i, c_i_k, duration):
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

    return lvl_scores


def index_score(lvl_scores, c_i, c_i_k):

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


#rewrite variables to increase legibility
def chaos_mesh(cell_patterns, run, layer):

    bound = binder(cell_patterns, layer, run)

    compendium = bound[0]
    duration = bound[1]

    comp_mesh = mesh(cell_patterns, compendium, duration, run)
    ao = comp_mesh[1]
    comp_mesh = comp_mesh[0]

    # print(" ")
    # print("comp_mesh")
    # for k in list(comp_mesh.keys()):
    #     print(" ")
    #     print(k)
    #     cmk = comp_mesh[k]
    #     print("cmk")
    #     print(cmk)
    #     for e in list(cmk.keys()):
    #         print(e)
    #
    # print(" ")
    # print("ao")
    # print(ao)
    # print(len(ao))

    c_i = index(compendium, comp_mesh, duration)
    c_i_k = sorted(list(c_i.keys()))

    lvl_scores = lvl_score(c_i, c_i_k, duration)

    c_i_s = index_score(lvl_scores, c_i, c_i_k)

    return c_i_s, compendium


structure = dict()

path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/axioms/1'

axioms = axiom_gen(view)

two_1 = axioms[0]
two_0 = axioms[1]

cell_patterns = dict()
rule_patterns = dict()

for x in range(256):
    print(x)
    m = map(length, width, x, base, start, direction, path, 2)

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
    cell_patterns[x] = m[0]
    rule_patterns[x] = m[1]



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


path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/vapor'

print("map")
for k in list(scores.keys()):

    print(" ")
    print(list(scores.keys()).index(k))
    print(k)

    m = map(length, width, k, base, start, direction, path, 1, 1)





# print(" ")
# print("ao")
# print(ao)



# cpks = list(dict(sorted(cell_patterns.items(), key=lambda x:x[-1][0], reverse=True)).keys())
#
# # print(cpks)
#
# path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/ao'
# print(" ")
# print(path)
# for k in cpks:
#
#     print(' ')
#     print(cpks.index(k))
#     print(k)
#
#     m = map(length, width, k, base, start, direction, path, 1)




# cell_mesh = chaos_mesh(structure, 256, 1)
#
# produce = 0
#
# if produce == 1:
#     rule_mesh = chaos_mesh(structure, 256, 2)
#
#     print(" ")
#     print('cell_mesh')
#     print(cell_mesh[0])
#     print(cell_mesh[1])
#
#     print(' ')
#     print("rule_mesh")
#     print(rule_mesh[0])
#     print(rule_mesh[1])
#
#     composit = dict()
#
#     for k in list(cell_mesh[0].keys()):
#         composit[k] = cell_mesh[0][k] + rule_mesh[0][k]
#
#     composit = dict(sorted(composit.items(), key=lambda x:x[1], reverse=True))
#
#     print(composit)
#
#     path = '/Users/edwardmaclean/PycharmProjects/CellularAutomata/axioms/composit'
#
#     for k in list(composit.keys()):
#
#         print(" ")
#         print(list(composit.keys()).index(k))
#         print(k)
#
#         m = map(length, width, k, base, start, direction, path, 1, 1)



# #####structure gen#####
#
# rc_net_map = dict()
# rcv_dex = dict()
#
# structure = dict()
#
# for x in range(256):
#
#     print(" ")
#     print("x")
#     print(x)
#
#     rc_net_map[x] = []
#
#     r_map = map(length, width, x, base, start, direction, path, rc=2, plot=0)
#
#     cell_patt = r_map[0]
#     rule_patt = r_map[1]
#     rule_call = r_map[2]
#     rc_val = r_map[3]
#     rc_net = r_map[4]
#
#     # rcv_dex[x] = rc_val
#
#     # print(cell_patt)
#     # print(rule_patt)
#     # print(rule_call)
#     # print(rc_val)
#     # print(rc_net)
#
#     rc_net_map[x].append(rule_call)
#
#     structure[x] = (cell_patt, rule_patt, rule_call, rc_val, rc_net)
#


# for x in range(256):
#
#     print(" ")
#     s_x = structure[x]
#     print("x")
#
#     for y in range(len(s_x)):
#         print(s_x[y])
#         print(len(s_x[y]))


# #####composit mesh#####
#
# value_mesh = chaos_mesh(structure, length, width, 256, 1)
#
# # print(" ")
# # print("value_mesh")
# # print(value_mesh[0])
# # print(value_mesh[1])
#
#
# rc_mesh = chaos_mesh(structure, length, width, 256, 2)
#
# # print(" ")
# # print("rc_mesh")
# # print(rc_mesh[0])
# # print(rc_mesh[1])
#
#
# composit = dict()
#
# for x in range(256):
#
#     composit[x] = 0
#     composit[x] += value_mesh[0][x]
#     composit[x] += rc_mesh[0][x]
#
# composit = dict(sorted(composit.items(), key=lambda x:x[1], reverse=True))
#
# # print(" ")
# # print("composit")
# # print(composit)
#
# # length = 256
# # width = 256
#
# for k in list(composit.keys()):
#     print(" ")
#     print("k")
#     print(k)
#     print(list(composit.keys()).index(k))
#
#     k_m = map(length, width, k, base, start, direction, path, rc=1, plot=1)
#
#

