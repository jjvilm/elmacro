#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot
import autopy
import time


# smaller area
#box = (195,107,543,331)
box = (7,41,680,458)
# initialize firs frame
firstFrame = None
def find_orcs(image):
    """finds just the orcs by hue color, returns new image"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #create mask of green hues
    low = np.array([72,89,34])
    high= np.array([80,197,63])
    green_mask = cv2.inRange(image, low, high)
    # brown hues  for fem orcs clothing
    #low = np.array([4,40,7])
    #high= np.array([12,115,62])
    #brown_mask = cv2.inRange(image, low,high)

    #combined_mask = cv2.add(green_mask, brown_mask)

    kernel = np.ones((5,5), np.uint8)
    #closing = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)

    blur = cv2.GaussianBlur(closing, (21,21),0)
    return blur

while True:
    # takes screenshot at box
    frame = pyscreenshot.grab(bbox=box)
    # conver to an array for cv2
    frame = np.array(frame)
    # convert to BGR format
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # takes out everything but green hues (leaves orcs in)
    # applies a blur as well
    gray  = find_orcs(frame)
    # convert to grayscale
    #gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply blurr
    #gray = cv2.GaussianBlur(gray, (21,21), 0)


    if firstFrame is None:
        firstFrame = gray
        time.sleep(.01)
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    #thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]


    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    #thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(frameDelta.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('firstframe', gray)
    cv2.imshow('framedelta', frameDelta)
    #cv2.imshow('thresh', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    break

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 1000:
            continue

        print(cv2.contourArea(c))


    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        # shows a green rect on the found moving conts
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #click in the middle of the rectangle
        x += (w/2)
        y += (h/2)
        # add the origin of screenshot
        x += box[0]
        y += box[1]

        # move and click
        autopy.mouse.move(x,y)
        time.sleep(.01)
        autopy.mouse.click(1)
        firstFrame = None
        time.sleep(2)

