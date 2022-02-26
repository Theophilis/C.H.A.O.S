import numpy as np
import matplotlib.pyplot as plt


base = []
step = 20
rule = 90
view = 3
var = 2


def base_gen(base, step):

    for x in range(step):

        base.append(0)

    base.append(1)

    for x in range(step):

        base.append(0)

    return base


def rule_gen(rule):

    rules = dict()

    bin_rule = list(str(bin(rule))[2:])
    print(" ")
    print("bin_rule")
    [print(bin_rule)]

    if len(bin_rule) < (2 ** view):

        diff = (2 ** view) - len(bin_rule)

        for x in range(diff):
            bin_rule.insert(0, str(0))

    # print(" ")
    # print("bin_rule")
    # [print(bin_rule)]

    for x in reversed(range(len(bin_rule))):

        key = str(bin(x))[2:]

        if len(key) < view:

            diff = view - len(key)
            key = list(key)

            for y in range(diff):

                key.insert(0, str(0))

        key = "".join(key)


        # print(" ")
        # print(x)
        # print("bin_rule_x")
        # print(bin_rule)
        # print(bin_rule[x])

        rules[tuple(key)] = bin_rule[x]

    return rules


base = base_gen(base, step)

print(" ")
print("base")
print(base)

rules = rule_gen(rule)

print(" ")
print("rules")
print(rules)

new_line = []

def line_gen(new_line, base, view):


    for x in range(len(base) - 2):

        # print(" ")
        # print("x")
        # print(x)
        #
        # print("len_base")
        # print(len(base) - 2)

        if x == 0:

            v_1 = ('0', '0',  str(base[x]))
            v_2 = ('0', str(base[x]), str(base[x + 1]))

            new_line.append(int(rules[v_1]))
            new_line.append(int(rules[v_2]))

        elif x == len(base) - 3:

            v_3 = (str(base[x]), str(base[x + 1]), '0')
            v_4 = (str(base[x]), '0',  '0')

            new_line.append(int(rules[v_3]))
            new_line.append(int(rules[v_4]))

        b = []
        for y in range(view):
            b.append(str(base[x + y]))

        v_0 = tuple(b)

        # print(" ")
        # print("v_0")
        # print(v_0)
        #
        # print("rules")
        # print(rules[v_0])

        new_line.append(int(rules[v_0]))

    new_line = new_line[1: len(new_line) - 1]


    return new_line


def cartographer(base, view, step, map = []):

    # print(" ")
    # print("step")
    # print(step)
    #
    # print(" ")
    # print("map")
    # print(len(map))

    new_line = []

    if len(map) == 0:

        new_line = line_gen(new_line, base, view)

        map.append(base)
        map.append(new_line)

        step -= 1

        if step == 0:

            return map

        else:

            map = cartographer(new_line, view, step, map)

            return map

    else:

        new_line = line_gen(new_line, base, view)

        map.append(new_line)

        step -= 1

        if step == 0:

            return map

        else:

            map = cartographer(new_line, view, step, map)

            return map


map = cartographer(base, view, step)

print(" ")
print("map")

for x in range(len(map)):
    print(map[x])