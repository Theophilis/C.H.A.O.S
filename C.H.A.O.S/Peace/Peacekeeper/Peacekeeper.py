# C.H.A.O.S

import numpy as np
from datetime import datetime
import random
import pygame
import os
import pickle
import sys
import pygame.midi
import time
from collections import deque
import math

from pygame import mixer


sys.setrecursionlimit(999999999)

pygame.font.init()

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

length = 8
# number of times given rule is applied and number of initial rows generated
width = length * 2 + 1
# number of cells in a row
rule = 90
# number who's x_base transformation gives the rules dictionary its values
view = 3
# size of the view window that scans a row for rule application
base = 3
# numerical base of the rule set. number of colors each cell can be
start = length
# position for a row 0 cell value 1
direction = 0


# if ^ = 0 view scans from left to right: else view scans right to left


#####to do#####
# translate complex numbers (pi, phi, e) to a base n digit sequence(where n is the number of possible rule states to be called).
##Then, trigger a rotation of a rule state based on the rule position given by the digit in the complex number

# add a record feature and button to menu. allows for recorder of all key inputs in a text file.


#####map#####

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


def rule_gen_2(rule, base, length):
    rules = dict()

    if base == 2:
        int_rule = bin(rule).replace('0b', '')

    else:
        int_rule = base_x(rule, base)

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


def viewer_1d_1(row, y, view, v_0, color_value, color_value_1):

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

            try:
                v_0.insert(0, str(color_value[tuple(row[int(y - len(v_0) / 2)])]))

            except:
                v_0.insert(0, str(color_value_1[tuple(row[int(y - len(v_0) / 2)])]))

    view -= 1

    if view == 0:

        return v_0

    else:

        v_0 = viewer_1d(row, y, view, v_0, color_value)

        return v_0


def Color_cells_1d(d_rule, cell_row_width, row_0):

    # print("")
    # print("row_0")
    # print(row_0)

    row_1 = np.zeros((1, cell_row_width), dtype='int8')

    row_1[0] = [d_rule[tuple(viewer_1d(row_0, x, view, []))] for x in range(len(row_0))]

    return row_1


#####game#####

pygame.init()
pygame.display.init()

current_display = pygame.display.Info()
WIDTH , HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
letter_values = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9, 'a': 10, 's': 11,
                 'd': 12, 'f': 13,
                 'g': 14, 'h': 15, 'j': 16, 'k': 17, 'l': 18, 'z': 19, 'x': 20, 'c': 21, 'v': 22, 'b': 23, 'n': 24,
                 'm': 25, ' ': 26}

pygame.display.set_caption("C.H.A.O.S")

click = False


