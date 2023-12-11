import numpy as np

rule = 90
base = 2
view = 3
bv = base**view
rule_d = {}
shade = 1
width = 5
height = width
width_3 = width*3
map_a = width_3*height
map = [0 for n in range(height*width*3)]
map[(int(width/2) + int(height/2)*width) *3] = shade
map[(int(width/2) + int(height/2)*width) *3 + 1] = shade
map[(int(width/2) + int(height/2)*width) *3 +2] = shade


value_color = {0: (0, 0, 0), 1: (shade, shade, shade), 2: (shade, shade, 0), 3: (0, shade, 0), 4: (0, shade, shade), 5: (0, 0, shade),
               6: (shade, 0, shade), 7: (shade, shade, shade)}


def print_map(map, width, height):
    print()
    for x in range(height):
        print(map[x*width*3:(x+1)*width*3])
    print()

def rule_gen(rule_d, rule, base, view, new=0):
    for x in range(bv):
        e = rule // base
        q = rule % base
        key = []

        if new == 0:
            for y in range(view):
                r = x // base
                w = x % base
                key += value_color[w]
                x = r
        else:
            key = list(rule_d.keys())[x]

        rule = e
        rule_d[tuple(key)] = value_color[q]

    return rule_d

rule_d = rule_gen(rule_d, rule, base, view)

print(rule_d)
print_map(map, width, height)


def hortosis(map, width, height, pos, dis=1, lr=0):

    # print()
    # print("hortosis")

    #left
    if lr == 0:

        for d in range(dis):
            d = d
            c = int((dis-d)/dis)*width_3
            cord = (pos[0] + pos[1]*width + d - int(dis/2)) * 3
            hood = (map[cord-3 + c], map[cord-2 + c], map[cord-1 + c],
                    map[cord], map[cord+1], map[cord+2],
                    map[(cord+3)%map_a], map[(cord+4)%map_a], map[(cord+5)%map_a])
            house = rule_d[hood]

            # print()
            # print(d)
            # print(int((dis-d)/dis))
            # print(cord)
            # print(hood)
            # print(house)

            for x in range(int(height/2)):

                x = int(height/2)-x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord-(x+1)*width_3)
                # print(map[cord-(x+1)*width_3:cord-(x+1)*width_3+3])
                map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord-(x)*width_3:cord-(x)*width_3+3]
                map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord+(x)*width_3:cord+(x)*width_3+3]



                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord+2] = house[2]


    #right
    if lr == 1:

        for d in range(dis):
            d = dis-d-1
            cord = (pos[0] + pos[1] * width + d - int(dis/2)) * 3
            hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                    map[cord], map[cord + 1], map[cord + 2],
                    map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])

            # print(cord)
            # for x in range(view*3):
            #     hood.append(map[(cord-3+x)%map_a])
            # print(hood)
            house = rule_d[hood]
            # print(house)

            for x in range(int(height / 2)):
                x = int(height / 2) - x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord - (x + 1) * width_3)
                # print(map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3])
                map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                    x) * width_3 + 3]
                map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                    x) * width_3 + 3]

                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord + 2] = house[2]

        # print_map(map, width, height)

    #in
    if lr == 2:

        for d in range(int(dis/2)):
            #left
            d = d
            cord = (pos[0] + pos[1]*width + d - int(dis/2)) * 3
            hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                    map[cord], map[cord + 1], map[cord + 2],
                    map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])

            # print(cord)
            # for x in range(view*3):
            #     hood.append(map[(cord-3+x)%map_a])
            # print(hood)
            house = rule_d[hood]
            # print(house)

            for x in range(int(height / 2)):
                x = int(height / 2) - x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord - (x + 1) * width_3)
                # print(map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3])
                map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                    x) * width_3 + 3]
                map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                    x) * width_3 + 3]

                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord + 2] = house[2]

            #right
            d = dis-d-1
            cord = (pos[0] + pos[1] * width + d - int(dis/2)) * 3
            hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                    map[cord], map[cord + 1], map[cord + 2],
                    map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])

            # print(cord)
            # for x in range(view*3):
            #     hood.append(map[(cord-3+x)%map_a])
            # print(hood)
            house = rule_d[hood]
            # print(house)

            for x in range(int(height / 2)):
                x = int(height / 2) - x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord - (x + 1) * width_3)
                # print(map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3])
                map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                    x) * width_3 + 3]
                map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                    x) * width_3 + 3]

                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord + 2] = house[2]

        #center
        cord = (pos[0] + pos[1] * width) * 3
        hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                map[cord], map[cord + 1], map[cord + 2],
                map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])
        house = rule_d[hood]

        for x in range(int(height / 2)):
            x = int(height / 2) - x - 1
            map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                x) * width_3 + 3]
            map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                x) * width_3 + 3]

        map[cord] = house[0]
        map[cord + 1] = house[1]
        map[cord + 2] = house[2]

        # print_map(map, width, height)

    #out
    if lr == 3:

        for d in range(int(dis/2)):
            #left
            d = d
            cord = (pos[0] + pos[1]*width + d+1) * 3
            hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                    map[cord], map[cord + 1], map[cord + 2],
                    map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])

            # print(cord)
            # for x in range(view*3):
            #     hood.append(map[(cord-3+x)%map_a])
            # print(hood)
            house = rule_d[hood]
            # print(house)

            for x in range(int(height / 2)):
                x = int(height / 2) - x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord - (x + 1) * width_3)
                # print(map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3])
                map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                    x) * width_3 + 3]
                map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                    x) * width_3 + 3]

                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord + 2] = house[2]

            #right
            d = dis-d-1
            cord = (pos[0] + pos[1] * width + d) * 3
            hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                    map[cord], map[cord + 1], map[cord + 2],
                    map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])

            # print(cord)
            # for x in range(view*3):
            #     hood.append(map[(cord-3+x)%map_a])
            # print(hood)
            house = rule_d[hood]
            # print(house)

            for x in range(int(height / 2)):
                x = int(height / 2) - x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord - (x + 1) * width_3)
                # print(map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3])
                map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                    x) * width_3 + 3]
                map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                    x) * width_3 + 3]

                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord + 2] = house[2]

        #center
        cord = (pos[0] + pos[1] * width) * 3
        hood = (map[cord - 3], map[cord - 2], map[cord - 1],
                map[cord], map[cord + 1], map[cord + 2],
                map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])
        house = rule_d[hood]

        for x in range(int(height / 2)):
            x = int(height / 2) - x - 1
            map[cord - (x + 1) * width_3:cord - (x + 1) * width_3 + 3] = map[cord - (x) * width_3:cord - (
                x) * width_3 + 3]
            map[cord + (x + 1) * width_3:cord + (x + 1) * width_3 + 3] = map[cord + (x) * width_3:cord + (
                x) * width_3 + 3]

        map[cord] = house[0]
        map[cord + 1] = house[1]
        map[cord + 2] = house[2]

        # print_map(map, width, height)

    print_map(map, width, height)

    return map

