import pygame
import pygame.camera
import pygame.surfarray as surfarray
import pygame.font
import cv2
import numpy as np
import pickle


pygame.init()
pygame.camera.init()

screen_width, screen_height = 1280, 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('C.H.A.O.S')




text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)




cam_list = pygame.camera.list_cameras()
if not cam_list:
    print("no cameras found")
    pygame.quit()
    exit()

print("camlist")
print(cam_list)

camera = pygame.camera.Camera(cam_list[0], (screen_width, screen_height))

camera.start()

image = camera.get_image()
value_color = {0: (0, 0, 0), 1: (255, 0, 0), 2: (255, 255, 0), 3: (0, 255, 0), 4: (0, 255, 255), 5: (0, 0, 255),
               6: (255, 0, 255), 7: (255, 255, 255), 8: (127, 127, 127)}


array_past = pygame.surfarray.array3d(image)
target= np.array(array_past[0][0])

points = 10
threshold = 128
thresholds = [threshold for x in range(points)]
rethresh = 0




# bets
digibet = {' ': 0, 'a': 1, 'i': 2, 't': 3,
           's': 4, 'c': 5, 'd': 6, 'm': 7,
           'g': 8, 'f': 9, 'w': 10, 'v': 11,
           'z': 12, 'q': 13, 'an': 14, 'er': 15,
           'ou': 16, 'in': 17, 'th': 18, 'j': 19,
           'x': 20, 'k': 21, 'y': 22, 'b': 23,
           'h': 24, 'p': 25, 'u': 26, 'l': 27,
           'n': 28, 'o': 29, 'r': 30, 'e': 31}
digibetu = {v: k for k, v in digibet.items()}
phrase = ''
phrase_pos = 0
score = 1
sign_bank = {}
phrase_past = phrase[::]

signame = "Theophilis"

try:
    filename = 'sign_bank/' + signame
    infile = open(filename, "rb")
    sign_bank = pickle.load(infile)
    infile.close

    print("loading" + signame)



except:
    print('new user')
    sign_bank = {}

