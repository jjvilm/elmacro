#!/usr/bin/python2
import os
import autopy
import time
import grids

cx,cy = autopy.mouse.get_pos()

grids.itmlst(330,120,1)
autopy.mouse.move(cx,cy)

