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

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)

def Chaos_Window():

    print(HEIGHT, WIDTH)

    run = 1
    rule = 21621
    base = 8
    view = 3
    bv = base ** view
    bbv = base ** base ** view


    path = [(0, 0), (0, 0)]
    g_mem = [0, 0]
    g_scale = 4
    direction = [0, 0]

    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255), 6:(255, 0, 255), 7:(255, 255, 255)}

    rule_d = {}

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

        WIN.blit(pygame.surfarray.make_surface(
            np.rot90(np.reshape(block, (height, width, 3)), 1, (1, 0))), (0, 0))

        #color
        x = int(WIDTH/2) - 250
        y = 20
        color_button = pygame.Rect(x, y, 500, 10)
        pygame.draw.rect(WIN, value_color[int(glove_values[2] / (127 / base) % base)], color_button)


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

        #mitosis
        if gloves > 0:

            if glove_values[5]>8:
                if int(glove_values[5]/g_scale+1) != g_mem[0]:
                    g_mem[0] = int(glove_values[5]/g_scale+1)
                    tile_h = int(glove_values[5]/g_scale+1) * 3
                    tile_w = int(glove_values[5]/g_scale+1) * 3
                    tile_w3 = tile_w * 3
                    tile_a = tile_w * tile_h * 3
                    tile = np.zeros((tile_h * tile_w * 3), dtype='uint8')
                    tile[int(tile_w / 2 * 3) - 1] = value_color[1][0]
                    tile[int(tile_w / 2 * 3)] = value_color[1][1]
                    tile[int(tile_w / 2 * 3) + 1] = value_color[1][2]

                path[1] = path[0]
                path[0] = (glove_values[0], glove_values[1])

                if path[0][0] != path[1][0]:
                    direction[0] = 0
                if path[0][1] != path[1][1]:
                    direction[0] = 1
                direction[1] = direction[0]

                block, tile = tiletosis(block, tile, rule_d, tile_w, tile_w3, tile_h, path[0], direction)



            # block = mitosis(block, rule_d, width, width_3)

        #rulings
        if heat_depth == 1:
            # print("")
            # print(glove_values[0]*glove_values[1]%bv)
            # print(int(glove_values[2]/(127/base)%base))
            tide += int(glove_values[11])
            rule_d[list(rule_d.keys())[(glove_values[0]*glove_values[1]+tide)%bv]] = value_color[int(glove_values[2]/(127/base)%base)]


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