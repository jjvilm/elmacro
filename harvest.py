#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot
import autopy
import time
import threading
from grids import action_btn, move, itmlst

stop = None
shoot_lock = threading.Lock()
cx,cy = 0, 0
harvest = False
previous_reading = 0

def redroses():
    try:
        img = shoot(260,270,550,480,"hsv")

        low = np.array([169,213,28])
        high= np.array([179,255,140])

        # black and white image of roses
        mask = cv2.inRange(img, low, high)

        kernel = np.ones((5,5), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        closing_c = closing.copy()

        contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        all_xs = []
        all_ys = []

        for con in contours:
            for element in con:
                all_xs.append(element[0][0])
                all_ys.append(element[0][1])

        x1 = min(all_xs)
        y1 = min(all_ys)
        x2 = max(all_xs)
        y2 = max(all_ys)

        movein = 20
        x1 += movein 
        y1 += movein
        x2 -= movein
        y2 -= movein

        # add img taken coords 
        x1 += 260
        y1 += 270
        x2 += 260
        y2 += 270
        # moves x and y to center of roses
        x1 = x1 +((x2-x1)/2)
        y1 = y1 +((y2-y1)/2)
        
        
        autopy.mouse.move(x1,y1)
        time.sleep(2)
        autopy.mouse.click(1)
        
        ############## DEBUG
#
#        cv2.imshow('closing', closing_c)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        return True
    except:
        return False

def snapdragons():
    try:
        img = shoot(260,270,550,480,"hsv")

        low = np.array([169,213,28])
        high= np.array([179,255,140])

        # black and white image of roses
        mask = cv2.inRange(img, low, high)

        kernel = np.ones((5,5), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        #closing_c = closing.copy()

        contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        all_xs = []
        all_ys = []

        cnt = contours[4]

        for con in cnt:
            for element in con:
                x1, y1 = element
                # add img taken coords 
                x1 += 260
                y1 += 270

                autopy.mouse.move(x1,y1)
                time.sleep(2)
                autopy.mouse.click(1)
#                all_xs.append(element[0][0])
#                all_ys.append(element[0][1])
            break
        
        ############## DEBUG
#
#        cv2.imshow('closing', closing_c)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        return True
    except:
        return False

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
    if stat_level < 50:
        heal()
            
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
        if stat_level < 70:
            autopy.mouse.move(770,70)
            time.sleep(.01)
            autopy.mouse.click(1)
            # moves back to original location
            autopy.mouse.move(cx,cy)
            time.sleep(17)
        else:
            time.sleep(2)

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
        if stat_level < 50:
            autopy.mouse.move(770,137)
            for _ in range(3):
                time.sleep(.01)
                autopy.mouse.click(1)
            else:
                autopy.mouse.move(cx,cy)
        time.sleep(15)

def calc_emu():
    global stop, harvest, previous_reading, instance
    while True:
        if stop == 'y':
            return
        with shoot_lock:
            # grabs food bar
            hsv_img = shoot(444,503,543,504, 'hsv')

        low = np.array([0,65,103])
        high= np.array([1,129,193])

        mask = cv2.inRange(hsv_img, low, high)

        #(conts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
        
        mask = np.array(mask)
        stat_level = 0
        for color in mask:
            for element in color:
                # looks to see how filled emu is
                if element == 255:
                    stat_level += 1
                # stops at where bar is filled
                else:
                    # will send a signal to harvest again
                    if stat_level == previous_reading:
                        print("same as previous reading")
                        harvest = True
                    print("{} {}".format(previous_reading, stat_level))
                    previous_reading = stat_level
                    break
        # goes to storage, and stores, come back to harvest
        if stat_level >= 99:
            to_storage()
            instance.go_harvest()
        time.sleep(9)

def get_location():
    global cx,cy
    while True:
        if stop == 'y':
            break
        cx,cy = autopy.mouse.get_pos()
        time.sleep(1)

def heal():
    """Used in calc_health function"""
    # inventory must be in clear view
    itmlst(330,196,2)
    time.sleep(.8)
    # eats spirit potion
    move(771,76)
    # casts restoration
    move(741,80)
    
def to_storage():
    # opens map, cliks on storage, closes map
    action_btn(13)
    move(226,178)
    action_btn(13)
    # waits till getting to storage
    time.sleep(18)
    #opens storage
    action_btn(8)
    time.sleep(1)
    #stores materials
    move(290,68)
    time.sleep(1)
    # checks health
    calc_health()
    #stores materials
    move(290,68)
    time.sleep(1)
    # closes storage
    action_btn(8)
    time.sleep(1)

def harvest_loop(instance):
    """Start at votd storage, with mostly empty inventory"""
    global stop, harvest
    while stop != 'y':
        if harvest:
            # if red roses are not found
            if not instance.detect():
                instance.go_harvest()
            harvest = False
        time.sleep(3)

class Harvest(object):
    def __init__(self, har_loc, sto_loc, harv_func):
        """pass har_loc and sto_loc as a tuple, and harv func is the function to detect the harvestable"""
        self.har_loc = har_loc
        self.sto_loc = sto_loc
        self.harv_func = harv_func

    def go_harvest(self):
        x , y = self.har_loc
        action_btn(13)
        # clicks on location to harvest on map
        move(x,y)
        action_btn(13)

    def detect(self):
        return self.harv_func()

def start_threads():
    global instance
    #health_thread = threading.Thread(target=calc_health)
    #health_thread.start()

    #mp_thread = threading.Thread(target=calc_mp)
    #mp_thread.start()
    # started by health thread 

    #food_thread = threading.Thread(target=calc_food)
    #food_thread.start()

    emu_thread = threading.Thread(target=calc_emu)
    emu_thread.start()

    harvest_thread = threading.Thread(target=harvest_loop, args=(instance,))
    harvest_thread.start()

    #location_thread = threading.Thread(target=get_location)
    #location_thread.start()

def run():
    global stop
    while True:
        if stop == 'y':
            break
        try:
            stop = raw_input('Press [ENTER] to stop\n')
        except:
            pass
        finally:
            stop = 'y'

snaps = Harvest((234,308),(227,177),snapdragons)
instance = snaps
start_threads()
run()
