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

sys.setrecursionlimit(999999999)

pygame.font.init()

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
# WIDTH , HEIGHT = current_display.current_w - 50, current_display.current_h - 100
WIDTH, HEIGHT = 1600, 800
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
    ts_0 = time.time()

    #window
    if analytics == 1:

        CELL_WIDTH = HEIGHT

    else:

        CELL_WIDTH = WIDTH


    #colors
    if base < 5:

        value_color = {0:(0, 0, 0), 1:(255, 0, 255), 2:(0, 255, 255), 3:(255, 255, 0)}
        color_value = {v:k for k, v in value_color.items()}

    else:

        value_color = {0:(0, 0, 0), 1:(32, 32, 32), 2:(255, 0, 255), 3:(0, 255, 255), 4:(255, 255, 0), 5:(192, 192, 192),
                      6:(255, 0, 0), 7:(0, 255, 0), 8:(0, 0, 255)}
        color_value = {v:k for k, v in value_color.items()}


    def redraw_window(input_box, v_input, zero_count, step_show, triggers, dt, timer):

        #preparation


        #cell drawing
        WIN.blit(pygame.surfarray.make_surface(np.moveaxis(cells_a, 0, 1)), (0, 0))


        #ui drawing
        if ui_on == 1:

            [pygame.draw.rect(WIN, value_color[i_rule[rule_models.index(cell)]], cell) for cell in rule_models]

        #vanilla labels
        rule_label_0_b = main_font.render(f"RUL3: {i_rule[0:int((base ** view) / 2)]}", 1, (255, 255, 255))
        rule_label_1_b = main_font.render(f"          {i_rule[int((base ** view) / 2):int((base ** view))]}", 1,
                                          (255, 255, 255))

        step_label_b = main_font.render(f"5T3P: {step}", 1, (255, 255, 255))
        rand_count_l = main_font.render(f"C0UNT: {rand_count}", 1, (255, 255, 255))
        time_label = lable_font.render(str(int(timer/60)), 1, (255, 255, 255))
        step_length = main_font.render(f"5T3P: {step- step_0}", 1, (255, 255, 255))


        #glove labels



        #vanilla blit
        if step_show == 1:

            WIN.blit(rule_label_0_b, (10, HEIGHT - 120))
            WIN.blit(rule_label_1_b, (7, HEIGHT - 80))

        # WIN.blit(step_label_b, (WIDTH - step_label_b.get_width(), 10))
        # WIN.blit(rand_count_l, (WIDTH - rand_count_l.get_width(), 50))
        # WIN.blit(time_label, (WIDTH - time_label.get_width() - 20, 10))
        WIN.blit(step_length, (WIDTH - step_length.get_width() - 20, 20))

        # WIN.blit(zero_count, (WIDTH - zero_count.get_width(), 90))
        # WIN.blit(origin_value, (WIDTH - origin_value.get_width(), 90))


        #glove blit
        # WIN.blit(trigger_thresholds, (WIDTH - trigger_thresholds.get_width(), HEIGHT - 50))
        # WIN.blit(trigger_values, (WIDTH - trigger_values.get_width(), HEIGHT - 100))
        # WIN.blit(tsp_values, (CELL_WIDTH + 120, 170))
        # WIN.blit(tsp_view, (CELL_WIDTH + 120, 135))

        # WIN.blit(gv, (WIDTH - gv.get_width(), 90))


        #conosle inputs
        if input_box == 1:
            v_input_r = small_font.render(v_input, 1, (0, 0, 0))

            type_box = pygame.Rect(10, 10, v_input_r.get_width() + 2, v_input_r.get_height() + 2)

            pygame.draw.rect(WIN, (255, 255, 255), type_box)

            WIN.blit(v_input_r, (11, 11))

        if list_count != 0:
            draw_text(str(list_count), small_font, (255, 255, 255), WIN, 11, 33)

        # draw_text(str(dt), small_font, (255, 255, 255), WIN, WIDTH - 40, 80)

        pygame.display.update()

    def input(letter, base, page, input_box, v_input):

        if echoing == 1:

            echo = 0

        echo = 1

        if input_box == 1:
            v_input += letter

        bv = base ** view

        if letter not in press:
            press[letter] = 0
        else:
            press[letter] += 1

        if echoing == 1:

            if press[letter] % 1 ==0:

                echo = 1


        place = int((letter_values[letter] + ((press[letter] % (int(bv / len(letter_values)) + 1)) * int(
            (bv / int(bv / len(letter_values) + 1))))) % bv)

        # print(' ')
        # print("place")
        # print(place)
        # print(letter_values[letter])
        # print((press[letter] % (int(bv / len(letter_values)) + 1)))
        # print((bv / int(bv / len(letter_values) + 1)))
        # print(bv)

        if i_rule[place] == 0:

            i_rule[place] = 1
            d_rule[list(d_rule.keys())[place]] = 1

            if echo % 2 == 0:

                # print('len(i_rule)')
                # print(len(i_rule))
                # print('int(place + len(i_rule)/2 % len(i_rule)) - 1')
                # print(int((place + len(i_rule)/2) % len(i_rule)) - 1)
                # print('list(d_rule.keys()))')
                # print(len(list(d_rule.keys())))

                i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 1
                d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 1

        elif i_rule[place] == 1:

            # print("i_rule_1")
            # print(i_rule)

            if base == 2:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 2
                d_rule[list(d_rule.keys())[place]] = 2

            if echo % 2 == 0:

                # print('echo')

                if base == 2:

                    # print('len(i_rule)')
                    # print(len(i_rule))
                    # print('int(place + len(i_rule)/2 % len(i_rule)) - 1')
                    # print(int(place + len(i_rule)/2 % len(i_rule)) - 1)
                    # print('list(d_rule.keys()))')
                    # print(len(list(d_rule.keys())))

                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 2
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 2

                # print("i_rule_2")
                # print(i_rule)

        elif i_rule[place] == 2:

            if base == 3:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 3
                d_rule[list(d_rule.keys())[place]] = 3

            if echo % 2 == 0:

                # print('echo')

                if base == 3:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 3
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 3

        elif i_rule[place] == 3:

            if base == 4:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 4
                d_rule[list(d_rule.keys())[place]] = 4

            if echo % 2 == 0:

                # print('echo')

                if base == 4:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 4
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 4

        elif i_rule[place] == 4:

            if base == 5:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 5
                d_rule[list(d_rule.keys())[place]] = 5

            if echo % 2 == 0:

                # print('echo')

                if base == 5:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0

                else:
                    i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 5
                    d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 5

        else:

            i_rule[place] = 0
            d_rule[list(d_rule.keys())[place]] = 0

            if echo % 2 == 0:

                print('echo')

                i_rule[int((place + len(i_rule)/2) % len(i_rule)) - 1] = 0
                d_rule[list(d_rule.keys())[int((place + len(i_rule)/2) % len(i_rule)) - 1]] = 0


        # if rule not in journal:
        #     journal[rule] = []
        #     journal[rule].append(line)
        #
        # else:
        #     journal[rule].append(line)

        return v_input

    def fibonacci(a, duration, list, calls=1, b=0):

        if b == 0:
            b = a

            list.append(a)
            list.append(b)

        c = a + b

        for x in range(calls):
            list.append(c)

        if duration != 0:
            duration -= 1

            fibonacci(c, duration, list, calls, a)

    def rl_gen(input_list):

        if input_list[0] == 'm':

            input_list = input_list[1:]

            if len(input_list) == 2:

                rule_list = [x * int(input_list[1]) for x in range(int(input_list[0]))]

            elif len(input_list) == 4:

                # print(" ")
                # print("input_list")
                # print(input_list)

                rule_list = [x * int(input_list[3]) for x in
                             range(int(input_list[0]), int(input_list[1]), int(input_list[2]))]

                # print(" ")
                # print("len() 4")
                # print(rule_list)

            elif len(input_list) == 5:

                rule_list = []

                rule_list_0 = [x * int(input_list[3]) for x in
                               range(int(input_list[0]), int(input_list[1]), int(input_list[2]))]

                for rule in rule_list_0:

                    for x in range(int(input_list[4])):
                        rule_list.append(rule)

                # print(rule_list)

            list_count = len(rule_list)

        elif input_list[0] == 'fib':

            input_list = input_list[1:]

            rule_list = []

            if len(input_list) == 1:

                fibonacci(1, int(input_list[0]), rule_list)

            elif len(input_list) == 2:

                fibonacci(1, int(input_list[0]), rule_list, int(input_list[1]))

            elif len(input_list) == 3:

                fibonacci(int(input_list[2]), int(input_list[0]), rule_list, int(input_list[1]))

            # print(" ")
            # print("rule_list")
            # print(rule_list)

            list_count = len(rule_list)

        elif input_list[0] == 'sqr':

            # print(" ")
            # print("sqr")

            input_list = input_list[1:]

            if len(input_list) == 2:
                rule_list = [x ** int(input_list[1]) for x in range(int(input_list[0]))]

                # print('rule_list')
                # print(rule_list)

            list_count = len(rule_list)

        elif input_list[0] == 'exp':

            # print(" ")
            # print("sqr")

            input_list = input_list[1:]

            rule_list = []

            if len(input_list) == 2:

                # print("")
                # print("exp len 2")
                # print(input_list)

                rule_list_0 = [x ** x for x in range(int(input_list[0]))]

                # print("rule_list_0")
                # print(rule_list_0)

                for rule in rule_list_0:

                    # print("rule")
                    # print(rule)
                    #
                    # print(input_list[1])

                    for x in range(int(input_list[1])):
                        rule_list.append(rule)

                # print('rule_list')
                # print(rule_list)

            list_count = len(rule_list)

        return rule_list, list_count

    def place_change(place):

        # print("place_change")
        # print(place)

        place = place % (base ** view)

        if i_rule[place] == 0:

            i_rule[place] = 1
            d_rule[list(d_rule.keys())[place]] = 1

        elif i_rule[place] == 1:

            # print("i_rule_1")
            # print(i_rule)

            if base == 2:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 2
                d_rule[list(d_rule.keys())[place]] = 2

        elif i_rule[place] == 2:

            if base == 3:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 3
                d_rule[list(d_rule.keys())[place]] = 3

        elif i_rule[place] == 3:

            if base == 4:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 4
                d_rule[list(d_rule.keys())[place]] = 4

        elif i_rule[place] == 4:

            if base == 5:
                i_rule[place] = 0
                d_rule[list(d_rule.keys())[place]] = 0

            else:
                i_rule[place] = 5
                d_rule[list(d_rule.keys())[place]] = 5

        else:

            i_rule[place] = 0
            d_rule[list(d_rule.keys())[place]] = 0


    #active variables
    run = 1
    pause = 0
    FPS = 120
    rule = 30
    start = 0
    step = 0
    step_0 = 0
    step_show = 0
    clock = pygame.time.Clock()
    origin_rule = 0
    bv = base ** view
    bbv = base ** base ** view
    rule_window_scale = 2

    #streams
    stream = 0
    stream_buffer = 8
    stream_direction = deque(maxlen=stream_buffer)
    stream_direction.append(0)
    momentum = {0:0, 1:0, 2:0, 3:0}
    momentum_step = 3
    momentum_scale_scale = 3

    #record keeping
    journal = dict()
    page = []
    rule_book = []
    press = dict()
    press_vault = dict()
    rule_point = list()
    bookmarks = [0]

    #random
    r_i = 0
    rand_count = 0
    iterate = 0

    #ui
    ui_on = 1
    ui_scale = 20

    rule_models = []
    precursor = []

    ir_height = base
    bar_height = 40
    bar_width = 20

    x_offset = CELL_WIDTH + 40
    y_offset = 160 + ui_scale * ir_height

    #input augments
    echoing = 0
    randomizer = 0
    midi_inputs = 1

    #glove emthods
    g_char = 0
    g_rule = 0
    g_words = 1

    zero_out = 6400
    zero_full = zero_out*9
    high_trigger = 80
    low_trigger = 40
    left_triggers = [0 for x in range(8)]
    right_triggers = [0 for x in range(8)]


    t_plus = 2
    t_minus = 1

    #chaos console
    input_box = 0
    list_count = 0
    v_input = ''
    write = 0
    j_name = ''
    max_rule = base ** base ** view

    #cell design
    cell_row_width = int(CELL_WIDTH)
    cell_rows = int(HEIGHT) + 1
    d_rule, i_rule = rule_gen(rule, base)

    print("")
    print("d_rule")
    print(d_rule)

    print("")
    print('cells: width height')
    print((cell_row_width, cell_rows))

    cells_a = np.zeros((cell_rows, cell_row_width, 3), dtype='uint8')

    if start == 0:

        cells_a[0, int(cell_row_width / 2)] = value_color[1]

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
        # cells_a[0] = Color_cells_1d(d_rule, cell_row_width, cells_a[1])

        for y in range(cell_row_width):

            cells_a[0, y] = value_color[d_rule[tuple(viewer_1d(cells_a[1], y, view, [], color_value))]]

    # print("")
    # print('value_color')
    # print(cells_a)


    if midi_inputs == 1:

        pygame.init()
        pygame.midi.init()
        pygame.fastevent.init()
        event_get = pygame.fastevent.get
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

        glove_values = [x for x in range(22)]
        glove_sums = [x for x in range(2)]

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

    if ui_on == 1:

        clunk = 0
        rule_models = []
        precursor = []

        ir_split = []

        [ir_split.append(i_rule[x * int(len(i_rule) / ir_height):(x + 1) * int(len(i_rule) / ir_height)]) for x in
         range(ir_height)]

        # x_offset = CELL_WIDTH + 40
        # y_offset = 20 + ui_scale + y

        [[rule_models.append(
            pygame.Rect(1 * ui_scale * x + x_offset, 1 * ui_scale + 20 + ui_scale * y, ui_scale, ui_scale)) for x in
          range(len(ir_split[y]))] for y in range(ir_height)]

        # x_offset = CELL_WIDTH + 40
        # y_offset = 20 + ui_scale * (ir_height + 1)

        [precursor.append(
            pygame.Rect(1 * ui_scale * x + x_offset, 1 * ui_scale + 20 + ui_scale * (ir_height + 1), ui_scale,
                        ui_scale)) for x in range(view)]

        # print("")
        # print("rule_models")
        # print(len(rule_models))
        # print(rule_models)

    print(" ")
    print("d_rule")
    print(d_rule)
    print("i_rule")
    print(i_rule)
    print(len(i_rule))


    #main loop
    while run == 1:

        # print("")
        # print("running")

        ts_1 = time.time()
        timer = ts_1 - ts_0

        # print("")
        # print("timer")
        # print(timer)
        # print(type(timer))
        WIN.fill((0, 0, 0))
        dt = clock.tick(FPS)
        redraw_window(input_box, v_input, 0, step_show, 0, dt, timer)

        #mitosis
        if pause == 0:
            for y in range(cell_vel):

                if len(stream_direction) > 1:

                    cells_a = np.rot90(cells_a, stream_direction[step % stream_buffer % len(stream_direction)], (0, 1))

                    if 1 in stream_direction and 3 in stream_direction or 0 in stream_direction and 2 in stream_direction:

                        momentum[stream_direction[step % stream_buffer % len(stream_direction)]] += int(glove_values[2] / momentum_scale_scale) + 1

                    else:

                        momentum[0] = 0
                        momentum[2] = 0
                        momentum[1] = 0
                        momentum[3] = 0


                cells_a = np.roll(cells_a, 1, 0)

                for x in range(len(cells_a[0])):
                    cells_a[(0 + momentum[stream_direction[step % stream_buffer % len(stream_direction)]]) % (len(cells_a[0]) - 1), x] = value_color[d_rule[tuple(viewer_1d(cells_a[1], x, view, [], color_value))]]

                if len(stream_direction) > 0:

                    cells_a = np.rot90(cells_a, 4 - stream_direction[step % stream_buffer % len(stream_direction)], (0, 1))

                    # cells_a = np.rot90(cells_a, 3, (0, 1))
                    # cells_a = np.rot90(cells_a, 2, (0, 1))
                    # cells_a = np.rot90(cells_a, 1, (0, 1))


                line = tuple(color_value[tuple(v)] for v in cells_a[0])

                if line in page:

                    if r_i == 0 and list_count == 0:

                        rand_count += 1

                        # print("duplicate")

                        rand = random.randrange(0, base ** view - 1)

                    else:
                        iterate += 1

                    # print(" ")
                    # print("rand")
                    # print(rand)

                    # print(rand)
                    # print(i_rule)
                    # print(d_rule)

                    # print(" ")
                    # print("rule")
                    # print(rule)

                    # rule = decimal(i_rule, base)
                    #
                    # if rule not in journal:
                    #
                    #     # print("")
                    #     # print("new rule")
                    #     # print(rule)
                    #
                    #     journal[rule] = []
                    #     journal[rule].append(page)
                    #
                    # else:
                    #     journal[rule].append(page)
                    #
                    # page = []

                    if randomizer == 1:

                        if list_count == 0:

                            # print("list_count == 0:")
                            # print("randomizer")

                            if base == 2:
                                if i_rule[rand] == 0:
                                    i_rule[rand] = 1
                                    d_rule[list(d_rule.keys())[rand]] = 1
                                elif i_rule[rand] == 1:
                                    i_rule[rand] = 0
                                    d_rule[list(d_rule.keys())[rand]] = 0

                            if base == 3:
                                if i_rule[rand] == 0:
                                    i_rule[rand] = 1
                                    d_rule[list(d_rule.keys())[rand]] = 1
                                elif i_rule[rand] == 1:
                                    i_rule[rand] = 2
                                    d_rule[list(d_rule.keys())[rand]] = 2
                                elif i_rule[rand] == 2:
                                    i_rule[rand] = 0
                                    d_rule[list(d_rule.keys())[rand]] = 0

                            if base == 4:

                                if i_rule[rand] == 0:
                                    i_rule[rand] = 1
                                    d_rule[list(d_rule.keys())[rand]] = 1
                                elif i_rule[rand] == 1:
                                    i_rule[rand] = 2
                                    d_rule[list(d_rule.keys())[rand]] = 2
                                elif i_rule[rand] == 2:
                                    i_rule[rand] = 3
                                    d_rule[list(d_rule.keys())[rand]] = 3
                                elif i_rule[rand] == 3:
                                    i_rule[rand] = 0
                                    d_rule[list(d_rule.keys())[rand]] = 0

                            if base == 5:

                                if i_rule[rand] == 0:
                                    i_rule[rand] = 1
                                    d_rule[list(d_rule.keys())[rand]] = 1
                                elif i_rule[rand] == 1:
                                    i_rule[rand] = 2
                                    d_rule[list(d_rule.keys())[rand]] = 2
                                elif i_rule[rand] == 2:
                                    i_rule[rand] = 3
                                    d_rule[list(d_rule.keys())[rand]] = 3
                                elif i_rule[rand] == 3:
                                    i_rule[rand] = 4
                                    d_rule[list(d_rule.keys())[rand]] = 4
                                elif i_rule[rand] == 4:
                                    i_rule[rand] = 0
                                    d_rule[list(d_rule.keys())[rand]] = 0

                            if base == 6:

                                if i_rule[rand] == 0:
                                    i_rule[rand] = 1
                                    d_rule[list(d_rule.keys())[rand]] = 1
                                elif i_rule[rand] == 1:
                                    i_rule[rand] = 2
                                    d_rule[list(d_rule.keys())[rand]] = 2
                                elif i_rule[rand] == 2:
                                    i_rule[rand] = 3
                                    d_rule[list(d_rule.keys())[rand]] = 3
                                elif i_rule[rand] == 3:
                                    i_rule[rand] = 4
                                    d_rule[list(d_rule.keys())[rand]] = 4
                                elif i_rule[rand] == 4:
                                    i_rule[rand] = 5
                                    d_rule[list(d_rule.keys())[rand]] = 5
                                elif i_rule[rand] == 5:
                                    i_rule[rand] = 0
                                    d_rule[list(d_rule.keys())[rand]] = 0

                    # print("change")
                    # print(i_rule)
                    # print(d_rule)

                else:
                    page.append(line)

                step += 1

                rule = str()
                for ir in i_rule:
                    rule += str(ir)
                rule = (rule, datetime.now())

                if i_rule != rule_point:
                    # print()
                    # print()
                    # print("align")
                    # print("i_rule & rule_point")
                    # print(i_rule)
                    # print(rule_point)
                    rule_point = i_rule[::]
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


        #console rule inputs
        if list_count != 0:

            if rule_list[0] < max_rule:

                # print("")
                # print('valid')
                # print(rule_list[0])

                d_rule, i_rule = rule_gen(rule_list[0], base)

            else:

                new_rule = rule_list[0] % max_rule

                d_rule, i_rule = rule_gen(new_rule, base)

            rule_list = rule_list[1:]

            list_count -= 1


        #inputs
        for event in pygame.event.get():

            current_digit = -1

            if event.type == pygame.QUIT:
                run = 2


            #keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    run = 2

                if event.key == pygame.K_q:
                    v_input = input('q', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_w:
                    v_input = input('w', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_e:
                    v_input = input('e', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_r:
                    v_input = input('r', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_t:
                    v_input = input('t', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_y:
                    v_input = input('y', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_u:
                    v_input = input('u', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_i:
                    v_input = input('i', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_o:
                    v_input = input('o', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_p:
                    v_input = input('p', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_a:
                    v_input = input('a', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_s:
                    v_input = input('s', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_d:
                    v_input = input('d', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_f:
                    v_input = input('f', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_g:
                    v_input = input('g', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_h:
                    v_input = input('h', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_j:
                    v_input = input('j', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_k:
                    v_input = input('k', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_l:
                    v_input = input('l', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_z:
                    v_input = input('z', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_x:
                    v_input = input('x', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_c:
                    v_input = input('c', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_v:
                    v_input = input('v', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_b:
                    v_input = input('b', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_n:
                    v_input = input('n', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_m:
                    v_input = input('m', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_SPACE:
                    v_input = input(' ', base, page, input_box, v_input)
                    page = []

                if event.key == pygame.K_0:

                    v = 0

                    if input_box == 1:
                        v_input += str(v)



                if event.key == pygame.K_TAB:
                    bookmarks.append(len(list(journal.keys())))
                    print("")
                    print("bookmarks")
                    print(bookmarks)

                    step_0 = step

                if event.key == pygame.K_F1:
                    book_rule = str()
                    for ir in i_rule:
                        book_rule += str(ir)
                    rule_book.append(book_rule)

                    print(len(rule_book))



                if event.key == pygame.K_1:

                    v = 1

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_2:

                    v = 2

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_3:

                    v = 3

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_4:

                    v = 4

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_5:

                    v = 5

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_6:

                    v = 6

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_7:

                    v = 7

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_8:

                    v = 8

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_9:

                    v = 9

                    if input_box == 1:
                        v_input += str(v)

                if event.key == pygame.K_BACKSPACE:
                    v_input = v_input[0:-1]

                if event.key == pygame.K_MINUS:
                    # print("underscore")

                    v_input += "-"

                if event.key == pygame.K_RETURN:

                    pause += 1
                    pause = pause % 2

                    print("")
                    print("pause")
                    print(pause)


                #console commands
                if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_SHIFT:

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

                                try:

                                    rule_list, list_count = rl_gen(input_list)

                                except:

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

                                        if ui_on == 1:

                                            clunk = 0
                                            rule_models = []
                                            precursor = []

                                            ir_split = []

                                            [ir_split.append(i_rule[x * int(len(i_rule) / ir_height):(x + 1) * int(
                                                len(i_rule) / ir_height)]) for x in
                                             range(ir_height)]

                                            # x_offset = CELL_WIDTH + 40
                                            # y_offset = 20 + ui_scale + y

                                            [[rule_models.append(
                                                pygame.Rect(1 * ui_scale * x + x_offset,
                                                            1 * ui_scale + 20 + ui_scale * y, ui_scale, ui_scale)) for x
                                                in
                                                range(len(ir_split[y]))] for y in range(ir_height)]

                                            # x_offset = CELL_WIDTH + 40
                                            # y_offset = 20 + ui_scale * (ir_height + 1)

                                            [precursor.append(
                                                pygame.Rect(1 * ui_scale * x + x_offset,
                                                            1 * ui_scale + 20 + ui_scale * (ir_height + 1), ui_scale,
                                                            ui_scale)) for x in range(view)]

                                            # print("")
                                            # print("rule_models")
                                            # print(len(rule_models))
                                            # print(rule_models)

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

                if event.key == pygame.K_PERIOD:

                    d_rule, i_rule = rule_gen(origin_rule, base)

                    for letter in press:

                        if letter in press_vault:

                            press_vault[letter] += press[letter]

                        else:
                            press_vault[letter] = press[letter]

                        press[letter] = 0

                if event.key == pygame.K_UP:

                    stream_direction.append(2)

                    # print('up')
                    # print(stream_direction)

                if event.key == pygame.K_RIGHT:

                    stream_direction.append(1)

                    # print("right")
                    # print(stream_direction)

                if event.key == pygame.K_DOWN:

                    stream_direction.append(0)

                    # print("down")
                    # print(stream_direction)

                if event.key == pygame.K_LEFT:

                    stream_direction.append(3)

                    # print('left')
                    # print(stream_direction)


            #midi
            if event.type in [pygame.midi.MIDIIN]:

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
                    glove_values[ev[1]-1] = ev[2]

                elif ev[0] == 177:
                    # print('left')
                    # print(ev)
                    glove_values[ev[1] + 10] = ev[2]

        #glove application
        if midi_inputs > 0:
            # print()
            # print(glove_values)

            for x in range(len(glove_sums)):
                glove_sums[x] = 0

            for x in range(11):
                #right
                glove_sums[1] += glove_values[x]
                #left
                glove_sums[0] += glove_values[x + 11]

            # print(glove_sums)

            if g_char > 0:

                for x in range(len(glove_sums)):
                    i_rule[glove_sums[x] % bv] = (i_rule[glove_sums[x] % bv] + 1) % base
                    d_rule[list(d_rule.keys())[glove_sums[x] % bv]] = i_rule[glove_sums[x] % bv]

            if g_rule > 0:

                rule_build = 0

                for x in range(len(glove_values)):

                    rule_build += glove_values[x] * 127 ** x

                print(rule_build)

                rule_build = rule_build % bbv

                d_rule, i_rule = rule_gen(rule_build, base)

            if g_words > 0:

                #trigger detection
                for x in range(4):

                    if glove_values[7 + x] > high_trigger:

                        # print("R-high" + str(x))
                        right_triggers[x] += t_plus
                        right_triggers[x + 4] -= t_minus

                    elif glove_values[7 + x] < low_trigger:

                        # print('R-low' + str(x))
                        right_triggers[x + 4] += t_plus
                        right_triggers[x] -= t_minus

                    if glove_values[18 + x] > high_trigger:

                        # print("L-high" + str(x))
                        left_triggers[x] += t_plus
                        left_triggers[x + 4] -= t_minus

                    elif glove_values[18 + x] < low_trigger:

                        # print('L-low' + str(x))
                        left_triggers[x + 4] += t_plus
                        left_triggers[x] -= t_minus

                #trigger zero
                for x in range(8):
                    if right_triggers[x] < 0 or right_triggers[x] > zero_out:
                        right_triggers[x] = 0

                    if left_triggers[x] < 0 or left_triggers[x] > zero_out:
                        left_triggers[x] = 0


                left_sorted = [left_triggers.index(x) for x in sorted(left_triggers[::], reverse=True)]
                right_sorted = [right_triggers.index(x) for x in sorted(right_triggers[::], reverse=True)]

                t_sums = [left_triggers[left_sorted[0]], right_triggers[right_sorted[0]]]

                for x in range(8):
                    t_sums[0] += left_triggers[x]
                    t_sums[1] += right_triggers[x]

                right_percentages = [right_triggers[x]/t_sums[1] for x in range(8)]
                left_percentages = [left_triggers[x]/t_sums[0] for x in range(8)]

                char_size = int(bv / rule_window_scale)


                right_char = [int(right_percentages[x] * int(char_size * (t_sums[1]/zero_full))) for x in range(8)]
                left_char = [int(left_percentages[x] * int(char_size * (t_sums[0]/zero_full))) for x in range(8)]

                # print()

                # print('left_triggers')
                # print(left_triggers)
                # print("right_triggers")
                # print(right_triggers)

                # print("char_size")
                # print(char_size)

                # print('left_sorted')
                # print(left_sorted)
                # print("right_sorted")
                # print(right_sorted)


                # print('t_sums')
                # print(t_sums)
                #
                # print('left_percentages')
                # print(left_percentages)
                # print('right_percentages')
                # print(right_percentages)

                # print('left_char')
                # print(left_char)
                # print('right_char')
                # print(right_char)

                left_used = []
                right_used = []

                left_palette = []
                right_palette = []

                for x in range(8):

                    if left_sorted[x] not in left_used:
                        for y in range(left_char[left_sorted[x]]):
                            left_palette.append(left_sorted[x])
                        left_used.append(left_sorted[x])

                    if right_sorted[x] not in right_used:
                        for y in range(right_char[right_sorted[x]]):
                            right_palette.append(right_sorted[x])
                        right_used.append(right_sorted[x])

                # print('left_palette')
                # print(left_palette)
                # print('right_palette')
                # print(right_palette)
                # print(glove_sums)

                for x in range(len(left_palette)):

                    steps = 0
                    scan = 0

                    place = (glove_sums[0] + x + steps) % bv - 1

                    while scan == 0:

                        if i_rule[place] != left_palette[x]:
                            i_rule[place] = left_palette[x]
                            d_rule[list(d_rule.keys())[place]] = left_palette[x]
                            scan = 1
                        else:
                            steps += 1

                        if steps == int(bv/rule_window_scale):
                            i_rule[place] = left_palette[x]
                            d_rule[list(d_rule.keys())[place]] = left_palette[x]
                            scan = 1

                for x in range(len(right_palette)):

                    steps = 0
                    scan = 0

                    place = (glove_sums[1] + x + steps) % bv - 1

                    while scan == 0:

                        if i_rule[place] != right_palette[x]:
                            i_rule[place] = right_palette[x]
                            d_rule[list(d_rule.keys())[place]] = right_palette[x]
                            scan = 1
                        else:
                            steps += 1

                        if steps == int(bv / rule_window_scale):
                            i_rule[place] = right_palette[x]
                            d_rule[list(d_rule.keys())[place]] = right_palette[x]
                            scan = 1














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


    #journal write
    if write == 1:

        journal['bookmarks'] = bookmarks
        journal['rule_book'] = rule_book

        if len(j_name) > 0:

            filename = 'journals/journal_' + j_name

        else:

            j_num = len(os.listdir('journals'))

            filename = 'journals/journal_' + str(j_num)

        outfile = open(filename, 'wb')
        pickle.dump(journal, outfile)
        outfile.close

        # print(len(journal))


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


Chaos_Window(9, 1, 1, 1)



