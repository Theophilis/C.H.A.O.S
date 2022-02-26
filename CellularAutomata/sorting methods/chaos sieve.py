import math
import sys
import pickle

infile = open('cell_patterns', 'rb')
cell_patterns = pickle.load(infile)
infile.close

passage = cell_patterns[(4, 15)]

sys.setrecursionlimit(10**6)

duration = int(math.log(len(passage), 2))


#####to do#####

#add adjustable unit size
##unit: the number of parts required to be considered a whole

#arrange each order agnostic tulple in the cb_mag
##apply negatives to the index of cb_mag based on tuple value order

#how should tuples be sorted in magnitude?
##does it even matter?

#create sibling arrays whose values are the rule called at each step

#merge individual rules cib values into a master dict?

#####create a hybrid scoring system based on a weighted simlarity rating of a rules comp and cbi values for each level

#####are negative zeros causing issues with the results?


#####comp#####


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

        mag = sorted(mag, key=lambda x: x[1] - x[0])

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


# rewrite variables to increase legibility
# comitt each section, denoted by variable being written to, to their own function call
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
    # comp-index dictionary. with the x, y (width, rule) tuples as keys, store the cbi_diff tuples with thier comp values

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

                        # should the polarity of the comp value be kept past this point?

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

            print(" ")
            print("k")
            print(k)
            print(c_i[k])

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

c_i_s = chaos_mesh(cell_patterns)

print(" ")
print("c_i_s")
print(c_i_s)



filename = 'c_i_s'
outfile = open(filename, 'wb')
pickle.dump(c_i_s, outfile)
outfile.close()