def Chaos_Window(base, cell_vel, analytics, device_id=-1):

    print("base")
    print(base)
    print("device_id")
    print(device_id)
    p_m_i = 0

    #window
    if analytics == 1:

        CELL_WIDTH = HEIGHT

    else:

        CELL_WIDTH = WIDTH

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

    color_list = [0, 0, 0, 32, 32, 32, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0,255]

    if base < 5:

        value_color = {0:color_0, 1:color_1, 2:color_2, 3:color_3}
        color_value = {v:k for k, v in value_color.items()}

    else:

        value_color = {0:color_0, 1:color_1, 2:color_2, 3:color_3, 4:color_4, 5:color_5,
                      6:color_6, 7:color_7, 8:color_8}
        color_value = {v:k for k, v in value_color.items()}

    # numerical
    letter_values = {' ': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11,
                     'l': 12, 'm': 13,
                     'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
                     'y': 25, 'z': 26, '.': 27, ',': 28, '"': 29, '(': 30, ')': 31}

    # frequency
    letter_values = {' ': 0, 'a': 1, 'i': 2, 't': 3,
                     's': 4, 'c': 5, 'd': 6, 'm': 7,
                     'g': 8, 'f': 9, 'w': 10, 'v': 11,
                     'z': 12, 'q': 13, ',': 14, '"': 15,
                     '/': 16, '.': 17, ';': 18, 'j': 19,
                     'x': 20, 'k': 21, 'y': 22, 'b': 23,
                     'h': 24, 'p': 25, 'u': 26, 'l': 27,
                     'n': 28, 'o': 29, 'r': 30, 'e': 31}

    value_letter = {v: k for k, v in letter_values.items()}

    color_post = {0: 1, 1: 5, 2: 2, 3: 6, 4: 3, 5: 7, 6: 4, 7: 8, 8: 0}

    scale_shift = {0:0, 1:2, 2:4, 3:5, 4:7, 5:9, 6:11, 7:12}
    chord_types = {0:(16, 19), 1:(16, 22), 2:(15, 19)}

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


            if g_brush == 4:
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

        if pce == 1:

            bold = 2

            hp_0 = pygame.Rect(WIDTH- health[0], HEIGHT/2, health[0], downs[0])
            pygame.draw.rect(WIN, value_color[states[0] + charge_0[0]], hp_0)
            hp_1 = pygame.Rect(0, HEIGHT/2, health[1], downs[1])
            pygame.draw.rect(WIN, value_color[states[1] + charge_1[0]], hp_1)

            ac_0 = pygame.Rect(WIDTH-health[0], glove_values[11]*(HEIGHT/128), health[0], downs[0])
            pygame.draw.rect(WIN, value_color[states[0] + charge_0[0]], ac_0)
            ac_1 = pygame.Rect(0, glove_values[23]*(HEIGHT/128), health[1], downs[1])
            pygame.draw.rect(WIN, value_color[states[1] + charge_1[0]], ac_1)

            pow_0 = pygame.Rect(WIDTH-health[0], power_0*(HEIGHT/128), health[0], downs[0])
            pygame.draw.rect(WIN, value_color[streak%8], pow_0)
            pow_1 = pygame.Rect(0, power_1*(HEIGHT/128), health[1], downs[1])
            pygame.draw.rect(WIN, value_color[streak%8], pow_1)

            draw_text(str(int(angle)), main_font, (10, 100, 10), WIN, WIDTH / 2 , 100)

        if pce == 3:

            if glove_values[11] > ac_trig:
                ac_0 = pygame.Rect(0, HEIGHT/2, WIDTH, 2)
                pygame.draw.rect(WIN, value_color[me + 1], ac_0)

            if glove_values[2] > 64:
                ac_0 = pygame.Rect(WIDTH/2, 0, 2, HEIGHT)
                pygame.draw.rect(WIN, value_color[me + 1], ac_0)

        if pce == 4:
            draw_text(str(value_letter[right_letter]), TITLE_FONT, (10, 100, 10), WIN, WIDTH - 64, 0)
            draw_text(str(value_letter[left_letter]), TITLE_FONT, (10, 100, 10), WIN, 32, 0)
            draw_text(voice, TITLE_FONT, (10, 100, 10), WIN, WIDTH/2, HEIGHT/2)


        pygame.display.update()

        return cv_pos

    def bass(n, c):
        path = r'audio\bass-' + str(n) + '.mp3'
        mixer.music.load(path)
        pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))

    def pluck(n, c):
        path = r'audio\pluck-' + str(n) + '.mp3'
        mixer.music.load(path)
        pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))

    def hh(n, c):
        path = r'audio\hh-' + str(n) + '.mp3'
        mixer.music.load(path)
        pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))

    def kick(c):
        path = r'audio/kick-0.mp3'
        mixer.music.load(path)
        pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))

    def snare(c):
        path = r'audio/snare-0.mp3'
        mixer.music.load(path)
        pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))

    def shake(c):
        path = r'audio/shake-0.mp3'
        mixer.music.load(path)
        pygame.mixer.Channel(c).play(pygame.mixer.Sound(path))


    def ome(n, c):
        path = r'audio\ome\ome_' + str(n) + '.mp3'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)
        pygame.mixer.Channel(c).play(w)

    def pong(n, c):
        path = r'audio\pong\pong_' + str(n) + '.mp3'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)
        pygame.mixer.Channel(c).play(w)

    def sinsaw(n, c):
        path = r'audio\sinsaw\sinsaw_' + str(n) + '.mp3'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)
        pygame.mixer.Channel(c).play(w)

    def saw(n, c):
        path = r'audio\saw\saw_' + str(n) + '.mp3'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)
        pygame.mixer.Channel(c).play(w)

    def sin(n, c):
        path = r'audio\sin\sin_' + str(n) + '.mp3'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)
        pygame.mixer.Channel(c).play(w)

    color_post = {0: 1, 1: 5, 2: 2, 3: 6, 4: 3, 5: 7, 6: 4, 7: 8, 8: 0}
    post_color = {v: k for k, v in color_post.items()}
    def glove(glove_values):

        # print()

        # print(glove_values)

        midi_colors = []
        new_rule = []

        value_g = (int(glove_values[6] / 64) * 2 ** 0) + (int(glove_values[7] / 64) * 2 ** 1) + (
                int(glove_values[8] / 64) * 2 ** 2) + (
                          int(glove_values[9] / 64) * 2 ** 3) + (int(glove_values[10] / 64) * 2 ** 4)
        # print(value_g)

        # if glove_values[2] > 64:
        #     if value_0 == 17:
        #         for x in range(canvas_rows):
        #                 for y in range(canvas_row_width):
        #                     canvas[x, y] = 0
        #
        #         phrase = '

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
        # for x in range(len(i_rule_0)):
        #     if midi_colors[x%len(midi_colors)] > 0:
        #         midi_colors[x%len(midi_colors)] -= 1
        #         new_rule.append(color_post[x%(len(midi_colors)-1)])

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


    #active variables
    run = 1
    rule = 30
    channel = 0
    pause = 0
    start = 0
    step = 0
    origin_rule = 0
    bv = base ** view
    bbv = base ** base ** view

    #eb
    eb = 0

    #input augments
    midi_inputs = 1
    gloves = 2
    right_letter = 0
    left_letter = 0
    voice = ' '

    #Peacekeeper
    pce = 4
    turn = 0
    streak = 0
    balance = [0, 0]
    angle = 0
    health = [WIDTH/2, WIDTH/2]
    states = [0, 0, 0]
    downs = [1, 1]
    juice = 3
    chalk = 0
    cad = []

        #1
    charge_0 = [0, 0]
    path_0 = [(0, 0), (0, 0)]
    power_0 = 0
    m_0 = 0

    charge_1 = [0, 0]
    path_1 = [(0, 0), (0, 0)]
    power_1 = 0
    m_1 = 0

        #2
    wu = 0
    my = 0
    walks = [0, 0, 0, 0, 0, 0, 0]

        #3
    me = 0
    ac_trig = 16
    toggles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    wake = [0, 0, 0, 0, 0]


    #input maps
    x_position_g0v = 0
    y_position_g0v = 1
    x_position_g1v = 12
    y_position_g1v = 13

    cell_vel = 1

    #micro_brush
    mixer.init()

    #streams
    streams = 3
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

    #record keeping
    journal = dict()
    page = []
    rule_point = list()

    #ui
    ui_on = 0
    ui_scale = 14
    bar_height = 15000
    bar_width = ui_scale + int(ui_scale / 1)
    cv_pos = 0


    midi_weights_0 = []
    midi_weights_1 = []


    #glove emthods
    g_brush = 4
    number_of_sensors = 12

    zero_out = 3200
    spin_speed = 8

    #chaos console
    input_box = 0
    v_input = ''

    #cell design
    canvas_rows = int(HEIGHT) + 1
    canvas_row_width = int(CELL_WIDTH)

    brush_width = 100
    brush_height = 100
    brush_scale_h = int(canvas_rows / 127)
    brush_scale_w = int(canvas_row_width / 127)

    brush_min_0 = 14
    brush_min_1 = 14

    spin = 0

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

    if start == 0:

        cells_a[0, int(cell_row_width / 2)] = value_color[1]
        cells_b[0, int(cell_row_width / 2)] = value_color[1]

    else:

        #fix this

        cells_a[0] = rule_gen_2(start, base, cell_row_width)[1]


    # print("")
    # print(cells_a)

    # print("")
    # print("genisis")
    # print(cells_a)

    for x in range(cell_rows - 1):

        cells_a = np.roll(cells_a, 1, 0)
        cells_b = np.roll(cells_b, 1, 0)
        # cells_a[0] = Color_cells_1d(d_rule, cell_row_width, cells_a[1])

        for y in range(cell_row_width):

            cells_a[0, y] = value_color[d_rule_0[tuple(viewer_1d(cells_a[1], y, view, [], color_value))]]
            cells_a[0, y] = value_color[d_rule_1[tuple(viewer_1d(cells_b[1], y, view, [], color_value))]]

    # print("")
    # print('value_color')
    # print(cells_a)


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

    if origin_rule == 0:

        magnify = 4
        colors = 1
        step_size = int(base ** view / (base - 1) / magnify)

        # print("")
        # print("step_size")
        # print(step_size)
        # print(base ** view)
        # print(base - 1)

        o_r = rule_gen(0, base)[1]

        # print(o_r)

        for x in range(int((base ** view) / step_size) + 1):

            # print("step_size * x")
            # print(step_size * x)
            # print("current place")
            # print(-((step_size * x + 1) % bv))

            if x > 0:

                o_r[-((step_size * x + 1) % bv)] = x % colors + 1

            else:

                o_r[-((step_size * x + 1) % bv)] = 1


        o_r[-1] = 1

        origin_rule = decimal(o_r, base)

        print("")
        print("origin rule")
        print(o_r)
        print(origin_rule)

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

            #notes
            if turn == 0:
                note_0 = (int(glove_values[0]/64)+int(glove_values[1]/64)*2)
                note_1 = (int(glove_values[12]/64)+int(glove_values[13]/64)*2)
            else:
                note_0 = (int(glove_values[12]/64)+int(glove_values[13]/64)*2)
                note_1 = (int(glove_values[0] / 64) + int(glove_values[1] / 64) * 2)

            #keeper 1
            if glove_values[11] < 4:

                states[0] = 0

                #power clear
                if charge_0[0] == 0:
                    power_0 = 0

                #path set
                if charge_0[0] != charge_0[1]:

                    if balance[0] == 0:
                        path_0[charge_0[0]] = (glove_values[0], glove_values[1])
                    charge_0[1] = charge_0[0]


                    #start
                    if charge_0[0] == 0:
                        if turn == 0:
                            kick(0)
                            bass(note_0, 1)
                            channel += 2
                        else:
                            pluck(note_0, 2)
                            channel += 1
                    #end
                    if charge_0[0] == 1:
                        if turn == 0:
                            bass(note_0, 3)
                            kick(4)
                            shake(5)
                            channel += 3
                        else:
                            pluck(note_0, 6)
                            channel += 1

                        num = path_0[1][1] - path_0[0][1]
                        den = path_0[1][0] - path_0[0][0]

                        # print()
                        # print('1')
                        # print(power_0)

                        #m set
                        try:
                            m_0 = num/den
                            # print(m_0)
                        #m = inf
                        except:
                            m_0 = 1000
                            # print(m_0)
                            # print("holy fuck")

                        balance[0] = 1
            #move
            else:

                states[0] = 1

                #charger
                if charge_0[0] == charge_0[1]:
                    charge_0[0] += 1
                    charge_0[0] = charge_0[0] % 2

                    if turn == 0:
                        hh(charge_0[0], 7)
                        channel += 1
                    else:
                        pluck(note_1, 8)
                        channel += 1

                #power
                if glove_values[11] > power_0:
                    power_0 = glove_values[11]


            #keeper 2
            if glove_values[23] < 4:

                states[1] = 0

                #power clear
                if charge_1[0] == 0:
                    power_1 = 0

                #path set
                if charge_1[0] != charge_1[1]:

                    if balance[1] == 0:
                        path_1[charge_1[0]] = (glove_values[12], glove_values[13])
                    charge_1[1] = charge_1[0]

                    #start
                    if charge_1[0] == 0:
                        if turn == 1:
                            kick(9)
                            bass(note_0, 10)
                            channel += 2
                        else:
                            pluck(note_0, 11)
                            channel += 1
                    #end
                    if charge_1[0] == 1:
                        if turn == 1:
                            bass(note_0, 12)
                            kick(13)
                            shake(14)
                            channel += 3
                        else:
                            pluck(note_0, 15)
                            channel += 1

                        num = path_1[1][1] - path_1[0][1]
                        den = path_1[1][0] - path_1[0][0]

                        # print()
                        # print('2')
                        # print(power_1)

                        try:
                            m_1 = num/den
                            # print(m_1)

                        except:
                            m_1 = 1000
                            # print(m_1)
                            # print("holy fuck")

                        balance[1] = 1
            #move
            else:

                states[1] = 1

                if charge_1[0] == charge_1[1]:
                    charge_1[0] += 1
                    charge_1[0] = charge_1[0] % 2

                    if turn == 1:
                        hh(charge_1[0], 16)
                        channel += 1
                    else:
                        pluck(note_1, 17)
                        channel += 1

                if glove_values[23] > power_1:
                    power_1 = glove_values[23]


            if balance[0] + balance[1] == 2:

                # print()
                # print("")

                try:
                    angle = math.degrees(math.atan(abs((m_1 - m_0)/(1 + m_1 * m_0))))
                except:
                    print('fuck off')

                if angle > 80 and states[2] == 1:
                    canvas = np.zeros((canvas_rows, canvas_row_width, 3), dtype='uint8')
                    turn += 1
                    turn = turn % 2
                    snare(18)
                    channel += 1
                    print("parry")
                    print("turn")
                    print(turn)
                    print(m_0, m_1)
                    print(path_0, path_1)
                    print(angle)


                if turn == 0:

                    # print('health')
                    # print(health[1])
                    # print('strike')
                    # print((power_0 - int(power_1*(angle/90)))/10)
                    if states[2] == 0:
                        # print("half_1")
                        power_1 = int(power_1/2)

                    health[1] = health[1] - (power_0 - int(power_1*(angle/90))) * juice

                    # print(health[1])

                else:

                    # print("health")
                    # print(health[0])
                    # print('strike')
                    # print((power_1 - int(power_0*(angle/90)))/10)
                    if states[2] == 0:
                        # print("half_0")
                        power_0 = int(power_0/2)


                    health[0] = health[0] - (power_1 - int(power_0*(angle/90))) * juice

                    # print(health[1])

                # print("balanced")
                # print('turn')
                # print(turn)
                # print("angle")
                # print(angle)
                # print("power")
                # print(power_0, power_1)
                # print(streak)


                balance[0] = 0
                balance[1] = 0
                streak += 1

                if health[0] < 0:
                    downs[0] += 1
                    health[0] = WIDTH/2
                    print("")
                    print("down_0")
                    print(downs)
                if health[1] < 0:
                    downs[1] += 1
                    health[1] = WIDTH/2
                    print("")
                    print("downs_1")
                    print(downs)






            if states[0] + states[1] == 2:
                states[2] = 1
                # print("moving")
            elif states[0] + states[1] == 0:
                states[2] = 0
                # print("still")

        if pce == 2:

            # print()
            # print("peace")

            for x in range(3):
                # print(glove_values[x], walks[x])

                if abs(walks[x] - glove_values[x]) > 16:
                    print()
                    print("walking " + str(x))
                    print(glove_values[x], walks[x])

                    if walks[x] > glove_values[x]:
                        walks[x + 3] = 0
                    else:
                        walks[x + 3] = 1

                    print(walks[x + 3])

                    walks[x] = glove_values[x]

                    feet = (walks[3] + walks[4]*2 + walks[5]*4)

                    if feet  != walks[-1]:
                        ome(feet, feet)
                        walks[-1] = feet
                        eb = HEIGHT



            brush_min_0 = int(glove_values[2]/4) + 3
            brush_min_1 = int(glove_values[2]/4) + 3

        if pce == 3:
            # print(glove_values[6:11])

            brush_min_0 = int(glove_values[2] / 4) + 14
            brush_min_1 = int(glove_values[2] / 4) + 14
            me = int(glove_values[2]/64) + int(abs((glove_values[0] - 127)/64))*2 + int(glove_values[1]/64)*4
            # print(int(abs((glove_values[0] - 128)/64)))


            #keeper 1
            if glove_values[11] < ac_trig:

                states[0] = 0

                #power clear
                if charge_0[0] == 0:
                    power_0 = 0

                #path set
                if charge_0[0] != charge_0[1]:

                    if balance[0] == 0:
                        path_0[charge_0[0]] = (glove_values[0], glove_values[1])
                    charge_0[1] = charge_0[0]


                    #start
                    if charge_0[0] == 0:
                        kick(6)
                    #end
                    if charge_0[0] == 1:
                        if turn == 0:
                            kick(6)
                            shake(7)
            #move
            else:

                states[0] = 1

                #charger
                if charge_0[0] == charge_0[1]:
                    charge_0[0] += 1
                    charge_0[0] = charge_0[0] % 2


                    hh(charge_0[0], 7)


                #power
                if glove_values[11] > power_0:
                    power_0 = glove_values[11]


            if int(glove_values[6]/64) != toggles[0]:
                toggles[0] = int(glove_values[6]/64)
                eb = HEIGHT

                ome(me, 1)
            if int(glove_values[7]/64) != toggles[1]:
                toggles[1] = int(glove_values[7]/64)
                # print(toggles)

                pong(0 + me, 2)
            if int(glove_values[8]/64) != toggles[2]:
                toggles[2] = int(glove_values[8]/64)
                # print(toggles)

                pong(2 + me, 3)
            if int(glove_values[9]/64) != toggles[3]:
                toggles[3] = int(glove_values[9]/64)
                # print(toggles)

                pong(4 + me, 4)
            if int(glove_values[10]/64) != toggles[4]:
                toggles[4] = int(glove_values[10]/64)
                # print(toggles)

                pong(7 + me, 5)

        if pce == 4:
            # print(glove_values[6:11])

            brush_min_0 = int(glove_values[2] / 4) + 2
            brush_min_1 = int(glove_values[14] / 4) + 2
            me = int(glove_values[2]/64) + int(abs((glove_values[0] - 127)/64))*2 + int(glove_values[1]/64)*4
            my = int(glove_values[14]/64) + int((glove_values[12])/64)*2 + int(glove_values[13]/64)*4
            # print(my)


            if int(glove_values[6]/64) != toggles[0]:
                toggles[0] = int(glove_values[6]/64)
                if toggles[0] == 1:
                    eb = HEIGHT
                    sin(0 + scale_shift[me], 0 + wake[0])
                    wake[0] += 1
                    wake[0] = wake[0]%4

            if int(glove_values[7]/64) != toggles[1]:
                toggles[1] = int(glove_values[7]/64)
                if toggles[1] == 1:
                    sin(12 + scale_shift[me], 4 + wake[1])
                    wake[1] += 1
                    wake[1] = wake[1]%4

            if int(glove_values[8]/64) != toggles[2]:
                toggles[2] = int(glove_values[8]/64)
                if toggles[2] == 1:
                    sin(chord_types[my%3][0] + scale_shift[me], 8 + wake[2])
                    wake[2] += 1
                    wake[2] = wake[2]%4

            if int(glove_values[9]/64) != toggles[3]:
                toggles[3] = int(glove_values[9]/64)
                if toggles[3] == 1:
                    sin(chord_types[my%3][1] + scale_shift[me], 12 + wake[3])
                    wake[3] += 1
                    wake[3] = wake[3]%4

            if int(glove_values[10]/64) != toggles[4]:
                toggles[4] = int(glove_values[10]/64)
                if toggles[4] == 1:
                    sin(24 + scale_shift[me], 16 + wake[4])
                    wake[4] += 1
                    wake[4] = wake[4]%4

            if int(glove_values[18]/64) != toggles[5]:
                toggles[5] = int(glove_values[18]/64)
                if toggles[5] == 1:
                    eb = HEIGHT
                    saw(0 + scale_shift[me], 0 + wake[0])
                    wake[0] += 1
                    wake[0] = wake[0]%4

            if int(glove_values[19]/64) != toggles[6]:
                toggles[6] = int(glove_values[19]/64)
                if toggles[6] == 1:
                    saw(12 + scale_shift[me], 4 + wake[1])
                    wake[1] += 1
                    wake[1] = wake[1]%4

            if int(glove_values[20]/64) != toggles[7]:
                toggles[7] = int(glove_values[20]/64)
                if toggles[7] == 1:
                    saw(chord_types[my%3][0] + scale_shift[me], 8 + wake[2])
                    wake[2] += 1
                    wake[2] = wake[2]%4

            if int(glove_values[21]/64) != toggles[8]:
                toggles[8] = int(glove_values[21]/64)
                if toggles[8] == 1:
                    saw(chord_types[my%3][1] + scale_shift[me], 12 + wake[3])
                    wake[3] += 1
                    wake[3] = wake[3]%4

            if int(glove_values[22]/64) != toggles[9]:
                toggles[9] = int(glove_values[22]/64)
                if toggles[9] == 1:
                    saw(24 + scale_shift[me], 16 + wake[4])
                    wake[4] += 1
                    wake[4] = wake[4]%4

            right_letter = int(glove_values[6]/64) + int(glove_values[7]/64)*2 + int(glove_values[8]/64)*4 + int(glove_values[9]/64)*8 + int(glove_values[10]/64)*16
            left_letter = int(glove_values[18]/64) + int(glove_values[19]/64)*2 + int(glove_values[20]/64)*4 + int(glove_values[21]/64)*8 + int(glove_values[22]/64)*16

            if right_letter == left_letter and glove_values[11] < 3:
                if voice[-1] != value_letter[right_letter]:
                    voice += value_letter[right_letter]
                    cad.append(time.time())
                    print()
                    print(voice)
                    print(cad)
                if right_letter == 0 and len(voice)>1:
                    voice = ' '
                    c_0 = cad[0]
                    for x in range(len(cad)):
                        cad[x] = cad[x]-c_0
                    print(cad)











        if eb > 0:
            zero = np.zeros((1, canvas_row_width, 3), dtype='uint8')
            eb = eb - 1
            canvas[eb] = zero


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
                        cells_a[(0 + momentum[stream_direction_0[step % stream_buffer % len(stream_direction_0)]]) % (len(cells_a[0]) - 1), x] = value_color[d_rule[tuple(viewer_1d(cells_a[1], x, view, [], color_value))]]

                if g_brush >= 2:

                    for x in range(len(cells_a[0])):
                        cells_a[(0 + momentum[stream_direction_0[step % stream_buffer % len(stream_direction_0)]]) % (
                                    len(cells_a[0]) - 1), x] = value_color[
                             d_rule_0[tuple(viewer_1d(cells_a[1], x, view, [], color_value))]]

                    for x in range(len(cells_b[0])):
                        cells_b[(0 + momentum[stream_direction_0[step % stream_buffer % len(stream_direction_0)]]) % (
                                len(cells_b[0]) - 1), x] = value_color[
                            d_rule_1[tuple(viewer_1d(cells_b[1], x, view, [], color_value))]]

                if len(stream_direction_0) > 0:

                    cells_a = np.rot90(cells_a, 4 - stream_direction_0[step % stream_buffer % len(stream_direction_0)], (0, 1))

                    # cells_a = np.rot90(cells_a, 3, (0, 1))
                    # cells_a = np.rot90(cells_a, 2, (0, 1))
                    # cells_a = np.rot90(cells_a, 1, (0, 1))


                line = tuple(color_value[tuple(v)] for v in cells_a[0])
                page.append(line)


                rule = str()
                for ir in i_rule_0:
                    rule += str(ir)
                rule = (rule, datetime.now())

                if i_rule_0 != rule_point:
                    # print()
                    # print()
                    # print("align")
                    # print("i_rule & rule_point")
                    # print(i_rule)
                    # print(rule_point)
                    rule_point = i_rule_0[::]
                    # print()
                    # print("i_rule & rule_point")
                    # print(i_rule)
                    # print(rule_point)

                    if rule not in journal:
                        journal[rule] = []
                        journal[rule].append(page)

                    else:
                        journal[rule].append(page)

                    page = []

                step += 1
            for y in range(cell_vel_1):

                cells_b = np.rot90(cells_b, stream_direction_1[step % stream_buffer % len(stream_direction_1)], (0, 1))

                cells_b = np.roll(cells_b, 1, 0)

                if g_brush == 1:
                    for x in range(len(cells_b[0])):
                        cells_b[(0 + momentum[stream_direction_1[step % stream_buffer % len(stream_direction_1)]]) % (
                                    len(cells_b[0]) - 1), x] = value_color[
                            d_rule[tuple(viewer_1d(cells_b[1], x, view, [], color_value))]]

                if g_brush >= 2:

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

                line = tuple(color_value[tuple(v)] for v in cells_b[0])
                page.append(line)

                rule = str()
                for ir in i_rule_0:
                    rule += str(ir)
                rule = (rule, datetime.now())

                if i_rule_0 != rule_point:
                    # print()
                    # print()
                    # print("align")
                    # print("i_rule & rule_point")
                    # print(i_rule)
                    # print(rule_point)
                    rule_point = i_rule_0[::]
                    # print()
                    # print("i_rule & rule_point")
                    # print(i_rule)
                    # print(rule_point)

                    if rule not in journal:
                        journal[rule] = []
                        journal[rule].append(page)

                    else:
                        journal[rule].append(page)

                    page = []

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



                #console commands
                elif event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_SHIFT:

                    if input_box == 0:

                        input_box = 1

                    else:

                        if len(v_input) != 0:

                            input_list = v_input.split()

                            # print(" ")
                            # print("input_list")
                            # print(input_list)
                            # print(len(input_list))
                            # print(len(input_list[0]))

                            if len(input_list) > 1:

                                if input_list[0] == 'base':

                                    print("##########based##########")

                                    base = int(input_list[1])
                                    bv = base ** view

                                    step_size = int(base ** view / (base - 1) / magnify)
                                    o_r = rule_gen(0, base)[1]
                                    for x in range(int((base ** view) / step_size) + 1):

                                        if x > 0:

                                            o_r[-((step_size * x + 1) % bv)] = x % colors + 1

                                        else:

                                            o_r[-((step_size * x + 1) % bv)] = 1
                                    o_r[-1] = 1
                                    origin_rule = decimal(o_r, base)
                                    ir_height = base

                                    # colors
                                    if base < 5:

                                        value_color = {0: (0, 0, 0), 1: (255, 0, 255), 2: (0, 255, 255),
                                                       3: (255, 255, 0), 4: (192, 192, 192), 5: (255, 0, 0),
                                                       6: (0, 255, 0), 7: (0, 0, 255)}
                                        color_value = {v: k for k, v in value_color.items()}

                                    else:

                                        value_color = {0: (0, 0, 0), 1: (32, 32, 32), 2: (255, 0, 255),
                                                       3: (0, 255, 255), 4: (255, 255, 0), 5: (192, 192, 192),
                                                       6: (255, 0, 0), 7: (0, 255, 0), 8: (0, 0, 255)}
                                        color_value = {v: k for k, v in value_color.items()}

                                    print("origin rule")
                                    print(o_r)
                                    print(origin_rule)

                                    d_rule, i_rule = rule_gen(origin_rule, base)

                                    print("d_rule, i_rule")
                                    print(d_rule)
                                    print(i_rule)
                                    print("new_row")
                                    print(rule_gen_2(origin_rule, base, cell_row_width)[1])

                                    # mitosis
                                    for x in range(cell_vel):

                                        cells_a = np.roll(cells_a, 1, 0)

                                        clunk = 0

                                        for y in rule_gen_2(origin_rule, base, cell_row_width)[1]:

                                            cells_a[0, clunk] = value_color[y]

                                            clunk += 1

                                elif input_list[0] == 'name':
                                    j_name = input_list[1]

                                    write = 1

                                elif input_list[0] == 't-clear':

                                    trigger_0 = 0
                                    trigger_1 = 0
                                    trigger_2 = 0
                                    trigger_3 = 0
                                    trigger_4 = 0
                                    trigger_5 = 0
                                    trigger_6 = 0
                                    trigger_7 = 0
                                    trigger_8 = 0

                                elif input_list[0] == 'dam':

                                    stream_direction = deque(maxlen=stream_buffer)


                            elif v_input == 'write':

                                write = 1

                            elif input_list[0] == 'invalid':

                                v_input = ''

                            else:

                                try:

                                    d_rule, i_rule = rule_gen(int(v_input), base)

                                except:

                                    v_input = 'invalid'

                                    continue

                            v_input = ''

                        input_box = 0

                elif event.key == pygame.K_PERIOD:

                    sin(wu, 1)
                    # saw(wu, 1)

                    wu += 1
                    print("wu")
                    print(wu)

                elif event.key == pygame.K_UP:

                    stream_direction.append(2)

                    # print('up')
                    # print(stream_direction)

                elif event.key == pygame.K_RIGHT:

                    stream_direction.append(1)

                    # print("right")
                    # print(stream_direction)

                elif event.key == pygame.K_DOWN:

                    stream_direction.append(0)

                    # print("down")
                    # print(stream_direction)

                elif event.key == pygame.K_LEFT:

                    stream_direction.append(3)

                    # print('left')
                    # print(stream_direction)


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

            value_0 = (int(glove_values[6] / 64) * 2 ** 0) + (int(glove_values[7] / 64) * 2 ** 1) + (
                    int(glove_values[8] / 64) * 2 ** 2) + (
                              int(glove_values[9] / 64) * 2 ** 3) + (int(glove_values[10] / 64) * 2 ** 4)

            value_1 = (int(glove_values[18] / 64) * 2 ** 0) + (int(glove_values[19] / 64) * 2 ** 1) + (
                    int(glove_values[20] / 64) * 2 ** 2) + (
                              int(glove_values[21] / 64) * 2 ** 3) + (int(glove_values[22] / 64) * 2 ** 4)

            # stream direction
            if streams == 3:

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


            if g_brush == 4:

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

                full_rule, midi_weights_1 = glove(glove_values[12:])
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


Chaos_Window(9, 1, 0, 1)




