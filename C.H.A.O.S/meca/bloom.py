
import numpy as np




def base_x(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, base=2, width=0, string=0):
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




#######flow######2d

base = 2
view = 3
bv = base ** view
bvv = base ** view ** view
rv = 137
rules, rule = rule_gen(rv, base)
# print(rule)
rule = np.array(rule)
# print(rule)
l = 11
h = l
lh = l*h


flow = np.zeros(l, dtype=int)
flow[int(l/2)] = 1
water = np.zeros((h, l), dtype=int)
water[0] = flow
# print("")
# print("water")
# print(water)
# print(flow)


currents = []
for x in range(view):

    x = x + 1

    if x == 0:
        currents.append(flow)
    else:
        if x%2 == 0:
            shift = -int(x/2)
        else:
            shift = int(x/2)
        flow_r = np.roll(flow, shift)
        currents.append(flow_r)

    # print()
    # print(currents[x-1])
current = currents[1]*1 + currents[0]*base + currents[2]*base**2
# print()
# print(current)
row = rule[-current.astype(int)]
# print()
# print(row)

water = np.roll(water, l)
water[0] = row
flow = water[0]

# print("")
# print("water")
# print(water)



#######flow###### 3d

base = 2
view = 5
bv = base ** view
bvv = base ** view ** view
rv = 137
rules, rule = rule_gen(rv, base)
print(rule)
rule = np.array(rule)
print(rule)
print(len(rule))
l = 5
h = l
lh = l*h


flow = np.zeros((h, l), dtype=int)
flow[int(l/2), int(h/2)] = 1
water = np.zeros((h, l), dtype=int)

# print("")
# print("water")
# print(water)
# print()
# print(flow)

for x in range(5):
    currents = []

    flow_1 = np.roll(flow, -1)
    flow_2 = np.roll(flow, 1)
    flow_3 = np.roll(flow, -l)
    flow_4 = np.roll(flow, l)

    currents = [flow, flow_1, flow_2, flow_3, flow_4]



    current = currents[3]*1 + currents[1]*base + currents[0]*base**2 + currents[2]*base**3 + currents[4]*base**4
    # print()
    # print(current)
    water = rule[-current.astype(int)]
    water = water.astype(int)
    # print()
    # print(row)

    flow = water
    # print()
    # print(flow)








