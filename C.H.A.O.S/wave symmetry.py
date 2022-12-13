
def base_x(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def crest_flow(base, fluid, cycles, start=0):

    if base == 2:
        print('fluid')
        print(fluid)
        print('cycles')
        print(cycles)

        crest = [0]
        flow = []

        #crest
        for x in range(len(fluid)):

            crest.append(fluid[x])
            crest.append(fluid[x])

        #flow
        flow.append(crest[1] * 2)
        for x in range(len(crest) - 1):

            if x % 2 == 0:
                flow.append(flow[-1] + crest[x + 1])
            else:
                flow.append(flow[-1] - crest[x + 1])

        print('')
        print('crest')
        print(crest)
        print('flow')
        print(flow)

        cycles -= 1
        if cycles == 0:
            return flow
            #
        else:
            flow = crest_flow(flow, cycles)
            return flow

    elif base == 3:
        # print('fluid')
        # print(fluid)
        # print('cycles')
        # print(cycles)

        crest = [start]
        flow = []

        # crest
        for x in range(len(fluid)):
            if x % 2 == 0:
                crest.append(fluid[x])
                crest.append(fluid[x])
                crest.append(fluid[x])
                crest.append(fluid[x])
            else:
                crest.append(fluid[x])
                crest.append(fluid[x])



        # flow
        flow.append(crest[1] * base)
        for x in range(len(crest) - 1):

            if x % 2 == 0:
                flow.append(flow[-1] + crest[x + 1])
            else:
                flow.append(flow[-1] - crest[x + 1])

        # print('')
        # print('crest')
        # print(crest)
        # print('flow')
        # print(flow)

        cycles -= 1
        if cycles == 0:
            return flow
            #
        else:
            flow = crest_flow(flow, cycles)
            return flow
def trough_flow(origin, fluid, cycles):

    # print()
    # print('origin')
    # print(origin)
    # print('fluid')
    # print(fluid)
    # print('cycles')
    # print(cycles)

    trough = [0]
    flow = []

    #trough
    for x in range(len(fluid)):

        trough.append(fluid[x])
        trough.append(fluid[x])

    #flow
    flow.append(origin)
    for x in range(len(trough) - 1):

        if x % 2 == 0:
            flow.append(flow[-1] - trough[x + 1])
        else:
            flow.append(flow[-1] + trough[x + 1])

    # print('')
    # print('trough')
    # print(trough)
    # print('flow')
    # print(flow)

    cycles -= 1
    if cycles == 0:
        return flow
        #
    else:
        flow = trough_flow(flow, cycles)
        return flow
def sym_gen(base, view, origin):

    if base == 2:
        flow = crest_flow(origin, view - 1)

        print()
        print("crest flow")
        print(flow)

        flow = trough_flow(base ** view - 1, flow, 1)

        print()
        print("trough flow")
        print(flow)

        z = [0]

        for x in range(len(flow)):
            z.append(z[-1] + flow[x])

        xl = []
        y = []

        # print()
        for x in range(base ** view * 2):
            xl.append(x)
            y.append(x + z[x])

            # print(x, y[x], z[x])

        # print('')
        # print('x, y, z')
        # print(xl)
        # print(y)
        # print(z)

        return xl, y, z

    elif base == 3:

        flow = crest_flow(origin, view - 1)

        # print()
        # print('crest_flow')
        # print(flow)

def difference(list):

    # print()
    # print('list')
    # print(list)

    d = []

    for x in range(len(list) - 1):
        d.append(list[x + 1] - list[x])

    # print('diff')
    # print(diff)

    return d
def even(list):
    evened = []
    last = 0

    for l in list:
        if l != last:
            evened.append(abs(l))
            last = l

    return evened

def collapse(diff):

    c = []

    for d in diff:
        if d > 0:
            c.append(d)

    return c
def extract(diff):
    diff = difference(diff)
    # print(diff)

    coll = collapse(diff)
    #
    # print('coll')
    # print(coll)

    return coll


# base = 2
# view = 5
# origin = [base * base - 1]
#
# x, y, z = sym_gen(base, view, origin)
# # print('')
# # print('x, y, z')
# # print(x)
# # print(y)
# # print(z)
# diff = difference(z)
# # print()
# # print('diff')
# # print(diff)
# for x in range(5):
#     diff = extract(diff)
#     # print(diff)


# base = 3
# view = 5
# origin = [base * base - 1]
#
# x, y, z = sym_gen(base, view, origin)
#
# print('x, y, z')
# print(x)
# print(y)
# print(z)

base = 2
view = 5

xb = [base_x(x, base) for x in range(base ** view)]
for x in range(len(xb)):
    if len(xb[x]) < view:
        tel = ''
        for y in range(view - len(xb[x])):
            tel += '0'
        xb[x] = list(tel + xb[x])

    else:
        xb[x] = list(xb[x])

# print(xb)
y = []

for b0 in xb:
    # print(xb.index(b0))
    b0 = list(reversed(b0))
    y.append(xb.index(b0))


print(y)

z = []

for x in range(base ** view):
    z.append(y[x] - x)

print(z)


diff = difference(z)

print()
print(diff)

e = even(diff)
print(e)

for x in range(view - 1):
    diff = difference(e)

    print()
    print(diff)

    c = collapse(diff)

    print(c)

    e = even(c)

    print(e)
