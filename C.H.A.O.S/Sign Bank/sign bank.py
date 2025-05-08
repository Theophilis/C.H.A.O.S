import time
import pygame
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

    #basic
    run = 1
    power = [0, 0]

    #clock
    clock = [0, 0]
    clock[0] = time.time()

    #phrase
    phrase = 'god bless'

    #bet
    digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
                     's': 4, 'c': 5, 'd': 6, 'm': 7,
                     'g': 8, 'f': 9, 'w': 10, 'v': 11,
                     'z': 12, 'q': 13, ',': 14, '"': 15,
                     '/': 16, '.': 17, ';': 18, 'j': 19,
                     'x': 20, 'k': 21, 'y': 22, 'b': 23,
                     'h': 24, 'p': 25, 'u': 26, 'l': 27,
                     'n': 28, 'o': 29, 'r': 30, 'e': 31}
    digibetu = {v: k for k, v in digibet.items()}

    filename = 'bets/armbet_2'
    infile = open(filename, "rb")
    armbet = pickle.load(infile)
    infile.close



    ###profile name###
    record_name = 'Theophilis'
    try:
        filename = 'records/' + record_name
        infile = open(filename, "rb")
        records = pickle.load(infile)
        infile.close
        print(records['name'])
    except:
        records = {}

        records['name'] = record_name
        records['sign'] = {}
        records['digibet'] = {}
        records['armbet'] = {}

        sign = record_name

        records['sign'][sign] = 1


        sign = sign.lower()
        for x in range(len(sign)):
            bigram = sign[x:x + 2]
            trigram = sign[x:x + 3]


            if bigram in armbet[sign[x]] and len(bigram)>1:

                if bigram in records['armbet']:
                    records['armbet'][bigram] += 1
                else:
                    records['armbet'][bigram] = 1

            if trigram in armbet[sign[x]] and len(bigram)>2:

                if trigram in records['armbet']:
                    records['armbet'][trigram] += 1
                else:
                    records['armbet'][trigram] = 1




    dimensions = ['sign', 'digibet', 'armbet']


    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255),
                   6:(255, 0, 255), 7:(255, 255, 255), 8:(127, 127, 127)}

    value_color_16 = {0:(0, 0, 0), 1:(127, 0, 0), 2:(255, 0, 0), 3:(255, 127, 0), 4:(255, 255, 0), 5:(127, 255, 0),
                      6:(0, 255, 0), 7:(0, 255, 127), 8:(0, 255, 255), 9:(0, 127, 255), 10:(0, 0, 255), 11:(127, 0, 255),
                      12:(255, 0, 255), 13:(255, 0, 127), 14:(127, 127, 127), 15:(255, 255, 255)}

    text_color = value_color[7]

    while run == 1:

        WIN.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        time_0 = round(time.time() - clock[0], 3)


        lesson_t = main_font.render(str(phrase), True, text_color)
        WIN.blit(lesson_t,(width_2 - lesson_t.get_width()/2, HEIGHT - lesson_t.get_height()*4))

        lesson_t = main_font.render(str(records['name']), True, text_color)
        WIN.blit(lesson_t,(width_2 - lesson_t.get_width()/2, height_16 - lesson_t.get_height()))


        i = 0
        for d in dimensions:
            x_pos = width_8 + width_8*i
            y_pos = height_8



            # digibet
            records_di = list(records[d].items())
            records_di = list(sorted(records_di, key=lambda ele: ele[1], reverse=True))[:16]



            for x in range(len(records_di)):
                sign = records_di[x][0]
                record = records[d][sign]
                lesson_t = small_font.render(str((sign, record)), True, text_color)
                WIN.blit(lesson_t, (x_pos - lesson_t.get_width() / 2, y_pos + lesson_t.get_height() * x))

            i+=1

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
                    print(phrase)
                    print(len(phrase))



                    def process(phrase, records):

                        if 'sign' not in records:
                            records['sign'] = {}
                        if 'digibet' not in records:
                            records['digibet'] = {}
                        if 'armbet' not in records:
                            records['armbet'] = {}

                        phrase = phrase.lower()

                        read = phrase.lower()
                        read = read.translate({ord('\n'): ' '})
                        read = read.translate({ord('-'): ' '})

                        read = read.translate({ord("."): ''})
                        read = read.translate({ord(","): ''})

                        if read[-1] == ' ':
                            read = read[:-1]

                        read = list(read.split(' '))

                        for sign in read:

                            #signs
                            if sign in records['sign']:
                                records["sign"][sign] += 1
                            else:
                                records['sign'][sign] = 1

                            #digibet
                            for s in sign:
                                if s in records['digibet']:
                                    records['digibet'][s] += 1
                                else:
                                    records['digibet'][s] = 1

                            #armbet
                            sign = sign.lower()
                            print()
                            print('#')
                            for x in range(len(sign)):
                                bigram = sign[x:x + 2]
                                trigram = sign[x:x + 3]

                                print()
                                print(x)
                                print(bigram)

                                if len(bigram) == 2 and bigram in armbet[sign[x]]:
                                    if bigram in records['armbet']:
                                        print('in')
                                        print(records['armbet'][bigram])
                                        records['armbet'][bigram] += 1
                                        print(records['armbet'][bigram])
                                    else:
                                        print('out')
                                        records['armbet'][bigram] = 1
                                        print(records['armbet'][bigram])
                                    print(records['armbet'][bigram])

                                print()
                                print(trigram)

                                if len(trigram) == 3 and trigram in armbet[sign[x]]:
                                    if trigram in records['armbet']:
                                        print('in')
                                        print(records['armbet'][trigram])
                                        records['armbet'][trigram] += 1
                                        print(records['armbet'][trigram])
                                    else:
                                        print('out')
                                        records['armbet'][trigram] = 1
                                        print(records['armbet'][trigram])
                                    print(records['armbet'][trigram])




                        return records

                    if len(phrase) > 0:
                        records = process(phrase, records)


                    clock[1] = clock[0]
                    clock[0] = time.time()
                    phrase = ''

                    print(records['name'])

                    filename = 'records/' + records['name']
                    outfile = open(filename, 'wb')
                    pickle.dump(records, outfile)
                    outfile.close



                elif event.key == pygame.K_F1:


                    print()


                elif event.key == pygame.K_LEFT:
                    print()

                elif event.key == pygame.K_RIGHT:
                    print()

                elif event.key == pygame.K_UP:
                    ripple_show += 1
                    ripple_show = ripple_show % 2
                    power[0] += 1

                elif event.key == pygame.K_DOWN:
                    print('wall')


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

