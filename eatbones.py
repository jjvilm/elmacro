#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot
import autopy
import time

cx, cy = autopy.mouse.get_pos()
# takes screenshot of inventory
ox, oy = 2,17
im = pyscreenshot.grab(bbox=(ox,oy,197,197))
# converts image to np array for opencv2 to be able to use
im = np.array(im)
# converts from RGB to BGR, opencv's format
im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
# now convert the image to grayscale for faster matching
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# now matching begins
#template = cv2.imread('bone.png', 0)
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

def match_(template):
    res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        x,y = pt
        x += ox
        y += oy
        # clicks on use button
        autopy.mouse.move(109,526)
        time.sleep(.07)
        autopy.mouse.click(1)

        autopy.mouse.move(x,y)
        for _ in xrange(5):
            time.sleep(.01)
            autopy.mouse.click(1)
        # makes sure to click only on the first bone it finds
        return True
    return False

if match_(template):
    # tries the first template
    pass
else:
    match_(template2)

# mix all
autopy.mouse.move(290,165)
time.sleep(.01)
autopy.mouse.click(1)
autopy.mouse.move(cx,cy)
