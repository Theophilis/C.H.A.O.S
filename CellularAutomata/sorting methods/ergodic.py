import math
import sys


passage = "SOCRATES: I dare say that you may be surprised to find, O son of Cleinias, that I, who am your first lover, not having spoken to you for many years, when the rest of the world were wearying you with their attentions, am the last of your lovers who still speaks to you. The cause of my silence has been that I was hindered by a power more than human, of which I will some day explain to you the nature; this impediment has now been removed; I therefore here present myself before you, and I greatly hope that no similar hindrance will again occur. Meanwhile, I have observed that your pride has been too much for the pride of your admirers; they were numerous and high-spirited, but they have all run away, overpowered by your superior force of character; not one of them remains. And I want you to understand the reason why you have been too much for them. You think that you have no need of them or of any other man, for you have great possessions and lack nothing, beginning with the body, and ending with the soul. In the first place, you say to yourself that you are the fairest and tallest of the citizens, and this every one who has eyes may see to be true; in the second place, that you are among the noblest of them, highly connected both on the father’s and the mother’s side, and sprung from one of the most distinguished families in your own state, which is the greatest in Hellas, and having many friends and kinsmen of the best sort, who can assist you when in need; and there is one potent relative, who is more to you than all the rest, Pericles the son of Xanthippus, whom your father left guardian of you, and of your brother, and who can do as he pleases not only in this city, but in all Hellas, and among many and mighty barbarous nations. Moreover, you are rich; but I must say that you value yourself least of all upon your possessions. And all these things have lifted you up; you have overcome your lovers, and they have acknowledged that you were too much for them. Have you not remarked their absence? And now I know that you wonder why I, unlike the rest of them, have not gone away, and what can be my motive in remaining"

sys.setrecursionlimit(10**6)

duration = int(math.log(len(passage), 2)) + 1


#####to do#####
##allow use of relative magnitude instead of frequency


#####comp#####


def cb_calc(s, t):

    if s == t:

        cb = (s, t)


    else:

        if s > t:

            cb = (-s, t)

        else:

            cb = (t, s)

    return cb


def passage_prep(passage, t = 0):

    if t == 0:

        passage = list(passage)

        passage = "".join(passage)

        passage = list(passage)

        ergod = []
        ergod = ergodic(passage, ergod, 0)

    else:

        ergod = []
        ergod = ergodic(passage, ergod, 0, 1)

    duration = int(math.log(len(passage), 2)) + 1

    if len(passage) < 2 ** duration:
        for x in range(2 ** duration - len(passage)):

            if t == 0:
                passage.append(ergod[0][0][0])
            else:
                passage.append(ergod[0])

    return passage


def ergodic(passage, omnidex = [], n=1, t=0):

    # t=0: list of strings, t=1 list of tuples

    ergod = dict()

    if len(passage) % (2 ** n) != 0:

        for x in range(len(passage) % (2 ** n) ):

            passage.append(omnidex[0][0][0])

    for x in range(0, len(passage), int(2 ** n)):

        if t == 0:

            bigram = "".join(passage[x:x + int(2 ** n)])

        else:
            bigram = passage[x:x + int(2 ** n)][0]

        if bigram not in ergod:

            ergod[bigram] = 1

        else:

            ergod[bigram] += 1

    if t == 0:
        ergod = sorted(ergod.items(), key=lambda x:x[1], reverse=True)

    else:

        ergod = dict(sorted(ergod.items(), key=lambda x:x[1], reverse=True))

        ergod = list(ergod.keys())

        # print("ergodic ergod")
        # print(ergod)

    return ergod


def ergodic_parse(passage, omnidex = []):
    omnidex = []

    duration = int(math.log(len(passage), 2)) + 1

    for x in range(duration):

        ergod_x = ergodic(passage, omnidex, x)

        o_apply = []

        for e in ergod_x:
            o_apply.append(e[0])

        omnidex.append(o_apply)

    return omnidex


def encode(passage, l_dex = [], o = 0):

    # print(" ")
    # print("l_dex")
    # print(l_dex)

    if o != 0:

        v_encode = []

        for p in passage:
            v_encode.append(int(l_dex[0].index(p) * 2) + 1)


    else:
        v_encode = passage

    c_b = []

    for x in range(0, len(v_encode), 2):
        pair = v_encode[x: x + 2]

        cb = cb_calc(pair[0], pair[1])

        c_b.append(cb)

    # print(" ")
    # print("v_encode")
    # print(v_encode)
    #
    # print("c_b")
    # print(c_b)

    c_tuples = []
    b_tuples = []

    for t in c_b:
        if t[0] > 0:
            c_tuples.append(t)
        else:
            t = (-t[0], t[1])
            b_tuples.append(t)

    # print("c_tuples")
    # print(c_tuples)
    # print("b_tuples")
    # print(b_tuples)

    # c_tuples = passage_prep(c_tuples, 1)
    # b_tuples = passage_prep(b_tuples, 1)
    #
    # print("prepped")
    # print(c_tuples)
    # print(len(c_tuples))
    # print(b_tuples)
    # print(len(b_tuples))

    c_ergod = ergodic(c_tuples, n=0, t=1)
    b_ergod = ergodic(b_tuples, n=0, t=1)

    # print("c_ergod")
    # print(c_ergod)
    # print("b_ergod")
    # print(b_ergod)

    cb_index = []

    for tuple in c_b:

        if tuple[0] > 0:

            cb_index.append(str(c_ergod.index(tuple)))

        else:
            tuple = ( - tuple[0], tuple[1])

            cb_index.append(str(- b_ergod.index(tuple)))


    # print(" ")
    # print("cb_index")
    # print(cb_index)


    ergod = ergodic(cb_index, 0, 0)

    v_dex = []

    for e in ergod:

        v_dex.append(e[0])


    # print(" ")
    # print("v_dex")
    # print(v_dex)
    # print(len(v_dex))

    comp = []

    for cb in cb_index:

        comp.append(v_dex.index(cb))

    # print(" ")
    # print("comp")
    # print(comp)
    # print(len(comp))

    return comp, v_dex, c_ergod, b_ergod


