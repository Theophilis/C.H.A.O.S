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
base = 2
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


infile = open("polar maps/polar_u-16", "rb")
polar_u_i = pickle.load(infile)
infile.close

# infile = open("organized-rules/roamers-2-3", "rb")
# roamers = pickle.load(infile)
# infile.close
#
# infile = open("organized-rules/right_roam-2-3", "rb")
# right_roam = pickle.load(infile)
# infile.close
#
# infile = open("organized-rules/left_roam-2-3", "rb")
# left_roam = pickle.load(infile)
# infile.close


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


def rule_gen(rule, base, length):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(rule, base)

    x = int_rule[::-1]

    while len(x) < length:
        x += '0'

    bnr = x[::-1]
    int_rul = list(bnr)
    int_rule = []
    for i in int_rul:
        int_rule.append(int(i))

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
        rules[tuple(key)] = int(int_rule[-x - 1])
    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


roamers = []
right_roam = []
left_roam = []
no_roam = []

for x in range(256):

    i_rule = rule_gen(x, base, 8)[1]

    i_rule[-2] = 1
    i_rule[3] = 1

    # print(i_rule)

    value = decimal(i_rule, 2)

    if value not in roamers:

        roamers.append(value)

for x in range(256):

    i_rule = rule_gen(x, base, 8)[1]

    i_rule[3] = 1

    # print(i_rule)

    value = decimal(i_rule, 2)

    if value not in right_roam and value not in roamers:
        right_roam.append(value)

for x in range(256):

    i_rule = rule_gen(x, base, 8)[1]

    i_rule[-2] = 1

    # print(i_rule)

    value = decimal(i_rule, 2)

    if value not in left_roam and value not in roamers:
        left_roam.append(value)


print("")
print("roamers")
print(roamers)
print(len(roamers))
print(right_roam)
print(len(right_roam))
print(left_roam)
print(len(left_roam))

rule_count = dict()

for p in polar_u_i:

    if p[2] not in rule_count:

        rule_count[p[2]] = 1

    else:

        rule_count[p[2]] += 1

rule_count = dict(sorted(list(rule_count.items()), key=lambda x:x[1], reverse=True))

print("")
print("rule_count")
print(rule_count)

for x in range(256):

    if x not in roamers and x not in right_roam and x not in left_roam:

        no_roam.append(x)

print("")
print("no_roam")
print(no_roam)
print(len(no_roam))


filename = 'organized-rules/roamers-2-3'
outfile = open(filename, 'wb')
pickle.dump(roamers, outfile)
outfile.close()

filename = 'organized-rules/right_roam-2-3'
outfile = open(filename, 'wb')
pickle.dump(right_roam, outfile)
outfile.close()

filename = 'organized-rules/left_roam-2-3'
outfile = open(filename, 'wb')
pickle.dump(left_roam, outfile)
outfile.close()

filename = 'organized-rules/no_roam-2-3'
outfile = open(filename, 'wb')
pickle.dump(no_roam, outfile)
outfile.close()