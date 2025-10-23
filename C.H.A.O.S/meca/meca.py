import pygame
import pygame.camera
import pygame.surfarray as surfarray
import pygame.font
import numpy as np
import pickle
import time
from datetime import datetime



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


def detect_change_in_roi_mse(img1, img2, roi_coords, threshold=1):
    y1, x1, y2, x2 = roi_coords
    roi1 = img1[y1:y2, x1:x2].astype(np.float32)
    roi2 = img2[y1:y2, x1:x2].astype(np.float32)

    mse = np.mean((roi1 - roi2) ** 2)

    # print("")
    # print(mse)
    # print(mse)

    return mse, mse > threshold, roi1, roi2


def base_x(n, b):
    e = n // b
    q = n % b
    if n == 0:
        return '0'
    elif e == 0:
        return str(q)
    else:
        return base_x(e, b) + str(q)


def rule_gen(rule, base=2, width=0, string=0):
    rules = dict()

    if string != 0:
        int_rule = [l for l in rule]


    else:

        if base == 2:

            int_rule = bin(rule).replace('0b', '')


        else:

            int_rule = base_x(rule, base)

        x = int_rule[::-1]

        if width == 0:
            while len(x) < base ** view:
                x += '0'

            bnr = x[::-1]
            int_rule = list(bnr)

        else:
            while len(x) < width:
                x += '0'

            bnr = x[::-1]
            int_rule = list(bnr)

    # print(" ")
    # print("int_rule")
    # [print(int_rule)]

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

        rules[tuple(key)] = int_rule[-x - 1]

    # print("")
    # print("rules")
    # print(rules)

    return rules, int_rule


#######flow######
# print("")
# print("water")
# print(water)
# print(flow)



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
value_color = {0: (0, 0, 0), 1: (255, 0, 255), 2: (0, 255, 255), 3: (255, 255, 0), 4: (128, 128, 128), 5: (255, 0, 0),
               6: (0, 255, 0), 7: (0, 0, 255), 8: (255, 255, 255), 9: (255, 255, 255)}
color_array = np.array(list(value_color.values()), dtype=int)

array_past = pygame.surfarray.array3d(image)
target= np.array(array_past[0][0])

points = 10
threshold = 64
thresholds = [threshold for x in range(points)]
rethresh = 0




# bets
ui = 0
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
goal_bin = '00000'

hands = [[], []]
code = ''
code_0 = ' '

score = 1
score_h = 0
sign_bank = {}
phrase_past = phrase[::]
tts = [0, 0]
times = []
tts_0 = time.time()
tts_1 = time.time()
stenograph = []

signame = "Theophilis"

try:
    filename = 'sign_bank/' + signame
    infile = open(filename, "rb")
    sign_bank = pickle.load(infile)
    infile.close

    print("loading" + signame)

    stenograph = sign_bank['steno']

except:
    print('new user')
    sign_bank = {}



ram = {}

mse_mem = {0:[threshold], 1:[threshold], 2:[threshold], 3:[threshold], 4:[threshold],
           5:[threshold], 6:[threshold], 7:[threshold], 8:[threshold], 9:[threshold]}

#####flow#####

pos_x = screen_width / 2
pos_y = screen_height / 2
dim = 2
base = 3
view = 5
bv = base ** view
bvv = base ** view ** view
bbv = base**base**view
rv = 137

rules, rule = rule_gen(rv, base)
rule = np.array(rule)

print(rule)

l = 592
h = l
lh = l * h
pos_x = int(screen_width / 2) - int(l / 2)
pos_y = int(screen_height / 3) - int(h / 2)
pos_z = 0

if dim == 1:
    flow = np.zeros(l, dtype=int)
    flow[int(l / 2)] = 1
    water = np.zeros((h, l), dtype=int)
    water[0] = flow

if dim == 2:
    flow = np.zeros((h, l), dtype=int)
    flow[int(l / 2), int(h / 2)] = 1
    water = np.zeros((h, l), dtype=int)


