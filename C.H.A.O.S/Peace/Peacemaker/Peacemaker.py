# C.H.A.O.S



import sys
import time
import pygame
import pygame.midi
import numpy as np
from pygame import mixer
from collections import deque
from datetime import datetime


sys.setrecursionlimit(999999999)
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

view = 3
# size of the view window that scans a row for rule application

def base_x(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)

def decimal(n, b):

    n = list(reversed(n))
    n = [int(v) for v in n]

    value = 0
    place = 0


    for c in n:

        value += int(c) * b ** place
        place += 1

    return value

def rule_gen(rule, base=2):

    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(int(rule), (base))

    x = int_rule[::-1]

    while len(x) < base ** view:
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

    return rules, int_rule[:base ** view]

def viewer_1d(row, y, view, v_0, color_value):

    # print('view')
    # print(view)
    # print("v_0_v")
    # print(v_0)
    # print(len(v_0))

    if len(v_0) % 2 == 1:

        if y + len(v_0) > len(row) - 1:

            v_0.append('0')

        else:

            v_0.append(str(color_value[tuple(row[y + int(len(v_0) / 2) + 1])]))



    else:

        if y - len(v_0) < -1:

            v_0.insert(0, '0')

        else:

            v_0.insert(0, str(color_value[tuple(row[int(y - len(v_0) / 2)])]))


    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer_1d(row, y, view, v_0, color_value)

        return v_0



#####game#####

pygame.init()
pygame.display.init()

current_display = pygame.display.Info()
WIDTH, HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption("C.H.A.O.S")

click = False


