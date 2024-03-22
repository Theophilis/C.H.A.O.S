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

    mixer.init()

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


    tone = {0:'in_', 1:'qr_', 2:'aw_'}



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


    #votes
    votes = {}
    voice = ''
    voice_l = 0


    #phrase
    walls = {0:'.', 1:'\n'}
    phrase = 'edward conlon cadden maclean'
    phrase_s = ''
    phrase_1 = ''
    ripple_show = 0
    wall = 0
    hail_mary = 0


    #text
    text_name = 'vote.txt'
    text_a = open(text_name, 'r')
    text = text_a.read()
    lessons = text.split('\n')
    callendar = int(math.sqrt(len(lessons))) + 1
    current = 2
    clock = [0, 0]
    clock[0] = time.time()
    time_1 = int(clock[0])
    time_05 = int(clock[0])


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


        #phrase
        text_color = value_color[7]

        phrase_t = main_font.render(str(phrase), True, text_color)
        WIN.blit(phrase_t,(width_8, height_8))

        phrase_t = main_font.render(str(phrase_s), True, text_color)
        WIN.blit(phrase_t,(width_8, height_4))

        votes_t = main_font.render(str(votes), True, text_color)
        WIN.blit(votes_t, (width_8, height_2))

        votes_t = main_font.render(str(voice), True, text_color)
        WIN.blit(votes_t, (width_8, height_2 + height_8))


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


                    phrase_s = phrase.split()

                    print(phrase_s)
                    voice = ''

                    if len(phrase_s) > voice_l:
                        voice_l = len(phrase_s)


                    for x in range(voice_l):
                        if x < len(phrase_s):
                            if x not in votes:
                                votes[x] = {}
                                votes[x][phrase_s[x]] = 1
                            elif phrase_s[x] not in votes[x]:
                                votes[x][phrase_s[x]] = 1
                            else:
                                votes[x][phrase_s[x]] += 1

                        print(votes[x])
                        votes_i = list(votes[x].items())
                        print(votes_i)
                        votes_i = sorted(votes_i, key=lambda v:v[1], reverse=True)

                        voice += votes_i[0][0] + ' '





                    phrase_1 = phrase[::]
                    phrase = ''
                    settings = 0



                elif event.key == pygame.K_F1:


                    print('wow')


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


        pygame.display.update()


Chaos_Window()