###clock###
time_d = time.time()
time_b = time.time()
print(time_d)
print(time_b)




##sythn##


sample_rate = 44100
duration = 1
frequency = 440 * (2 ** 1 / 12) ** digibet[code_0]
max_amplitude = 2 ** 15 - 1
previous_note = []


t = np.linspace(0, duration, int(sample_rate * duration), False)
mono_wave = max_amplitude * np.sin(frequency * t * 2 * np.pi)
mono_samples = mono_wave.astype(np.int16)

pygame.mixer.pre_init(sample_rate, -16, channels=1)

stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
stereo_sound = pygame.sndarray.make_sound(stereo_samples)


start = 55
key_sin = []
key_square = []
key_saw = []
key_triangle = []

key_track = {}
track_shift = 0

waffle_house = [2, 2, 1, 2, 2, 2, 1]
pentatonic = [0, 2, 2, 3, 2, 3, 2, 2]
major = [0, 7, 5, 4, 3, 5, 7, 5]

scale = pentatonic
octave = 12

for x in range(128):

    ###sin###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sin_wave = max_amplitude * np.sin(frequency * t * 2 * np.pi)
    mono_samples = sin_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)
    key_sin.append(stereo_sound)


    ###square###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    square_wave = max_amplitude * np.sign(np.sin(frequency * t * 2 * np.pi))
    mono_samples = square_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)

    key_square.append(stereo_sound)

    ###saw###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    saw_wave = max_amplitude * (t * frequency % 1 * 2 - 1)
    mono_samples = saw_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)
    key_saw.append(stereo_sound)

    ###triangle###
    frequency = start * 2**(x/12)
    # print(frequency)

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    triangle_wave = max_amplitude * (2 * np.abs(saw_wave / max_amplitude) - 1)
    mono_samples = triangle_wave.astype(np.int16)

    pygame.mixer.pre_init(sample_rate, -16, channels=1)

    stereo_samples = np.repeat(mono_samples.reshape(-1, 1), 2, axis=1)
    stereo_sound = pygame.sndarray.make_sound(stereo_samples)

    key_triangle.append(stereo_sound)




#drums

def generate_kick(duration_s, sample_rate=44100, max_amplitude=32767):

    t = np.linspace(0, duration_s, int(sample_rate*duration_s), endpoint=False)

    decaying_freq = 200 * np.exp(-t * 20) + 50

    phase = np.cumsum(decaying_freq/sample_rate) * 2 * np.pi
    kick_wave = max_amplitude * np.sin(phase)

    envelope = np.exp(-t * 8)
    kick_wave *= envelope

    return kick_wave.astype(np.int16)

def generate_snare(duration_s, sample_rate = 44100, max_amplitude = 32767):

    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)

    body_freq = 200
    body_envelope = np.exp(-t * 20)
    body_wave = np.sin(2*np.pi*body_freq*t) * body_envelope

    noise = np.random.uniform(-1, 1, len(t))

    noise_envelope = np.exp(-t * 50)
    noise_wave = noise * noise_envelope

    snare_wave = (0.5 * body_wave + 0.5 * noise_wave)

    final_envelope = np.exp(-t * 10)

    snare_wave *= final_envelope

    snare_wave *= max_amplitude

    return snare_wave.astype(np.int16)

def generate_hihat(duration_s, sample_rate=44100, max_amplitude=32767):

    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)

    white_noise = np.random.uniform(-1, 1, len(t))

    envelope = np.exp(-t * 40)

    hihat_wave = white_noise * envelope
    hihat_wave *= max_amplitude

    return hihat_wave.astype(np.int16)




tempo = 0

kick_sample = generate_kick(0.3)
snare_sample = generate_snare(0.25)
hihat_sample = generate_hihat(0.1)


