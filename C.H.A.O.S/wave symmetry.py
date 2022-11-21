
base = 2
view = 5
origin = [3]

def crest_flow(fluid, cycles):

    # print('fluid')
    # print(fluid)
    # print('cycles')
    # print(cycles)

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
    flow = crest_flow(origin, view - 1)

    # print()
    # print("crest flow")
    # print(flow)

    flow = trough_flow(base ** view - 1, flow, 1)

    # print()
    # print("trough flow")
    # print(flow)

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


x, y, z = sym_gen(base, view, origin)

print('')
print('x, y, z')
print(x)
print(y)
print(z)

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

def collapse(diff):

    c = []

    for d in diff:
        if d > 0:
            c.append(d)

    return c

diff = difference(z)
print()
print('diff')
print(diff)

def extract(diff):
    diff = difference(diff)
    # print(diff)

    coll = collapse(diff)
    #
    # print('coll')
    # print(coll)

    return coll

for x in range(5):
    diff = extract(diff)
    print(diff)