def Chaos_Window(base, device_id=-1):

    print("base")
    print(base)
    print("device_id")
    print(device_id)
    p_m_i = 0
    mixer.init()

    #colors
    color_0 = (0, 0, 0)
    color_1 = (64, 64, 64)
    color_2 = (255, 0, 255)
    color_3 = (0, 255, 255)
    color_4 = (255, 255, 0)
    color_5 = (255, 255, 255)
    color_6 = (255, 0, 0)
    color_7 = (0, 255, 0)
    color_8 = (0, 0, 255)
    if base < 5:

        value_color = {0:color_0, 1:color_1, 2:color_2, 3:color_3}
        color_value = {v:k for k, v in value_color.items()}
    else:

        value_color = {0:color_0, 1:color_1, 2:color_2, 3:color_3, 4:color_4, 5:color_5,
                      6:color_6, 7:color_7, 8:color_8}
        color_value = {v:k for k, v in value_color.items()}

    #dicts
    letter_values = {' ': 0, 'a': 1, 'i': 2, 't': 3,
                     's': 4, 'c': 5, 'd': 6, 'm': 7,
                     'g': 8, 'f': 9, 'w': 10, 'v': 11,
                     'z': 12, 'q': 13, ',': 14, '"': 15,
                     '/': 16, '.': 17, ';': 18, 'j': 19,
                     'x': 20, 'k': 21, 'y': 22, 'b': 23,
                     'h': 24, 'p': 25, 'u': 26, 'l': 27,
                     'n': 28, 'o': 29, 'r': 30, 'e': 31}
    value_letter = {v: k for k, v in letter_values.items()}
    metabet_6 = {0: ' ', 1: 't', 2: 'o', 3: 'n', 4: 'h', 5: 'd', 6: 'u', 7: 'm', 8: 'w', 9: 'y', 10: 'b', 11: 'k',
                 12: 'j', 13: 'z', 14: ",",
                 15: 'th', 16: 'in', 17: 'an', 18: 'nd', 19: 'en', 20: 'ou', 21: 'ha', 22: 'or', 23: 'is', 24: 'es',
                 25: 'the', 26: 'ing',
                 27: 'hat', 28: 'tha', 29: 'for', 30: 'ion', 31: 'was', 32: 'you', 33: 'ter', 34: 'ent', 35: 'ere',
                 36: 'his', 37: 'her',
                 38: 'and', 39: 'ng', 40: 'hi', 41: 'it', 42: 'to', 43: 'ed', 44: 'at', 45: 'on', 46: 're', 47: 'er',
                 48: 'he', 49: "'",
                 50: '.', 51: 'q', 52: 'x', 53: 'v', 54: 'p', 55: 'g', 56: 'f', 57: 'c', 58: 'l', 59: 'r', 60: 's',
                 61: 'i', 62: 'a', 63: 'e'}
    r_dict = {0:0, 1:1, 2:1, 3:1}
    p_dict = {0:0, 1:0, 2:0, 3:2}
    tone = {0:'in_', 1:'qr_', 2:'aw_'}
    scale_lable = {0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'}

    def redraw_window():

        #preparation


        #cell drawing
        WIN.blit(pygame.surfarray.make_surface(np.moveaxis(canvas, 0, 1)), (0, 0))


        #ui drawing
        if ui_on > 0:

            #palettese
            for y in range(27):
                for x in range(27):
                    bar = pygame.Rect(WIDTH-27*6 + x * 3, 800 + y * 3, 3, 3)
                    pygame.draw.rect(WIN, value_color[i_rule_0[x + 27 * y]], bar)

            for y in range(27):
                    for x in range(27):
                        bar = pygame.Rect(27*3 + x * 3, 800 + y * 3, 3, 3)
                        pygame.draw.rect(WIN, value_color[i_rule_1[x + 27 * y]], bar)


            if g_brush == 1:
                for x in range(len(midi_weights_0)):

                        bar = pygame.Rect(int(WIDTH) + bar_width * x - bar_width * len(midi_weights_0) - 4*bar_width,
                                          int(HEIGHT) - int(bar_height * ((midi_weights_0[x] / zero_out))),
                                          bar_width, int(bar_height * ((midi_weights_0[x] / zero_out))))
                        pygame.draw.rect(WIN, value_color[x], bar)

                for x in range(len(midi_weights_1)):

                        bar = pygame.Rect(bar_width * x + bar_width*4,
                                          int(HEIGHT) - int(bar_height * ((midi_weights_1[x] / zero_out))),
                                          bar_width, int(bar_height * ((midi_weights_1[x] / zero_out))))
                        pygame.draw.rect(WIN, value_color[x], bar)

        if pce > 0:


            draw_text(str(value_letter[right_letter]), TITLE_FONT, (10, 100, 10), WIN, WIDTH - 64, 0)
            draw_text(str(value_letter[left_letter]), TITLE_FONT, (10, 100, 10), WIN, 32, 0)
            draw_text(voice, text_font, (10, 100, 10), WIN, WIDTH/2, 40)
            draw_text(voice_l[0], text_font, (10, 100, 10), WIN, WIDTH/2 + WIDTH/4, 40)
            draw_text(voice_l[1], text_font, (10, 100, 10), WIN, WIDTH/4, 40)

            cross_0 = pygame.Rect((glove_values[0]*14), HEIGHT/2, int(glove_values[2]/64) * 160 + 7, glove_values[11] + 3)
            pygame.draw.rect(WIN, value_color[5], cross_0)
            cross_0 = pygame.Rect(WIDTH/2, HEIGHT - (glove_values[1]*7), glove_values[11] + 3, int(glove_values[2]/64) * 160 + 7)
            pygame.draw.rect(WIN, value_color[5], cross_0)

            cross_1 = pygame.Rect((glove_values[12] * 14), HEIGHT / 2, int(glove_values[14] / 64) * 160 + 7, glove_values[23] + 3)
            pygame.draw.rect(WIN, value_color[5], cross_1)
            cross_1 = pygame.Rect(WIDTH / 2, HEIGHT - (glove_values[13] * 7), glove_values[23] + 3, int(glove_values[14] / 64) * 160 + 7)
            pygame.draw.rect(WIN, value_color[5], cross_1)

            if pce == 1:
                draw_text(str((scale_lable[thumb%12], scale_lable[pointer%12], scale_lable[middle%12], scale_lable[ring%12], scale_lable[pinky%12])), small_font, (255, 255, 255), WIN, WIDTH / 2 - 120, HEIGHT - 50)
                draw_text(str(heat[:5]), small_font, (255, 255, 255), WIN,
                          WIDTH / 2 + WIDTH/4 - 60, HEIGHT - 50)
                draw_text(str(heat[5:]), small_font, (255, 255, 255), WIN,
                          WIDTH / 4 - 60, HEIGHT - 50)

                motion_0 = pygame.Rect(WIDTH / 2 + 16, HEIGHT / 2, 32, 32)
                pygame.draw.rect(WIN, value_color[mc_0%6], motion_0)
                motion_1 = pygame.Rect(WIDTH / 2 - 16, HEIGHT / 2, 32, 32)
                pygame.draw.rect(WIN, value_color[mc_1%6], motion_1)

            if pce == 2:
                draw_text(str((scale_lable[thumb%12], scale_lable[pointer%12], scale_lable[middle%12], scale_lable[ring%12], scale_lable[pinky%12])), small_font, (255, 255, 255), WIN, WIDTH / 2 - 120, HEIGHT - 50)
                draw_text(str(heat[:5]), small_font, (255, 255, 255), WIN,
                          WIDTH / 2 + WIDTH/4 - 60, HEIGHT - 50)
                draw_text(str(heat[5:]), small_font, (255, 255, 255), WIN,
                          WIDTH / 4 - 60, HEIGHT - 50)

                motion_0 = pygame.Rect(WIDTH / 2 + 16, HEIGHT / 2, 32, 32)
                pygame.draw.rect(WIN, value_color[mc_0%6], motion_0)
                motion_1 = pygame.Rect(WIDTH / 2 - 16, HEIGHT / 2, 32, 32)
                pygame.draw.rect(WIN, value_color[mc_1%6], motion_1)

        pygame.display.update()

        return cv_pos

    def drum_track(n, c):
        if n == 1:
            path = r'audio/hat/hat_0.mp3'
            mixer.music.load(path)
            pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))
        if n == 2:
            path = r'audio/clap/clap_0.mp3'
            mixer.music.load(path)
            pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))
        if n == 3:
            path = r'audio/kick/kick_0.mp3'
            mixer.music.load(path)
            pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))

    def loop_8(n, c, lvl = 0, v=0):

        n = n%60

        path = r'audio\loop_8\s' + str(tone[lvl%3]) + str(n) + '.mp3'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)
        w.set_volume(v)
        pygame.mixer.Channel(c).play(w)

        return w


    color_post = {0: 1, 1: 5, 2: 2, 3: 6, 4: 3, 5: 7, 6: 4, 7: 8, 8: 0}
    post_color = {v: k for k, v in color_post.items()}

    def glove(glove_values, invert=0):

        if invert == 1:
            for x in range(5):
                glove_values[x + 6] = 127 - glove_values[x+6]


        midi_colors = []
        new_rule = []

        midpoint = 64

        for x in range(4):

            if glove_values[7 + x] > midpoint:
                midi_colors.append(glove_values[7 + x] - 64)
            else:
                midi_colors.append(0)

            if glove_values[7 + x] < midpoint:
                midi_colors.append(64 - glove_values[7 + x])
            else:
                midi_colors.append(0)


        midi_colors.append(max(midi_colors))


        mc_total = sum(midi_colors)


        # print(len(i_rule_0))
        # print(midi_colors)
        # print(mc_total)

        for x in range(len(midi_colors)):
            midi_colors[x] = round(midi_colors[x]/mc_total, 2)


        midi_weights = midi_colors[::]

        sorted_weights = []
        for x in range(len(midi_weights)):

            sorted_weights.append(midi_weights[post_color[x]])

        # print(color_post)
        # print(sorted_weights)

        for x in range(len(sorted_weights)):


            sorted_weights[x] = int(sorted_weights[x] * 81)
            # print(sorted_weights)


            for y in range(sorted_weights[x]):
                new_rule.append(x)

        # print(sorted_weights)
        # print(len(new_rule))
        # print(new_rule)

        if len(new_rule) < 81:
            for x in range(81 - len(new_rule)):
                new_rule.append(0)

        # print(len(new_rule))
        # print(new_rule)

        paint_brush = []
        for x in range(len(new_rule)):
            # print(new_rule[x])
            for y in range(9):
                paint_brush.append(new_rule[x])

        # print(len(paint_brush))
        # print(paint_brush)

        for x in range(base):
            for y in range(27):
                if y%3 == 0:
                    paint_brush[x*81 + x*9 + x-81 + 3*y] = paint_brush[(x-3)*81 + (x-1)]
                elif y%3 == 1:
                    paint_brush[x*81 + x*9 + x-81 + 3*y] = paint_brush[(x-2)*81 + (x-1)]
                else:
                    paint_brush[x*81 + x*9 + x-81 + 3*y] = paint_brush[(x-1)*81 + (x-1)]


        return paint_brush, sorted_weights

    def erosion():
        for x in range(5):
            sand[x] += int(glove_values[6 + x] / 8) * int((glove_values[11]+glove_values[23]) / 4)
            sand[x + 5] += int(glove_values[18 + x] / 8) * int((glove_values[11]+glove_values[23]) / 4)
            if glove_values[6 + x] < 8:
                sand[x] = 0
                heat[x] = 0
            if glove_values[18 + x] < 8:
                sand[x + 5] = 0
                heat[x + 5] = 0


    #active variables
    run = 1
    rule = 30
    pause = 0
    step = 0
    wu = 0
    volume = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    bv = base ** view
    bbv = base ** base ** view
    t_0 = time.time()

    #eb
    eb = 0
    zero_r = np.zeros((1, WIDTH, 3), dtype='uint8')

    #input augments
    midi_inputs = 1
    gloves = 2
    right_letter = 0
    left_letter = 0
    voice = ' '
    voice_l = ['', '']
    v_time = []

    #Peace
    pce = 2
    drum = 0
    key = 0
    tempo = 1
    beat = 0
    speed = 8
    mc_0, mc_1 = 0, 0
    strike = [0, 0]

        #gloves
    sand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    heat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    echo = [[], []]
    me_0 = [0, 0]
    my_0 = [0, 0]
    thumb = 0
    pointer = 0
    middle = 0
    ring = 0
    pinky = 0

        #loops
    lp_0 = loop_8(0, 1)
    lp_1 = loop_8(12, 2)
    lp_2 = loop_8(16, 3)
    lp_3 = loop_8(19, 4)
    lp_4 = loop_8(24, 5)
    lp_5 = loop_8(12, 6)
    lp_6 = loop_8(24, 7)
    lp_7 = loop_8(28, 8)
    lp_8 = loop_8(31, 9)
    lp_9 = loop_8(36, 10)


    #input maps
    x_position_g0v = 0
    y_position_g0v = 1
    x_position_g1v = 12
    y_position_g1v = 13


    #streams
    streams = 1
    stream_buffer = 2

    stream_direction_0 = deque(maxlen=stream_buffer)
    stream_direction_0.append(0)
    stream_direction_1 = deque(maxlen=stream_buffer)
    stream_direction_1.append(0)

    momentum = {0:0, 1:0, 2:0, 3:0}

    last_x_0 = 0
    last_y_0 = 0

    last_x_1 = 0
    last_y_1 = 0

    #ui
    ui_on = 0
    ui_scale = 14
    bar_height = 15000
    bar_width = ui_scale + int(ui_scale / 1)
    cv_pos = 0

    midi_weights_0 = []
    midi_weights_1 = []

    #glove emthods
    g_brush = 1
    number_of_sensors = 12
    zero_out = 3200
    spin_speed = 8
    spin = 0

    #cell design
    canvas_rows = int(HEIGHT)
    canvas_row_width = int(WIDTH)

    brush_width = 100
    brush_height = 100
    brush_scale_h = int(canvas_rows / 127)
    brush_scale_w = int(canvas_row_width / 127)

    brush_min_0 = 14
    brush_min_1 = 14

    cell_row_width = brush_width
    cell_rows = brush_height

    d_rule_0, i_rule_0 = rule_gen(rule, base)
    d_rule_1, i_rule_1 = rule_gen(rule, base)

    print("")
    print("d_rule")
    print(d_rule_0, d_rule_1)

    print("")
    print('cells: width height')
    print((cell_row_width, cell_rows))

    canvas = np.zeros((canvas_rows, canvas_row_width, 3), dtype='uint8')
    cells_a = np.zeros((cell_rows, cell_row_width, 3), dtype='uint8')
    cells_b = np.zeros((cell_rows, cell_row_width, 3), dtype='uint8')

    cells_a[0, int(cell_row_width / 2)] = value_color[1]
    cells_b[0, int(cell_row_width / 2)] = value_color[1]


    for x in range(cell_rows - 1):

        cells_a = np.roll(cells_a, 1, 0)
        cells_b = np.roll(cells_b, 1, 0)

        for y in range(cell_row_width):

            cells_a[0, y] = value_color[d_rule_0[tuple(viewer_1d(cells_a[1], y, view, [], color_value))]]
            cells_a[0, y] = value_color[d_rule_1[tuple(viewer_1d(cells_b[1], y, view, [], color_value))]]

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

    print(" ")
    print("d_rule")
    print(d_rule_0, d_rule_1)
    print("i_rule")
    print(i_rule_0, i_rule_1)
    print(len(i_rule_0), len(i_rule_1))


    #main loop
    while run == 1:

        redraw_window()


        if pce == 1:

            #brush
            g1_size = 0
            g2_size = 0
            for x in range(5):
                g1_size += glove_values[6 + x]
                g2_size += glove_values[18 + x]

            brush_min_0 = int(g1_size/32) + 2
            brush_min_1 = int(g2_size/32) + 2

            #octant
            scale = 12
            my = int(glove_values[0]/64) + int((glove_values[1])/64)*2
            me = int(glove_values[12]/64) + int((glove_values[13])/64)*2 + int(glove_values[14]/64)*4

            thumb = scale + me*2 + int(glove_values[2]/64)
            pointer = 12 + scale + me*2 + int(glove_values[2]/64)
            middle = 12 + scale + me*2 + 3 + int(glove_values[1]/64) + int(glove_values[2]/64)
            ring = 12 + scale + me*2 + 6 + r_dict[my] + int(glove_values[2]/64)
            pinky = 12 + scale + me*2 + 12 - p_dict[my] + int(glove_values[2]/64)


            if glove_values[11] > speed:
                strike[0] = 1
                mc_0 = 5
                for x in range(5):
                    sand[x] += int(glove_values[6 + x]/8) * int(glove_values[11]/4)
                    if glove_values[6 + x] < 8:
                        sand[x] = 0
                        continue

            else:
                mc_0 = 0
                if max(sand[:5]) > 0 and max(sand[:5]) > 128:

                    #heat
                    for x in range(5):
                        if sand[x] > 0:
                            heat[x] += 1
                        else:
                            heat[x] = 0

                    ma = int(max(sand[:5])/2 + 1)

                    right_letter = int(sand[0]/ma) + int(sand[1]/ma) * 2 + int(sand[2]/ma) * 4 + int(sand[3]/ma) * 8 + int(sand[4]/ma) * 16
                    voice_l[0] += value_letter[right_letter]
                    v_time.append(time.time())

                    lp_0 = loop_8(thumb + 12, 0, int(heat[0]/8), volume[0])
                    lp_1 = loop_8(pointer + 12, 1, int(heat[1]/8), volume[1])
                    lp_2 = loop_8(middle + 12, 2, int(heat[2]/8), volume[2])
                    lp_3 = loop_8(ring + 12, 3, int(heat[3]/8), volume[3])
                    lp_4 = loop_8(pinky + 12, 4, int(heat[4]/8), volume[4])
                    lp_5 = loop_8(thumb, 5, int(heat[5]/8), volume[5])
                    lp_6 = loop_8(pointer, 6, int(heat[6]/8), volume[6])
                    lp_7 = loop_8(middle, 7, int(heat[7]/8), volume[7])
                    lp_8 = loop_8(ring, 8, int(heat[8]/8), volume[8])
                    lp_9 = loop_8(pinky, 9, int(heat[9]/8), volume[9])

                if my != my_0[0]:
                    my_0[0] = my
                    echo[0].append(time.time() - my_0[1])
                    my_0[1] = time.time()
                    tempo = echo[0][-1]
                    print('')
                    print("echo_0")
                    print(echo[0])
                    for x in range(10):
                        if heat[x] > 8:
                            heat[x] = heat[x] - 8

                sand[0] = 0
                sand[1] = 0
                sand[2] = 0
                sand[3] = 0
                sand[4] = 0

            if glove_values[23] > speed:
                strike[1] = 1
                mc_1 = 5
                for x in range(5):
                    if glove_values[18 + x] < 8:
                        sand[x+5] = 0
                        continue
                    sand[x+5] += int(glove_values[18 + x]/8)  * int(glove_values[23]/4)

            else:
                mc_1 = 0
                if max(sand[5:10]) > 0 and max(sand[5:10]) > 128:

                    #heat
                    for x in range(5):
                        if sand[x + 5] > 0:
                            heat[x + 5] += 1
                        else:
                            heat[x + 5] = 0

                    ma = int(max(sand[5:10])/2 + 1)

                    left_letter = int(sand[5]/ma) + int(sand[6]/ma) * 2 + int(sand[7]/ma) * 4 + int(sand[8]/ma) * 8 + int(sand[9]/ma) * 16
                    voice_l[1] += value_letter[left_letter]

                    lp_0 = loop_8(thumb + 12, 0, int(heat[0]/8), volume[0])
                    lp_1 = loop_8(pointer + 12, 1, int(heat[1]/8), volume[1])
                    lp_2 = loop_8(middle + 12, 2, int(heat[2]/8), volume[2])
                    lp_3 = loop_8(ring + 12, 3, int(heat[3]/8), volume[3])
                    lp_4 = loop_8(pinky + 12, 4, int(heat[4]/8), volume[4])
                    lp_5 = loop_8(thumb, 5, int(heat[5]/8), volume[5])
                    lp_6 = loop_8(pointer, 6, int(heat[6]/8), volume[6])
                    lp_7 = loop_8(middle, 7, int(heat[7]/8), volume[7])
                    lp_8 = loop_8(ring, 8, int(heat[8]/8), volume[8])
                    lp_9 = loop_8(pinky, 9, int(heat[9]/8), volume[9])

                if me != me_0[0]:
                    me_0[0] = me
                    echo[1].append(time.time() - me_0[1])
                    me_0[1] = time.time()
                    tempo = echo[1][-1]
                    print('')
                    print('echo_1')
                    print(echo[1])

                    for x in range(10):
                        if heat[x] > 8:
                            heat[x] = heat[x] - 8

                sand[5] = 0
                sand[6] = 0
                sand[7] = 0
                sand[8] = 0
                sand[9] = 0


            if right_letter == left_letter and right_letter == 17:
                eb = HEIGHT
                voice_l = ['', '']
                heat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                echo = [[], []]


            for x in range(5):
                volume[x] = glove_values[6+x]/128
                volume[x + 5] = glove_values[18+x]/128

            lp_0.set_volume(volume[0])
            lp_1.set_volume(volume[1])
            lp_2.set_volume(volume[2])
            lp_3.set_volume(volume[3])
            lp_4.set_volume(volume[4])
            lp_5.set_volume(volume[5])
            lp_6.set_volume(volume[6])
            lp_7.set_volume(volume[7])
            lp_8.set_volume(volume[8])
            lp_9.set_volume(volume[9])

            #beat
            if time.time() - t_0 > tempo/4:
                print(strike)
                print(strike[0] + strike[1])
                drum_track(strike[0] + strike[1] + 1, 11)
                t_0 = time.time()
                beat += 1
                strike = [0, 0]

        if pce == 2:

            #brush
            g1_size = 0
            g2_size = 0
            for x in range(5):
                g1_size += sum(heat[:5])
                g2_size += sum(heat[5::])

            brush_min_0 = int(g1_size/8) + 2
            brush_min_1 = int(g2_size/8) + 2

            #octant
            scale = 12
            my = int(glove_values[0]/64) + int((glove_values[1])/64)*2
            me = int(glove_values[12]/64) + int((glove_values[13])/64)*2 + int(glove_values[14]/64)*4

            thumb = scale + me*2 + int(glove_values[2]/64)
            pointer = 12 + scale + me*2 + int(glove_values[2]/64)
            middle = 12 + scale + me*2 + 3 + int(glove_values[1]/64) + int(glove_values[2]/64)
            ring = 12 + scale + me*2 + 6 + r_dict[my] + int(glove_values[2]/64)
            pinky = 12 + scale + me*2 + 12 - p_dict[my] + int(glove_values[2]/64)


            if glove_values[11] > speed or glove_values[23] > speed:
                strike[0] = int(glove_values[11]/8)
                strike[1] = int(glove_values[23]/8)
                mc_0 = int(glove_values[11]/8) * 5
                mc_1 = int(glove_values[23]/8) * 5
                erosion()

            else:
                mc_0 = 0
                mc_1 = 0

                if max(sand) > 256:
                    #heat
                    for x in range(10):
                        if sand[x] > 0:
                            heat[x] += 1
                        else:
                            heat[x] = 0

                    ma = int(max(sand)/2 + 1)

                    right_letter = int(sand[0]/ma) + int(sand[1]/ma) * 2 + int(sand[2]/ma) * 4 + int(sand[3]/ma) * 8 + int(sand[4]/ma) * 16
                    voice_l[0] += value_letter[right_letter]
                    left_letter = int(sand[5]/ma) + int(sand[6]/ma) * 2 + int(sand[7]/ma) * 4 + int(sand[8]/ma) * 8 + int(sand[9]/ma) * 16
                    voice_l[1] += value_letter[left_letter]
                    meta_letter = int(sand[0]/ma) + int(sand[1]/ma)*2 + int(sand[2]/ma)*16 + int(sand[5]/ma)*4 + int(sand[6]/ma)*8 + int(sand[7]/ma)*32
                    print(int(sand[0]/ma) + int(sand[1]/ma)*2 + int(sand[2]/ma)*16 + int(sand[1]/ma)*4 + int(sand[2]/ma)*8 + int(sand[1]/ma)*32)
                    print(meta_letter)
                    voice += metabet_6[meta_letter]
                    v_time.append(time.time())

                    lp_0 = loop_8(thumb + 12, 0, int(heat[0]/8), volume[0])
                    lp_1 = loop_8(pointer + 12, 1, int(heat[1]/8), volume[1])
                    lp_2 = loop_8(middle + 12, 2, int(heat[2]/8), volume[2])
                    lp_3 = loop_8(ring + 12, 3, int(heat[3]/8), volume[3])
                    lp_4 = loop_8(pinky + 12, 4, int(heat[4]/8), volume[4])
                    lp_5 = loop_8(thumb, 5, int(heat[5]/8), volume[5])
                    lp_6 = loop_8(pointer, 6, int(heat[6]/8), volume[6])
                    lp_7 = loop_8(middle, 7, int(heat[7]/8), volume[7])
                    lp_8 = loop_8(ring, 8, int(heat[8]/8), volume[8])
                    lp_9 = loop_8(pinky, 9, int(heat[9]/8), volume[9])

                    if my + int(glove_values[2]/64) != my_0[0] + int(glove_values[2]/64):
                        my_0[0] = my+ int(glove_values[2]/64)
                        echo[0].append(time.time() - my_0[1])
                        my_0[1] = time.time()
                        tempo = echo[0][-1]
                        print('')
                        print("echo_0")
                        print(echo[0])

                    elif me != me_0[0]:
                        me_0[0] = me
                        echo[1].append(time.time() - me_0[1])
                        me_0[1] = time.time()
                        tempo = echo[1][-1]
                        print('')
                        print('echo_1')
                        print(echo[1])

                    sand[0] = 0
                    sand[1] = 0
                    sand[2] = 0
                    sand[3] = 0
                    sand[4] = 0
                    sand[5] = 0
                    sand[6] = 0
                    sand[7] = 0
                    sand[8] = 0
                    sand[9] = 0




            # if glove_values[11] < speed:
            #     mc_0 = 0
            #     if max(sand) > 128:
            #
            #         #heat
            #         for x in range(5):
            #             if sand[x] > 0:
            #                 heat[x] += 1
            #             else:
            #                 heat[x] = 0
            #
            #         ma = int(max(sand[:5])/2 + 1)
            #
            #         right_letter = int(sand[0]/ma) + int(sand[1]/ma) * 2 + int(sand[2]/ma) * 4 + int(sand[3]/ma) * 8 + int(sand[4]/ma) * 16
            #         voice_l[0] += value_letter[right_letter]
            #         left_letter = int(sand[5]/ma) + int(sand[6]/ma) * 2 + int(sand[7]/ma) * 4 + int(sand[8]/ma) * 8 + int(sand[9]/ma) * 16
            #         voice_l[1] += value_letter[left_letter]
            #         v_time.append(time.time())
            #
            #         lp_0 = loop_8(thumb + 12, 0, int(heat[0]/8), volume[0])
            #         lp_1 = loop_8(pointer + 12, 1, int(heat[1]/8), volume[1])
            #         lp_2 = loop_8(middle + 12, 2, int(heat[2]/8), volume[2])
            #         lp_3 = loop_8(ring + 12, 3, int(heat[3]/8), volume[3])
            #         lp_4 = loop_8(pinky + 12, 4, int(heat[4]/8), volume[4])
            #         lp_5 = loop_8(thumb, 5, int(heat[5]/8), volume[5])
            #         lp_6 = loop_8(pointer, 6, int(heat[6]/8), volume[6])
            #         lp_7 = loop_8(middle, 7, int(heat[7]/8), volume[7])
            #         lp_8 = loop_8(ring, 8, int(heat[8]/8), volume[8])
            #         lp_9 = loop_8(pinky, 9, int(heat[9]/8), volume[9])
            #
            #     if my != my_0[0]:
            #         my_0[0] = my
            #         echo[0].append(time.time() - my_0[1])
            #         my_0[1] = time.time()
            #         tempo = echo[0][-1]
            #         print('')
            #         print("echo_0")
            #         print(echo[0])
            #
            #
            #     sand[0] = 0
            #     sand[1] = 0
            #     sand[2] = 0
            #     sand[3] = 0
            #     sand[4] = 0
            #
            #
            # if glove_values[23] < speed:
            #     mc_1 = 0
            #     if max(sand) > 128:
            #
            #         #heat
            #         for x in range(5):
            #             if sand[x + 5] > 0:
            #                 heat[x + 5] += 1
            #             else:
            #                 heat[x + 5] = 0
            #
            #         ma = int(max(sand[5:10])/2 + 1)
            #
            #         left_letter = int(sand[5]/ma) + int(sand[6]/ma) * 2 + int(sand[7]/ma) * 4 + int(sand[8]/ma) * 8 + int(sand[9]/ma) * 16
            #         voice_l[1] += value_letter[left_letter]
            #
            #         lp_0 = loop_8(thumb + 12, 0, int(heat[0]/8), volume[0])
            #         lp_1 = loop_8(pointer + 12, 1, int(heat[1]/8), volume[1])
            #         lp_2 = loop_8(middle + 12, 2, int(heat[2]/8), volume[2])
            #         lp_3 = loop_8(ring + 12, 3, int(heat[3]/8), volume[3])
            #         lp_4 = loop_8(pinky + 12, 4, int(heat[4]/8), volume[4])
            #         lp_5 = loop_8(thumb, 5, int(heat[5]/8), volume[5])
            #         lp_6 = loop_8(pointer, 6, int(heat[6]/8), volume[6])
            #         lp_7 = loop_8(middle, 7, int(heat[7]/8), volume[7])
            #         lp_8 = loop_8(ring, 8, int(heat[8]/8), volume[8])
            #         lp_9 = loop_8(pinky, 9, int(heat[9]/8), volume[9])
            #
            #     if me != me_0[0]:
            #         me_0[0] = me
            #         echo[1].append(time.time() - me_0[1])
            #         me_0[1] = time.time()
            #         tempo = echo[1][-1]
            #         print('')
            #         print('echo_1')
            #         print(echo[1])
            #
            #
            #     sand[5] = 0
            #     sand[6] = 0
            #     sand[7] = 0
            #     sand[8] = 0
            #     sand[9] = 0


            if right_letter == left_letter and right_letter == 17:
                eb = HEIGHT
                voice = ''
                voice_l = ['', '']
                heat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                echo = [[], []]


            for x in range(5):
                volume[x] = (glove_values[6+x] - glove_values[11])/128
                volume[x + 5] = (glove_values[18+x] - glove_values[23])/128

            lp_0.set_volume(volume[0])
            lp_1.set_volume(volume[1])
            lp_2.set_volume(volume[2])
            lp_3.set_volume(volume[3])
            lp_4.set_volume(volume[4])
            lp_5.set_volume(volume[5])
            lp_6.set_volume(volume[6])
            lp_7.set_volume(volume[7])
            lp_8.set_volume(volume[8])
            lp_9.set_volume(volume[9])

            #beat
            if time.time() - t_0 > tempo/4:
                # print(strike)
                # print(strike[0] + strike[1])
                drum_track(strike[0] + strike[1] + 1, 11)
                t_0 = time.time()
                beat += 1
                strike = [0, 0]


        if eb > 0:
            eb = eb - 1
            canvas[eb] = zero_r
            canvas[-eb] = zero_r


        #mitosis
        if pause == 0:

            brush_height_0 = brush_min_0
            brush_width_0 = brush_height_0
            brush_height_1 = brush_min_1
            brush_width_1 = brush_height_1

            #brush x,y
            brush_x_0 = (glove_values[x_position_g0v] * brush_scale_w)
            brush_y_0 = (glove_values[y_position_g0v] * brush_scale_h)
            brush_x_1 = (glove_values[x_position_g1v] * brush_scale_w)
            brush_y_1 = (glove_values[y_position_g1v] * brush_scale_h)


            cells_a = np.zeros((brush_height_0, brush_width_0, 3), dtype='uint8')
            cells_b = np.zeros((brush_height_1, brush_width_1, 3), dtype='uint8')


            #canvas to brush
            for y in range(brush_height_0):
                for x in range(brush_width_0):
                    cells_a[y, x] = canvas[(y - brush_y_0) % canvas_rows, (x + brush_x_0) % canvas_row_width]
            for y in range(brush_height_1):
                for x in range(brush_width_1):
                    cells_b[y, x] = canvas[(y - brush_y_1) % canvas_rows, (x + brush_x_1) % canvas_row_width]

            #brush_step
            cell_vel_0 = brush_width_0
            cell_vel_1 = brush_width_1

            for y in range(cell_vel_0):

                cells_a = np.rot90(cells_a, stream_direction_0[step % stream_buffer % len(stream_direction_0)], (0, 1))

                cells_a = np.roll(cells_a, 1, 0)

                if g_brush == 1:

                    for x in range(len(cells_a[0])):
                        cells_a[(0 + momentum[stream_direction_0[step % stream_buffer % len(stream_direction_0)]]) % (
                                    len(cells_a[0]) - 1), x] = value_color[
                             d_rule_0[tuple(viewer_1d(cells_a[1], x, view, [], color_value))]]

                if len(stream_direction_0) > 0:

                    cells_a = np.rot90(cells_a, 4 - stream_direction_0[step % stream_buffer % len(stream_direction_0)], (0, 1))

                    # cells_a = np.rot90(cells_a, 3, (0, 1))
                    # cells_a = np.rot90(cells_a, 2, (0, 1))
                    # cells_a = np.rot90(cells_a, 1, (0, 1))

                step += 1

            for y in range(cell_vel_1):

                cells_b = np.rot90(cells_b, stream_direction_1[step % stream_buffer % len(stream_direction_1)], (0, 1))

                cells_b = np.roll(cells_b, 1, 0)

                if g_brush == 1:

                    for x in range(len(cells_b[0])):
                        cells_b[(0 + momentum[stream_direction_1[step % stream_buffer % len(stream_direction_1)]]) % (
                                len(cells_b[0]) - 1), x] = value_color[
                            d_rule_1[tuple(viewer_1d(cells_b[1], x, view, [], color_value))]]

                if len(stream_direction_1) > 0:
                    cells_b = np.rot90(cells_b, 4 - stream_direction_1[step % stream_buffer % len(stream_direction_1)],
                                       (0, 1))

                    # cells_a = np.rot90(cells_a, 3, (0, 1))
                    # cells_a = np.rot90(cells_a, 2, (0, 1))
                    # cells_a = np.rot90(cells_a, 1, (0, 1))

                step += 1

            #brush to canvas
            for y in range(brush_height_0):
                for x in range(brush_width_0):
                    canvas[(y - brush_y_0) % canvas_rows, (x + brush_x_0) % canvas_row_width] = cells_a[y, x]
            for y in range(brush_height_1):
                for x in range(brush_width_1):
                    canvas[(y - brush_y_1) % canvas_rows, (x + brush_x_1) % canvas_row_width] = cells_b[y, x]


        #inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2


            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


            #keyboard
            elif event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_SPACE:

                    if base < 5:

                        value_color = {0: color_0, 1: color_1, 2: color_2, 3: color_3}
                        color_value = {v: k for k, v in value_color.items()}

                    else:

                        value_color = {0: color_0, 1: color_1, 2: color_2, 3: color_3, 4: color_4, 5: color_5,
                                       6: color_6, 7: color_7, 8: color_8}
                        color_value = {v: k for k, v in value_color.items()}

                    pygame.midi.quit()
                    if midi_inputs == 1:

                        pygame.init()
                        pygame.midi.init()
                        pygame.fastevent.init()
                        event_post = pygame.fastevent.post

                        # rtmidi init
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
                        glove_sums = [x for x in range(gloves)]

                        print("")
                        print("glove_values")
                        print(glove_values)

                        mode_brake = 0
                        x_brake = 0
                        y_brake = 0
                        z_brake = 0
                        l_brake = 0
                        r_brake = 0

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

                    health = [WIDTH/2, WIDTH/2]


                elif event.key == pygame.K_F2:
                    # book_rule = str()
                    # for ir in i_rule:
                    #     book_rule += str(ir)
                    # rule_book.append(book_rule)

                    ui_on += 1
                    ui_on = ui_on % 3

                elif event.key == pygame.K_F3:
                    for y in range(canvas_rows):
                        for x in range(canvas_row_width):
                            canvas[y, x] = 0



                elif event.key == pygame.K_RETURN:

                    pause += 1
                    pause = pause % 2

                    print("")
                    print("pause")
                    print(pause)



                elif event.key == pygame.K_PERIOD:

                    # sqr_8(wu, 1)
                    # kick(1)

                    loop_8(wu, 0, 20, 10, 1)
                    wu += 1
                    print("wu")
                    print(wu)

                elif event.key == pygame.K_UP:

                    key = key + 1
                    print(key)

                elif event.key == pygame.K_DOWN:

                    key = key - 1
                    print(key)

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


        #glove application
        if midi_inputs > 0:
            # print()
            # print(glove_values)


            # stream direction
            if streams == 1:

                if last_x_0 > brush_x_0:
                    stream_direction_0.append(1)
                if last_x_0 < brush_x_0:
                    stream_direction_0.append(3)

                if last_y_0 > brush_y_0:
                    stream_direction_0.append(0)
                if last_y_0 < brush_y_0:
                    stream_direction_0.append(2)

                last_x_0 = brush_x_0
                last_y_0 = brush_y_0


                if last_x_1 > brush_x_1:
                    stream_direction_1.append(1)
                if last_x_1 < brush_x_1:
                    stream_direction_1.append(3)

                if last_y_1 > brush_y_0:
                    stream_direction_0.append(0)
                if last_y_1 > brush_y_0:
                    stream_direction_1.append(2)

                last_x_1 = brush_x_1
                last_y_1 = brush_y_1


            if g_brush == 1:

                # print(glove_values)

                full_rule, midi_weights_0 = glove(glove_values)
                i_rule_0 = full_rule
                spin += int(glove_values[11]/spin_speed)
                for x in range((glove_values[11] + spin)%bbv):
                    y = i_rule_0[0]
                    i_rule_0 = i_rule_0[1:]
                    i_rule_0.append(y)
                for x in range(len(i_rule_0[:729])):
                    # print(d_rule_0[list(d_rule_0.keys())[x]], i_rule_0[x])
                    d_rule_0[list(d_rule_0.keys())[x]] = i_rule_0[x]

                full_rule, midi_weights_1 = glove(glove_values[12:], 1)
                i_rule_1 = full_rule
                spin += int(glove_values[23]/spin_speed)
                for x in range((glove_values[23] + spin) % bbv):
                    y = i_rule_1[0]
                    i_rule_1 = i_rule_1[1:]
                    i_rule_1.append(y)
                for x in range(len(i_rule_1[:729])):
                    # print(d_rule_0[list(d_rule_0.keys())[x]], i_rule_0[x])
                    d_rule_1[list(d_rule_1.keys())[x]] = i_rule_1[x]



                # print()
                # print(test_rule)
                # print(midi_weights)


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







