#!/usr/bin/python2
#import os
import autopy
import time
import grids

cx,cy = autopy.mouse.get_pos()
# mix all
time.sleep(.1)
grids.inventory(5,9, 1)

##os.system('xdotool mousemove 702 478 sleep .1 click 1')
#autopy.mouse.move(702,478)
#time.sleep(.1)
#autopy.mouse.click(1)
time.sleep(.01)
autopy.mouse.move(cx,cy)



