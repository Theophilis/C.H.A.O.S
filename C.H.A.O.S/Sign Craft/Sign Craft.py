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

    alphabet = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
                'z': 0, ' ': 0}
    bigrams = {}
    history = {0:[], 1:[]}

    phrase = 'edward conlon cadden maclean'

    filename = 'library/niv_bible_words'
    infile = open(filename, "rb")
    lexicon = pickle.load(infile)
    infile.close

    text = open('library/bible-niv.txt', 'r')
    text = text.read()


    points = {0: 0, 1: 0}
    board = [0, 0]


    value_color = {0:(0, 0, 0), 1:(255, 0, 0), 2:(255, 255, 0), 3:(0, 255, 0), 4:(0, 255, 255), 5:(0, 0, 255), 6:(255, 0, 255), 7:(255, 255, 255)}

    # for p in phrase:
    #     print(p)
    #     alphabet[p] += 1
    #
    #
    # print(alphabet)
    #
    # alphabet = dict(sorted(alphabet.items(), key=lambda x: x[1], reverse=True))
    # print(alphabet)
    #
    # for a in alphabet.items():
    #     print()
    #     print(a)
    #     points[0] += int(100/ (a[1] + 1))
    #     print(points)

    def draw_text(text, font, color_dt, surface, x, y):
        textobj = font.render(text, 1, color_dt)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def speak(lexicon, alphabet, bigrams, phrase, points, turn, valid):

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

        phrase = phrase.lower()


        if phrase in history[0] or phrase in history[1]:
            valid = 1

            return alphabet, bigrams, phrase, points, valid

        if phrase in lexicon:
            valid =3

            for x in range(len(phrase)):
                alphabet[phrase[x]] += 1
                alphabet[phrase[x]] = alphabet[phrase[x]]

                if phrase[x] != ' ' and phrase[(x+1)%len(phrase)] != ' ':
                    bi = str(phrase[x] + phrase[(x+1)% len(phrase)])
                    if bi not in bigrams:
                        bigrams[bi] = 1

                    else:
                        bigrams[bi] += 1



            # print(alphabet)

            alphabet = dict(sorted(alphabet.items(), key=lambda x: x[1], reverse=True))
            bigrams = dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True))
            # print(alphabet)

            sum = 0
            for p in phrase:
                # print()
                # print(p, alphabet[p], list(alphabet.keys()).index(p))
                sum += list(alphabet.keys()).index(p)


            points[turn] += sum
            board[turn] = sum
        else:
            valid = 1

        return alphabet, bigrams, phrase, points, valid

    def sing(text, lexicon, alphabet, bigrams, phrase, points, turn, valid):

        phrase_c = phrase[::]

        if phrase in history[0] or phrase in history[1]:
            valid = 1

            return alphabet, bigrams, phrase, points, valid

        if phrase in text:
            print()
            print('found')
            print('phrase')
            print(phrase)
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

            phrase = phrase.lower()

            phrase = phrase.split()

            print("phrase")
            print(phrase)

            sum = 0
            for y in range(len(phrase)):
                print(y)
                if phrase[y] in lexicon:
                    valid =3

                    print(phrase[y])

                    for x in range(len(phrase[y])):
                        alphabet[phrase[y][x]] += 1
                        alphabet[phrase[y][x]] = alphabet[phrase[y][x]]

                        if phrase[y][x] != ' ' and phrase[y][(x+1)%len(phrase[y])] != ' ':
                            bi = str(phrase[y][x] + phrase[y][(x+1)% len(phrase[y])])
                            if bi not in bigrams:
                                bigrams[bi] = 1

                            else:
                                bigrams[bi] += 1



                    # print(alphabet)

                    alphabet = dict(sorted(alphabet.items(), key=lambda x: x[1], reverse=True))
                    bigrams = dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True))
                    # print(alphabet)

                    for p in phrase[y]:
                        # print()
                        # print(p, alphabet[p], list(alphabet.keys()).index(p))
                        sum += list(alphabet.keys()).index(p)

                else:
                    valid = 1
                    return alphabet, bigrams, phrase_c, points, valid

                points[turn] += sum
                board[turn] = sum

        return alphabet, bigrams, phrase_c, points, valid



    while run == 1:

        mx, my = pygame.mouse.get_pos()

        #display
        WIN.fill((0, 0, 0))

        phrase_t = main_font.render('{' + str(phrase) + '}', True, (255, 255, 255))
        WIN.blit(phrase_t, (width_2 - int(phrase_t.get_width()/2), height_2))

        valid_sign = pygame.Rect(width_2 - 50,height_32, 100, 100)
        pygame.draw.rect(WIN, value_color[valid], valid_sign)
        level_t = TITLE_FONT.render(str(int(level/2)), True, (255, 255, 255))
        WIN.blit(level_t, (width_2 - int(level_t.get_width()/2), height_32))
        points_t = TITLE_FONT.render(str(points[0]), True, (255, 255, 255))
        WIN.blit(points_t, (width_4 - int(points_t.get_width()/2), height_32))
        board_t = lable_font.render(str(board[0]), True, (255, 255, 255))
        WIN.blit(board_t, (width_4 - int(board_t.get_width()/2), height_8))

        points_1 = TITLE_FONT.render(str(points[1]), True, (255, 255, 255))
        WIN.blit(points_1, (width_4 + width_2 - int(points_1.get_width()/2), height_32))
        board_1 = lable_font.render(str(board[1]), True, (255, 255, 255))
        WIN.blit(board_1, (width_4 + width_2 - int(board_1.get_width()/2), height_8))

        if level > 7:
            #challenge
            challenge_button = pygame.Rect(width_2 - 100, height_4, 200, 50)
            pygame.draw.rect(WIN, (255, 0, 0), challenge_button)
            challenge_button = pygame.Rect(width_2 - 98, height_4 + 1, 196, 46)
            pygame.draw.rect(WIN, (0, 0, 0), challenge_button)
            challenge_t = main_font.render('challenge', True, (255, 255, 255))
            WIN.blit(challenge_t, (width_2 - int(challenge_t.get_width()/2), height_4))
            if challenge_button.collidepoint((mx, my)):
                if click:
                    challenge = 1

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

                        challenge = 0

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

                        challenge = 0


        step = 0
        for a in alphabet.items():

            color_button = pygame.Rect(int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/4) - 23 + (int((a[1]%100)/2)), 40, 4)
            pygame.draw.rect(WIN, value_color[int(a[1]/12 + 1)%8], color_button)
            a_t = small_font.render(str(a[0]), True, (255, 255, 255))
            WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/4) - 25))
            # a_t = small_font.render(str(list(alphabet.keys()).index(a[0])), True, (255, 255, 255))
            # WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/4)))
            a_t = small_font.render(str(a[1]), True, (255, 255, 255))
            WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/4)))
            step += 1

        step = 0
        for x in range(len(list(bigrams.items()))):
            if x > 26:
                continue
            a = list(bigrams.items())[x]
            color_button = pygame.Rect(int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/8) - 23 + (int((a[1]%100)/2)), 40, 4)
            pygame.draw.rect(WIN, value_color[int(a[1]/12 + 1)%8], color_button)
            a_t = small_font.render(str(a[0]), True, (255, 255, 255))
            WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/8) - 25))
            # a_t = small_font.render(str(list(alphabet.keys()).index(a[0])), True, (255, 255, 255))
            # WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/4)))
            a_t = small_font.render(str(a[1]), True, (255, 255, 255))
            WIN.blit(a_t, (int((WIDTH - 50*27) / 2)+step*50, int(HEIGHT - HEIGHT/8)))
            step += 1

        for x in range(2):
            step_0 = 0
            # print("x")
            # print(x)
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

                    while phrase[0] == ' ':
                        phrase = phrase[1:]
                    while phrase[-1] == ' ':
                        phrase = phrase[:-1]

                    if ' ' in phrase:
                        alphabet, bigrams, phrase, points, valid = sing(text, lexicon, alphabet, bigrams, phrase, points,
                                                                         turn, valid)

                    else:
                        alphabet, bigrams, phrase, points, valid = speak(lexicon, alphabet, bigrams, phrase, points, turn, valid)

                    phrase = phrase.lower()
                    history[turn].append(phrase)

                    turn += 1
                    turn = turn%2
                    level += 1

                    phrase = ''

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





                elif event.key == pygame.K_BACKSPACE:
                    phrase = phrase[:-1]


        if len(phrase) > int(level/2):
            phrase = phrase[1:]

Chaos_Window()
