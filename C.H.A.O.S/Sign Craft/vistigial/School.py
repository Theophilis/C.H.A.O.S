import time
import pygame
import pygame.midi
import math
import pickle

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

    print(HEIGHT, WIDTH)
    #dimensions
    width_2 = int(WIDTH/2)
    width_4 = int(WIDTH/4)
    width_8 = int(WIDTH/8)
    width_16 = int(WIDTH/16)
    width_32 = int(WIDTH/32)
    height_2 = int(HEIGHT/2)
    height_4 = int(HEIGHT/4)
    height_8 = int(HEIGHT/8)
    height_16 = int(HEIGHT/16)
    height_32 = int(HEIGHT/32)

    #active
    run = 1
    level = 2
    valid = 0
    clock = [0, 0]
    clock[0] = time.time()


    #midi
    gloves = 1
    glove_sensors = 12
    glove_values = [0 for x in range(gloves * glove_sensors)]

    #input augments
    midi_inputs = 0
    gloves = 1
    number_of_sensors = 12
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
    except:
        midi_inputs = 0


    #bet
    bet = 1
    beat = time.time()
    digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
                     's': 4, 'c': 5, 'd': 6, 'm': 7,
                     'g': 8, 'f': 9, 'w': 10, 'v': 11,
                     'z': 12, 'q': 13, ',': 14, '"': 15,
                     '/': 16, '.': 17, ';': 18, 'j': 19,
                     'x': 20, 'k': 21, 'y': 22, 'b': 23,
                     'h': 24, 'p': 25, 'u': 26, 'l': 27,
                     'n': 28, 'o': 29, 'r': 30, 'e': 31}
    tebigid = {v: k for k, v in digibet.items()}
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
    tebatem_6 = {v: k for k, v in metabet_6.items()}
    hourglass = [0, 0, 0, 0, 0]
    hand = [0, 0, 0, 0, 0]
    focus = 0


    #record
    recording = 1
    name = 'Edward MacLean'
    title = 'bible-niv'
    filename = name + '/' + title
    infile = open(filename, "rb")
    record = pickle.load(infile)
    infile.close

    def eye(record, current, pace):

        view = record[current][0]

        for x in range(pace-1):
            view += ' '
            view += record[current + x+1][0]


        print(current)
        print(pace)
        print(view)

        return view

    phrase = ''
    current = record['current']
    pace = record['pace']
    window = 7
    frame = eye(record, current, window)
    view = eye(record, current, pace)
    print(view)

    callendar = int(math.sqrt(record['length'])) + 1
    print(callendar)
    print(callendar**2)


    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255), 6:(255, 0, 255), 7:(255, 255, 255)}



    while run == 1:

        WIN.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        time_0 = round(time.time() - clock[0], 3)


        #display

        focus_color = (255, 255, 255)

        lesson_t = main_font.render('{' + record[current][0] + '}', True, focus_color)
        WIN.blit(lesson_t,
                 (width_2 - int(lesson_t.get_width() / 2), height_2))

        lesson_t = main_font.render('{' + frame + '}', True, focus_color)
        WIN.blit(lesson_t,
                 (width_2 - int(lesson_t.get_width() / 2), height_2 - 100))

        for x in range(window):
            lesson_t = main_font.render('{' + record[current + x][0] + '}', True, focus_color)
            WIN.blit(lesson_t,
                     (width_2 - int(lesson_t.get_width() / 2) -300, height_2 + 100 + 40*x))

        for x in range(window):
            lesson_t = main_font.render('{' + record[current - x][0] + '}', True, focus_color)
            WIN.blit(lesson_t,
                     (width_2 - int(lesson_t.get_width() / 2) + 300, height_2 + 100 + 40*x))

        row_width = 80
        for x in range(int(len(phrase) / row_width) + 1):
            phrase_t = main_font.render('{' + str(phrase[x*row_width:(x+1)*row_width]) + '}', True,
                                         (255, 255, 255))
            WIN.blit(phrase_t,
                     (width_2 - int(phrase_t.get_width() / 2), height_2 + height_4 + x * phrase_t.get_height()))


        valid_sign = pygame.Rect(width_2 - 50,height_32, 100, 100)
        pygame.draw.rect(WIN, value_color[valid], valid_sign)
        time_t = TITLE_FONT.render(str(time_0), True, (255, 255, 255))
        WIN.blit(time_t, (width_2, height_32))

        record_t = TITLE_FONT.render(str(record[current][1]), True, (255, 255, 255))
        WIN.blit(record_t, (width_2, height_32 + record_t.get_height()))

        pygame.display.update()




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

                if event.key == pygame.K_ESCAPE:
                    run = 2

                elif event.key == pygame.K_RETURN:

                    phrase = ''

                elif event.key == pygame.K_SPACE:

                        if phrase == record[current][0]:
                            current += 1
                            record['current'] = current

                            frame = eye(record, current, window)
                            phrase = ''

                            record['current'] = current

                        if phrase == record[current]:
                            valid = 3
                            pace += 1
                        else:
                            print(phrase)
                            print(view)
                            valid = 1
                            pace -= 1

                        clock[1] = clock[0]
                        clock[0] = time.time()

                        # records
                        if valid == 3:

                            if recording == 1:

                                if time_0 < record[current][1]:
                                    record[current][1] = time_0
                                    valid = 4

                            current += 1

                            frame = eye(record, current, pace)

                        phrase = ''

                        filename = name + '/' + title
                        outfile = open(filename, 'wb')
                        pickle.dump(record, outfile)
                        outfile.close





                elif event.key == pygame.K_LEFT:
                    current -= 1

                elif event.key == pygame.K_RIGHT:
                    current += 1



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
                elif event.key == pygame.K_8 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    phrase += '*'
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





                elif event.key == pygame.K_BACKSPACE:
                    phrase = phrase[:-1]

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
                    glove_values[ev[1] + glove_sensors] = ev[2]



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
