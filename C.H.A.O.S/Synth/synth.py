import numpy as np
import scipy.io.wavfile as wav
import socket
import pickle
import pygame
import time
from pygame import mixer

pygame.mixer.init()
pygame.mixer.set_num_channels(64)

#https://www.youtube.com/watch?v=zBFeT8fkjfI


def interpolate_linearly(wave_table, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wave_table.shape[0]

    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    final_interpolation = (truncated_index_weight * wave_table[truncated_index] +
                   next_index_weight * wave_table[next_index])

    return final_interpolation


#fades
def fade_in_out(signal, fade_length=27000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    return signal

def fade_in(signal, fade_length=27000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    return signal

def fade_out(signal, fade_length=27000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    return signal

#sawtooth
def sawtooth(x):
    return (x + np.pi) / np.pi % 2-1


def main(f=110):

    sample_rate = 44100
    # f = 110
    t = 3
    # waveform = np.sin
    waveform = sawtooth
    waveform_type = 'sawtooth'

    wavetable_length = 64
    wave_table = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((t * sample_rate,))

    index = 0
    indexIncrement = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        # output[n] = wave_table[int(np.floor(index))]
        output[n] = interpolate_linearly(wave_table, index)
        index += indexIncrement
        index %= wavetable_length

    #volume
    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    #fade
    output = fade_out(output, 24000)

    wav.write(waveform_type + '/' + waveform_type + str(f) + 'hz' + '.wav', sample_rate, output.astype(np.float32))

# if __name__ == '__main__':
#     main()

for x in range(4):
    main(100 + x*100)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '192.168.1.3', 21621
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
# sock.bind(server_address)

x=x
#####game#####

pygame.init()
pygame.display.init()
current_display = pygame.display.Info()
WIDTH, HEIGHT = current_display.current_w - 50, current_display.current_h - 100
# WIDTH, HEIGHT = 400, 400
width_2 = int(WIDTH / 2)
width_3 = int(WIDTH / 3)
width_4 = int(WIDTH / 4)
width_8 = int(WIDTH / 8)
width_16 = int(WIDTH / 16)
width_32 = int(WIDTH / 32)
width_64 = int(WIDTH / 64)
width_128 = int(WIDTH / 128)
width_256 = int(WIDTH / 256)
width_512 = int(WIDTH / 512)

height_2 = int(HEIGHT / 2)
height_4 = int(HEIGHT / 4)
height_8 = int(HEIGHT / 8)
height_16 = int(HEIGHT / 16)
height_32 = int(HEIGHT / 32)
height_64 = int(HEIGHT / 64)
height_128 = int(HEIGHT / 128)
height_256 = int(HEIGHT / 256)
height_512 = int(HEIGHT / 512)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

text_font = pygame.font.SysFont("leelawadeeuisemilight", 16)
small_font = pygame.font.SysFont("leelawadeeuisemilight", 24)
main_font = pygame.font.SysFont("leelawadeeuisemilight", 32)
lable_font = pygame.font.SysFont("leelawadeeuisemilight", 48)
TITLE_FONT = pygame.font.SysFont("leelawadeeuisemilight", 64)


click = False

value_color = {0: (0, 0, 0), 1: (255, 0, 0), 2: (255, 255, 0), 3: (0, 255, 0), 4: (0, 255, 255), 5: (0, 0, 255),
               6: (255, 0, 255), 7: (255, 255, 255), 8: (127, 127, 127)}

run = 1
#number_of_sensors
nos = 8

clock = pygame.time.Clock()

glove_name = 'gos'
glove_values = [[0, [0, 0, 0, 0, 0, 0]] for x in range(nos)]
sensor_order = ['arm', 'wrist', 'hand', 'thumb', 'index', 'middle', 'ring', 'pinky']

#orients
orients = ['FB', 'LR', 'UD']
#chaotomata
if glove_name == 'chaotomata':
    orientation = {'FB':{0:1, 1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0},
                   'LR':{0:0, 1:0, 2:0, 3:1, 4:1, 5:1, 6:1, 7:1},
                   'UD':{0:2, 1:2, 2:2, 3:3, 4:3, 5:2, 6:2, 7:2}}
#gos
if glove_name == 'gos':
    orientation = {'FB':{0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0},
                   'LR':{0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1},
                   'UD':{0:2, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2}}

calibrations = {'FB': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'LR': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'UD': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}
midpoints = {'FB': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'LR': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                'UD': [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}

#calibrations
try:
    filename = 'calibrations/' + glove_name
    infile = open(filename, "rb")
    revelations = pickle.load(infile)
    infile.close

except:

    revelations = {'FB':[[0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
                    'LR':[[0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
                    'UD':[[0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]}


compass = [[0, 0, 0, 0, 0, 0] for x in range(nos)]
g_time = [[time.time(), 0] for x in range(nos)]
g_sum = [[0, 0, 0] for x in range(nos)]
g_switch = [1 for x in range(nos)]




def interpolate_linearly(wave_table, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wave_table.shape[0]

    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    final_interpolation = (truncated_index_weight * wave_table[truncated_index] +
                   next_index_weight * wave_table[next_index])

    return final_interpolation

#fades
def fade_in_out(signal, fade_length=27000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    return signal

def fade_in(signal, fade_length=27000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    return signal

def fade_out(signal, fade_length=27000):
    fade_in = (1-np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    return signal

#sawtooth
def sawtooth(x):
    return (x + np.pi) / np.pi % 2-1

def main(f=110, waveform_type='sine', sample_rate=44100):

    # sample_rate = 44100
    # f = 110
    t = 3

    if waveform_type == 'sine':
        waveform = np.sin
    elif waveform_type == 'sawtooth':
        waveform = sawtooth

    wavetable_length = 64
    wave_table = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((t * sample_rate,))

    index = 0
    indexIncrement = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        # output[n] = wave_table[int(np.floor(index))]
        output[n] = interpolate_linearly(wave_table, index)
        index += indexIncrement
        index %= wavetable_length

    #volume
    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    #fade
    output = fade_out(output, 24000)

    wav.write(waveform_type + '/' + waveform_type + str(f) + 'hz' + '.wav', sample_rate, output.astype(np.float32))

def synthesize(c=0, v=1.0, frequency=256, waveform_type='sine', sample_rate=44100):

    try:
        path = waveform_type + '/' + waveform_type + str(frequency) + 'hz' + '.wav'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)

    except:
        main(frequency, waveform_type, sample_rate)
        path = waveform_type + '/' + waveform_type + str(frequency) + 'hz' + '.wav'
        mixer.music.load(path)
        w = pygame.mixer.Sound(path)

    w.set_volume(v)
    pygame.mixer.Channel(c).play(w)


for x in range(4):
    main(100 + x*100)


mixer.init()

sample_rate = 44100
frequency = 440
waveform_type = 'sine'


while run == 1:

    clock.tick()
    WIN.fill((0, 0, 0))
    mx, my = pygame.mouse.get_pos()


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = 2

        click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                run = 2

            elif event.key == pygame.K_a:

                print('a')

                value = 1
                synthesize(c=value, frequency=value*100, waveform_type='sawtooth')

            elif event.key == pygame.K_s:

                print('a')

                value = 2
                synthesize(c=value, frequency=value*100, waveform_type='sawtooth')

            elif event.key == pygame.K_d:

                print('a')

                value = 3
                synthesize(c=value, frequency=value * 100, waveform_type='sawtooth')

            elif event.key == pygame.K_f:

                print('a')

                value = 4
                synthesize(c=value, frequency=value * 100, waveform_type='sawtooth')



    pygame.display.update()











