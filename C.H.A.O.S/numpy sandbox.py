import numpy as np

view = 3

length = 3
width = 3

def base_x(n, b):

    e = n // b
    q = n % b

    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def base_x_10(coord, n, b):

    e = n // b
    q = n % b

    if n == 0:
        coord.append(0)
        return coord

    elif e == 0:
        coord.append(q)
        return coord

    else:
        coord.append(q)
        coord = base_x_10(coord, e, b)
        return coord


def rule_gen_10(rule, base, length):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = list(reversed(base_x_10([], rule, base)))

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


array = np.zeros((length, width), dtype='uint8')

print("")
print("array")
print(array)

print("")

def diagonals(length, width):

    diagonal_paths = dict()

    diagonal_num = length + width - 2
    elbow = int((length + width)/2)


    for x in range(elbow):

        left = []
        right = []
        coord_model = []

        x += 1

        for y in range(x):
            left.append(y)
            right.insert(0, y)

        for z in range(len(left)):

            coord_model.append((left[z], right[z]))

        # print(coord_model)
        diagonal_paths[x - 1] = coord_model



    for x in range(elbow - 1):

        left = []
        right = []
        coord_model = []

        x += 1

        for y in range(x):
            left.append(length - y - 1)
            right.insert(0, width - y - 1)

        for z in range(len(left)):

            coord_model.append((left[z], right[z]))

        # print(coord_model)
        diagonal_paths[diagonal_num - x + 1] = tuple(reversed(coord_model))

    diagonal_paths = dict(sorted(diagonal_paths.items(), key=lambda x:x[0]))

    diagonal_coords = []

    for d in diagonal_paths:

        # print("")
        # print(d)
        # print(diagonal_paths[d])

        for i in diagonal_paths[d]:

            diagonal_coords.append((d, i))

    return tuple(diagonal_coords), diagonal_paths

diagonal_coords, diagonal_paths = diagonals(length, width)


for d in diagonal_coords:

    array[d[1]] = diagonal_coords.index(d)

print("")
print("array")
print(array)

print("")
print('diagonal')
print(diagonal_coords)
print("")
print(diagonal_paths)






