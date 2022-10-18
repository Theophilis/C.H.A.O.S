import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors as c
import pandas as pd
import pickle


np.set_printoptions(linewidth=np.inf)
plt.ioff()


length = 501
#number of times given rule is applied and number of initial rows generated
width = length
#number of cells in a row
rule = 21621
#number who's x_base transformation gives the rules dictionary its values
view = 3
#size of the view window that scans a row for rule application
base = 3
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

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

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


def viewer(row, y, view, v_0):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(row) - 1:

            v_0.append('0')

        else:

            v_0.append(str(row[y + int(len(v_0) / 2) + 1]))

    else:

        if y - len(v_0) < 0:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(row[int(y - len(v_0) / 2)]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer(row, y, view, v_0)

        return v_0


def Color_cells(d_rule, cell_row_width, row_0):

    rc = []
    row_1 = [0 for x in range(cell_row_width)]

    for y in range(len(row_0)):

        # if direction != 0:
        #     y = len(row_0) - y - 1

        v_0 = []

        # print(" ")
        # print("y")
        # print(y)

        v_0 = tuple(viewer(row_0, y, view, v_0))

        # print("v_0")
        # print(v_0)
        #
        # print("rule")
        # print(d_rule[v_0])

        rc.append(list(d_rule.keys()).index(v_0))

        # print("color_cells")
        # print("y")
        # print(y)
        # print('len(row_1)')
        # print(len(row_1))
        # print("v_0")
        # print(v_0)

        row_1[y] = int(d_rule[v_0])

    return row_1, rc





####everything needed to develope journal patterns takes place here####

#name of the journal to be developed. must be in quotation marks(single or double)(journal name should be completely green)
j_name = 'journal_oatmeal-3'

#number of colors
base = 3

###color bank###
#each color is made of three values between 0 and 1. (Red, Green, Blue)
#the website below used values betwen 0 and 255, so any values taken must be converted/aproximated
#https://color.adobe.com/create/color-wheel
black = (0, 0, 0)
white = (1, 1, 1)
red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
magenta = (1, 0, 1)
cyan = (0, 1, 1)
yellow = (1, 1, 0)

magenta_d = (.8, 0, .8)
yellow_d = (.8, .8, 0)
cyan_d = (0, .8, .8)
red_d = (.8, 0, 0)

grey = (.1, .1, .1)
purple = (.6, 0, .6)
turquoise = (0, .8, .8)
light_grey = (.8, .8, .8)
moss = (.2, .4, .2)
orange = (1, .5, .1)


#corresponding to the number of colors indicated above. Order of colors matters, change to get new variations of a design.
color_list_0 = [cyan, white, yellow, grey, black]
color_list_1 = [red, yellow, orange]
color_list_2 = [blue, magenta, cyan, red]
color_list_3 = [black, grey, cyan, magenta, yellow]


#0=no reflection 1=reflected image across the top
reflect = 1

###dimensions

##length adjustment. length = length * scale / shrink
#increase the number of cells in each rule call (multiplicative)
scale_l = 1
#decrease the number of cells in each rule call (divisive)
shrink_l = 2

##width adjustment width = width * scale_w / shrink_w
#multiplicative
scale_w = 2
#(divisive)
shrink_w = 1



###experimental
#0=one image per journal. 2+ will develope multiple of equal number of key strokes, but different lengths due to differences in the time between them.
split = 0


#keep this at zero
width = 0

infile = open("journals/" + j_name, "rb")
journal = pickle.load(infile)
infile.close

path = 'synthesis'

print("len of journals")
print(len(list(journal.keys())))

try:
    print("bookmarks")
    print(journal['bookmarks'])
    bookmarks = journal['bookmarks']

except:
    #dont touch
    bookmarks = [0]

bookmarks = [0]



#choose which bookmarked segments you want to stitch together. numbers must be separated by commas.
bookmark_choices = []

center_seed = 1


def synthesize(j_name, width, split, s_f, color_list):

    cMap = c.ListedColormap(color_list)

    color_list_label = []
    for color in color_list:

        color_list_label.append((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    if split != 0:

        l_j = len(list(journal.keys()))
        s_j = int(len(list(journal.keys())) / split)

        print("")
        print("l_j")
        print(l_j)

        print("")
        print("s_j")
        print(s_j)

        for x in range(split):

            synthesis = []
            frame = []

            print("split")
            print(x)

            journal_key = list(journal.keys())[x * s_j:(x + 1) * s_j]

            print("")
            print('journal_key')
            print((x * s_j, (x + 1) * s_j))

            if s_f == 0:

                for k in journal_key:

                    # print(k[0])
                    jk = journal[k]

                    if len(jk[0]) > 0:

                        # print('')
                        print(list(journal.keys()).index(k))
                        # print(k)
                        # print(jk)

                        width += len(jk[0])

                        for j in jk:

                            for k in j:

                                synthesis.append(k)



                synthesis = np.asarray(synthesis)

                j_name += '-simple'

            if s_f == 1:

                for k in journal_key:

                    # print(k[0])
                    jk = journal[k]

                    if list(journal.keys()).index(k) == 0:

                        # print('')
                        # print(list(journal.keys()).index(k))
                        # print(k)
                        # print(jk)

                        rows = 0

                        for j in jk:

                            for j_1 in j:

                                rows += 1
                                width += 1

                        try:
                            i_rule = rule_gen(int(k), base)[1]

                        except:
                            i_rule = rule_gen(k[0], base, string=1)[1]


                        k_str = ''

                        for i in i_rule:

                            k_str += i

                        frame.append((k_str, int(rows * scale_l / shrink_l) + 1))

                        continue


                    if len(jk[0]) > 0:

                        # print('')
                        # print(list(journal.keys()).index(k))
                        # print(k)
                        # print(jk)


                        frame.append((k[0], int(len(jk[0]) * scale_l / shrink_l) + 1))

                        width += int(len(jk[0]) * scale_l / shrink_l) + 1

                print("")
                # print("frame")
                # print(frame)
                print('width')
                print(width)

                row = [0 for x in range(width)]
                row[int(len(row)/2)] = 1

                synthesis.append(row)

                # print('row')
                # print(row)
                print(len(row))

                for f in frame:

                    count = 0

                    d_rule, i_rule = rule_gen(f[0], base, string=1)

                    while count < f[1]:

                        synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                        count += 1

                # print("")
                # print("synthesis")
                # print(synthesis)

                synthesis = np.asarray(synthesis)

                j_name += '-full'

                # print("")
                # print("synthesis")
                # print(synthesis)

            file = str(base) + '-' + j_name + '-' + str(scale_l) + '-' + str(shrink_l) + '-' + str(x)
            path_name = os.path.join(path, file)

            ax = plt.gca()
            ax.set_aspect(1)

            plt.margins(0, None)

            plt.pcolormesh(synthesis, cmap=cMap)

            #hide x-axis
            ax.get_xaxis().set_visible(False)

            #hide y-axis
            ax.get_yaxis().set_visible(False)

            print("")
            print("printing")

            # plt.show()
            plt.savefig(path_name, dpi=width, bbox_inches='tight',pad_inches = 0)
            plt.close()

    else:

        synthesis = []
        frame = []

        journal_key = list(journal.keys())[1:]

        print("")
        print('journal_key')

        #simple
        if s_f == 0:

            for k in journal_key:

                # print(k[0])
                jk = journal[k]

                if len(jk[0]) > 0:

                    # print('')
                    print(list(journal.keys()).index(k))
                    # print(k)
                    # print(jk)

                    width += len(jk[0])

                    for j in jk:

                        for k in j:
                            synthesis.append(k)

            print("len syn")
            print(len(synthesis))

            if reflect == 1:

                for s in synthesis[:]:

                    synthesis.append(s)

            print(len(synthesis))

            synthesis = np.asarray(synthesis)


            j_name += '-simple'

            j_name += '-full'

            # print("")
            # print("synthesis")
            # print(synthesis)

            file = str(base) + '-' + j_name + '_length' + str(scale_l) + '-' + str(shrink_l) + '_width' + str(
                scale_w) + '-' + str(shrink_w) + '_Colors-' + str(color_list_label)
            path_name = os.path.join(path, file)

            ax = plt.gca()
            ax.set_aspect(1)

            plt.margins(0, None)

            plt.pcolormesh(synthesis, cmap=cMap)

            # hide x-axis
            ax.get_xaxis().set_visible(False)

            # hide y-axis
            ax.get_yaxis().set_visible(False)

            print("")
            print("printing")

            # plt.show()
            plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
            plt.close()

        #full
        if s_f == 1:

            if len(bookmarks) == 1:

                for rule in journal_key:

                    if type(rule) == str:
                        continue

                    # print(k[0])
                    #journal[rule]
                    jr = journal[rule]

                    #first rule
                    if list(journal.keys()).index(rule) == 0:

                        rows = 0

                        for page in jr:

                            for line in page:
                                rows += 1
                                width += 1

                        try:
                            i_rule = rule_gen(int(rule), base)[1]

                        except:
                            i_rule = rule_gen(rule[0], base, string=1)[1]

                        k_str = ''

                        for i in i_rule:
                            k_str += i

                        frame.append((k_str, int(rows * scale_l / shrink_l) + 1))

                        continue

                    if len(jr[0]) > 0:
                        # print('')
                        # print(list(journal.keys()).index(k))
                        # print(k)
                        # print(jk)

                        frame.append((rule[0], int(len(jr[0]) * scale_l / shrink_l) + 1))

                        width += int(len(jr[0]) * scale_l / shrink_l) + 1

                print("")
                print('width')
                print(width)

                width = int(width * scale_w /shrink_w)

                row = [0 for x in range(width)]
                if center_seed == 1:
                    for y in range(base):
                        row[int(len(row) / 2) + y - base] = y

                synthesis.append(row)

                for f in frame:

                    count = 0

                    d_rule, i_rule = rule_gen(f[0], base, string=1)

                    while count < f[1]:
                        synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                        count += 1

                print("len syn")
                print(len(synthesis))

                if reflect == 1:

                    for s in reversed(synthesis[:]):

                        # print("")
                        # print("s")
                        # print(s)
                        # print(type(s))

                        # s = list(reversed(s[:]))

                        # print(s)
                        # print(type(s))

                        synthesis.append(s)

                print(len(synthesis))

                j_name += '-full'

                # print("")
                # print("synthesis")
                # print(synthesis)

                file = str(base) + '-' + j_name + '_length' + str(scale_l) + '-' + str(shrink_l) + '_width' + str(
                    scale_w) + '-' + str(shrink_w) + '_Colors-' + str(color_list_label)
                path_name = os.path.join(path, file)

                ax = plt.gca()
                ax.set_aspect(1)

                plt.margins(0, None)

                plt.pcolormesh(synthesis, cmap=cMap)

                # hide x-axis
                ax.get_xaxis().set_visible(False)

                # hide y-axis
                ax.get_yaxis().set_visible(False)

                print("")
                print("printing")

                # plt.show()
                plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
                plt.close()

            else:

                if len(bookmark_choices) == 0:

                    for x in range(len(bookmarks) - 1):

                        synthesis = []
                        frame = []
                        width = 0

                        print()
                        print("bookmarks")
                        print(bookmarks[x], bookmarks[x + 1])

                        journal_bookmark = journal_key[bookmarks[x]:bookmarks[x + 1]]

                        for rule in journal_bookmark:

                            if type(rule) == str:
                                continue

                            # print(k[0])
                            # journal[rule]
                            jr = journal[rule]

                            # first rule
                            if list(journal.keys()).index(rule) == 0:

                                rows = 0

                                for page in jr:

                                    for line in page:
                                        rows += 1
                                        width += 1

                                try:
                                    i_rule = rule_gen(int(rule), base)[1]

                                except:
                                    i_rule = rule_gen(rule[0], base, string=1)[1]

                                k_str = ''

                                for i in i_rule:
                                    k_str += i

                                frame.append((k_str, int(rows * scale_l / shrink_l) + 1))

                                continue

                            if len(jr[0]) > 0:
                                # print('')
                                # print(list(journal.keys()).index(k))
                                # print(k)
                                # print(jk)

                                frame.append((rule[0], int(len(jr[0]) * scale_l / shrink_l) + 1))

                                width += int(len(jr[0]) * scale_l / shrink_l) + 1

                        print('width')
                        print(width)

                        width = int(width * scale_w / shrink_w)

                        row = [0 for x in range(width)]
                        if center_seed == 1:
                            for y in range(base):
                                row[int(len(row) / 2) + y - base] = y

                        synthesis.append(row)

                        for f in frame:

                            count = 0

                            d_rule, i_rule = rule_gen(f[0], base, string=1)

                            while count < f[1]:
                                synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                                count += 1

                        print("len syn")
                        print(len(synthesis))

                        if reflect == 1:

                            for s in reversed(synthesis[:]):
                                # print("")
                                # print("s")
                                # print(s)
                                # print(type(s))

                                # s = list(reversed(s[:]))

                                # print(s)
                                # print(type(s))

                                synthesis.append(s)

                        j_name += '-bookmarks-'
                        j_name += str(bookmarks[x])

                        # print("")
                        # print("synthesis")
                        # print(synthesis)

                        file = str(base) + '-' + j_name + '_length' + str(scale_l) + '-' + str(shrink_l) + '_width' + str(
                            scale_w) + '-' + str(shrink_w) + '_Colors-' + str(color_list_label)
                        path_name = os.path.join(path, file)

                        ax = plt.gca()
                        ax.set_aspect(1)

                        plt.margins(0, None)

                        plt.pcolormesh(synthesis, cmap=cMap)

                        # hide x-axis
                        ax.get_xaxis().set_visible(False)

                        # hide y-axis
                        ax.get_yaxis().set_visible(False)

                        print("printing")

                        # plt.show()
                        plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
                        plt.close()

                else:

                    journal_bookmark = []
                    synthesis = []
                    frame = []
                    width = 0

                    for b in bookmark_choices:
                        for o in range(bookmarks[b] - bookmarks[b - 1]):
                            journal_bookmark.append(journal_key[bookmarks[b-1] + o])

                    for rule in journal_bookmark:

                        if type(rule) == str:
                            continue

                        # print(k[0])
                        # journal[rule]
                        jr = journal[rule]

                        # first rule
                        if list(journal.keys()).index(rule) == 0:

                            rows = 0

                            for page in jr:

                                for line in page:
                                    rows += 1
                                    width += 1

                            try:
                                i_rule = rule_gen(int(rule), base)[1]

                            except:
                                i_rule = rule_gen(rule[0], base, string=1)[1]

                            k_str = ''

                            for i in i_rule:
                                k_str += i

                            frame.append((k_str, int(rows * scale_l / shrink_l) + 1))

                            continue

                        if len(jr[0]) > 0:
                            # print('')
                            # print(list(journal.keys()).index(k))
                            # print(k)
                            # print(jk)

                            frame.append((rule[0], int(len(jr[0]) * scale_l / shrink_l) + 1))

                            width += int(len(jr[0]) * scale_l / shrink_l) + 1

                    print('width')
                    print(width)

                    width = int(width * scale_w / shrink_w)

                    row = [0 for x in range(width)]

                    if center_seed == 1:
                        for y in range(base):
                            row[int(len(row) / 2) + y - base] = y

                    synthesis.append(row)

                    for f in frame:

                        count = 0

                        d_rule, i_rule = rule_gen(f[0], base, string=1)

                        while count < f[1]:
                            synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                            count += 1

                    print("len syn")
                    print(len(synthesis))

                    if reflect == 1:

                        for s in reversed(synthesis[:]):
                            # print("")
                            # print("s")
                            # print(s)
                            # print(type(s))

                            # s = list(reversed(s[:]))

                            # print(s)
                            # print(type(s))

                            synthesis.append(s)

                    j_name += '-bookmarks-'
                    j_name += str(bookmark_choices)

                    # print("")
                    # print("synthesis")
                    # print(synthesis)

                    file = str(base) + '-' + j_name + '_length' + str(scale_l) + '-' + str(shrink_l) + '_width' + str(
                        scale_w) + '-' + str(shrink_w) + '_Colors-' + str(color_list_label)
                    path_name = os.path.join(path, file)

                    ax = plt.gca()
                    ax.set_aspect(1)

                    plt.margins(0, None)

                    plt.pcolormesh(synthesis, cmap=cMap)

                    # hide x-axis
                    ax.get_xaxis().set_visible(False)

                    # hide y-axis
                    ax.get_yaxis().set_visible(False)

                    print("printing")

                    # plt.show()
                    plt.savefig(path_name, dpi=width, bbox_inches='tight', pad_inches=0)
                    plt.close()








synthesize(j_name, width, split, 1, color_list_1)



