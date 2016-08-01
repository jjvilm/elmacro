#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot
import autopy
import time
import threading

stop = None
shoot_lock = threading.Lock()
cx,cy = 0, 0

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

def calc_health():
    global stop
    while True:
        if stop == 'y':
            return
        with shoot_lock:
            hsv_img = shoot(308,502,407,503, 'hsv')
        #hsv_img = shoot(0,0,800,600, 'hsv')
        low = np.array([0,100,100])
        high = np.array([10,255,255])

        mask = cv2.inRange(hsv_img, low, high)

        # converts img to an array to measure the empty color space of the bar 
        mask = np.array(mask)
        stat_level = 0
        for color in mask:
            for element in color:
                # looks for all the white pixels, if it hits 0 its black so stops there
                if element == 0:
                    break
                stat_level += 1

        # casts restoration if helath falls below 38%
        if stat_level < 45:
            autopy.mouse.move(739,77)
            time.sleep(.01)
            autopy.mouse.click(1)
            autopy.mouse.move(cx,cy)
            time.sleep(2)
        else:
            time.sleep(.5)
            
def calc_mp():
    while True:
        global stop
        if stop == 'y':
            return
        with shoot_lock:
            # grabs blue bar
            hsv_img = shoot(36,504,135,505, 'hsv')
        low = np.array([110,100,100])
        high = np.array([130,255,255])

        mask = cv2.inRange(hsv_img, low, high)

        #(conts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
        
        mask = np.array(mask)
        stat_level = 0
        for color in mask:
            for element in color:
                if element == 0:
                    break
                stat_level += 1
        if stat_level >=  34:
            autopy.mouse.move(740,111)
            time.sleep(.1)
            autopy.mouse.click(1)
            # moves back to original location
            autopy.mouse.move(cx,cy)
            time.sleep(1)
        else:
            for _ in xrange(60):
                if stop == 'y':
                    return
                time.sleep(1)

def calc_food():
    global stop
    while True:
        if stop == 'y':
            return
        with shoot_lock:
            # grabs food bar
            hsv_img = shoot(172,503,271,504, 'hsv')
        low = np.array([0,100,100])
        high = np.array([179,255,255])

        mask = cv2.inRange(hsv_img, low, high)

        #(conts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
        
        mask = np.array(mask)
        stat_level = 0
        for color in mask:
            for element in color:
                if element == 0:
                    break
                stat_level += 1
        if stat_level <= 25:
            autopy.mouse.move(774,74)
            for _ in range(1):
                time.sleep(.3)
                autopy.mouse.click(1)
            else:
                autopy.mouse.move(cx,cy)

        for _ in xrange(60):
            if stop == 'y':
                break
            else:
                time.sleep(1)

def get_location():
    global cx,cy
    while True:
        if stop == 'y':
            break
        cx,cy = autopy.mouse.get_pos()
        time.sleep(1)

def start_threads():
    #health_thread = threading.Thread(target=calc_health)
    #health_thread.start()

    mp_thread = threading.Thread(target=calc_mp)
    mp_thread.start()
    # started by health thread 

    food_thread = threading.Thread(target=calc_food)
    food_thread.start()

    location_thread = threading.Thread(target=get_location)
    location_thread.start()

start_threads()

while True:
    if stop == 'y':
        break
    try:
        stop = raw_input('Press [y] to stop\n')
    except:
        pass
    finally:
        stop = 'y'