pos = (int(width/2), int(width/2))

dis = 5
#
# for y in range(4):
#     print()
#     print(y)
#     map = [0 for n in range(height*width*3)]
#     map[(int(width/2) + int(height/2)*width) *3] = shade
#     map[(int(width/2) + int(height/2)*width) *3 + 1] = shade
#     map[(int(width/2) + int(height/2)*width) *3 +2] = shade
#
#     for x in range(3):
#         hortosis(map, width, height, pos, dis, y)
#     print_map(map, width, height)
#

def vertosis(map, width, height, pos, dis=1, du=0):

    # print("")
    # print('vertosis')

    #down
    if du == 0:

        for d in range(dis):
            d = d
            cord = (pos[0] + pos[1]*width + d*width - int(dis/2)*width) * 3 %map_a
            hood = (map[cord - width_3], map[cord - width_3+1], map[cord - width_3+2],
                    map[cord], map[cord+1], map[cord+2],
                    map[(cord+width_3)%map_a], map[(cord+1+width_3)%map_a], map[(cord+2+width_3)%map_a])
            house = rule_d[hood]

            # print()
            # print(d)
            # print(cord)
            # print(hood)
            # print(house)

            for x in range(int(width/2)):

                x = int(width/2)-x - 1
                # print("")
                # print(x)
                # print(cord)
                # print(cord-(x+1)*width_3)
                # print(map[cord-(x+1)*width_3:cord-(x+1)*width_3+3])
                map[cord - (x + 1)*3:cord - (x + 1)*3 + 3] = map[cord-(x)*3:cord-(x)*3+3]
                map[cord + (x + 1)*3:cord + (x + 1)*3 + 3] = map[cord+(x)*3:cord+(x)*3+3]



                # map[cord-width_3] = map[cord]
                # map[cord - width_3 + 1] = map[cord + 1]
                # map[cord - width_3 + 2] = map[cord + 2]
                # map[cord+width_3] = map[cord]
                # map[cord+width_3+1] = map[cord+1]
                # map[cord+width_3+2] = map[cord+2]

            map[cord] = house[0]
            map[cord + 1] = house[1]
            map[cord+2] = house[2]

        print_map(map, width, height)

    return map

pos = (int(width/2), int(width/2))

# #hortosis
# print('hortosis')
# map_h = [0 for n in range(height * width * 3)]
# map_h[(int(width / 2) + int(height / 2) * width) * 3] = shade
# map_h[(int(width / 2) + int(height / 2) * width) * 3 + 1] = shade
# map_h[(int(width / 2) + int(height / 2) * width) * 3 + 2] = shade
# print_map(map_h, width, height)
# hortosis(map_h, width, height, pos, dis)
# hortosis(map_h, width, height, pos, dis)
# hortosis(map_h, width, height, pos, dis)
#
# #vertosis
# print('vertosis')
# map_v = [0 for n in range(height * width * 3)]
# map_v[(int(width / 2) + int(height / 2) * width) * 3] = shade
# map_v[(int(width / 2) + int(height / 2) * width) * 3 + 1] = shade
# map_v[(int(width / 2) + int(height / 2) * width) * 3 + 2] = shade
# print_map(map_v, width, height)
# vertosis(map_v, width, height, pos, dis)
# vertosis(map_v, width, height, pos, dis)
# vertosis(map_v, width, height, pos, dis)



#hortosis

#hv maps
map_h = [0 for n in range(height * width * 3)]
map_h[(int(width / 2) + int(height / 2) * width) * 3] = shade
map_h[(int(width / 2) + int(height / 2) * width) * 3 + 1] = shade
map_h[(int(width / 2) + int(height / 2) * width) * 3 + 2] = shade

map_v = [0 for n in range(height * width * 3)]
map_v[(int(width / 2) + int(height / 2) * width) * 3] = shade
map_v[(int(width / 2) + int(height / 2) * width) * 3 + 1] = shade
map_v[(int(width / 2) + int(height / 2) * width) * 3 + 2] = shade


print()
print("h, v")
print_map(map_h, width, height)
print_map(map_v, width, height)
print("round 1")
hortosis(map_h, width, height, pos, dis)
vertosis(map_v, width, height, pos, dis)
print('round 2')
hortosis(map_h, width, height, pos, dis)
vertosis(map_v, width, height, pos, dis)
print('round 3')
hortosis(map_h, width, height, pos, dis)
vertosis(map_v, width, height, pos, dis)
