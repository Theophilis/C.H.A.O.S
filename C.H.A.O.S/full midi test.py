import sys
import os
import pygame
import pygame.midi
import time
import rtmidi2 as rtmidi


#pygame.midi interface

def print_device_into():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

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

def input_main(device_id=None):

    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    #rtmidi init
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_port_name(1)
    print(" ")
    print("midiout")
    print(midiout)
    print("available ports")
    print(available_ports)

    if available_ports:
        midiout.open_port(1)
    else:
        midiout.open_virtual_port('My virtual output')

    pygame.midi.init()

    print(" ")
    print("device info")
    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print(' ')
    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    print('i')
    print(i)

    print(" ")
    print("device info")
    _print_device_info()

    pygame.display.set_mode((1, 1))
    going = True

    while going:
        events = event_get()
        for e in events:

            # print(" ")
            # print('e')
            # print(e)
            # print(type(e))


            if e.type in [pygame.QUIT]:
                going = False
            if e.type in [pygame.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:

                # print(e)

                clean_e = str(e)[21:-3]
                list_e = clean_e.split(',')
                ev = []
                for l in list_e:
                    ev.append(int(l.split(':')[1]))

                print(" ")
                print("ev")
                print(ev)
                print(e)

                if ev[0] == 144:
                    midiout.send_noteon(ev[0], ev[1], ev[2])
                elif ev[0] == 128:
                    midiout.send_noteoff(ev[0], ev[1])

        if i.poll():

            # print(' ')
            # print('i')
            # print(i)

            midi_events = i.read(10)
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)

    del i
    pygame.midi.quit()


input_main()
