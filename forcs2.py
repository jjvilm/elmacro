#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot
#import autopy
import time
import threading



# smaller area
#box = (195,107,543,331)
box = (7,41,680,458)
img = None

def shoot():
    global box, img
    # takes screenshot at box
    frame = pyscreenshot.grab(bbox=box)
    # conver to an array for cv2
    frame = np.array(frame)
    # convert to BGR format
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    img = frame

def display_img():
    global img
    fgmask = fgbg.apply(img)
    cv2.imshow('fg', fgmask)

fgbg = cv2.BackgroundSubtractorMOG2()
shoot_lock = threading.Lock()
for _ in range(100):
    shoot_thread = threading.Thread(target=shoot)
    shoot_thread.start()
    shoot_thread.join()

    display_thread = threading.Thread(target=display_img)
    display_thread.start()

cv2.destroyAllWindows()
