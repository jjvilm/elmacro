#!/usr/bin/python2
import cv2
import numpy as np
import pyscreenshot



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
            print('sending hsv')
            # returns hsv image
            hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
            return  hsv
            
    except:
        return cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)


#takes a screenshot of healthbar on the HUD
def calc_health():
    hsv_img = shoot(308,502,407,503, 'hsv')
    #hsv_img = shoot(0,0,800,600, 'hsv')
    low = np.array([0,100,100])
    high = np.array([10,255,255])

    mask = cv2.inRange(hsv_img, low, high)

    (conts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    
    mask = np.array(mask)
    newmask = 0
    for color in mask:
        for element in color:
            if element == 0:
                break
            newmask += 1
            
    print(newmask)

    #cv2.imshow('hsv',mask)
    cv2.imwrite('screenshot.png', mask)
    return

calc_health()
