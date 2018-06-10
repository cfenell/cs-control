# cs-control
(C) Carl-Fredrik Enell 2018
fredrik@kyla.kiruna.se


## Introduction
I bought a Yamaha Reface CS, a virtual analogue mini synthesizer, and
got annoyed that Yamaha provides only an iOS app to store and set the
sound parameters. There is also an online service, SoundMondo, that
can share settings online using Web Midi in Google Chrome. It works
but requires internet access and registration.

Here are therefore two simple command line programs written in
Python with PyGame Midi.

See the Reface MIDI implementation document available at <URL?>


# Dependencies
* Python 2.x
* PyGame MIDI

# Installation
A setup script is provided. Typically

$sudo python setup.py install


# Usage
cs_setsound <FILE>: read sound settings from FILE and write to Reface CS

TODO: add cs_getsound <FILE>: read sound settings from Reface CS and store to FILE

# File format
See the included example in examples/patch1

