#!/usr/bin/python2
from cv2 import cvtColor, COLOR_RGB2BGR,COLOR_BGR2GRAY, COLOR_BGR2HSV,inRange,threshold, THRESH_BINARY  
from numpy import array
from pyscreenshot import grab
import autopy 
from threading import Lock, Thread
from contWithdraw import  mix_dict 
from grids import mix_all, wait
from InterfaceDetect import open_itmlst_window

stop = False
# used to avoid taking screenshots at the same time with 2 different threads
shoot_lock = Lock()
# used to avoid colliding with other mouse move actions
turn_lock = Lock()
cx,cy = 0, 0
# here to type what to make
instance = raw_input("Make what?:\n")
mix_iterations = int(raw_input("How many iterations?\n"))
item_instance = mix_dict(instance)

def shoot(x1,y1,x2,y2, *args, **kwargs):
    """Takes screenshot at given coordinates as PIL image format, the converts to cv2 grayscale image format and returns it"""
    # PIL format as RGB
    im = grab(bbox=(x1,y1,x2,y2)) #X1,Y1,X2,Y2
    #im.save('screenshot.png')

    # Converts to an array used for OpenCV
    im = array(im)
    # Next line needs to be taken out, messes up the array order when 
    # looking for hsv values
    #cv_img = im.astype(np.uint8)
    # Converts to BGR format for OpenCV
    cv_img = cvtColor(im, COLOR_RGB2BGR)
    #cv2.imwrite('screenshot.png', cv_img)
    #cv2.imshow('screenshot', cv_img)
    #cv2.waitKey(0)
    #cv2.killAll()
    #return 

    try:
        if args[0] == 'hsv':
            #print('sending hsv')
            # returns hsv image
            hsv = cvtColor(cv_img, COLOR_BGR2HSV)
            return  hsv
            
    except:
        return cvtColor(cv_img, COLOR_BGR2GRAY)
    
def calc_food():
    global stop, item_instance
    iterations = 0
    while not stop:
        with shoot_lock:
            # grabs food bar
            hsv_img = shoot(172,503,271,504, 'hsv')
        low = array([0,100,100])
        high = array([179,255,255])

        mask = inRange(hsv_img, low, high)

        #(conts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
        
        # turns the food bar into a 1 pixle wide binary image
        mask = array(mask)
        percentage = 0
        for color in mask:
            for element in color:
                if element == 0:
                    break
                percentage += 1
        # if the food bar is less than 1%
        if percentage < 1:
            with turn_lock:
                iterations += 1
                # on 4th iteration it withdraws more bones
                if iterations == 4:
                    open_itmlst_window()
                    wait(.1)
                    item_instance.get_bones() 
                    iterations = 0
                item_instance.eat()
                mix_all()

        wait(1)

def stopped_working():
    global stop

    letter = array([       [  0,   0,   0,   0,   0,   0,   0,   0],
                              [255, 255,   0, 255, 255, 255,   0,   0],
                              [  0, 255, 255,   0,   0,   0, 255,   0],
                              [  0, 255, 255,   0,   0,   0, 255, 255],
                              [  0, 255, 255,   0,   0,   0, 255, 255],
                              [  0, 255, 255,   0,   0,   0, 255, 255],
                              [  0, 255, 255,   0,   0,   0, 255,   0],
                              [  0, 255, 255, 255, 255, 255,   0,   0],
                              [  0, 255, 255,   0,   0,   0,   0,   0],
                              [  0, 255, 255, 255, 255,   0,   0,   0],
                              [255, 255, 255, 255, 255,   0,   0,   0]], dtype="uint8")

    while not stop:
        with shoot_lock:
            # screenshots letter "N" as gray object, of the word "Nothing"
            # when "Nothing to mix..." comes up.
            gray_img = shoot(61,222,69,233)

        ret, thresh = threshold(gray_img, 50, 255,THRESH_BINARY)
        # numpy array of letter "N"
        if (letter == thresh).all():
            with turn_lock:
                mix_all()
                wait(1)
        else:
            wait(1)