def encoder(passage, duration, d, l_dex, full_encode):

    # print(" ")
    # print("d")
    # print(d)

    if d == duration:

        encode_1 = encode(passage, l_dex, 1)

        # print("")
        # print("encode_1")
        # print(encode_1[0])
        # print(encode_1[1])

        full_encode[duration - d] = encode_1

        d -= 1

        encode_2 = encoder(encode_1, duration, d, l_dex, full_encode)

        return encode_2, full_encode

    else:

        v_encode = passage[0]

        encode_1 = encode(v_encode)

        # print(" ")
        # print("encode_2")
        # print(encode_1[0])
        # print(encode_1[1])

        full_encode[duration - d] = encode_1

        d -= 1

        if d == 0:

            return encode_1, full_encode

        else:
            encode_2 = encoder(encode_1, duration, d, l_dex, full_encode)

            return encode_2, full_encode


def compress(passage, duration):

    passage = passage_prep(passage)

    l_dex = ergodic_parse(passage)


    # print(" ")
    # print("l_dex")
    # for x in range(len(l_dex)):
    #     print(l_dex[x])

    # c_dex = c_gen(l_dex)

    # print(" ")
    # print("c_dex")
    # for x in range(len(c_dex)):
    #     print(c_dex[x])

    full_encode = dict()

    full_encode = encoder(passage, duration, duration, l_dex, full_encode)

    # omnidex = omni_gen(l_dex, c_dex)

    return full_encode[1], l_dex


#####decomp/analysis#####


def abs_diff(v_l):
    d_l = []

    for x in range(len(v_l) - 1):
        v_1 = abs(int(v_l[x]))
        v_2 = abs(int(v_l[x + 1]))

        d_l.append(abs(v_2 - v_1))

    return d_l


def frame(c_dex, n, frame_1 = []):


    dex = c_dex[n]

    f_1 = []

    if n == 0:

        return frame_1


    if len(frame_1) == 0:

        for d in dex:

            if d[0] > 0:

                s = d[1]
                t = d[2]

            else:

                s = d[2]
                t = d[1]

            f_1.append(s)
            f_1.append(t)

        n -= 1

        f_2 = frame(c_dex, n, f_1)

        return f_2


    else:
        for f in frame_1:

            f = int(f / 2 + 0.5) - 1

            d = dex[f]

            if d[0] > 0:

                s = d[1]
                t = d[2]

            else:

                s = d[2]
                t = d[1]

            f_1.append(s)
            f_1.append(t)

        n -= 1

        f_2 = frame(c_dex, n, f_1)

        return f_2


def author(omnidex):

    l_dex = omnidex[0]
    c_dex = omnidex[1:]

    n = len(c_dex) - 1

    frame_1 = frame(c_dex, n)

    draft = []

    for f in frame_1:

        f = int(f / 2 + 0.5) - 1

        draft.append(l_dex[f])

    draft = "".join(draft)



    return draft, frame_1



full_encode = compress(passage, duration)

l_dex = full_encode[1]
full_encode = full_encode[0]

omnidex = []
comp = []

for x in range(duration):

    code = full_encode[x]

    omnidex.append(code[1])
    comp.append(code[0])



cb_full = []

for x in range(duration):

    code = full_encode[x]

    if len(code[2]) != 0:

        for c in code[2]:
            cb_full.append(c)

    for c in code[3]:
        cb_full.append(c)

cb_full = passage_prep(cb_full, 1)

cb_ergod = ergodic(cb_full, n=0, t=1)

c_dex = []
b_dex = []
for x in range(duration):

    code = full_encode[x]

    c_index = []
    b_index = []

    if len(code[2]) != 0:

        for c in code[2]:
            c_index.append(cb_ergod.index(c))

    for c in code[3]:
        b_index.append(cb_ergod.index(c))

    c_dex.append(c_index)
    b_dex.append(b_index)


print("final structure")

print(" ")
print("l_dex")
print(l_dex[0])

print(" ")
print("cb_ergod")
print(cb_ergod)


print(" ")
print("comp")
for x in range(duration):
    print(comp[x])


print(" ")
print("omnidex")
for x in range(duration):
    print(omnidex[x])


print(" ")
print("c_dex")
for x in range(duration):
    print(c_dex[x])


print(" ")
print("b_dex")
for x in range(duration):
    print(b_dex[x])