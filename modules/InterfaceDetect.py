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

if __name__ == "__main__":
    open_itmlst_window()
