#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot
from autopy import mouse
from threading import Lock

def shoot(x1,y1,x2,y2, *args, **kwargs):
    """Takes screenshot at given coordinates as PIL image format, the converts to cv2 grayscale image format and returns it"""
    # PIL format as RGB
    im = pyscreenshot.grab(bbox=(x1,y1,x2,y2)) #X1,Y1,X2,Y2
    #im.save('screenshot.png')

    # Converts to an array used for OpenCV
    im = np.array(im)
    # Next line needs to be taken out, messes up the array order when 
    # looking for hsv values
    #cv_img = im.astype(np.uint8)
    # Converts to BGR format for OpenCV
    cv_img = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    #cv2.imwrite('screenshot.png', cv_img)
    #cv2.imshow('screenshot', cv_img)
    #cv2.waitKey(0)
    #cv2.killAll()
    #return 

    try:
        if args[0] == 'hsv':
            #print('sending hsv')
            # returns hsv image
            hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
            return  hsv
            
    except:
        return cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

def open_itmlst_window():
    shoot_lock = Lock()
    def itmlst_toggle():
        mouse.move(290,198)
        mouse.click(1)

    letter_I = np.array([       [255, 255, 255, 255, 255, 255],
                                [255, 255, 255, 255, 255, 255],
                                [  0,   0, 255, 255,   0,   0],
                                [  0,   0, 255, 255,   0,   0],
                                [  0,   0, 255, 255,   0,   0],
                                [  0,   0, 255, 255,   0,   0],
                                [  0,   0, 255, 255,   0,   0],
                                [  0,   0, 255, 255,   0,   0],
                                [  0,   0, 255, 255,   0,   0],
                                [255, 255, 255, 255, 255, 255],
                                [  0,   0,   0,   0,   0,   0]], dtype="uint8")

    with shoot_lock:
        # screenshots letter "F" as gray object, of the word "Nothing"
        # when "Nothing to mix..." comes up.
        img = shoot(385,2,391,13)

    _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY) 
    #cv2.imwrite('thresh.png', thresh)

    # if all elements in array equate to True
    if (letter_I == thresh).all():
        pass
    else:
        # opens item list window if not opened already
        itmlst_toggle()

def find_eat_bones():
    from autopy import mouse
    from time import sleep
    from random import random
    ox, oy = 2,17
    # takes screenshot of inventory
    im = shoot(ox,oy,197,197)

    # bone image as a list :D
    template = np.array(
    [[  0,   1,   0,   0,   0,  42,  53,  83, 197, 221,  42,   3],
    [  0,   0,   0,   1,  28,  62,  78, 203, 222, 111,   0,   0],
    [  0,   3,  14,  41,  55,  88, 177, 216, 194,  13,   0,   0],
    [  8,  70,  77,  80, 101, 171, 227, 204, 160,   0,   0,   0],
    [ 27, 103,  29, 103, 217, 225, 227, 204,  70,   0,   0,   0],
    [ 23,  68,  96, 237, 237, 229, 229, 226,  70,   1,   0,   0],
    [ 17,  76,  40, 152, 230, 226, 230, 246,  79,   3,   0,   0],
    [  0,  11,  23,  24,  51, 173, 230, 246,  79,   3,   0,   0],
    [  0,   0,   0,   0,   6,  48,  63,  82,  54,   0,   0,   0]], dtype=np.uint8)

    template2 = np.array([
    [4, 90, 170, 96, 0, 0, 0],
    [13, 135, 130, 146, 43, 45, 2],
    [1, 67, 69, 204, 163, 88, 75],
    [0, 0, 125, 218, 250, 211, 175],
    [0, 102, 150, 240, 222, 178, 89],
    [8, 107, 168, 240, 99, 3, 0],
    [23, 116, 185, 231, 39, 2, 0],
    [64, 115, 235, 229, 37, 0, 0]], dtype=np.uint8)
    # finds image
    def match_(template):
        res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            x,y = pt
            x += ox
            y += oy
            # clicks on use button
            mouse.move(109,526)
            sleep(.07)
            mouse.click(1)

            mouse.move(x,y)
            for _ in xrange(5):
                sleep(random())
                mouse.click(1)
            return True
        return False

    if match_(template):
        pass
    else:
        match_(template2)

if __name__ == "__main__":
    #open_itmlst_window()
    find_eat_bones()
