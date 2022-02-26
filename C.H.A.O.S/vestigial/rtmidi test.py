import time
import rtmidi2 as rtmidi

midiout = rtmidi.MidiOut()

available_ports = midiout.get_port_name(5)

print(available_ports)

if available_ports:
    midiout.open_port(5)
else:
    midiout.open_virtual_port('My virtual output')


note_on = [0x90, 60, 112]
note_off = [0x80, 60, 0]
midiout.send_noteon(note_on[0], note_on[1], note_on[2])


time.sleep(0.5)
midiout.send_noteoff(note_off[0], note_off[1])

del midiout
