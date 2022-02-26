import math


def base_x(n, b):
    e = n//b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, view, base = 2, width = 0):

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


# for x in range(1,256):
#
#     print(" ")
#     print(x)
#
#     rule = rule_gen(x, 3)
#
#     print(rule[1])

two_1 = [3, 5, 6, 9, 10, 12, 17, 18, 20, 24, 33, 34, 36, 40, 48, 65, 66, 68, 72, 80, 96, 129, 130, 132, 136, 144, 160, 192]
two_0 = [252, 250, 249, 246, 245, 243, 238, 237, 235, 231, 222, 221, 219, 215, 207, 190, 189, 187, 183, 175, 159, 126, 125, 123, 119, 111, 95, 63]

two_1 = []
two_0 = []

def axiom_gen(view):

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

axioms = axiom_gen(3)
two_1 = axioms[0]
two_0 = axioms[1]


print(two_1)
print(two_0)

