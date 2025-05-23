import time
import pygame
import pygame.midi
import math
import pickle
from pygame import mixer

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

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

    def bin_gen(n, b, p):
        def base_x(n, b):
            e = n // b
            q = n % b
            if n == 0:
                return '0'
            elif e == 0:
                return str(q)
            else:
                return base_x(e, b) + str(q)

        bin = base_x(n, b)

        while len(bin) < p:
            bin = '0' + bin
        return bin


    print(HEIGHT, WIDTH)
    width_2 = int(WIDTH/2)
    width_3 = int(WIDTH/3)
    width_4 = int(WIDTH/4)
    width_8 = int(WIDTH/8)
    width_16 = int(WIDTH/16)
    width_32 = int(WIDTH/32)
    height_2 = int(HEIGHT/2)
    height_4 = int(HEIGHT/4)
    height_8 = int(HEIGHT/8)
    height_16 = int(HEIGHT/16)
    height_32 = int(HEIGHT/32)

    run = 1
    level = 2
    valid = 0
    strokes = 1
    pulse = 1
    cross = 0
    power = [0, 0]

    #midi
    gloves = 2
    glove_sensors = 12
    glove_values = [0 for x in range(gloves * glove_sensors)]

    #input augments
    midi_inputs = 0
    device_id = 1

    try:
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

            glove_values = [x for x in range(gloves * glove_sensors)]

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
    except:
        midi_inputs = 0
        print('fuck')



    #bet
    bet = 1
    digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
                     's': 4, 'c': 5, 'd': 6, 'm': 7,
                     'g': 8, 'f': 9, 'w': 10, 'v': 11,
                     'z': 12, 'q': 13, ',': 14, '"': 15,
                     '/': 16, '.': 17, ';': 18, 'j': 19,
                     'x': 20, 'k': 21, 'y': 22, 'b': 23,
                     'h': 24, 'p': 25, 'u': 26, 'l': 27,
                     'n': 28, 'o': 29, 'r': 30, 'e': 31}
    digibetu = {v: k for k, v in digibet.items()}
    filename = 'bets/metabet_10'
    infile = open(filename, "rb")
    metabet = pickle.load(infile)
    infile.close
    metabetu = {v: k for k, v in metabet.items()}
    print(metabet)
    print(metabetu)
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
    bet_length = 10
    tebatem_6 = {v: k for k, v in metabet_6.items()}
    hourglass = [0 for x in range(bet_length)]
    letter_value = 0
    specials = [495, 527, 559, 879]
    capture = 0

    #phrase
    walls = {0:'.', 1:'\n'}
    phrase = 'edward conlon cadden maclean'
    phrase_c = ''
    phrase_1 = ''
    ripple_show = 0
    wall = 0
    hail_mary = 0


    #text
    text_name = 'bible-Theophilis.txt'
    text_a = open('library/' + text_name, 'r')
    text = text_a.read()
    lessons = text.split('\n')
    callendar = int(math.sqrt(len(lessons))) + 1
    current = 2
    clock = [0, 0]
    clock[0] = time.time()
    time_1 = int(clock[0])
    time_05 = int(clock[0])

    #records
    record = 1
    ###profile name###
    record_name = 'Theophilis_niv'
    try:
        filename = 'records/' + record_name
        infile = open(filename, "rb")
        records = pickle.load(infile)
        infile.close
        current = records['current']

        print("current")
        print(current)
        print(records[current])

        rec_len = len(list(records.items()))

        print('rec_len')
        print(rec_len)
        print("lessons")
        print(len(lessons))

        dif = len(lessons)- rec_len
        print("dif")
        print(dif)

        if dif > 0:
            for x in range(dif):
                records[rec_len+x] = 999

    except:
        records = {}
        for x in range(len(lessons)):
            records[x] = 999

        records['current'] = current

    #settings
    settings = 0
    mend = 0
    replace = 0


    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255),
                   6:(255, 0, 255), 7:(255, 255, 255), 8:(127, 127, 127)}

    value_color_16 = {0:(0, 0, 0), 1:(127, 0, 0), 2:(255, 0, 0), 3:(255, 127, 0), 4:(255, 255, 0), 5:(127, 255, 0),
                      6:(0, 255, 0), 7:(0, 255, 127), 8:(0, 255, 255), 9:(0, 127, 255), 10:(0, 0, 255), 11:(127, 0, 255),
                      12:(255, 0, 255), 13:(255, 0, 127), 14:(127, 127, 127), 15:(255, 255, 255)}

    while run == 1:

        WIN.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        time_0 = round(time.time() - clock[0], 3)

        # second
        if int(time_0) != time_1:

            strokes += 1
            strokes = strokes % len(value_color_16)

            time_1 = int(time_0)
            capture = 1
        else:
            time_05 = int(round(time_0 - time_1, 2) * 100)
            cross = abs(strokes % 2 * 100 - time_05) * 2

        #pulse
        if pulse > 0:

            # cross
            circle_scale = 8
            cross_height = height_8 + height_32
            cross_width = width_2

            if settings == 1:
                for c in range(len(value_color_16)):
                    x = width_8 + width_16
                    y = height_8 + height_32*c
                    cross_a = pygame.Rect(x, y, 32, 32)
                    pygame.draw.rect(WIN, value_color_16[c], cross_a)

            #toptri
            if power[0] > 3:
                x = cross_width
                y = cross_height - cross/2
                cross_23 = cross*2/3
                line_width = int(cross/16)
                pygame.draw.line(WIN, value_color_16[(strokes + 2)%16],  (x, y), (x+cross_23, y+cross_23), line_width)
                pygame.draw.line(WIN, value_color_16[(strokes + 2)%16],  (x, y), (x-cross_23, y+cross_23), line_width)
                pygame.draw.line(WIN, value_color_16[(strokes + 6)%16],  (x-cross_23, y+cross_23), (x+cross_23, y+cross_23), int(line_width*2/3))

            #bottri
            if power[0] > 4:
                x = cross_width
                y = cross_height - cross/2
                cross_23 = cross*2/3
                line_width = int(cross/16)
                pygame.draw.line(WIN, value_color_16[(strokes + 14)%16],  (x, y+cross), (x+cross_23, y+cross-cross_23), line_width)
                pygame.draw.line(WIN, value_color_16[(strokes + 14)%16],  (x, y+cross), (x-cross_23, y+cross-cross_23), line_width)
                pygame.draw.line(WIN, value_color_16[(strokes + 10)%16],  (x-cross_23, y+cross/3), (x+cross_23, y+cross/3), int(line_width*2/3))

            ##center circle
            if power[0] > 2:
                x = cross_width
                y = cross_height - int(cross / 10)
                pygame.draw.circle(WIN, value_color_16[(strokes + 8) % 16], (x, y), cross / circle_scale * 2)

            ##cross arms
            x = cross_width - int(cross / 8) / 2
            y = cross_height - int(cross) / 2
            cross_a = pygame.Rect(x, y, cross / 8, cross)
            pygame.draw.rect(WIN, value_color_16[strokes], cross_a)

            ##cross legs
            x = cross_width - int(cross) / 2
            y = cross_height - int(cross / 6)
            cross_l = pygame.Rect(x, y, cross, cross / 8)
            pygame.draw.rect(WIN, value_color_16[strokes], cross_l)

            #bottri
            if power[0] > 4:
                x = cross_width
                y = cross_height - cross/2
                cross_23 = cross*2/3
                line_width = int(cross/16)
                pygame.draw.line(WIN, value_color_16[(strokes + 14)%16],  (x, y+cross), (x+cross_23, y+cross-cross_23), line_width)
                pygame.draw.line(WIN, value_color_16[(strokes + 14)%16],  (x, y+cross), (x-cross_23, y+cross-cross_23), line_width)
                pygame.draw.line(WIN, value_color_16[(strokes + 10)%16],  (x-cross_23, y+cross/3), (x+cross_23, y+cross/3), int(line_width*2/3))



            ##top/bot circle
            if power[0] > 0:
                x = cross_width
                y = cross_height - int(cross / 2)
                pygame.draw.circle(WIN, value_color_16[(strokes + 4) % 16], (x, y), cross / circle_scale)
                x = cross_width
                y = cross_height + int(cross / 2)
                pygame.draw.circle(WIN, value_color_16[(strokes + 4) % 16], (x, y), cross / circle_scale)
            ##left/right circle
            if power[0] > 1:
                x = cross_width - int(cross / 2)
                y = cross_height - int(cross / 10)
                pygame.draw.circle(WIN, value_color_16[(strokes + 12) % 16], (x, y), cross / circle_scale)
                x = cross_width + int(cross / 2)
                y = cross_height - int(cross / 10)
                pygame.draw.circle(WIN, value_color_16[(strokes + 12) % 16], (x, y), cross / circle_scale)

        #bet
        if bet > 0:

            if bet == 1:

                #current
                try:
                    lcp = lessons[current][len(phrase)%len(lessons[current]):len(phrase)%len(lessons[current])+3]
                except:
                    current += 1

                #grams
                gram = metabet[lcp[0].upper()]
                if lcp[:2] in metabet:
                    bigram = metabet[lcp[:2]]
                    #
                else:
                    bigram = 0
                    #
                if lcp in metabet:
                    trigram = metabet[lcp]
                    #
                else:
                    trigram = 0
                    #

                #bin
                def bin_print(bin, x, y, size, space=1, length = 1):
                    lb2 = int(len(bin)/2)



                    for z in range(lb2):

                        color_0 = ((int(bin[z]))*192 + 63, (int(bin[z]))*192 + 63, (int(bin[z]))*192 + 63)
                        color_1 = ((int(bin[lb2 +lb2-z-1]))*192 + 63, (int(bin[lb2 +lb2-z-1]))*192 + 63, (int(bin[lb2 +lb2-z-1]))*192 + 63)

                        size_0 = size + size*int(bin[z])*length
                        size_1 = size + size *int(bin[lb2 +lb2-z-1])*length

                        digit = pygame.Rect(x-int(size_0/2), y + (size+space)*(lb2- z), size_0, size)
                        pygame.draw.rect(WIN, color_0, digit)

                        digit = pygame.Rect(x - int(size_1/2) + (size+1)*(lb2), y + (size+space)*z, size_1, size)
                        pygame.draw.rect(WIN, color_1, digit)


                    # print(bin)
                bin_1 = bin_gen(gram, 2, 10)
                bin_2 = bin_gen(bigram, 2, 10)
                bin_3 = bin_gen(trigram, 2, 10)

                bp_size = 8
                space = 2
                bp_offset = (int(len(bin_1)/2))*(bp_size+space)
                bin_height = height_2 + height_8
                bin_width = width_2

                bin_print(bin_1, width_2-300 - bp_offset, bin_height, bp_size, space, 4)
                bin_t = main_font.render(str(lcp[0]), True, (255, 255, 255))
                WIN.blit(bin_t, (bin_width-200 - bp_offset, bin_height))

                bin_print(bin_2, width_2 - bp_offset, bin_height, bp_size, space, 4)
                bin_t = main_font.render(str(lcp[:2]), True, (255, 255, 255))
                WIN.blit(bin_t, (bin_width+100 - bp_offset, bin_height))

                bin_print(bin_3, width_2+300 - bp_offset, bin_height, bp_size, space, 4)
                bin_t = main_font.render(str(lcp), True, (255, 255, 255))
                WIN.blit(bin_t, (bin_width+400 - bp_offset, bin_height))

            # gloves
            if midi_inputs > 0:


                # hourglass
                for x in range(int(bet_length / 2)):
                    hourglass[x] = glove_values[6 + x]
                    hourglass[x + int(bet_length / 2)] = glove_values[18 + x]

                mid = int((max(hourglass) - min(hourglass)) / 2)

                for y in range(bet_length):
                    if hourglass[y] < mid:
                        hourglass[y] = 0
                    else:
                        hourglass[y] = 1

                # second
                if capture == 1:

                    capture = 0
                    letter_value = 0
                    r_value = hourglass[0] + hourglass[1]*2 + hourglass[2]*4 + hourglass[3]*8 + hourglass[4]*16
                    l_value = hourglass[5] + hourglass[6]*2 + hourglass[7]*4 + hourglass[8]*8 + hourglass[9]*16

                    for x in range(bet_length):

                        if hourglass[x] > 0:
                            letter_value += 1 * 2 ** x


                    letter = metabetu[letter_value]

                    if letter_value == gram:
                        phrase += lcp[0]
                        power[0] += 1
                    elif letter_value == bigram:
                        phrase += metabetu[bigram]
                        power[0] += 2
                    elif letter_value == trigram:
                        phrase += metabetu[trigram]
                        power[0] += 3
                    elif letter == 'next':
                        current += 1
                    elif letter == 'last':
                        current -= 1
                    elif letter == 'back':
                        phrase = phrase[:-1]
                    elif letter == 'enter':
                        print()
                        print(lessons[current])
                        print(len(lessons[current]))
                        print(phrase)
                        print(len(phrase))

                        records['current'] = current

                        focus = 0

                        if phrase == lessons[current]:
                            valid = 3
                            power[0] += 1
                        else:
                            valid = 1
                            power[0] = 0

                        clock[1] = clock[0]
                        clock[0] = time.time()

                        # records
                        if valid == 3:

                            if record == 1:

                                if time_0 < records[current]:
                                    records[current] = time_0
                                    valid = 4

                                filename = 'records/' + record_name
                                outfile = open(filename, 'wb')
                                pickle.dump(records, outfile)
                                outfile.close

                            current += 1

                        phrase = ''
                    else:
                        power[0] = 0

                record_t = main_font.render(str(metabetu[letter_value]), True, (255, 255, 255))
                WIN.blit(record_t, (width_2 - int(record_t.get_width() / 2), height_2 - height_16 + height_8))

                for s in range(len(specials)):
                    bin_s = bin_gen(specials[s], 2, 10)
                    bin_print(bin_s, WIDTH - width_8, height_4 + s * height_8, bp_size, space, 4)
                    special_t = main_font.render(str(metabetu[specials[s]]), True, (255, 255, 255))
                    WIN.blit(special_t, (WIDTH - width_16, height_4 + s * height_8))

                # fingers
                record_t = main_font.render(str((r_value, l_value)), True, (255, 255, 255))
                WIN.blit(record_t,(width_2, height_2 + height_16 + height_8))
                f_width = 64
                f_buffer = 8
                f_x = width_2 + width_8
                f_y = HEIGHT
                for x in range(5):
                    finger_sign = pygame.Rect(f_x + (f_width + f_buffer) * x, f_y - glove_values[6 + x], f_width,
                                              glove_values[6 + x])
                    pygame.draw.rect(WIN, value_color[hourglass[x] * 8], finger_sign)

                    finger_sign = pygame.Rect(
                        f_x - width_4 - (5 * (f_width + f_buffer)) + f_buffer + (f_width + f_buffer) * x,
                        f_y - glove_values[18 + 4 - x], f_width, glove_values[18 + 4 - x])
                    pygame.draw.rect(WIN, value_color[hourglass[4 - x + 5] * 8], finger_sign)

        #lessons current
        text_color = value_color[7]
        text_valid = value_color[3]
        text_wrong = value_color[1]
        x_place = 0
        y_place = 0
        row_width = 64
        current_height = height_4 + height_16
        current_width = width_4

        lesson_t = main_font.render(str('{'), True,
                                    text_color)
        WIN.blit(lesson_t,
                 (current_width + x_place-11, current_height + y_place))
        for x in range(len(lessons[current])):

            try:
                if phrase[x] == lessons[current][x]:
                    letter_color = text_valid
                else:
                    letter_color = text_wrong
            except:
                letter_color = text_color

            x_pos = current_width + x_place
            y_pos = current_height + y_place
            lesson_t = main_font.render(str(lessons[current][x]), True, letter_color)
            if letter_color == text_wrong and lessons[current][x] == ' ':
                lesson_t = main_font.render(str(phrase[x]), True, letter_color)
            WIN.blit(lesson_t,(x_pos, y_pos))

            if x == len(phrase):
                valid_sign = pygame.Rect(x_pos, y_pos + lesson_t.get_height(), lesson_t.get_width(), 3)
                pygame.draw.rect(WIN, letter_color, valid_sign)

            x_place += lesson_t.get_width()

            if x % row_width == 0 and x != 0:
                x_place = 0
                y_place += lesson_t.get_height()

        lesson_t = main_font.render(str('}'), True, text_color)
        WIN.blit(lesson_t,(current_width + x_place+11, current_height + y_place))


        # print(len(lessons))
        for x in range(callendar):
            for y in range(callendar):

                if x + y*callendar <current:
                    lesson_sign = pygame.Rect(50 + 1*x, 50 + 2*y, 1, 1)
                    pygame.draw.rect(WIN, value_color[6], lesson_sign)

                else:
                    lesson_sign = pygame.Rect(50 + 1*x, 50 + 2*y, 1, 1)
                    pygame.draw.rect(WIN, value_color[5], lesson_sign)

        #valid sign
        x = WIDTH - width_16
        y = height_32
        valid_sign = pygame.Rect(x, y, 64, 64)
        pygame.draw.rect(WIN, value_color[valid], valid_sign)
        if valid_sign.collidepoint((mx, my)):
            valid = 2
            record_t = main_font.render(str(valid), True, (255, 255, 255))
            WIN.blit(record_t, (x, y))
            if click:
                settings = 1
                valid = 5

        time_t = main_font.render(str(time_0), True, (255, 255, 255))
        WIN.blit(time_t, (width_2 + width_4 + width_8, height_32))

        record_t = main_font.render(str(records[current]), True, (255, 255, 255))
        WIN.blit(record_t, (width_2 + width_4 + width_8, height_32 + record_t.get_height()))

        record_t = main_font.render(str(current), True, (255, 255, 255))
        WIN.blit(record_t, (width_2 - record_t.get_width()/2, record_t.get_height()/8))




        #settings
        if settings == 1:
            x = WIDTH - width_8
            y = height_2
            mend_button = pygame.Rect(x, y, 200, 50)
            mend_button_i = pygame.Rect(x, y, 197, 43)
            pygame.draw.rect(WIN, (0, 192, 192), mend_button)
            pygame.draw.rect(WIN, (0, 64, 63), mend_button_i)
            if mend_button.collidepoint((mx, my)):
                record_t = main_font.render('mend', True, (255, 255, 255))
                WIN.blit(record_t, (x, y))
                if click:
                    print('mend')

                    if mend == 0:
                        mend = 1
                        phrase = phrase_1[::]
                    if mend == 1:
                        lessons[current] = phrase

            y = height_2 + height_16
            replace_button = pygame.Rect(x, y, 200, 50)
            replace_button_i = pygame.Rect(x, y, 197, 43)
            pygame.draw.rect(WIN, (192, 0, 192), replace_button)
            pygame.draw.rect(WIN, (63, 0, 63), replace_button_i)
            if replace_button.collidepoint((mx, my)):
                replace_t = main_font.render('replace', True, (255, 255, 255))
                WIN.blit(replace_t, (x, y))
                if click:
                    print()
                    print("replace")
                    click = False

                    replacements = phrase.split(':')
                    phrase = ''
                    print(replacements)


                    try:
                        if replacements[0] in text:
                            valid = 6
                        text = text.replace(replacements[0], replacements[1])
                    except:
                        continue

                    with open('library/' + text_name, 'w') as file:
                        file.write(text)
                        file.close()

                    text_a = open('library/' + text_name, 'r')
                    text = text_a.read()
                    lessons = text.split('\n')


            y = height_2 + height_8
            clear_button = pygame.Rect(x, y, 200, 50)
            clear_button_i = pygame.Rect(x, y, 197, 43)
            pygame.draw.rect(WIN, (0, 0, 192), clear_button)
            pygame.draw.rect(WIN, (0, 0, 63), clear_button_i)
            if clear_button.collidepoint((mx, my)):
                clear_t = main_font.render('clear', True, (255, 255, 255))
                WIN.blit(clear_t, (x, y))
                if click:
                    print("clear")
                    click = False
                    phrase = ''


            # phrase
            row_width = 64
            for x in range(int(len(phrase) / row_width) + 1):
                phrase_t = small_font.render('{' + str(phrase[x * row_width:(x + 1) * row_width]) + '}', True,
                                             (255, 255, 255))
                WIN.blit(phrase_t,
                         (width_2 - int(phrase_t.get_width() / 2), height_2 + height_4 + x * phrase_t.get_height()))



        #inputs
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = 2

            click = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            #keyboard

            elif event.type == pygame.KEYDOWN:

                def type(phrase, letter):
                    print("letter")

                    phrase += letter

                    return phrase

                if event.key == pygame.K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_RETURN:

                    print()
                    print(current)
                    print(lessons[current])
                    print(phrase)

                    print(len(lessons[current]))
                    print(len(phrase))

                    records['current'] = current

                    focus = 0

                    if phrase == lessons[current]:
                        valid = 3
                        power[0] += 1
                    else:
                        valid = 1
                        power[0] = 0


                    clock[1] = clock[0]
                    clock[0] = time.time()

                    #records
                    if valid == 3:

                        if record == 1:

                            if time_0 < records[current]:
                                records[current] = time_0
                                valid = 4

                            filename = 'records/' + record_name
                            outfile = open(filename, 'wb')
                            pickle.dump(records, outfile)
                            outfile.close

                        current += 1

                    phrase_1 = phrase[::]
                    phrase = ''
                    settings = 0
                    men = 0


                elif event.key == pygame.K_F1:

                    print("wu")



                elif event.key == pygame.K_LEFT:
                    current -= 1

                elif event.key == pygame.K_RIGHT:
                    current += 1

                elif event.key == pygame.K_UP:
                    ripple_show += 1
                    ripple_show = ripple_show % 2
                    power[0] += 1

                elif event.key == pygame.K_DOWN:
                    print('wall')
                    print(wall)
                    wall += 1
                    wall = wall %2

                    hail_mary += 1
                    hail_mary = hail_mary %2

                    if valid == 3:

                        left = 0
                        right = 0
                        look_behind = text.index(phrase_c)
                        look_ahead = text.index(phrase_c)
                        index_0 = text.index(phrase_c)
                        while left == 0 or right == 0:

                            if text[look_behind] == walls[wall]:
                                left = look_behind
                            else:
                                look_behind = look_behind - 1

                            if text[look_ahead] == walls[wall]:
                                right = look_ahead
                            else:
                                look_ahead = look_ahead + 1

                        if left < 0:
                            left = 0

                        ripple = text[left:right]

                    power[0] -= 1

                #upper
                elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'A'

                elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'B'

                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'C'

                elif event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'D'

                elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'E'

                elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'F'

                elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'G'

                elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'H'

                elif event.key == pygame.K_i and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'I'

                elif event.key == pygame.K_j and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'J'

                elif event.key == pygame.K_k and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'K'

                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'L'

                elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'M'

                elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'N'

                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'O'

                elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'P'

                elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'Q'

                elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'R'

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'S'

                elif event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'T'

                elif event.key == pygame.K_u and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'U'

                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'V'

                elif event.key == pygame.K_w and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'W'

                elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'X'

                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'Y'

                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += 'Z'

                elif event.key == pygame.K_9 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += '('

                elif event.key == pygame.K_0 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += ')'

                elif event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += '!'

                #number
                elif event.key == pygame.K_0:
                    phrase += '0'
                elif event.key == pygame.K_1:
                    phrase += '1'
                elif event.key == pygame.K_2:
                    phrase += '2'
                elif event.key == pygame.K_3:
                    phrase += '3'
                elif event.key == pygame.K_4:
                    phrase += '4'
                elif event.key == pygame.K_5:
                    phrase += '5'
                elif event.key == pygame.K_6:
                    phrase += '6'
                elif event.key == pygame.K_7:
                    phrase += '7'
                elif event.key == pygame.K_8:
                    phrase += '8'
                elif event.key == pygame.K_9:
                    phrase += '9'



                #lower
                elif event.key == pygame.K_a:
                    phrase += 'a'

                elif event.key == pygame.K_b:
                    phrase += 'b'

                elif event.key == pygame.K_c:
                    phrase += 'c'

                elif event.key == pygame.K_d:
                    phrase += 'd'

                elif event.key == pygame.K_e:
                    phrase += 'e'

                elif event.key == pygame.K_f:
                    phrase += 'f'

                elif event.key == pygame.K_g:
                    phrase += 'g'

                elif event.key == pygame.K_h:
                    phrase += 'h'

                elif event.key == pygame.K_i:
                    phrase += 'i'

                elif event.key == pygame.K_j:
                    phrase += 'j'

                elif event.key == pygame.K_k:
                    phrase += 'k'

                elif event.key == pygame.K_l:
                    phrase += 'l'

                elif event.key == pygame.K_m:
                    phrase += 'm'

                elif event.key == pygame.K_n:
                    phrase += 'n'

                elif event.key == pygame.K_o:
                    phrase += 'o'

                elif event.key == pygame.K_p:
                    phrase += 'p'

                elif event.key == pygame.K_q:
                    phrase += 'q'

                elif event.key == pygame.K_r:
                    phrase += 'r'

                elif event.key == pygame.K_s:
                    phrase += 's'

                elif event.key == pygame.K_t:
                    phrase += 't'

                elif event.key == pygame.K_u:
                    phrase += 'u'

                elif event.key == pygame.K_v:
                    phrase += 'v'

                elif event.key == pygame.K_w:
                    phrase += 'w'

                elif event.key == pygame.K_x:
                    phrase += 'x'

                elif event.key == pygame.K_y:
                    phrase += 'y'

                elif event.key == pygame.K_z:
                    phrase += 'z'

                elif event.key == pygame.K_SPACE:
                        phrase += ' '

                elif event.key == pygame.K_PERIOD:
                    phrase += '.'

                elif event.key == pygame.K_COMMA:
                    phrase += ','

                elif event.key == pygame.K_SLASH and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += '?'

                elif event.key == pygame.K_EXCLAIM:
                    phrase += '!'

                elif event.key == pygame.K_SEMICOLON and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += ':'

                elif event.key == pygame.K_SEMICOLON:
                    phrase += ';'

                elif event.key == pygame.K_QUOTE and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += '"'

                elif event.key == pygame.K_QUOTE:
                    phrase += "'"

                elif event.key == pygame.K_MINUS:
                    phrase += "-"

                elif event.key == pygame.K_LEFTBRACKET:
                    phrase += '['

                elif event.key == pygame.K_RIGHTBRACKET:
                    phrase += ']'





                elif event.key == pygame.K_BACKSPACE:
                    phrase = phrase[:-1]



        pygame.display.update()


Chaos_Window()

