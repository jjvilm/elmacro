#!/usr/bin/python2
import grids
import os
import time
import subprocess

# moves to travel, then takes out the 4 items in it
# takes out all itmes needed
def take_out_essences(sa= False):
    if sa == True:
        grids.store_all() 
    grids.itmlst(330,270,4)


f = '/home/jj/.elc/main/srv_log.txt'
def tely():
    # click on teleport spell
    grids.move(738,111)
    time.sleep(5)

take_out_essences()
tely()

for _ in xrange(10) :
    last_line = subprocess.check_output(['tail', '-1', f])
    if 'Spell failed!' in last_line:
        print('spell failed')
        tely()
        time.sleep(1)
    elif 'You need' in last_line:
        take_out_essendces(sa=True)

    else:
        break
    # here check ouput of el console to make sure it teleported
    # if not then keep clicking

os.system('xdotool key Alt+d')
