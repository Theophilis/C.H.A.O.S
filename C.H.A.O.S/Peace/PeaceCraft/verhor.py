import pygame
import pygame.midi
import numpy as np




#####game#####

pygame.init()
pygame.display.init()
current_display = pygame.display.Info()
WIDTH, HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)

def Chaos_Window():

    print(HEIGHT, WIDTH)

    run = 1
    base = 8
    view = 3
    bv = base ** view
    bbv = base ** base ** view

    rule = 90
    base = 2
    view = 3
    bv = base ** view
    rule_d = {}
    shade = 255
    mwidth = 31
    mheight = mwidth
    mwidth_3 = mwidth * 3
    dis = mwidth
    map_a = mwidth_3 * mheight
    map = [0 for n in range(mheight * mwidth * 3)]
    map[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3] = shade
    map[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3 + 1] = shade
    map[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3 + 2] = shade

    value_color = {0: (0, 0, 0), 1: (shade, 255, 255), 2: (shade, shade, 0), 3: (0, shade, 0), 4: (0, shade, shade),
                   5: (0, 0, shade),
                   6: (shade, 0, shade), 7: (shade, shade, shade)}

    def print_map(map, width, height):
        print()
        for x in range(height):
            print(map[x * width * 3:(x + 1) * width * 3])
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
    # print_map(map, mwidth, mheight)

    def hortosis(map, width, height, width_3, pos, dis=1, lr=0):

        # print('hortosis')
        # print_map(map, width, height)
        # print(width, height, width_3)
        # print(pos, dis)

        # left
        if lr == 0:



            for d in range(dis):
                town = map[pos[1] * width_3:pos[1] * width_3 + width * 3]
                town_a = len(town)
                # print()
                # print(d)
                c = int((dis - d) / dis) * width_3
                # print(c)
                cord = (pos[0] + pos[1] * width + d - int(dis / 2)) * 3
                cord_0 = (pos[0]  + d - int(dis / 2)) * 3
                # print(cord)
                hood = (map[cord - 3 + c], map[cord - 2 + c], map[cord - 1 + c],
                        map[cord], map[cord + 1], map[cord + 2],
                        map[(cord + 3) % map_a], map[(cord + 4) % map_a], map[(cord + 5) % map_a])

                hood_0 = (town[cord_0 - 3 + c], town[cord_0 - 3 + c], town[cord_0 - 3 + c],
                          town[cord_0], town[cord_0 + 1], town[cord_0 + 2],
                          town[(cord_0 + 3) % town_a], town[(cord_0 + 4) % town_a], town[(cord_0 + 5) % town_a])
                # print(hood)
                house = rule_d[hood_0]
                # print(house)

                # print()
                # print(d)
                # print(int((dis-d)/dis))
                # print(pos)
                # print(cord)
                # print(cord_0)
                # print(town)
                # print(hood)
                # print(hood_0)
                # print(house)

                for x in range(int(height / 2)):
                    x = int(height / 2) - x - 1
                    # print("")
                    # print(x)
                    # print(cord)
                    # print(cord-(x+1)*width_3)
                    # print(map[cord-(x+1)*width_3:cord-(x+1)*width_3+3])
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

        # right
        if lr == 1:

            for d in range(dis):
                d = dis - d - 1
                cord = (pos[0] + pos[1] * width + d - int(dis / 2)) * 3
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

        # in
        if lr == 2:

            for d in range(int(dis / 2)):
                # left
                d = d
                cord = (pos[0] + pos[1] * width + d - int(dis / 2)) * 3
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

                # right
                d = dis - d - 1
                cord = (pos[0] + pos[1] * width + d - int(dis / 2)) * 3
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

            # center
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

        # out
        if lr == 3:

            for d in range(int(dis / 2)):
                # left
                d = d
                cord = (pos[0] + pos[1] * width + d + 1) * 3
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

                # right
                d = dis - d - 1
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

            # center
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

        # print_map(map, width, height)

        return map

    pos = (int(mwidth / 2), int(mwidth / 2))



    def vertosis(map, width, height, width_3, pos, dis=1, du=0):

        # print("")
        # print('vertosis')

        # down
        if du == 0:

            for d in range(dis):
                d = d
                cord = (pos[0] + pos[1] * width + d * width - int(dis / 2) * width) * 3 % map_a
                hood = (map[cord - width_3], map[cord - width_3 + 1], map[cord - width_3 + 2],
                        map[cord], map[cord + 1], map[cord + 2],
                        map[(cord + width_3) % map_a], map[(cord + 1 + width_3) % map_a],
                        map[(cord + 2 + width_3) % map_a])
                house = rule_d[hood]

                # print()
                # print(d)
                # print(cord)
                # print(hood)
                # print(house)

                for x in range(int(width / 2)):
                    x = int(width / 2) - x - 1
                    # print("")
                    # print(x)
                    # print(cord)
                    # print(cord-(x+1)*width_3)
                    # print(map[cord-(x+1)*width_3:cord-(x+1)*width_3+3])
                    map[cord - (x + 1) * 3:cord - (x + 1) * 3 + 3] = map[cord - (x) * 3:cord - (x) * 3 + 3]
                    map[cord + (x + 1) * 3:cord + (x + 1) * 3 + 3] = map[cord + (x) * 3:cord + (x) * 3 + 3]

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

        return map

    pos_m = (int(mwidth / 2), int(mheight / 2))

    map_w = [255 for n in range(mheight * mwidth * 3)]
    # hv maps
    map_h = [0 for n in range(mheight * mwidth * 3)]
    map_h[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3] = value_color[1][0]
    map_h[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3 + 1] = value_color[1][1]
    map_h[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3 + 2] = value_color[1][2]

    map_v = [0 for n in range(mheight * mwidth * 3)]
    map_v[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3] = value_color[1][0]
    map_v[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3 + 1] = value_color[1][1]
    map_v[(int(mwidth / 2) + int(mheight / 2) * mwidth) * 3 + 2] = value_color[1][2]


    print()
    print("h, v")
    # print_map(map_h, mwidth, mheight)
    # print_map(map_v, mwidth, mheight)
    print("round 1")
    hortosis(map_h, mwidth, mheight, mwidth_3, pos_m, dis)
    vertosis(map_v, mwidth, mheight, mwidth_3, pos_m, dis)
    print_map(map_h, mwidth, mheight)
    print('round 2')
    hortosis(map_h, mwidth, mheight, mwidth_3, pos_m, dis)
    vertosis(map_v, mwidth, mheight, mwidth_3, pos_m, dis)
    print_map(map_h, mwidth, mheight)
    print('round 3')
    hortosis(map_h, mwidth, mheight, mwidth_3, pos_m, dis)
    vertosis(map_v, mwidth, mheight, mwidth_3, pos_m, dis)
    print_map(map_h, mwidth, mheight)


    #block
    height = HEIGHT
    width = WIDTH + 1
    width_3 = width*3
    height_3 = height*3
    block_a = width_3 * height
    block = np.zeros((height, width, 3), dtype='uint8')

    def graph(block, map, mwidth_3, mwidth, mheight, pos):
        # print(graph)

        for x in range(mheight):
            for y in range(mwidth):
                block[(x+pos[1])%height, (y + pos[0])%width] = map[x*mwidth_3 + (y*3):x*mwidth_3 + (y*3)+3]

        return block

    def cut(block, mwidth_3, mwidth, mheight, pos, dis):

        map_c = []
        pos_h = (int(mwidth/2), int(mheight/2))

        for x in range(mheight):
            for y in range(mwidth):
                map_c.append(block[(x + pos[1]) % height, (y + pos[0]) % width][0])
                map_c.append(block[(x + pos[1]) % height, (y + pos[0]) % width][1])
                map_c.append(block[(x + pos[1]) % height, (y + pos[0]) % width][2])

        map_c[pos_h[1]*mwidth_3 + pos_h[0]*3] = shade
        map_c[pos_h[1] * mwidth_3 + pos_h[0]*3+1] = shade
        map_c[pos_h[1] * mwidth_3 + pos_h[0]*3+2] = shade

        print_map(map_c, mwidth, mheight)

        map_g = hortosis(map_c, mwidth, mheight, mwidth_3, pos_h, dis)

        print_map(map_g, mwidth, mheight)

        for x in range(mheight):
            for y in range(mwidth):
                block[(x + pos[1]) % height, (y + pos[0]) % width] = map_g[x * mwidth_3 + (y * 3):x * mwidth_3 + (y * 3) + 3]

        return block

    # pos = (int(width/2), int(height/2))
    # block = graph(block, map_h, mwidth_3, mwidth, mheight, pos)

    def slice(block, pos, slope,depth):
        print('slice')

        for x in range(3, depth):

            pos = (pos[0] + slope[0]*int(x/2), pos[1]+slope[1]*int(x/2))

            block = cut(block, x*3, x, x, pos, x)

        return block


    def rule_gen(rule_d, rule, base, view, new=0):
        for x in range(bv):
            e = rule//base
            q = rule%base
            key = []

            if new == 0:
                for y in range(view):
                    r = x//base
                    w = x%base
                    key += value_color[w]
                    x = r
            else:
                key = list(rule_d.keys())[x]

            rule = e
            rule_d[tuple(key)] = value_color[q]

        return rule_d

    def _print_device_info():
        for i in range(pygame.midi.get_count()):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r

            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"

            print(
                "%2i: interface :%s:, name :%s:, opened :%s:  %s"
                % (i, interf, name, opened, in_out)
            )

    def input_main(device_id=None):

        pygame.init()
        pygame.fastevent.init()
        event_get = pygame.fastevent.get
        event_post = pygame.fastevent.post

        # rtmidi init
        # midiout = rtmidi.MidiOut()
        # available_ports = midiout.get_port_name(1)
        # print(" ")
        # print("midiout")
        # print(midiout)
        # print("available ports")
        # print(available_ports)
        #
        # if available_ports:
        #     midiout.open_port(1)
        # else:
        #     midiout.open_virtual_port('My virtual output')

        pygame.midi.init()

        print(" ")
        print("device info")
        _print_device_info()

        if device_id is None:
            input_id = pygame.midi.get_default_input_id()
        else:
            input_id = device_id

        print(' ')
        print("using input_id :%s:" % input_id)
        i = pygame.midi.Input(input_id)

        # print('i')
        # print(i)
        #
        # print(" ")
        # print("device info")
        # _print_device_info()

        pygame.display.set_mode((1, 1))
        going = True

        while going:
            events = event_get()
            for e in events:

                # print(" ")
                # print('e')
                # print(e)
                # print(type(e))

                if e.type in [pygame.QUIT]:
                    going = False
                if e.type in [pygame.KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN]:

                    # print(e)

                    clean_e = str(e)[21:-3]
                    list_e = clean_e.split(',')
                    ev = []
                    for l in list_e:
                        ev.append(int(l.split(':')[1]))

                    # print(" ")
                    # print("ev")
                    # print(ev)
                    # print(e)

                    # if ev[0] == 144:
                    #     midiout.send_noteon(ev[0], ev[1], ev[2])
                    # elif ev[0] == 128:
                    #     midiout.send_noteoff(ev[0], ev[1])

            if i.poll():

                # print(' ')
                # print('i')
                # print(i)

                midi_events = i.read(10)
                midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

                for m_e in midi_evs:
                    event_post(m_e)

        del i
        pygame.midi.quit()




    #input augments
    midi_inputs = 1
    gloves = 1
    number_of_sensors = 12
    device_id = 1

    if midi_inputs == 1:

        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()
        event_post = pygame.fastevent.post

        #rtmidi init
        if device_id >= 0:

            print(" ")
            print("device info")
            _print_device_info()

            input_id = device_id
            print("input_id")
            print(input_id)

            print(' ')
            print("using input_id :%s:" % input_id)
            pygame.midi.get_device_info(input_id)
            p_m_i = pygame.midi.Input(device_id)

        glove_values = [x for x in range(gloves * number_of_sensors)]

        print("")
        print("glove_values")
        print(glove_values)


        if device_id > 0:

            if midi_inputs == 1:

                if p_m_i.poll():

                    # print(' ')
                    # print('i')
                    # print(i)

                    midi_events = p_m_i.read(999)
                    midi_evs = pygame.midi.midis2events(midi_events, p_m_i.device_id)

                    for m_e in midi_evs:
                        event_post(m_e)



    while run == 1:

        mx, my = pygame.mouse.get_pos()

        WIN.fill((0, 0, 0))


        rule += 1
        rule = rule%bbv
        rule_d = rule_gen(rule_d, rule, base, view)


        # pos_h = (int(width/2), int(height/2))
        # cut_s = 51
        # block = cut(block, cut_s*3, cut_s, cut_s, pos_h, cut_s)

        pos_h = (int(width/4), int(height/4))
        cut_s = 31
        slope = (1, 1)
        block = slice(block, pos_h, slope, cut_s)


        WIN.blit(pygame.surfarray.make_surface(
            np.rot90(np.reshape(block, (height, width, 3)), 1, (1, 0))), (0, 0))




        pygame.display.update()

        #inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            #midi
            elif event.type in [pygame.midi.MIDIIN]:

                # print(event)

                clean_e = str(event)[21:-3]
                # print(clean_e)
                list_e = clean_e.split(',')
                ev = []
                # print(list_e)

                for l in list_e:

                    ev.append(int(l.split(':')[1]))


                if ev[0] == 176:
                    # print('right')
                    # print(ev)
                    glove_values[ev[1]] = ev[2]

                if ev[0] == 177:
                    # print('left')
                    # print(ev)
                    glove_values[ev[1] + number_of_sensors] = ev[2]


            #keyboard
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = 2

                if event.key == pygame.K_UP:
                    rule += 1
                    rule_d = rule_gen(rule_d, rule, base, view, 1)
                if event.key == pygame.K_DOWN:
                    rule -= 1
                    rule_d = rule_gen(rule_d, rule, base, view, 1)

                if event.key == pygame.K_F1:
                    block = np.zeros((height * width * 3), dtype='uint8')
                    block[int(width / 2 * 3) - 1] = value_color[1][0]
                    block[int(width / 2 * 3)] = value_color[1][1]
                    block[int(width / 2 * 3) + 1] = value_color[1][2]


        #midi clean up
        if device_id > 0:

            if midi_inputs == 1:

                if p_m_i.poll():

                    # print(' ')
                    # print('i')
                    # print(i)

                    midi_events = p_m_i.read(1024)
                    midi_evs = pygame.midi.midis2events(midi_events, p_m_i.device_id)

                    for m_e in midi_evs:
                        event_post(m_e)




Chaos_Window()