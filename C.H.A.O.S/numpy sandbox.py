import numpy as np

view = 3

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


array = np.zeros((3, 3, 3), dtype='uint8')

print("")
print("array")
print(array)

coords = []

for x in range(27):

    coords.append(tuple(reversed(rule_gen_10(x, 3, 3)[1])))

print("")
print("coords")
print(coords)


for c in coords:

    array[c] = coords.index(c)


print("")
print("c_array")
print(array)



print(array[slice(0, -1), 0, 0])