def nothing_to_mix():
    """needs fixing to a binary threshold"""
    global stop, item_instance, mix_iterations

    letter = array([       [  0, 255,   0,   0, 255, 255, 255,   0],
                              [255, 255, 255,   0, 255, 255, 255, 255],
                              [  0, 255, 255,   0,   0,   0, 255,   0],
                              [  0, 255, 255, 255,   0,   0, 255,   0],
                              [  0, 255, 255, 255,   0,   0, 255,   0],
                              [  0, 255, 255, 255, 255,   0, 255,   0],
                              [  0, 255,   0,   0, 255,   0, 255,   0],
                              [  0, 255,   0,   0, 255, 255, 255,   0],
                              [  0, 255,   0,   0,   0, 255, 255,   0],
                              [255, 255, 255, 255,   0,   0, 255,   0],
                              [  0,   0,   0,   0,   0,   0,   0,   0]], dtype="uint8")

    iterations = 0

    while not stop: 
        with shoot_lock:
            # screenshots letter "N" as gray object, of the word "Nothing"
            # when "Nothing to mix..." comes up.
            gray_img = shoot(5,220,13,231)
        _, gray_img = threshold(gray_img, 50,255,THRESH_BINARY)
        # numpy array of letter "N"
        if (letter == gray_img).all():
            if mix_iterations == iterations:
                stop = True
                break
            with turn_lock:
                # opens item list window
                open_itmlst_window()
                wait(.1)
                # withdraw more items 
                item_instance.run()
                iterations += 1
                print("Iterations: {}".format(iterations))
                wait(1)
        wait(3)

def you_failed():
    global stop
    letter_f = array([[  0,   0,   0, 255, 255, 255,   0],
                         [  0,   0, 255, 255, 255, 255, 255],
                         [  0,   0, 255,   0,   0,   0,   0],
                         [255, 255, 255, 255, 255, 255,   0],
                         [  0,   0, 255,   0,   0,   0,   0],
                         [  0,   0, 255,   0,   0,   0,   0],
                         [  0,   0, 255,   0,   0,   0,   0],
                         [  0,   0, 255,   0,   0,   0,   0],
                         [  0,   0, 255,   0,   0,   0,   0],
                         [255, 255, 255, 255, 255, 255,   0],
                         [  0,   0,   0,   0,   0,   0,   0]], dtype="uint8")
    
    while not stop:
        with shoot_lock:
            # screenshots letter "F" as gray object, of the word "Nothing"
            # when "Nothing to mix..." comes up.
            gray_img = shoot(38,220,45,231)
        # thresh is a binary image omg gray_img
        _, thresh = threshold(gray_img, 50, 255, THRESH_BINARY) 
        #cv2.imwrite('thresh.png', thresh)

        # if all elements in array equate to True
        if (letter_f == thresh).all():
            with turn_lock:
                mix_all()
                wait(1)
        wait(2)

def safefail_mix():
    """Clicks on mix all in case a rare item is made, or something else not detected"""
    global stop

    counter = 0
    while not stop:
        # clicks mix all every 2 mins
        # in case a rare item is created or some other reason
        # to kickstart the other detector threads
        if counter == 120:
            with turn_lock:
                counter = 0
                mix_all()
        counter += 1
        wait(1)

def start_threads():
    # checks health every 3 secsonds
    food_thread = Thread(target=calc_food)
    food_thread.start()
    # checks for letter N in Nothing
    nothing_to_mix_thread = Thread(target=nothing_to_mix)
    nothing_to_mix_thread.start()
    # checks for letter f in failed
    you_failed_thread = Thread(target=you_failed)
    you_failed_thread.start()

    stopped_working_thread = Thread(target=stopped_working)
    stopped_working_thread.start()
    # clicks on mix all every minute no matter what
    # to be a safefail 
    safefail_mix_thread = Thread(target=safefail_mix)
    safefail_mix_thread.start()

if __name__ == "__main__":
    start_threads()
    #stopped_working()
    #you_failed()
    #nothing_to_mix()
    #itmlst_window()
    #calc_food()

    #while True:
    raw_input('Press [ENTER] to stop\n')
    stop = True
