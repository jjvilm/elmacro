#!/usr/bin/python2
import os
import autopy
import time
import grids
import subprocess
from InterfaceDetect import find_eat_bones

# gets initial mouse position to place it back when all functions are finished
# boolean to know when itm list window is opened
itmlst_open = False

class mix_Items(object):
    """x,y is the location of the item label in itmlist window, n is the number of items to take out from there"""
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

    def run(self):
        # stores all items before withdrawing any
        grids.store_all()
        # withdraws items 
        grids.itmlst(self.x,self.y,self.n)
        self.eat()
        # clics mix all button in inventory 
        grids.mix_all()

    def eat(self):
        """ n == last slot where bones reside
         eats bones 5 times
         0 == first row (0th row)"""
#        # clicks on the use button first
#        grids.action_btn(4)
#        time.sleep(.1)
#        # cliks the bones 5 times
#        grids.inventory(0,self.n-1,5)
        find_eat_bones()

    def get_bones(self):
        grids.item_itmlst(0,self.n-1)

def move(x,y, repeat):
    """Moves the cursor to x,y and then clicks"""
    #os.system('xdotool mousemove {} {} sleep .1 click --delay 100 --repeat {} 1'.format(x,y, repeat))
    autopy.mouse.move(x,y)
    time.sleep(1)
    for n in range(repeat):
        autopy.mouse.click(1)
        time.sleep(.001)
    time.sleep(1)

def wait():
    """Change to a higher number to compensate for lagg"""
    time.sleep(.3)

def category(name):
    """Clicks on the item category"""
    cat = {'Food':0,'Coins':0,'Flowers':(353,69),'Ores':(345,82),'Minerals':(357,109), 'Essences':(357,174),'Animal':(347,199)}
    x, y = cat[name]
    move(x,y,1)
    wait()

def inbank(times):
    """Deposits held item into bank then right clicks"""
    time.sleep(1)
    move(85,95,times)
    time.sleep(1)
    autopy.mouse.click(3)
    time.sleep(1)

def store_all():
    """Stores all items in inventory"""
    # store all
    move(290,65,1)
    time.sleep(.5)

def mix_dict(item):
    """runs the withdraw process, and mix.  Lastly returns the position of the bones"""
    items = {
        "ME":mix_Items(339, 234,5),
        "HE": mix_Items(330,197,3),
        "EE":mix_Items(330,142,4),
        "FE":mix_Items(330,163,4),
        "WE":mix_Items(330,305,5),
        "silverBar":mix_Items(330,287,4),
        "ironBar": mix_Items(330,214, 4),
        "steelBar": mix_Items(330,286,4),
        "vial": mix_Items(330,307,4),
        "PSR": mix_Items(330,250,6),
        "silverMedallion":mix_Items(330,305,3),
        "moonMedallion":mix_Items(330,272,4)

    }
    x_instance = items[item]

    return x_instance

########################################
if __name__ == "__main__":
    item = mix_dict('moonMedallion')
    item.get_bones()
    cx,cy = autopy.mouse.get_pos()