kick_stereo = np.repeat(kick_sample.reshape(-1, 1), 2, axis=1)
snare_stereo = np.repeat(snare_sample.reshape(-1, 1), 2, axis=1)
hihat_stereo = np.repeat(hihat_sample.reshape(-1, 1), 2, axis=1)


kick_sound = pygame.sndarray.make_sound(kick_stereo)
snare_sound = pygame.sndarray.make_sound(snare_stereo)
hihat_sound = pygame.sndarray.make_sound(hihat_stereo)


running = True
while running:

    screen.fill((0, 0, 0))

    image = camera.get_image()
    image_array = pygame.surfarray.array3d(image)

    ###flow###
    if dim == 1:
        currents = []
        for x in range(view):

            x = x + 1

            if x == 0:
                currents.append(flow)
            else:
                if x % 2 == 0:
                    shift = -int(x / 2)
                else:
                    shift = int(x / 2)
                flow_r = np.roll(flow, shift)
                currents.append(flow_r)

            # print(currents[x-1])
        current = currents[1] * 1 + currents[0] * base + currents[2] * base**2
        # print(current)
        row = rule[-current.astype(int)]
        # print(row)

        water = np.roll(water, l)
        water[0] = row
        flow = water[0]
        code_flow = digibet[code_0]
        # print(code_flow)
        flow[0+ code_flow * int(l/32)] = 1

        image_flow = color_array[water]

        image_array[pos_x:pos_x+l, pos_y:pos_y+h] = np.rot90(image_flow, 4)

    elif dim == 2:
        flow[int(l / 2), int(h / 2)] = 1
        currents = []

        flow_1 = np.roll(flow, -1)
        flow_2 = np.roll(flow, 1)
        flow_3 = np.roll(flow, -l)
        flow_4 = np.roll(flow, l)

        currents = [flow, flow_1, flow_2, flow_3, flow_4]

        current = currents[3] * 1 + currents[1] * base + currents[0] * base ** 2 + currents[2] * base ** 3 + currents[4] * base ** 4
        # print()
        # print(current)
        water = rule[-current.astype(int)]
        water = water.astype(int)
        # print()
        # print(row)




        flow = water
        sign_value = digibet[code_0]
        flow[int(l / 2), int(h / 2) +sign_value] = 1

        image_flow = color_array[flow]
        image_array[pos_x:pos_x+l, pos_y:pos_y+h] = image_flow

        # flatten = water.flatten()
        # scaled = (flatten * 2 - 1) * max_amplitude
        # sample = scaled.astype(np.int16)
        # stereo = sample.reshape(-1, 1)
        # stack = np.column_stack((stereo, stereo))
        # flow_sound = pygame.sndarray.make_sound(stack)
        #
        # flow_sound.play()



    image = pygame.surfarray.make_surface(image_array)
    screen.blit(image, (0, 0))


    ####right hand####
    x_s = 32
    y_s = 32
    x_g = 4
    y_g = 0
    x_pos = 32
    y_pos = 640
    palm_x = x_pos + x_s*6
    palm_y = y_pos + y_s*9

    hand = [0, 0, 0, 0, 0]
    tips = [64, 16, 0, 24, 0]

    for x in range(5):

        x_pos += x_s + x_g


        if x == 4:
            x_pos += x_s*1
            y_pos += y_s*5


        roi = (x_pos + x*x_s, y_pos + tips[x], x_pos +x_s + x*x_s, y_pos + y_s + tips[x])



        mse, change, roi1, roi2 = detect_change_in_roi_mse(array_past, image_array, roi, thresholds[x])


        if rethresh == 1:

            mask_color = image_array[int(screen_width/2), int(screen_height/2)]


            ram[x] = [roi1, roi2]

            mse_mem[x].append(mse)


            if thresholds[x] != mse:
                thresholds[x] = mse + threshold


        mse_avg = int(sum(mse_mem[x])/len(mse_mem[x]))

        if mse < mse_avg + thresholds[x]:
            hand[x] = 0
        else:
            hand[x] = 1

        # hand[x] = change

        # print('')
        # print("change")
        # print(change)


        if ui == 1:

            lesson_t = small_font.render(str(hand[x]), True, value_color[7])
            screen.blit(lesson_t, (screen_width/64 + x*128, screen_height / 2 + screen_height/4))
            lesson_t = small_font.render(str(int(mse)), True, value_color[7])
            screen.blit(lesson_t, (screen_width/64 +x * 128, screen_height /2 + screen_height/4 + 64))
            lesson_t = small_font.render(str(int(mse_avg)), True, value_color[7])
            screen.blit(lesson_t, (screen_width/64 +x * 128, screen_height /2 + screen_height/4 + 96))
            lesson_t = small_font.render(str(int(thresholds[x])), True, value_color[7])
            screen.blit(lesson_t, (screen_width/64 +x * 128, screen_height /2 + screen_height/4 + 128))

        value_rect = pygame.Rect(palm_x + x*x_s/2, palm_y, x_s/2, y_s/2)
        pygame.draw.rect(screen, value_color[0 + hand[x]*9], value_rect)

        tip_rect = pygame.Rect(roi[0], roi[1], x_s, y_s)
        pygame.draw.rect(screen, value_color[0 + hand[x]*9], tip_rect)

        pygame.draw.line(screen, value_color[0 + int(goal_bin[x]) * 9], (palm_x, palm_y), (roi[0], roi[1]))


    hand_value = hand[0]*16 + hand[1]*8 + hand[2]*4 + hand[3]*2 + hand[4]*1

    lesson_t = main_font.render(str(hand_value), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 4 - 64, screen_height / 2 + 64))

    lesson_t = main_font.render(str(digibetu[hand_value]), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 4 - 32, screen_height / 2 + 64))


    letter = digibetu[hand_value]

    hands[0] = letter

    ####left hand####
    x_s = 32
    y_s = 32
    x_g = 4
    y_g = 0
    x_pos = 880
    y_pos = 640
    palm_x = x_pos + x_s*6
    palm_y = y_pos + y_s*9


    hand = [0, 0, 0, 0, 0]
    tips = [0, 24, 0, 16, 64]

    for x in range(5):

        x_pos += x_s + x_g

        if x == 0:
            x_pos -= x_s*1
            y_pos += y_s*5

        elif x == 1:
            x_pos += x_s*2
            y_pos -= y_s*6

        roi = (x_pos + x * x_s, y_pos + tips[x], x_pos + x_s + x * x_s, y_pos + y_s + tips[x])

        roi_palm = (x_pos + x*x_s, y_pos + y_s*4)

        mse, change, roi1, roi2 = detect_change_in_roi_mse(array_past, image_array, roi, thresholds[x+5])

        if rethresh == 1:

            ram[x+5] = [roi1, roi2]

            mse_mem[x+5].append(mse)


            if thresholds[x+5] != mse:
                thresholds[x+5] = mse + threshold

        mse_avg = int(sum(mse_mem[x+5])/len(mse_mem[x+5]))

        if mse < mse_avg + thresholds[x+5]:
            hand[x] = 0
        else:
            hand[x] = 1

        # hand[x] = change

        # print('')
        # print("change")
        # print(change)

        if ui == 1:

            lesson_t = small_font.render(str(hand[x]), True, value_color[7])
            screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4))
            lesson_t = small_font.render(str(int(mse)), True, value_color[7])
            screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4 + 64))
            lesson_t = small_font.render(str(int(mse_avg)), True, value_color[7])
            screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4 + 96))
            lesson_t = small_font.render(str(int(thresholds[x])), True, value_color[7])
            screen.blit(lesson_t, (screen_width / 2 + x * 128, screen_height / 2 + screen_height / 4 + 128))

        t_line = pygame.Rect(palm_x + x * x_s / 2, palm_y, x_s / 2, y_s / 2)
        pygame.draw.rect(screen, value_color[0 + hand[x] * 9], t_line)

        t_line = pygame.Rect(roi[0], roi[1], x_s, y_s)
        pygame.draw.rect(screen, value_color[0 + hand[x] * 9], t_line)

        goal_bin_r = goal_bin[::-1]
        pygame.draw.line(screen, value_color[0 + int(goal_bin_r[x]) * 9], (palm_x, palm_y), (roi[0], roi[1]))

    rethresh = 0
    hand_value = hand[0] * 1 + hand[1] * 2 + hand[2] * 4 + hand[3] * 8 + hand[4] * 16

    lesson_t = main_font.render(str(hand_value), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 2 + screen_width/4, screen_height / 2 + 64))

    lesson_t = main_font.render(str(digibetu[hand_value]), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 2 + screen_width/4, screen_height / 2 + 96))

    lesson_t = main_font.render(str(rv), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 2, screen_height / 32))

    lesson_t = main_font.render(str(tts_0), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 2, screen_height / 4))


    ###stats###
    times_limit = 10
    for x in range(len(times)):
        if x > times_limit:
            break
        lesson_t = small_font.render(str(times[x]), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 8, screen_height / 8 + lesson_t.get_height()*x))

    times_limit = 10
    sign_items = list(sign_bank.items())[::]

    for s in sign_items:
        if s[0] == 'steno':
            sign_items.pop(sign_items.index(s))

    sign_items = sorted(sign_items, key=lambda x: x[1][0], reverse=True)
    for x in range(len(sign_items)):
        if x > times_limit:
            break
        lesson_t = small_font.render(str((sign_items[x][1][0], sign_items[x][0])), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 2 + screen_width/4, screen_height / 8 + lesson_t.get_height()*x))

    walk = 0
    for x in range(len(phrase)):
        color = value_color[9]
        if x == phrase_pos:
            color = value_color[5]
        lesson_t = lable_font.render(str(phrase[x]), True, color)
        screen.blit(lesson_t, (screen_width / 2 + walk - len(phrase)*8, screen_height / 4 + lesson_t.get_height()))
        walk += lesson_t.get_width()

    letter = digibetu[hand_value]

    hands[1] = letter




    ####code####
    if hands[0] == hands[1]:

        if hands[0] != code_0:

            code += hands[0]
            code_0 = hands[0]

            stenograph.append((code_0, round(time.time() - tts_1, 3), datetime.now()))

            sign_bank['steno'] = stenograph

            tts_1 = time.time()

            rv += digibet[code_0]
            rv = rv%bbv

            # print("")
            # print(rv)
            # print(rule)
            rules, rule = rule_gen(rv, base)
            # print(rule)

            rule = np.array(rule)


    ###typing###
    if phrase != '':
        goal_bin = base_x(digibet[phrase[phrase_pos]], 2)
        if len(goal_bin) < 5:
            zeros = ''
            for x in range(5-len(goal_bin)):
                zeros += '0'
            goal_bin = zeros + goal_bin
        # print(goal_bin)

        if phrase != phrase_past:
            tts[0] = time.time()
            score = 1

            if phrase not in sign_bank:
                sign_bank[phrase] = (score, rv, [])

                score, rv, times = sign_bank[phrase]
            else:

                try:
                    score, rv , times = sign_bank[phrase]
                except:

                    try:
                        score, rv = sign_bank[phrase]
                        times = []

                    except:

                        score = sign_bank[phrase]
                        rv = rv
                        times = []




            # print(phrase, sign_bank[phrase])

            phrase_past = phrase[::]

            filename = 'sign_bank/' + signame
            outfile = open(filename, 'wb')
            pickle.dump(sign_bank, outfile)
            outfile.close

        elif letter == phrase[phrase_pos] or letter == phrase[phrase_pos:phrase_pos+2]:

            phrase_pos += 1
            if len(letter) == 2:
                phrase_pos += 1

            if phrase_pos == 1:
                tts[0] = time.time()

            if phrase_pos == len(phrase):

                score += 1
                phrase_pos = 0
                tts[1] = time.time()


                tts_0 = round(tts[1] - tts[0], 3)
                tts[0] = time.time()

                times_0 = []
                t_max = 99999999999999999999999999999999999999
                for t in times:
                    if t < t_max and t > 0:
                        times_0.append(round(t, 3))
                times = times_0

                # print()
                # print(tts)
                # print(tts_0)

                times.append(tts_0)
                times = sorted(times)

                # print()
                # print("times")
                # print(times)

                code = ''

                sign_bank[phrase] = (score, rv, times)

                filename = 'sign_bank/' + signame
                outfile = open(filename, 'wb')
                pickle.dump(sign_bank, outfile)
                outfile.close

                for x in range(len(phrase)):
                    rv += digibet[phrase[x]]
                rv = rv % bbv

                # print("")
                # print(rv)
                # print(rule)
                rules, rule = rule_gen(rv, base)
                # print(rule)

                rule = np.array(rule)



    for x in range(int(len(code)/64)+1):
        lesson_t = main_font.render(str(code), True, value_color[9])
        screen.blit(lesson_t, (screen_width / 2 - int(lesson_t.get_width()/2), screen_height / 8 - 128 + x*lesson_t.get_height()))

    lesson_t = lable_font.render(str(score), True, value_color[9])
    screen.blit(lesson_t, (screen_width / 2, screen_height / 8 - 64))



    ###synth###



    beat = 1
    #####drums####
    #
    # if time.time() - time_d > beat/8:
    #
    #     # print(tempo)
    #
    #
    #     if tempo % 16 == 0:
    #         # print('kick')
    #         kick_sound.play()
    #
    #     if tempo % 16 == 10:
    #         # print('kick')
    #         kick_sound.play()
    #
    #
    #
    #     if tempo%16 == 4:
    #         snare_sound.play()
    #
    #     if tempo%16 == 12:
    #         hihat_sound.play()
    #
    #
    #     tempo += 1
    #
    #     time_d = time.time()
    #
    #
    #

    volume = 0.5

    ######bong#####
    if time.time() - time_b > beat:

        # if dim == 1:
        #     water0 = np.rot90(water[::], 2)
        # elif dim == 2:
        #     water0 = water

        flatten = water.flatten()
        scaled = (flatten * 2 - 1) * max_amplitude
        sample = scaled.astype(np.int16)
        stereo = sample.reshape(-1, 1)
        stack = np.column_stack((stereo, stereo))
        flow_sound = pygame.sndarray.make_sound(stack)

        flow_sound.play()



        # print()
        # print('bong')
        #



        # note_value = digibet[code_0]
        #
        #
        # # print(note_value)
        #
        # octave = 24

        # note_shape = int(note_value/8)
        # note_scale = sum(waffle_house[:note_value%8])
        #
        # note_scale = sum(scale[:note_value%8])
        # note_scale += track_shift
        # note_scale = note_scale + octave % len(key_sin)

        # print(note_shape)
        # print(note_scale)

        # note_shape = 0
        # note_scale = note_value + octave
        #
        # if note_shape == 0:
        #
        #     key_sin[note_scale].set_volume(volume)
        #     key_sin[note_scale].play()
        #
        # elif note_shape == 1:
        #
        #     key_square[note_scale].set_volume(volume-.25)
        #     key_square[note_scale].play()
        #
        # elif note_shape == 2:
        #
        #     key_saw[note_scale].set_volume(volume-.25)
        #     key_saw[note_scale].play()
        #
        # elif note_shape == 3:
        #
        #     key_triangle[note_scale].set_volume(volume)
        #     key_triangle[note_scale].play()
        #


        time_b = time.time()







    ####events####
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
                array_past = image_array

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
                phrase_pos -= 1
                if phrase_pos < 0:
                    phrase_pos = 0

    #####################
    pygame.display.flip()
    pygame.display.flip()

camera.stop()
pygame.quit()


