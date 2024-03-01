import numpy as np
import pygame
import pygame.midi

#####game#####

pygame.init()
pygame.display.init()
current_display = pygame.display.Info()
WIDTH, HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

width_2 = int(WIDTH / 2)
width_3 = int(WIDTH / 3)
width_4 = int(WIDTH / 4)
width_8 = int(WIDTH / 8)
width_16 = int(WIDTH / 16)
width_32 = int(WIDTH / 32)
width_64 = int(WIDTH / 64)
width_128 = int(WIDTH / 128)
width_256 = int(WIDTH / 256)
width_512 = int(WIDTH / 512)

height_2 = int(HEIGHT / 2)
height_4 = int(HEIGHT / 4)
height_8 = int(HEIGHT / 8)
height_16 = int(HEIGHT / 16)
height_32 = int(HEIGHT / 32)
height_64 = int(HEIGHT / 64)
height_128 = int(HEIGHT / 128)
height_256 = int(HEIGHT / 256)
height_512 = int(HEIGHT / 512)

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)

def Chaos_Window():

    print(HEIGHT, WIDTH)

    #basic
    run = 1
    rule = 90
    base = 8
    view = 3
    bv = base ** view
    bbv = base ** base ** view
    mandala = 1

    #glove mappings
    lr_map = 0
    ud_map = 1
    color_map = 2
    brush_size = 7
    paint_speed = 6
    tide_map = 11



    path = [(0, 0), (0, 0), (0, 0), (0, 0)]
    g_mem = [0, 0, 0, 0]
    g_scale = 7
    direction = [0, 0, 0, 0]

    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255), 6:(255, 0, 255), 7:(255, 255, 255)}

    rule_d = {}
    rule_d2 = {}

    #block
    height = HEIGHT
    width = WIDTH + 1
    width_3 = width*3
    height_3 = height*3
    block_a = width_3 * height
    block = np.zeros((height*width*3), dtype='uint8')
    block[int(width/2*3)-1] = value_color[1][0]
    block[int(width/2*3)] = value_color[1][1]
    block[int(width/2*3)+1] = value_color[1][2]

    #tile
    tile_h = int(HEIGHT/127)*3
    tile_w = int(WIDTH/127)*3
    tile_w3 = tile_w*3
    tile_a = tile_w*tile_h*3
    tile = np.zeros((tile_h*tile_w*3), dtype='uint8')
    tile[int(tile_w/2*3)-1] = value_color[1][0]
    tile[int(tile_w/2*3)] = value_color[1][1]
    tile[int(tile_w/2*3)+1] = value_color[1][2]

    # mountosis
    mheight = 31
    mwidth = mheight
    mwidth_3 = mwidth * 3
    mheight_3 = mheight * 3
    mount_a = mwidth_3 * mheight
    mount = np.zeros((mheight * mwidth * 3), dtype='uint8')
    mount[int(mwidth / 2 * 3) - 1] = 255
    mount[int(mwidth / 2 * 3)] = 255
    mount[int(mwidth / 2 * 3) + 1] = 255

    slope = {'slope':0, 0:{}, 1:{}, 2:{}, 3:{}}
    print(slope)
    for x in range(mwidth):
        for y in range(mheight):
            slope[0][(x, y)] = (x, y)
            slope[1][(x, y)] = (mheight - 1 - x, y)
            slope[2][(x, y)] = (y, mheight - 1 - x)
            slope[3][(x, y)] = (mwidth - 1 - y, x)



    #step
    step_h = int(HEIGHT/127)
    step_w = int(WIDTH/127)
    step_w3 = step_w*3
    step_a = step_w*step_h*3


    heat_depth = 1
    tide = 0

    def draw_text(text, font, color_dt, surface, x, y):
        textobj = font.render(text, 1, color_dt)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


    def print_3d(array, h, w):
        for x in range(int(h/3)):
            print(array[x*w:x*w+w])
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
    def mitosis(block, rule_d, width, width_3):
        block = np.roll(block, width_3)

        for x in range(width):
            x3 = x*3
            hood = tuple(block[width_3-3+x3:width_3+6+x3])
            dojo = rule_d[hood]

            block[0+x3] = dojo[0]
            block[1+x3] = dojo[1]
            block[2+x3] = dojo[2]

        return block
    def tiletosis(block, tile, rule_d, tile_w, tile_w3, tile_h, path, direction):

        if direction[0] == 0:
            p_0 = path[0] * step_w3 - int(step_w / 2) * 3
            p_1 = path[1] * width_3 * step_h
            p_ = p_0 + p_1

            # block to tile
            for x in range(tile_h):
                try:
                    tile[x * tile_w3:x * tile_w3 + tile_w3] = block[p_ + x * width_3:p_ + x * width_3 + tile_w3]
                except:
                    continue

            tile[int(tile_w / 2 * 3) - 1] = value_color[1][1]
            tile[int(tile_w / 2 * 3)] = value_color[1][2]
            tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

            # tile mitosis
            tile = mitosis(tile, rule_d, tile_w, tile_w3)

            # tile to block
            for x in range(tile_h):
                try:
                    block[p_ + x * width_3:p_ + x * width_3 + tile_w3] = tile[x * tile_w3:x * tile_w3 + tile_w3]
                except:
                    continue

            # mirror
            p_ = p_ - (tile_h * width_3)

            # block to tile
            for x in range(tile_h):
                try:
                    tile[tile_a - (x + 1) * tile_w3:tile_a - (x + 1) * tile_w3 + tile_w3] = block[
                                                                                            p_ + x * width_3:p_ + x * width_3 + tile_w3]
                except:
                    continue

            tile[int(tile_w / 2 * 3) - 1] = value_color[1][0]
            tile[int(tile_w / 2 * 3)] = value_color[1][1]
            tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

            # tile mitosis
            tile = mitosis(tile, rule_d, tile_w, tile_w3)

            # tile to block
            for x in range(tile_h):
                try:
                    block[p_ + x * width_3:p_ + x * width_3 + tile_w3] = tile[tile_a - (x + 1) * tile_w3:tile_a - (
                                x + 1) * tile_w3 + tile_w3]
                except:
                    continue

        if direction[0] == 1:
            p_0 = path[0] * step_w3 + int(tile_w/2)*3
            p_1 = path[1] * width_3 * step_h - width_3 * int(tile_h/2+1)
            p_ = p_0 + p_1

            # block to tile
            for x in range(tile_h):
                for y in range(tile_w):
                    try:
                        tile[x * tile_w3 + y * 3:x * tile_w3 + y * 3 + 3] = block[
                                                                            p_ + y * width_3 + x * 3:p_ + y * width_3 + x * 3 + 3]
                    except:
                        continue

            tile[int(tile_w / 2 * 3) - 1] = value_color[1][0]
            tile[int(tile_w / 2 * 3)] = value_color[1][1]
            tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

            # tile mitosis
            tile = mitosis(tile, rule_d, tile_w, tile_w3)

            # tile to block
            for x in range(tile_h):
                for y in range(tile_w):
                    try:
                        block[p_ + y * width_3 + x * 3:p_ + y * width_3 + x * 3 + 3] = tile[
                                                                                       x * tile_w3 + y * 3:x * tile_w3 + y * 3 + 3]
                    except:
                        continue

            # mirror
            p_ = p_ - int(tile_w)*3

            # block to tile
            for x in range(tile_h):
                for y in range(tile_w):
                    try:
                        tile[(tile_h - x - 1) * tile_w3 + y * 3:(tile_h - x - 1) * tile_w3 + y * 3 + 3] = block[
                                                                                                          p_ + y * width_3 + x * 3:p_ + y * width_3 + x * 3 + 3]
                    except:
                        continue

            tile[int(tile_w / 2 * 3) - 1] = value_color[1][0]
            tile[int(tile_w / 2 * 3)] = value_color[1][1]
            tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

            # tile mitosis
            tile = mitosis(tile, rule_d, tile_w, tile_w3)

            # tile to block
            for x in range(tile_h):
                for y in range(tile_w):
                    try:
                        block[p_ + y * width_3 + x * 3:p_ + y * width_3 + x * 3 + 3] = tile[(
                                                                                                        tile_h - x - 1) * tile_w3 + y * 3:(
                                                                                                                                                      tile_h - x - 1) * tile_w3 + y * 3 + 3]
                    except:
                        continue

        return block, tile

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


    rule_d = rule_gen(rule_d, rule, base, view)
    rule_d2 = rule_gen(rule_d2, rule, base, view)


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


    #########construction#########

    def mitosis(block, rule_d, width, width_3):
        block = np.roll(block, width_3)

        for x in range(width):
            x3 = x*3
            hood = tuple(block[width_3-3+x3:width_3+6+x3])
            dojo = rule_d[hood]

            block[0+x3] = dojo[0]
            block[1+x3] = dojo[1]
            block[2+x3] = dojo[2]

        return block

    def ridge(kaldera, magma, rule_d, width):

        for x in range(width):
            kaldera = np.roll(kaldera, 3)
            magma[:3] = rule_d[tuple(kaldera[:3 * view])]
            magma = np.roll(magma, 3)

        return magma

    def trek(mount, rule_d, width, width_3):

        kaldera = mount[:width_3]
        magma = np.zeros((width_3), dtype='uint8')
        magma = ridge(kaldera, magma, rule_d, width)
        mount = np.roll(mount, width_3)
        mount[:width_3] = magma

        return mount

    def carve(block, mount, path, rule_d, mheight, mwidth, mwidth_3, slope):


        for x in range(mheight):

            block[1000000 * 3 + x * width_3:1000000 * 3 + mwidth_3 + x * width_3] = mount[x * mwidth_3:x * mwidth_3 + mwidth_3]


            # for y in range(mwidth):
            #     xs, ys = slope[0][x, y]
            #     # print(xs, ys)
            #
            #     alt = xs * mwidth_3 + ys
            #     hood = 1000000 * 3 + xs * width_3 + ys
            #     mount[alt] = block[hood]


            block[100000 * 3 + x * width_3:100000 * 3 + mwidth_3 + x * width_3] = mount[x * mwidth_3:x * mwidth_3 + mwidth_3]


        mount = trek(mount, rule_d, mwidth, mwidth_3)



        return block, mount



    block, mount = carve(block, mount, path, rule_d, mheight, mwidth, mwidth_3, slope)



    # print()
    # print("mount")
    # print(mount)
    # print(rule_d)
    # mount = mitosis(mount, rule_d, mwidth, mwidth_3)
    # print(mount)


    while run == 1:

        mx, my = pygame.mouse.get_pos()

        WIN.fill((0, 0, 0))

        # block, mount = carve(block, mount, path, rule_d, mheight, mwidth, mwidth_3, slope)


        WIN.blit(pygame.surfarray.make_surface(
            np.rot90(np.reshape(block, (height, width, 3)), 1, (1, 0))), (0, 0))

        x = int(WIDTH / 2) - 500
        y = 20
        color_button = pygame.Rect(x + 245, y-2, 510, 24)
        pygame.draw.rect(WIN, value_color[7-mandala], color_button)
        color_button = pygame.Rect(x + 250, y, 500, 20)
        pygame.draw.rect(WIN, value_color[int(glove_values[color_map] / (127 / base) % base)], color_button)

        if color_button.collidepoint((mx, my)):
            if click:
                mandala += 1
                mandala = mandala%2

        # x = WIDTH - width_8 - width_32
        # y = height_4 + height_8
        # integrate_button = pygame.Rect(x, y, width_8 - width_64, height_16)
        # pygame.draw.rect(WIN, value_color[3], integrate_button)
        # integrate_button = pygame.Rect(x + 2, y + 2, width_8 - width_64 - 4, height_16 - 4)
        # pygame.draw.rect(WIN, value_color[0], integrate_button)
        # if integrate_button.collidepoint((mx, my)):
        #     record_t = main_font.render('integrate: ' + str(integrate), True, value_color[7])
        #     WIN.blit(record_t, (x + width_128, y + height_128))
        #     if click:
        #         integrate = (integrate + 1) % 2
        #         click = False


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

                if event.key == pygame.K_m:
                    mandala += 1
                    mandala = mandala%2

        #mitosis
        if gloves > 0:
            # color
            x = int(WIDTH / 2) - 250
            y = 20
            color_button = pygame.Rect(x + 250, y, 500, 10)
            pygame.draw.rect(WIN, value_color[int(glove_values[color_map] / (127 / base) % base)], color_button)


            size_r = brush_size

            if int(glove_values[size_r]/g_scale+1) != g_mem[0]:
                g_mem[0] = int(glove_values[size_r]/g_scale+1)
                tile_h = int(glove_values[size_r]/g_scale+1) * 3
                tile_w = int(glove_values[size_r]/g_scale+1) * 3
                tile_w3 = tile_w * 3
                tile_a = tile_w * tile_h * 3
                tile = np.zeros((tile_h * tile_w * 3), dtype='uint8')
                tile[int(tile_w / 2 * 3) - 1] = value_color[1][0]
                tile[int(tile_w / 2 * 3)] = value_color[1][1]
                tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

            path[1] = path[0]
            path[0] = (glove_values[lr_map], glove_values[ud_map])

            if path[0][0] != path[1][0]:
                direction[0] = 0
            if path[0][1] != path[1][1]:
                direction[0] = 1
            direction[1] = direction[0]

            block, tile = tiletosis(block, tile, rule_d, tile_w, tile_w3, tile_h, path[0], direction)

            if mandala == 1:
                mandala_path = [127-path[0][0], 127-path[0][1]]
                block, tile = tiletosis(block, tile, rule_d, tile_w, tile_w3, tile_h, mandala_path, direction)

            if gloves > 1:
                size_l = brush_size + 12

                color_button = pygame.Rect(x - 250, y, 500, 10)
                pygame.draw.rect(WIN, value_color[int(glove_values[color_map + 12] / (127 / base) % base)], color_button)

                if int(glove_values[size_l] / g_scale + 1) != g_mem[2]:
                    g_mem[2] = int(glove_values[size_l] / g_scale + 1)
                    tile_h = int(glove_values[size_l] / g_scale + 1) * 3
                    tile_w = int(glove_values[size_l] / g_scale + 1) * 3
                    tile_w3 = tile_w * 3
                    tile_a = tile_w * tile_h * 3
                    tile = np.zeros((tile_h * tile_w * 3), dtype='uint8')
                    tile[int(tile_w / 2 * 3) - 1] = value_color[1][0]
                    tile[int(tile_w / 2 * 3)] = value_color[1][1]
                    tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

                path[3] = path[2]
                path[2] = (glove_values[lr_map], glove_values[ud_map])

                if path[2][0] != path[3][0]:
                    direction[2] = 0
                if path[2][1] != path[3][1]:
                    direction[2] = 1
                direction[3] = direction[2]

                block, tile = tiletosis(block, tile, rule_d2, tile_w, tile_w3, tile_h, path[2], direction)

                if mandala == 1:
                    mandala_path = [127 - path[1][0], 127 - path[1][1]]
                    block, tile = tiletosis(block, tile, rule_d, tile_w, tile_w3, tile_h, mandala_path, direction)

            #rulings
            if heat_depth == 1:
                ts = 7
                # print("")
                # print(glove_values[0]*glove_values[1]%bv)
                # print(int(glove_values[2]/(127/base)%base))
                for x in range(int(glove_values[paint_speed]/ts + 1)):
                    tide += int(glove_values[tide_map])

                    depth_r = int(glove_values[color_map]/(127/base)%base)
                    if depth_r == 8:
                        depth_r = tide%8

                    rule_d[list(rule_d.keys())[(glove_values[lr_map] * glove_values[ud_map] + (tide * x)) % bv]] = value_color[depth_r]



                if gloves > 1:
                    for x in range(int(glove_values[paint_speed + 12]/ts + 1)):
                        tide += int(glove_values[tide_map + 12])

                        depth_l = int(glove_values[color_map + 12] / (127 / base) % base)
                        if depth_l == 8:
                            depth_l = tide%8

                        rule_d2[list(rule_d2.keys())[(glove_values[lr_map] * glove_values[ud_map] + (tide * x)) % bv]] = \
                        value_color[depth_l]



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



