import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as c
import os
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
j_name = 'journal_xx'

#number of colors
base = 3

###color bank###
#each color is made of three values between 0 and 1. (Red, Green, Blue)
#the website below used values betwen 0 and 255, so any values taken must be converted/aproximated
#https://color.adobe.com/create/color-wheel

black = (0, 0, 0)
grey = (.5, .5, .5)
white = (1, 1, 1)
red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
magenta = (1, 0, 1)
cyan = (0, 1, 1)
yellow = (1, 1, 0)


magenta_d = (.3, 0, .3)
yellow_d = (.8, .8, 0)
cyan_d = (0, .7, .7)

red_d = (.7, 0, 0)


grey_scale = 1

grey = (.01*grey_scale, .01*grey_scale, .01*grey_scale)
grey1 = (.02*grey_scale, .02*grey_scale, .02*grey_scale)
grey2 = (.03*grey_scale, .03*grey_scale, .03*grey_scale)
grey3 = (.04*grey_scale, .04*grey_scale, .04*grey_scale)
grey4 = (.05*grey_scale, .05*grey_scale, .05*grey_scale)
grey5 = (.06*grey_scale, .06*grey_scale, .06*grey_scale)
grey6 = (.07*grey_scale, .07*grey_scale, .07*grey_scale)
grey7 = (.08*grey_scale, .08*grey_scale, .08*grey_scale)
grey8 = (.09*grey_scale, .09*grey_scale, .09*grey_scale)

rg0 = (1, 0, 0)
rg1 = (1, .25, 0)
rg2 = (1, .5, 0)
rg3 = (1, .75, 0)
rg4 = (1, 1, 0)
rg5 = (.75, 1, 0)
rg6 = (.5, 1, 0)
rg7 = (.25, 1, 0)
rg8 = (0, 1, 0)

rb0 = (1, 0, 0)
rb1 = (1, 0, .25)
rb2 = (1, 0, .5)
rb3 = (1, 0, .75)
rb4 = (1, 0, 1)
rb5 = (.75, 0, 1)
rb6 = (.5, 0, 1)
rb7 = (.25, 0, 1)
rb8 = (0, 0, 1)

gb0 = (0, 1, 0)
gb1 = (0, 1, .25)
gb2 = (0, 1, .5)
gb3 = (0, 1, .75)
gb4 = (0, 1, 1)
gb5 = (0, .75, 1)
gb6 = (0, .5, 1)
gb7 = (0, .25, 1)
gb8 = (0, 0, 1)







purple = (.6, 0, .6)
light_grey = (.8, .8, .8)
moss = (.1, .3, .1)
orange = (1, .5, .1)


#corresponding to the number of colors indicated above. Order of colors matters, change to get new variations of a design.
color_list_0 = [cyan, white, yellow, grey, black]
color_list_1 = [red, yellow, orange]
color_list_2 = [magenta, cyan, yellow]
color_list_3 = [black, grey, cyan, magenta, yellow]
color_list_4 = [white, cyan, magenta, yellow, blue]

#6 color
color_list_6 = [grey6, cyan, red, magenta_d, white, moss]

#9 color
color_list_9 = [black, grey, cyan, magenta, yellow, light_grey, red, blue, green]
color_list_10 = [black, cyan, grey, grey2, grey3, red, grey5, grey6, grey7, grey8]
color_list_rb = [rb0, rb1, rb2, rb3, rb4, rb5, rb6, rb7, rb8]
color_list_rg = [rg0, rg1, rg2, rg3, rg4, rg5, rg6, rg7, rg8]
color_list_gb = [gb0, gb1, black, gb3, magenta, gb5, white, gb7, gb8]


#0=no reflection, 1=reflected image across the top, 2=reflection across bottom
reflect = 1

###dimensions

##length adjustment. length = length * scale / shrink
#increase the number of cells in each rule call (multiplicative)
scale_l = 1
#decrease the number of cells in each rule call (divisive)
shrink_l = 2

##width adjustment width = width * scale_w / shrink_w
#multiplicative
scale_w = 1
#(divisive)
shrink_w = 1



###experimental
#0=one image per journal. 2+ will develope multiple of equal number of key strokes, but different lengths due to differences in the time between them.
split = 0

s_f = 1


infile = open("journals/" + j_name, "rb")
journal = pickle.load(infile)
infile.close

path = 'synthesis'

print("len of journals")
print(len(list(journal.keys())))
print("bookmarks")
print(journal['bookmarks'])
bookmarks = journal['bookmarks']



#full print overide
# bookmarks = [0]



#choose which bookmarked segments you want to stitch together. numbers must be separated by commas.
bookmark_choices = []

center_seed = 1
seed_distro = 1


def synthesize(j_name, color_list):

    cMap = c.ListedColormap(color_list)

    color_list_label = []
    for color in color_list:

        color_list_label.append((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))

    journal_key = list(journal.keys())[1:]

    # print("")
    # print('journal_key')
    # print(journal_key)

    if len(bookmark_choices) == 0:

        for x in range(len(bookmarks)-1):

            synthesis = []
            frame = []
            width = 0

            # print()
            # print("bookmarks")
            # print(bookmarks[x], bookmarks[x + 1])

            journal_bookmark = journal_key[bookmarks[x]:bookmarks[x + 1]]
            # print(journal_bookmark)

            for rule in journal_bookmark:

                frame.append((rule[0], journal[rule]))
                width += journal[rule]

            # print("frame")
            # print(frame)
            #
            # print('width')
            # print(width)

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

            print()
            print(x)
            print("len syn")
            print(len(synthesis))

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

        # print("journal bookmark")
        # print(journal_bookmark)
        # print(len(journal_bookmark))

        for rule in journal_bookmark:
            frame.append((rule[0], journal[rule]))
            width += journal[rule]

        # print('width')
        # print(width)

        width = int(width * scale_w / shrink_w)


        row = [0 for x in range(width)]

        if center_seed == 1:
            for z in range(seed_distro):
                z += 1
                for y in range(base):
                    row[int(len(row) / (1 + seed_distro)) * z + y - base] = y

        synthesis.append(row)

        for f in frame:

            count = 0

            d_rule, i_rule = rule_gen(f[0], base, string=1)

            while count < f[1]:
                synthesis.append(Color_cells(d_rule, width, synthesis[-1])[0])

                count += 1

        print()
        print("width")
        print(width)
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

        if reflect == 2:

            synthesis = list(reversed(synthesis))

            for s in reversed(synthesis[:]):
                synthesis.append(s)

        j_name += '-bookmarks-'
        j_name += str(bookmark_choices)

        # print("")
        # print("synthesis")
        # print(synthesis)

        file = str(base) + '-' + j_name + '_length' + str(scale_l) + '-' + str(shrink_l) + '_width' + str(
            scale_w) + '-' + str(shrink_w) + '_Colors-' + str(color_list_label) + '-' + str(reflect)
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



synthesize(j_name, color_list_2)



