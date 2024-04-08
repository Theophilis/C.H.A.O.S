import numpy as np
import scipy.io.wavfile as wav

#https://www.youtube.com/watch?v=zBFeT8fkjfI


def main():
    sample_rate = 44100
    f = 440
    t = 3
    waveform = np.sin

    wavetable_length = 64
    wave_table = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((t * sample_rate,))

    index = 0
    indexIncrement = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        output[n] = wave_table[int(np.floor(index))]
        index += indexIncrement
        index %= wavetable_length

    #volume
    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    wav.write('sine440Hzamp.wav', sample_rate, output.astype(np.float32))

if __name__ == '__main__':
    main()