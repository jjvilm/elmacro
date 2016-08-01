import autopy
import os
import time
import random
import cv2
import numpy as np

from modules import Screenshot

def setup():
    os.system("xdotool search --name Eternal windowmove 0 0 ")

def map_click(x,y,button=1):
    """Move Click"""
    click(400,530)
    time.sleep(.5)
    autopy.mouse.move(x,y)
    time.sleep(1)
    autopy.mouse.click(button)
    time.sleep(1)
    click(400,530)
    time.sleep(.5)
def click(x,y,button=1, wait='no'):
    if wait == 'no':
        autopy.mouse.move(x,y)
        time.sleep(1)
        autopy.mouse.click(button)
    else:
        autopy.mouse.move(x,y)
        autopy.mouse.click(button)

def run():
    """To work keep directional needle pointing North"""
    ## Goes Outsides Desert Pines Storage
    map_click(486,592)
    time.sleep(9)
    ## Clicks the cave to go outside storage
    print("clicking outside")
    click(530,175)
    time.sleep(1)
    ## On map Clicks on Crystal Caves
    print("to CC")
    map_click(403,275)
    time.sleep(89)

    ## Clicks on CC to go inside
    print("Inside CC")
    click(500,275)
    #goes to sulphur
    map_click(392,41)
    mine()
    time.sleep(400)
    to_storage()

def mine():
    time.sleep(28)
    print("Mining the biggest sulphur rock")
    detect_sul()

def to_storage():
    map_click(727,130)
    time.sleep(34)
    click(545,245)
    time.sleep(1)
    map_click(430,491)
    time.sleep(83)
    click(466,303)
    map_click(486,522)
    time.sleep(8)
    click(513,328)
    time.sleep(1)
    # Stores all items
    click(401,81)
    # Closes Storage window and item window
    time.sleep(.5)
    click(407,26, 1,'no wait')
    click(813,28,1, 'no wait')

def detect_sul():
    # Screenshot rectangle mid-center of the game screen not relevant to the game window
    img = Screenshot.shoot(100,80,800,560, 'hsv')
    # Lower and uppper colors of the sulphur rocks
    low = np.array([0,35,51])
    high= np.array([179,55,83])

    mask = cv2.inRange(img, low, high)
    
    # Removes noise
    kernel = np.ones((10,10), np.uint8)
    # closing is the img w/ no nosie
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    blur = cv2.GaussianBlur(closing, (5,5),0)

    contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    
    # Finds min max coords of first contour
    all_xs = []
    all_ys = []
    for a in cnt:
        for b in a:
            all_xs.append(b[0])
            all_ys.append(b[1])
    # getting the rectangle of contour
    x1 = min(all_xs)
    y1 = min(all_ys)

    x2 = max(all_xs)
    y2 = max(all_ys)

    w = x2 - x1
    h = y2 - y1

    x1 += ((w/2)/2)
    y1 += ((h/2)/2)
    x2 -= ((w/2)/2)
    y2 -= ((h/2)/2)

    x = random.randint(x1,x2)
    y = random.randint(y1,y2)

    # adding the points of the image back the coords
    x += 100
    y += 80
    click(x,y)

#setup()
#run()
#detect_sul()
#to_storage()
# storage
map_click(228,179)
time.sleep(15)
# open store
click(240,530)
time.sleep(1)
# store
click(290,60)
time.sleep(2)
# close store
click(240,530)
time.sleep(1)

map_click(272,303)