running = True
while running:

    screen.fill((0, 0, 0))

    x = 20
    y = 20

    h = 10
    w = 10

    pos_x = int(screen_width/2 - h/2)
    pos_y = int(screen_height/2 - w/2)

    image = camera.get_image()

    # print()
    # print('image')
    # print(image)

    image_array = pygame.surfarray.array3d(image)


    def detect_change_in_roi_mse(img1, img2, roi_coords, threshold=1):

        y1, x1, y2, x2 = roi_coords
        roi1 = img1[y1:y2, x1:x2].astype(np.float32)
        roi2 = img2[y1:y2, x1:x2].astype(np.float32)

        mse = np.mean((roi1 - roi2)**2)

        # print("")
        # print(mse)
        # print(mse)


        return mse, mse > threshold




    # array_past = image_array

    image = pygame.surfarray.make_surface(image_array)


    screen.blit(image, (0, 0))


    ####right hand####
    x_s = 32
    y_s = 32
    x_g = 4
    y_g = 0
    x_pos = 128
    y_pos = 480
    palm_x = 320
    palm_y = 700


    hand = [0, 0, 0, 0, 0]
    tips = [48, 0, 0, 0, 0]

    for x in range(5):

        x_pos += x_s + x_g


        if x == 4:
            x_pos += x_s*2
            y_pos += y_s*6


        roi = (x_pos + x*x_s, y_pos + tips[x], x_pos +x_s + x*x_s, y_pos + y_s + tips[x])



        mse, change = detect_change_in_roi_mse(array_past, image_array, roi, thresholds[x])

        if rethresh == 1:
            if thresholds[x] < mse:
                thresholds[x] = mse

        hand[x] = change

        # print('')
        # print("change")
        # print(change)

        lesson_t = small_font.render(str(change), True, value_color[7])
        screen.blit(lesson_t, (screen_width/64 + x*128, screen_height / 2 + screen_height/4))
        lesson_t = small_font.render(str(int(mse)), True, value_color[7])
        screen.blit(lesson_t, (screen_width/64 +x * 128, screen_height /2 + screen_height/4 + 64))
        lesson_t = small_font.render(str(int(thresholds[x])), True, value_color[7])
        screen.blit(lesson_t, (screen_width/64 +x * 128, screen_height /2 + screen_height/4 + 128))

        t_line = pygame.Rect(palm_x + x*x_s/2, palm_y, x_s/2, y_s/2)
        pygame.draw.rect(screen, value_color[0 + change*7], t_line)

        t_line = pygame.Rect(roi[0], roi[1], x_s, y_s)
        pygame.draw.rect(screen, value_color[0 + change*7], t_line)

    hand_value = hand[0]*16 + hand[1]*8 + hand[2]*4 + hand[3]*2 + hand[4]*1

    lesson_t = main_font.render(str(hand_value), True, value_color[7])
    screen.blit(lesson_t, (screen_width / 4, screen_height / 4))

    lesson_t = main_font.render(str(digibetu[hand_value]), True, value_color[7])
    screen.blit(lesson_t, (screen_width / 4, screen_height / 4 + 64))


    letter = digibetu[hand_value]

    if phrase != '':
        if phrase != phrase_past:

            if phrase not in sign_bank:
                sign_bank[phrase] = score
            else:
                score = sign_bank[phrase]
                sign_bank[phrase] = score


            print(phrase, sign_bank[phrase])

            phrase_past = phrase[::]
            score = 1

            filename = 'sign_bank/' + signame
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close


        elif letter == phrase[phrase_pos]:
            phrase_pos += 1

            if phrase_pos == len(phrase):

                score += 1
                phrase_pos = 0

    ####left hand####
    x_s = 32
    y_s = 32
    x_g = 4
    y_g = 0
    x_pos = 700
    y_pos = 480
    palm_x = 800
    palm_y = 700

    hand = [0, 0, 0, 0, 0]
    tips = [0, 0, 0, 0, 48]

    for x in range(5):

        x_pos += x_s + x_g

        if x == 0:
            x_pos -= x_s*2
            y_pos += y_s*6

        elif x == 1:
            x_pos += x_s*2
            y_pos -= y_s*6

        roi = (x_pos + x * x_s, y_pos + tips[x], x_pos + x_s + x * x_s, y_pos + y_s + tips[x])

        mse, change = detect_change_in_roi_mse(array_past, image_array, roi, thresholds[x+5])

        if rethresh == 1:
            if thresholds[x+5] < mse:
                thresholds[x+5] = mse


        hand[x] = change

        # print('')
        # print("change")
        # print(change)


        lesson_t = small_font.render(str(change), True, value_color[7])
        screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4))
        lesson_t = small_font.render(str(int(mse)), True, value_color[7])
        screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4 + 64))
        lesson_t = small_font.render(str(int(thresholds[x])), True, value_color[7])
        screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4 + 128))

        t_line = pygame.Rect(palm_x + x * x_s / 2, palm_y, x_s / 2, y_s / 2)
        pygame.draw.rect(screen, value_color[0 + change * 7], t_line)

        t_line = pygame.Rect(roi[0], roi[1], x_s, y_s)
        pygame.draw.rect(screen, value_color[0 + change * 7], t_line)

    rethresh = 0
    hand_value = hand[0] * 1 + hand[1] * 2 + hand[2] * 4 + hand[3] * 8 + hand[4] * 16

    lesson_t = main_font.render(str(hand_value), True, value_color[7])
    screen.blit(lesson_t, (screen_width / 2 + screen_width/4, screen_height / 4))

    lesson_t = main_font.render(str(digibetu[hand_value]), True, value_color[7])
    screen.blit(lesson_t, (screen_width / 2 + screen_width/4, screen_height / 4 + 64))

    walk = 0
    for x in range(len(phrase)):
        color = value_color[7]
        if x == phrase_pos:
            color = value_color[4]
        lesson_t = lable_font.render(str(phrase[x]), True, color)
        screen.blit(lesson_t, (screen_width / 2 + walk, screen_height / 8))
        walk += lesson_t.get_width()

    letter = digibetu[hand_value]

    if phrase != '':
        if phrase != phrase_past:

            if phrase not in sign_bank:
                sign_bank[phrase] = score
            else:
                score = sign_bank[phrase]
                sign_bank[phrase] = score


            print(phrase, sign_bank[phrase])

            phrase_past = phrase[::]
            score = 1

            filename = 'sign_bank/' + signame
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close

        elif letter == phrase[phrase_pos]:
            phrase_pos += 1

            if phrase_pos == len(phrase):

                score += 1
                phrase_pos = 0


    lesson_t = lable_font.render(str(score), True, value_color[7])
    screen.blit(lesson_t, (screen_width / 2, screen_height / 8 - 64))

    #####################
    pygame.display.flip()










    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            filename = 'sign_bank/' + signame
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         pygame.quit()
        #
        #     elif event.key == pygame.K_RETURN:
        #
        #         threshold = mse
        #         array_past = image_array
        #
        #         print(threshold)
        #         print('past')

        # keyboard
        elif event.type == pygame.KEYDOWN:

            def type(phrase, letter):
                print("letter")

                phrase += letter

                return phrase


            if event.key == pygame.K_ESCAPE:
                filename = 'sign_bank/' + signame
                outfile = open(filename, 'wb')
                pickle.dump(sign_bank, outfile)
                outfile.close
                pygame.quit()

            elif event.key == pygame.K_RETURN:


                rethresh = 1

                # print()
                # print(current)
                # print(lessons[current])
                # print(phrase)
                #
                # print(len(lessons[current]))
                # print(len(phrase))
                #
                # records['current'] = current
                #
                # focus = 0
                #
                # if phrase == lessons[current]:
                #     valid = 3
                #     power[0] += 1
                # else:
                #     valid = 1
                #     power[0] = 0
                #
                # clock[1] = clock[0]
                # clock[0] = time.time()
                #
                # # records
                # if valid == 3:
                #
                #     if record == 1:
                #
                #         if time_0 < records[current]:
                #             records[current] = time_0
                #             valid = 4
                #
                #         filename = 'records/' + record_name
                #         outfile = open(filename, 'wb')
                #         pickle.dump(records, outfile)
                #         outfile.close
                #
                #     current += 1
                #
                # phrase_1 = phrase[::]
                # phrase = ''
                # settings = 0
                # men = 0


            elif event.key == pygame.K_F1:

                print("wu")
                phrase = ''


            elif event.key == pygame.K_F2:
                array_past = image_array

            # elif event.key == pygame.K_LEFT:
            #     current -= 1
            #
            # elif event.key == pygame.K_RIGHT:
            #     current += 1
            #
            elif event.key == pygame.K_UP:

                for x in range(len(thresholds)):
                    thresholds[x] += 1

            elif event.key == pygame.K_DOWN:

                for x in range(len(thresholds)):
                    thresholds[x] = thresholds[x] - 1

            # upper
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

            # number
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



            # lower
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

camera.stop()
pygame.quit()


