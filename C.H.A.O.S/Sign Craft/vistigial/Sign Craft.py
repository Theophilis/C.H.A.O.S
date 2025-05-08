import numpy as np
import pygame
import pygame.midi
import pickle

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
    turn = 0
    level = 2
    valid = 0
    challenge = 0

    walls = {0:'.', 1:'\n'}
    counter_mary = {0:'counter', 1:'hail mary'}
    alphabet = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
                'z': 0, ' ': 0}
    history = {0:[], 1:[]}

    phrase = 'edward conlon cadden maclean'
    phrase_c = ''
    ripple = ''
    ripple_show = 0
    wall = 0
    index_0 = 0
    memory = 0

    count_step = {0:20, 1:-20}
    rosary = [0, 0]
    mary_counter = [0, 0]
    hail_mary = 0
    streak = 7


    filename = '../library/niv_bible_words'
    infile = open(filename, "rb")
    lexicon = pickle.load(infile)
    infile.close

    text = open('../library/bible-niv.txt', 'r')
    text = text.read()


    points = {0: 0, 1: 0}
    board = [0, 0]


    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255), 6:(255, 0, 255), 7:(255, 255, 255)}

    def sing(text, lexicon, alphabet, phrase, points, turn, valid):

        print()
        print('sing')
        print(phrase)
        phrase_c = phrase[::]

        if phrase in history[0] or phrase in history[1]:
            valid = 1
            history[turn].append(phrase_c)

            return alphabet, phrase, points, valid

        if phrase in text:

            phrase = phrase.translate({ord(':'): None})
            phrase = phrase.translate({ord(';'): None})
            phrase = phrase.translate({ord('.'): None})
            phrase = phrase.translate({ord('?'): None})
            phrase = phrase.translate({ord('!'): None})
            phrase = phrase.translate({ord(','): None})
            phrase = phrase.translate({ord("'"): None})
            phrase = phrase.translate({ord('('): None})
            phrase = phrase.translate({ord(')'): None})

            phrase = phrase.translate({ord('0'): None})
            phrase = phrase.translate({ord('1'): None})
            phrase = phrase.translate({ord('2'): None})
            phrase = phrase.translate({ord('3'): None})
            phrase = phrase.translate({ord('4'): None})
            phrase = phrase.translate({ord('5'): None})
            phrase = phrase.translate({ord('6'): None})
            phrase = phrase.translate({ord('7'): None})
            phrase = phrase.translate({ord('8'): None})
            phrase = phrase.translate({ord('9'): None})

            phrase = phrase.split()

            if '-' in phrase:
                phrase = phrase.split('-')

            print("split")
            print(phrase)

            sum = 0
            for y in range(len(phrase)):
                print(y)
                if phrase[y] in lexicon:
                    valid = 3

                    print(phrase[y])

                    for x in range(len(phrase[y])):
                        alphabet[phrase[y][x].lower()] += 1

                    # print(alphabet)

                    alphabet = dict(sorted(alphabet.items(), key=lambda x: x[1], reverse=True))

                    for p in phrase[y]:
                        # print()
                        # print(p, alphabet[p], list(alphabet.keys()).index(p))
                        sum += list(alphabet.keys()).index(p.lower())

                else:
                    valid = 1
                    break

                points[turn] += sum
                board[turn] = sum

        else:
            valid = 1

        history[turn].append(phrase_c)

        return alphabet, phrase_c, points, valid


    while run == 1:

        mx, my = pygame.mouse.get_pos()

        #display
        WIN.fill((0, 0, 0))

        phrase_t = main_font.render('{' + str(phrase) + '}', True, (255, 255, 255))
        WIN.blit(phrase_t, (width_2 - int(phrase_t.get_width()/2), height_2 + height_4))



        valid_sign = pygame.Rect(width_2 - 50,height_32, 100, 100)
        pygame.draw.rect(WIN, value_color[valid], valid_sign)
        level_t = TITLE_FONT.render(str(int(level/2)), True, (255, 255, 255))
        WIN.blit(level_t, (width_2 - int(level_t.get_width()/2), height_32))

        point_bar_0 = pygame.Rect(0, 0, 21, points[0])
        pygame.draw.rect(WIN, value_color[5], point_bar_0)
        points_t0 = TITLE_FONT.render(str(points[0]), True, (255, 255, 255))
        WIN.blit(points_t0, (width_4 - int(points_t0.get_width()/2), height_32))
        board_t0 = lable_font.render(str(board[0]), True, (255, 255, 255))
        WIN.blit(board_t0, (width_4 - int(board_t0.get_width()/2), height_8))

        point_bar_1 = pygame.Rect(WIDTH-21, 0, 21, points[1])
        pygame.draw.rect(WIN, value_color[5], point_bar_1)
        points_t1 = TITLE_FONT.render(str(points[1]), True, (255, 255, 255))
        WIN.blit(points_t1, (width_4 + width_2 - int(points_t1.get_width()/2), height_32))
        board_t1 = lable_font.render(str(board[1]), True, (255, 255, 255))
        WIN.blit(board_t1, (width_4 + width_2 - int(board_t1.get_width()/2), height_8))



        # challenge
        if level > 7:

            #challenge
            if challenge == 0:
                challenge_button = pygame.Rect(width_2 - 100, height_4, 200, 50)
                pygame.draw.rect(WIN, (255, 0, 0), challenge_button)
                challenge_button = pygame.Rect(width_2 - 98, height_4 + 1, 196, 46)
                pygame.draw.rect(WIN, (0, 0, 0), challenge_button)
                challenge_t = main_font.render('challenge', True, (255, 255, 255))
                WIN.blit(challenge_t, (width_2 - int(challenge_t.get_width()/2), height_4))
                if challenge_button.collidepoint((mx, my)):
                    if click:
                        challenge = 1

            #good evil
            if challenge == 1:
                good_button = pygame.Rect(width_2 - 100, height_4 + 50, 100, 50)
                pygame.draw.rect(WIN, (255, 255, 255), good_button)
                good_button = pygame.Rect(width_2 - 99, height_4 + 51, 98, 46)
                pygame.draw.rect(WIN, (0, 0, 0), good_button)
                good_t = main_font.render('good', True, (255, 255, 255))
                WIN.blit(good_t, (width_2 - int(good_t.get_width() / 2) - 50, height_4 + 50))
                if good_button.collidepoint((mx, my)):
                    if click:
                        # print()
                        # print('good')
                        # print(turn)
                        # print(phrase)
                        # print(board)
                        # print(points)

                        points[turn_0] -= board[turn_0]
                        points[turn] += board[turn_0]

                        # print(points)

                        challenge = 2

                evil_button = pygame.Rect(width_2, height_4 + 50, 100, 50)
                pygame.draw.rect(WIN, (255, 255, 255), evil_button)
                evil_button = pygame.Rect(width_2+1, height_4 + 51, 98, 46)
                pygame.draw.rect(WIN, (0, 0, 0), evil_button)
                evil_t = main_font.render('evil', True, (255, 255, 255))
                WIN.blit(evil_t, (width_2 - int(evil_t.get_width() / 2) + 50, height_4 + 50))
                if evil_button.collidepoint((mx, my)):
                    if click:
                        # print()
                        # print('evil')
                        # print(turn)
                        # print(points)
                        # print(board)

                        points[turn] -= board[turn_0]

                        challenge = 5

            #counter
            if challenge == 2:

                if wall == 1:
                    counter_button = pygame.Rect(width_2 - 25, height_4 - 50, 50, 200)
                    pygame.draw.rect(WIN, (0, 255, 0), counter_button)
                    counter_button = pygame.Rect(width_2 - 24, height_4 - 48, 46, 196)
                    pygame.draw.rect(WIN, (0, 0, 0), counter_button)

                counter_button = pygame.Rect(width_2 - 100, height_4, 200, 50)
                pygame.draw.rect(WIN, (0, 255, 0), counter_button)
                counter_button = pygame.Rect(width_2 - 98, height_4 + 1, 196, 46)
                pygame.draw.rect(WIN, (0, 0, 0), counter_button)



                challenge_t = main_font.render(counter_mary[hail_mary], True, (255, 255, 255))
                WIN.blit(challenge_t, (width_2 - int(challenge_t.get_width()/2), height_4))
                if challenge_button.collidepoint((mx, my)):
                    if click:
                        challenge = 3

            #good evil
            if challenge == 3:
                good_button = pygame.Rect(width_2 - 100, height_4 + 50, 100, 50)
                pygame.draw.rect(WIN, (255, 255, 255), good_button)
                good_button = pygame.Rect(width_2 - 99, height_4 + 51, 98, 46)
                pygame.draw.rect(WIN, (0, 0, 0), good_button)
                good_t = main_font.render('good', True, (255, 255, 255))
                WIN.blit(good_t, (width_2 - int(good_t.get_width() / 2) - 50, height_4 + 50))
                if good_button.collidepoint((mx, my)):
                    if click:
                        # print()
                        # print('good')
                        # print(turn)
                        # print(phrase)
                        # print(board)
                        # print(points)

                        points[turn] -= board[turn_0] * (2 + 2*hail_mary)
                        points[turn_0] += board[turn_0] * (2 + 2*hail_mary)

                        # print(points)

                        challenge = 5

                evil_button = pygame.Rect(width_2, height_4 + 50, 100, 50)
                pygame.draw.rect(WIN, (255, 255, 255), evil_button)
                evil_button = pygame.Rect(width_2+1, height_4 + 51, 98, 46)
                pygame.draw.rect(WIN, (0, 0, 0), evil_button)
                evil_t = main_font.render('evil', True, (255, 255, 255))
                WIN.blit(evil_t, (width_2 - int(evil_t.get_width() / 2) + 50, height_4 + 50))
                if evil_button.collidepoint((mx, my)):
                    if click:
                        # print()
                        # print('evil')
                        # print(turn)
                        # print(points)
                        # print(board)

                        points[turn_0] -= board[turn_0]*(2 + 2*hail_mary)

                        challenge = 5

            #ripple
            if challenge == 3:
                row_width = 80
                for x in range(int(len(ripple) / row_width) + 1):
                    ripple_t = small_font.render('{' + str(ripple[x * row_width:(x + 1) * row_width]) + '}', True,
                                                 (255, 255, 255))
                    WIN.blit(ripple_t,
                             (width_2 - int(ripple_t.get_width() / 2), height_4 + height_8 + x * ripple_t.get_height()))

        if ripple_show:
            row_width = 80
            for x in range(int(len(ripple) / row_width) + 1):
                ripple_t = small_font.render('{' + str(ripple[x * row_width:(x + 1) * row_width]) + '}', True,
                                             (255, 255, 255))
                WIN.blit(ripple_t,
                         (width_2 - int(ripple_t.get_width() / 2), height_4 + height_8 + x * ripple_t.get_height()))

        step = 0
        for a in alphabet.items():

            color_button = pygame.Rect(int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - height_8) - 23 + (int((a[1]%100)/2)), 40, 4)
            pygame.draw.rect(WIN, value_color[int(a[1]/12 + 1)%8], color_button)
            a_t = small_font.render(str(a[0]), True, (255, 255, 255))
            WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - height_8) - 25))
            # a_t = small_font.render(str(list(alphabet.keys()).index(a[0])), True, (255, 255, 255))
            # WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/4)))
            a_t = small_font.render(str(a[1]), True, (255, 255, 255))
            WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - height_8)))
            step += 1

        for x in range(2):

            turn_bar = pygame.Rect(width_8 + (width_2)*x, + 10, width_4, 10)
            pygame.draw.rect(WIN, value_color[(turn+x+1)%2*7], turn_bar)

            for hm in range(mary_counter[x]):
                mary_count_bar = pygame.Rect(width_8 + (width_2 + width_4) * x + count_step[x]*hm, height_8, 10, 10)
                pygame.draw.rect(WIN, value_color[5], mary_count_bar)

            for bead in range(rosary[x]):
                mary_count_bar = pygame.Rect(width_4 - width_16 + width_8 + (width_2 - width_8) * x + 30*bead, height_8, 20, 20)
                pygame.draw.rect(WIN, value_color[7], mary_count_bar)
                if mary_count_bar.collidepoint((mx, my)):
                    if click:
                        hail_mary = 1
                        wall = 1
                        rosary[x] -= 1


            step_0 = 0
            for h in history[x]:
                # print('step')
                # print(step_0)
                # print(int(HEIGHT / 4) - 50 + step_0 * 30)
                a_t = small_font.render(str(h), True, (255, 255, 255))
                WIN.blit(a_t, (int(WIDTH/8) + x*int(WIDTH/2 + WIDTH/4) - int(a_t.get_width()/2), int(HEIGHT / 4) - 50 + step_0 * 30))
                step_0 += 1
            if step_0 > 10:
                history[x] = history[x][1:]

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

                    turn_0 = turn

                    try:
                        while phrase[0] == ' ':
                            phrase = phrase[1:]
                        while phrase[-1] == ' ':
                            phrase = phrase[:-1]
                    except:
                        continue


                    alphabet, phrase_c, points, valid = sing(text, lexicon, alphabet, phrase, points, turn, valid)


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


                    if len(phrase) == int(level/2):
                        mary_counter[turn] += 1

                        if mary_counter[turn] == streak:
                            rosary[turn] += 1
                            rosary[turn] = rosary[turn] % 4
                            mary_counter[turn] = 0


                    turn += 1
                    turn = turn%2
                    level += 1
                    memory = 0
                    challenge = 0

                    phrase = ''



                elif event.key == pygame.K_LEFT:
                    print('left')

                elif event.key == pygame.K_RIGHT:
                    print()
                    print('right')

                    if valid == 3:
                        try:
                            memory += index_0
                            memory = memory % len(text)

                            # print(index_0)
                            # print(memory)
                            # print("phrase_c")
                            # print(phrase_c)


                            text_0 = text[memory + len(phrase_c)::]
                            # print(text_0[:200])

                            left = 0
                            right = 0
                            look_behind = text_0.index(phrase_c) + memory
                            look_ahead = text_0.index(phrase_c) + memory
                            index_0 = text_0.index(phrase_c) + 1

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
                            # print(left)
                            # print(text[left:right])
                            ripple = text[left:right]
                        except:
                            memory = 0

                elif event.key == pygame.K_UP:
                    ripple_show += 1
                    ripple_show = ripple_show % 2

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





                elif event.key == pygame.K_BACKSPACE:
                    phrase = phrase[:-1]


        if len(phrase) > int(level/2):
            phrase = phrase[1:]

Chaos_Window()
