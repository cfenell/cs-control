#! /usr/bin/python

# Just a test script. Move parts to main module and delete.

from pygame import midi

# Device no
devno=1 #
# Sysex tone generator dump request
dumpreq=[0xF0,0x43,0x20+devno,0x7F,0x1C,0x03,0x30,0x00,0x00,0xF7]

midi.init()
# midiin=midi.Input(3) # hardcoded devices here...
midiout=midi.Output(2)

# Send sysex
midiout.write_sys_ex(midi.time(),dumpreq)
midiout.close()
del(midiout) # no duplex...

midiin=midi.Input(3) # hardcoded devices here...
# Read MIDI channels
while True:
    if midiin.poll():
        msg=midiin.read(1)
        print(msg)

