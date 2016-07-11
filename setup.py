#!/usr/bin/python
import os

try:
    os.system('xdotool search --name Eternal windowmove 0 0')
    print('trying')
except:
    os.system('xdotool search --name Eternal windowmove 0 0')
    os.system('xdotool search --name Alas windowmove 0 0')
    os.system('xdotool search --name Arko windowmove 794 0')
    os.system('xdotool search --name Vilm windowmove 0 565')
    print('exception')
