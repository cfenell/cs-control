# cs-control
(C) Carl-Fredrik Enell 2019
fredrik@kyla.kiruna.se


## Introduction
I bought a Yamaha Reface CS, a virtual analog mini synthesizer, and
got annoyed that Yamaha provides only an iOS app to store the sound settings.
There is also an online service, SoundMondo, that
shares Reface sound settings using Web Midi in Google Chrome. 
It works but requires internet access and registration.

Thus, here are two simple command line utilities to read and write 
Reface CS sound settings.

In order for cs_setsound to work you need to enable MIDI-Control on the Reface
CS. You can do that by holding E2 while powering on. Looper LEDs should light
up if MIDI control is enabled. 

# Dependencies
* Python 3
* configparser
* MIDO and MIDI backend, see https://mido.readthedocs.io/.
  Suggested Debian packages: python3-mido, python3-rtmidi


# Installation
A setup script is provided. Typically

$sudo python3 setup.py install


# Usage
cs_setsound FILE: read sound settings from FILE and write to Reface CS

cs_getsound FILE: read sound settings from Reface CS and write to FILE
  
# File format
See the included example in examples/patch1