# menus

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)


def draw_text(text, font, color_dt, surface, x, y):
    textobj = font.render(text, 1, color_dt)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def menu():

    click = False
    input_text_c = ''
    input_text_v = ''
    device_id = None
    analytics = 0

    pygame.init()
    pygame.fastevent.init()

    pygame.midi.init()

    print(" ")
    print("device info")
    _print_device_info()

    mc = pygame.midi.get_count()
    print("mc")
    print(mc)

    ports = dict()

    print("")
    print("mdi")
    for m in range(pygame.midi.get_count()):


        mdi = pygame.midi.get_device_info(m)
        print(mdi)

        ports[m] = str(mdi[1])




    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print(' ')
    print("using input_id :%s:" % input_id)
    p_m_i = pygame.midi.Input(input_id)
    device_id = -1

    while True:


        WIN.fill((0, 0, 0))
        t_line = pygame.Rect(WIDTH / 2 - 633, 200, 1360, 2)
        draw_text('C311UL4R H4PT1C 4UT0M4T4 0P3R4T1NG 5Y5T3M', TITLE_FONT, (10, 100, 10), WIN, WIDTH / 2 - 655, 100)
        pygame.draw.rect(WIN, (10, 100, 10), t_line)

        text_surface_c = main_font.render(input_text_c, True, (100, 10, 10))
        text_surface_v = main_font.render(input_text_v, True, (100, 10, 100))
        mx, my = pygame.mouse.get_pos()


        for p in ports:

            # print("")
            # print(p)
            # print(ports[p])

            port_button = pygame.Rect(WIDTH / 2 + 400, 600 + p * 40, 362, 34)
            pygame.draw.rect(WIN, (192, 128, 0), port_button)

            port_button = pygame.Rect(WIDTH / 2 + 400, 600 + p * 40, 360, 30)
            pygame.draw.rect(WIN, (0, 0, 0), port_button)

            if port_button.collidepoint((mx, my)):

                # print("collide")
                # print(p)

                if click:

                    print(p)

                    device_id = int(p)
                    draw_text('> ' + str(ports[p]), small_font, (255, 255, 255), WIN, WIDTH / 2 + 400, 600 + p * 40)

            draw_text('> ' + str(ports[p]), small_font, (192, 128, 0), WIN, WIDTH / 2 + 400, 600 + p * 40)

        size_2 = pygame.Rect(WIDTH / 2 - 300, 400, 200, 50)
        size_3 = pygame.Rect(WIDTH / 2 - 300, 500, 200, 50)
        size_5 = pygame.Rect(WIDTH / 2 - 300, 600, 200, 50)
        size_10 = pygame.Rect(WIDTH / 2 - 300, 700, 200, 50)
        size_2_i = pygame.Rect(WIDTH / 2 - 300, 400, 197, 43)
        size_3_i = pygame.Rect(WIDTH / 2 - 300, 500, 197, 43)
        size_5_i = pygame.Rect(WIDTH / 2 - 300, 600, 197, 43)
        size_10_i = pygame.Rect(WIDTH / 2 - 300, 700, 197, 43)

        # binary = pygame.Rect(WIDTH/2 + 100, 400, 200, 50)
        # ternary = pygame.Rect(WIDTH/2 + 100, 500, 200, 50)
        # quaternary = pygame.Rect(WIDTH/2 + 100, 600, 200, 50)
        # binary_i = pygame.Rect(WIDTH/2 + 100, 400, 197, 43)
        # ternary_i = pygame.Rect(WIDTH/2 + 100, 500, 197, 43)
        # quaternary_i = pygame.Rect(WIDTH/2 + 100, 600, 197, 43)

        color_rect = pygame.Rect(WIDTH / 2 + 100, 400, 200, 50)
        color_rect_i = pygame.Rect(WIDTH / 2 + 100, 400, 197, 43)

        vel_rect = pygame.Rect(WIDTH / 2 + 100, 500, 200, 50)
        vel_rect_i = pygame.Rect(WIDTH / 2 + 100, 500, 197, 43)

        enter = pygame.Rect(WIDTH / 2 + 100, 700, 200, 50)
        enter_i = pygame.Rect(WIDTH / 2 + 100, 700, 197, 43)

        underline_2 = pygame.Rect(WIDTH / 2 - 300, 385, 200, 2)

        analytics_button = pygame.Rect(WIDTH / 2 + 470, 300, 200, 50)
        pygame.draw.rect(WIN, (0, 192, 192), analytics_button)
        analytics_button = pygame.Rect(WIDTH / 2 + 470, 300, 197, 43)
        pygame.draw.rect(WIN, (0, 0, 0), analytics_button)
        draw_text('analytics ^ 0 off - 1 on', small_font, (0, 192, 192), WIN,WIDTH / 2 + 470, 350)


        pygame.draw.rect(WIN, (10, 100, 10), size_2)
        pygame.draw.rect(WIN, (10, 100, 10), size_3)
        pygame.draw.rect(WIN, (10, 100, 10), size_5)
        pygame.draw.rect(WIN, (10, 100, 10), size_10)
        pygame.draw.rect(WIN, (0, 0, 0), size_2_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_3_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_5_i)
        pygame.draw.rect(WIN, (0, 0, 0), size_10_i)
        draw_text(' small', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 400)
        draw_text(' medium', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 500)
        draw_text(' large', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 600)
        draw_text(' X-large', main_font, (10, 100, 10), WIN, WIDTH / 2 - 300, 700)
        draw_text('Cell Size', main_font, (10, 100, 10), WIN, WIDTH / 2 - 280, 340)
        pygame.draw.rect(WIN, (10, 100, 10), underline_2)

        # pygame.draw.rect(WIN, (100, 10, 10), binary)
        # pygame.draw.rect(WIN, (100, 10, 10), ternary)
        # pygame.draw.rect(WIN, (100, 10, 10), quaternary)
        # pygame.draw.rect(WIN, (0, 0, 0), binary_i)
        # pygame.draw.rect(WIN, (0, 0, 0), ternary_i)
        # pygame.draw.rect(WIN, (0, 0, 0), quaternary_i)
        # draw_text(' Two', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 400)
        # draw_text(' Three', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 500)
        # draw_text(' Four', main_font, (100, 10, 10), WIN, WIDTH/2 + 100, 600)
        # draw_text('Number of Colors', main_font, (100, 10, 10), WIN, WIDTH/2 + 80, 340)
        # pygame.draw.rect(WIN, (100, 10, 10), underline_1)

        pygame.draw.rect(WIN, (100, 10, 10), color_rect)
        pygame.draw.rect(WIN, (0, 0, 0), color_rect_i)
        draw_text('<place mouse-pointer on box to type;', small_font, (100, 10, 10), WIN, WIDTH / 2 + 350, 400)
        draw_text('choose a single number between 2 and 9', small_font, (100, 10, 10), WIN, WIDTH / 2 + 360, 425)

        pygame.draw.rect(WIN, (100, 10, 100), vel_rect)
        pygame.draw.rect(WIN, (0, 0, 0), vel_rect_i)
        draw_text('<place mouse-pointer on box to type;', small_font, (100, 10, 100), WIN, WIDTH / 2 + 350, 500)
        draw_text('numbers between 1-10 recommended', small_font, (100, 10, 100), WIN, WIDTH / 2 + 360, 525)

        pygame.draw.rect(WIN, (10, 10, 100), enter)
        pygame.draw.rect(WIN, (0, 0, 0), enter_i)
        draw_text(' Enter', main_font, (10, 10, 100), WIN, WIDTH / 2 + 100, 700)

        draw_text('Instructions:', small_font, (200, 200, 200), WIN, 50, 225)
        draw_text('1. Choose a cell-size. [GREEN]', small_font, (200, 200, 200), WIN, 50, 275)
        draw_text('     -Start with X-large to be safe. Smaller cells', text_font, (200, 200, 200), WIN, 50, 315)
        draw_text('         may cause issues on slower computers.', text_font, (200, 200, 200), WIN, 50, 340)
        draw_text('2. Choose the number of cell colors. [RED]', small_font, (200, 200, 200), WIN, 50, 375)
        draw_text('3. Set a desired speed. [PURPLE]', small_font, (200, 200, 200), WIN, 50, 425)
        draw_text('4. Press Enter [BLUE]', small_font, (200, 200, 200), WIN, 50, 475)
        draw_text('     The program will have loaded once you see Step & Count', text_font, (200, 200, 200), WIN, 50,
                  525)
        draw_text('     in the top right, and Rule in the bottom left.', text_font, (200, 200, 200), WIN, 50, 550)
        draw_text('     Typing has no effect until the first row of colored', text_font, (200, 200, 200), WIN, 50, 575)
        draw_text('     cells reach the bottom of the page.', text_font, (200, 200, 200), WIN, 50, 600)
        draw_text('     Two cell colors uses the keys (asdf jkl;) to change the rules.', text_font, (200, 200, 200),
                  WIN, 50, 625)
        draw_text('     For three colors+, the best effects are seen while typing full sentences', text_font,
                  (200, 200, 200), WIN, 50, 650)
        draw_text('     Press the escape key to exit the program at any time.', text_font, (200, 200, 200), WIN, 50,
                  675)
        draw_text('     Enjoy!', text_font, (200, 200, 200), WIN, 50, 700)
        draw_text('Command Menu (Advanced Technique)', small_font, (200, 200, 200), WIN, 50, 750)
        draw_text(
            '     Press shift & enter keys, at the same time, to activate. A white box will appear in the top left corner of the screen.',
            text_font, (200, 200, 200), WIN, 50, 800)
        draw_text(
            '     Once the desired command is typed into the box, press the shift & enter keys again to input the command and close the box.',
            text_font, (200, 200, 200), WIN, 50, 825)
        draw_text(
            '     All commands are lowercase or integer values, spaces matter, and invalid commands will return a warning in the type field',
            text_font, (200, 200, 200), WIN, 50, 850)
        draw_text(
            '     To save the designs found during a session input(write) or (name *desired-name*). names longer than one word must be separated by a -',
            text_font, (200, 200, 200), WIN, 50, 875)
        draw_text('     All values are accepted as inputs and will change the rule accordingly', text_font,
                  (200, 200, 200), WIN, 50, 900)

        if size_2.collidepoint((mx, my)):
            if click:
                print("size_2")
                pixel_res = 2
                draw_text(' small', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 400)
        if size_3.collidepoint((mx, my)):
            if click:
                print("size_3")
                pixel_res = 3
                draw_text(' medium', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 500)
        if size_5.collidepoint((mx, my)):
            if click:
                print("size_5")
                pixel_res = 5
                draw_text(' large', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 600)
        if size_10.collidepoint((mx, my)):
            if click:
                print("size_10")
                pixel_res = 10
                draw_text(' X-large', main_font, (255, 255, 255), WIN, WIDTH / 2 - 300, 700)

        # if binary.collidepoint((mx, my)):
        #     if click:
        #         print("binary")
        #         base = 2
        #         draw_text(' Two', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 400)
        # if ternary.collidepoint((mx, my)):
        #     if click:
        #         print("ternary")
        #         base = 3
        #         draw_text(' Three', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 500)
        # if quaternary.collidepoint((mx, my)):
        #     if click:
        #         print("quaternary")
        #         base = 4
        #         draw_text(' Four', main_font, (255, 255, 255), WIN, WIDTH / 2 + 100, 600)

        if color_rect.collidepoint((mx, my)):
            draw_text('Colors:', main_font, (100, 10, 10), WIN, WIDTH / 2 + 100, 400)
            WIN.blit(text_surface_c, (WIDTH / 2 + 200, 400))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text_c += '1'
                    if event.key == K_2:
                        input_text_c += '2'
                    if event.key == K_3:
                        input_text_c += '3'
                    if event.key == K_4:
                        input_text_c += '4'
                    if event.key == K_5:
                        input_text_c += '5'
                    if event.key == K_6:
                        input_text_c += '6'
                    if event.key == K_7:
                        input_text_c += '7'
                    if event.key == K_8:
                        input_text_c += '8'
                    if event.key == K_9:
                        input_text_c += '9'
                    if event.key == K_0:
                        input_text_c += '0'
                    if event.key == K_BACKSPACE:
                        input_text_c = input_text_c[:len(input_text_c) - 1]
                    print(input_text_c)

            if len(input_text_c) > 0:
                base = int(input_text_c)

        if vel_rect.collidepoint((mx, my)):
            draw_text('Speed:', main_font, (100, 10, 100), WIN, WIDTH / 2 + 100, 500)
            WIN.blit(text_surface_v, (WIDTH / 2 + 200, 500))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        input_text_v += '1'
                    if event.key == K_2:
                        input_text_v += '2'
                    if event.key == K_3:
                        input_text_v += '3'
                    if event.key == K_4:
                        input_text_v += '4'
                    if event.key == K_5:
                        input_text_v += '5'
                    if event.key == K_6:
                        input_text_v += '6'
                    if event.key == K_7:
                        input_text_v += '7'
                    if event.key == K_8:
                        input_text_v += '8'
                    if event.key == K_9:
                        input_text_v += '9'
                    if event.key == K_0:
                        input_text_v += '0'
                    if event.key == K_BACKSPACE:
                        input_text_v = input_text_v[:len(input_text_v) - 1]
                    print(input_text_v)

            if len(input_text_v) > 0:
                cell_vel = int(input_text_v)


        if enter.collidepoint((mx, my)):
            if click:
                print("enter")
                print("pixel_res")
                print(pixel_res)
                draw_text('Enter', main_font, (255, 255, 255), WIN, WIDTH / 2 - 100, 800)
                Chaos_Window(base, pixel_res, cell_vel, analytics, device_id)

        if analytics_button.collidepoint((mx, my)):
            if click:
                print('analytics on')

                if analytics == 0:

                    analytics = 1

                else:

                    analytics = 0

            draw_text('analytics: ' + str(analytics), main_font, (0, 192, 192), WIN, WIDTH / 2 + 480, 300)


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        mainClock.tick(60)


#pygame.midi interface

def print_device_into():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

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

    #rtmidi init
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


# input_main()


# menu()


Chaos_Window(9, 2)




