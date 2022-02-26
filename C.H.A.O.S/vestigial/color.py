import numpy as np

direction = 0
base = 2
view = 3

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

    # print(" ")
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


def Color(color, d_rule, cell_row_width):

    color_n = []
    rc = []
    row_0 = np.zeros((1, cell_row_width), dtype='int8')
    row_1 = np.zeros((1, cell_row_width), dtype='int8')

    print('rows')
    print(row_0)
    print(row_1)

    for c in color:
        row_0[0, c] = 1

    print(row_0)

    for y in range(len(row_0[0])):

        if direction != 0:
            y = len(row_0) - y - 1

        v_0 = []

        print(" ")
        print("y")
        print(y)

        v_0 = tuple(viewer(row_0[0], y, view, v_0))

        print("v_0")
        print(v_0)

        print("rule")
        print(d_rule[v_0])
        print(d_rule)
        print(d_rule[v_0])
        rc.append(list(d_rule.keys()).index(v_0))

        print(" ")
        print("rc")
        print(rc)

        row_1[0, y] = d_rule[v_0]
        if int(d_rule[v_0]) == 1:
            # print("bingo")
            # print(y)
            color_n.append(y)

    return color_n


cells = []
cell_row_width = 17

rule = rule_gen(90, base)

d_rule = rule[0]
i_rule = rule[1]

print(" ")
print("d_rule")
print(d_rule)
print("i_rule")
print(i_rule)

color =[int(cell_row_width/2)]

color = Color(color, d_rule, cell_row_width)
print(color)